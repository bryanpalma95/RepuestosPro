#!/usr/bin/env python3
"""Aplica lotes aditivos y verificables sobre db.json/db-compat.json.

No elimina vehículos, componentes, referencias ni compatibilidades. Cada lote
incluye selectores con conteos esperados para fallar de forma segura si cambia
la estructura del catálogo.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import tempfile
from pathlib import Path


VALID_STATUSES = {"confirmed", "verify"}


def reference_key(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def compatibility_key(value: str) -> str:
    return re.sub(r"\s+", "", value.upper())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, payload: dict) -> None:
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    if path.name == "db-compat.json" or "\n" in original:
        encoded = json.dumps(payload, ensure_ascii=False, indent=1)
        if original.endswith("\n"):
            encoded += "\n"
    else:
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    handle, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as temporary:
            temporary.write(encoded)
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def select_vehicles(catalog: dict, selector: dict) -> list[tuple[str, dict]]:
    pattern = re.compile(selector["vehicle_id_regex"])
    years = {str(year) for year in selector.get("years", [])}
    info_any = [str(value).casefold() for value in selector.get("info_any", [])]
    selected: list[tuple[str, dict]] = []
    for vehicle_id, vehicle in catalog.items():
        match = pattern.fullmatch(vehicle_id)
        if not match:
            continue
        year = match.groupdict().get("year") or vehicle_id.rsplit("-", 1)[-1]
        if years and year not in years:
            continue
        info = str(vehicle.get("info", "")).casefold()
        if info_any and not any(value in info for value in info_any):
            continue
        selected.append((vehicle_id, vehicle))
    selected.sort()
    expected = int(selector["expected_matches"])
    if len(selected) != expected:
        raise ValueError(
            f"Selector {selector['vehicle_id_regex']} encontró {len(selected)} vehículos; "
            f"se esperaban {expected}."
        )
    return selected


def select_part(vehicle_id: str, vehicle: dict, category: str) -> dict:
    matches = [
        part
        for parts in vehicle.get("categories", {}).values()
        for part in parts
        if str(part.get("cat", "")) == category
    ]
    if len(matches) != 1:
        raise ValueError(
            f"{vehicle_id}: categoría {category!r} encontró {len(matches)} componentes; se esperaba 1."
        )
    return matches[0]


def append_once(current: str, addition: str) -> tuple[str, bool]:
    current = str(current or "").strip()
    addition = str(addition or "").strip()
    if not addition or addition in current:
        return current, False
    return (current + (" · " if current else "") + addition), True


def apply_part_operation(catalog: dict, operation: dict, counters: dict[str, int]) -> None:
    reference = operation["reference"]
    code = str(reference["code"]).strip()
    status = str(reference["status"]).strip()
    if status not in VALID_STATUSES:
        raise ValueError(f"Estado no válido: {status}")
    source_link = operation.get("source_link") or {}

    for vehicle_id, vehicle in select_vehicles(catalog, operation["selector"]):
        part = select_part(vehicle_id, vehicle, operation["part_category"])
        refs = part.setdefault("refs", [])
        existing = next(
            (item for item in refs if reference_key(str(item.get("r", ""))) == reference_key(code)),
            None,
        )
        if existing is None:
            refs.append({"r": code, "s": status})
            counters["references_added"] += 1
        elif existing.get("s") == "verify" and status == "confirmed":
            existing["s"] = "confirmed"
            counters["references_promoted"] += 1

        new_details, changed = append_once(part.get("details", ""), operation.get("details", ""))
        if changed:
            part["details"] = new_details
            counters["details_enriched"] += 1

        if source_link:
            links = part.setdefault("links", [])
            if not any(link.get("u") == source_link.get("url") for link in links):
                links.append({"t": source_link["label"], "u": source_link["url"]})
                counters["source_links_added"] += 1


def merge_unique_dicts(existing: list, incoming: list) -> int:
    added = 0
    fingerprints = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in existing}
    for item in incoming:
        fingerprint = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if fingerprint not in fingerprints:
            existing.append(copy.deepcopy(item))
            fingerprints.add(fingerprint)
            added += 1
    return added


def merge_compatibility(compatibility: dict, specification: dict, counters: dict[str, int]) -> None:
    key = compatibility_key(specification["key"])
    incoming = specification["entry"]
    if key not in compatibility:
        compatibility[key] = copy.deepcopy(incoming)
        counters["compatibility_entries_added"] += 1
        return

    target = compatibility[key]
    for field, value in incoming.items():
        if isinstance(value, list):
            target.setdefault(field, [])
            counters["compatibility_items_added"] += merge_unique_dicts(target[field], value)
        elif field not in target or not target[field]:
            target[field] = copy.deepcopy(value)
        elif target[field] != value:
            raise ValueError(f"Conflicto no aditivo en compatibilidad {key}, campo {field}.")


def apply_batch(repo: Path, batch_path: Path, apply_changes: bool) -> dict[str, int]:
    catalog_path = repo / "db.json"
    compatibility_path = repo / "db-compat.json"
    catalog = copy.deepcopy(load_json(catalog_path))
    compatibility = copy.deepcopy(load_json(compatibility_path))
    batch = load_json(batch_path)
    counters = {
        "references_added": 0,
        "references_promoted": 0,
        "details_enriched": 0,
        "source_links_added": 0,
        "compatibility_entries_added": 0,
        "compatibility_items_added": 0,
    }

    for operation in batch.get("part_operations", []):
        apply_part_operation(catalog, operation, counters)
    for specification in batch.get("compatibility_entries", []):
        merge_compatibility(compatibility, specification, counters)

    json.loads(json.dumps(catalog, ensure_ascii=False))
    json.loads(json.dumps(compatibility, ensure_ascii=False))
    if apply_changes:
        write_json_atomic(catalog_path, catalog)
        write_json_atomic(compatibility_path, compatibility)
    return counters


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Escribe los JSON; sin esta opción solo valida")
    args = parser.parse_args()
    repo = args.repo.resolve()
    batch_path = args.batch if args.batch.is_absolute() else repo / args.batch
    counters = apply_batch(repo, batch_path.resolve(), args.apply)
    print(json.dumps({"mode": "apply" if args.apply else "check", **counters}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
