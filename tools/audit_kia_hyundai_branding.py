#!/usr/bin/env python3
"""Audit Kia vehicles incorrectly published under Hyundai.

Read-only by design. The script compares db.json, db-nav.json and an explicit
migration proposal. It never edits the catalog or SQLite database.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "kia-hyundai-brand-migration-proposal.json"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_name(value: str) -> tuple[str, str, str] | None:
    match = re.match(r"^(.*?)\s+[—-]\s+(\d{4})$", value)
    if not match:
        return None
    left, year = match.groups()
    words = left.strip().split()
    if not words:
        return None
    return words[0], " ".join(words[1:]), year


def component_rows(vehicle: dict[str, Any]) -> list[dict[str, Any]]:
    return [part for parts in vehicle.get("categories", {}).values() for part in parts]


def payload_hash(vehicle: dict[str, Any]) -> str:
    payload = dict(vehicle)
    payload.pop("name", None)
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def component_signatures(vehicle: dict[str, Any]) -> set[str]:
    signatures = set()
    for part in component_rows(vehicle):
        refs = sorted((ref.get("r", ""), ref.get("s", "")) for ref in part.get("refs", []))
        signatures.add(json.dumps([part.get("cat", ""), refs], ensure_ascii=False, sort_keys=True))
    return signatures


def ref_stats(vehicle: dict[str, Any]) -> Counter[str]:
    result: Counter[str] = Counter()
    for part in component_rows(vehicle):
        refs = part.get("refs", [])
        if not refs:
            result["parts_without_refs"] += 1
        for ref in refs:
            result[f"refs_{ref.get('s', 'unknown')}"] += 1
    result["parts"] += len(component_rows(vehicle))
    return result


def nav_has(nav: dict[str, Any], brand: str, model: str, year: str) -> bool:
    return year in nav.get(brand, {}).get(model, [])


def sqlite_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    connection = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    try:
        return {row[0] for row in connection.execute("SELECT id FROM vehicles")}
    finally:
        connection.close()


def build_report(root: Path, manifest_path: Path) -> tuple[dict[str, Any], list[str]]:
    catalog = load_json(root / "db.json")
    nav = load_json(root / "db-nav.json")
    manifest = load_json(manifest_path)
    sql_ids = sqlite_ids(root / "db.sqlite")
    errors: list[str] = []
    families = []
    totals: Counter[str] = Counter()

    for rule in manifest["families"]:
        pattern = re.compile(rule["source_pattern"])
        matches = []
        for source_id, vehicle in catalog.items():
            match = pattern.fullmatch(source_id)
            if not match:
                continue
            parsed = parse_name(vehicle.get("name", ""))
            year = match.groupdict().get("year") or (parsed[2] if parsed else "")
            target_id = rule["target_pattern"].format(year=year)
            target = catalog.get(target_id)
            stats = ref_stats(vehicle)
            source_nav_ok = bool(parsed and nav_has(nav, parsed[0], parsed[1], parsed[2]))
            target_nav_exists = nav_has(nav, rule["target_brand"], rule["target_model"], year)
            row = {
                "year": year,
                "source_id": source_id,
                "source_name": vehicle.get("name", ""),
                "target_id": target_id,
                "target_exists": target is not None,
                "payload_identical_to_target": bool(target and payload_hash(vehicle) == payload_hash(target)),
                "source_in_navigation": source_nav_ok,
                "target_in_navigation": target_nav_exists,
                "source_in_sqlite": source_id in sql_ids,
                "target_in_sqlite": target_id in sql_ids,
                **stats,
            }
            matches.append(row)
            totals.update(stats)
            totals["vehicles"] += 1
            totals["target_collisions"] += int(target is not None)
            totals["taller_exact_match_failures"] += int(target is None)
            totals["source_ids_in_sqlite"] += int(source_id in sql_ids)
            totals["target_ids_in_sqlite"] += int(target_id in sql_ids)

        if len(matches) != rule["expected_count"]:
            errors.append(
                f"{rule['source_model']}: expected {rule['expected_count']} records, found {len(matches)}"
            )
        collisions = sum(item["target_exists"] for item in matches)
        family_report = {
                "source": f"{rule['source_brand']} {rule['source_model']}",
                "target": f"{rule['target_brand']} {rule['target_model']}",
                "records": len(matches),
                "years": [item["year"] for item in matches],
                "target_collisions": collisions,
                "technical_payloads_differ_at_collisions": sum(
                    item["target_exists"] and not item["payload_identical_to_target"] for item in matches
                ),
                "rows": matches,
            }
        collision_row = next((item for item in matches if item["target_exists"]), None)
        if collision_row:
            source_vehicle = catalog[collision_row["source_id"]]
            target_vehicle = catalog[collision_row["target_id"]]
            source_parts = component_signatures(source_vehicle)
            target_parts = component_signatures(target_vehicle)
            family_report["collision_example"] = {
                "year": collision_row["year"],
                "source_info": source_vehicle.get("info", ""),
                "target_info": target_vehicle.get("info", ""),
                "source_components": len(component_rows(source_vehicle)),
                "target_components": len(component_rows(target_vehicle)),
                "shared_exact_component_signatures": len(source_parts & target_parts),
                "source_only_component_signatures": len(source_parts - target_parts),
                "target_only_component_signatures": len(target_parts - source_parts),
            }
        families.append(family_report)

    # These invariants explain the visible catalog and Taller impact.
    if any(not row["source_in_navigation"] for family in families for row in family["rows"]):
        errors.append("At least one source record is absent from db-nav.json")
    unexpected_target_nav = [
        row["target_id"]
        for family in families
        for row in family["rows"]
        if not row["target_exists"] and row["target_in_navigation"]
    ]
    if unexpected_target_nav:
        errors.append(f"Navigation contains missing target IDs: {unexpected_target_nav[:5]}")

    report = {
        "audit": "kia-hyundai-brand-ownership",
        "manifest": str(manifest_path.relative_to(root)),
        "catalog_vehicle_count": len(catalog),
        "summary": dict(sorted(totals.items())),
        "families": families,
        "findings": [
            "La causa está en los scripts de carga Hyundai: incluyen explícitamente estas familias Kia con IDs hyundai-* y les asignan familias técnicas Hyundai genéricas.",
            "db-nav.json deriva la marca de la primera palabra de vehicle.name; por eso los registros mal rotulados aparecen bajo Hyundai.",
            "Taller construye un slug exacto con marca, modelo y año; si no existe el ID Kia de destino, no puede confirmar la coincidencia.",
            "Antes de cambiar IDs se necesita un mapa de alias históricos; de otro modo, datos guardados en Taller pueden perder su vínculo con el catálogo.",
            "Las colisiones de destino deben compararse y fusionarse manualmente: pertenecer al mismo grupo automotor no prueba compatibilidad de repuestos.",
        ],
        "validation_errors": errors,
    }
    return report, errors


def markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Auditoría de marca Kia/Hyundai",
        "",
        "Auditoría de solo lectura. La propuesta asociada no se aplica automáticamente.",
        "",
        "## Resumen",
        "",
        f"- Registros Kia publicados bajo Hyundai: {summary.get('vehicles', 0)}",
        f"- Colisiones con IDs Kia existentes: {summary.get('target_collisions', 0)}",
        f"- Coincidencias exactas que Taller no puede resolver como Kia: {summary.get('taller_exact_match_failures', 0)}",
        f"- IDs de origen presentes también en SQLite: {summary.get('source_ids_in_sqlite', 0)}",
        f"- IDs Kia de destino presentes en SQLite: {summary.get('target_ids_in_sqlite', 0)}",
        f"- Componentes afectados: {summary.get('parts', 0)}",
        f"- Referencias confirmadas: {summary.get('refs_confirmed', 0)}",
        f"- Referencias por verificar: {summary.get('refs_verify', 0)}",
        "",
        "## Familias",
        "",
        "| Publicado como | Debe revisarse como | Registros | Años | Colisiones | Payload distinto |",
        "|---|---|---:|---|---:|---:|",
    ]
    for family in report["families"]:
        years = family["years"]
        span = f"{min(years)}–{max(years)}" if years else "—"
        lines.append(
            f"| {family['source']} | {family['target']} | {family['records']} | {span} | "
            f"{family['target_collisions']} | {family['technical_payloads_differ_at_collisions']} |"
        )
    lines.extend(["", "## Colisiones que bloquean una migración automática", ""])
    for family in report["families"]:
        if not family.get("collision_example"):
            continue
        example = family["collision_example"]
        lines.append(
            f"- {family['target']} {example['year']}: `{example['source_info']}` vs `{example['target_info']}`; "
            f"{example['shared_exact_component_signatures']} componentes coinciden exactamente, "
            f"{example['source_only_component_signatures']} quedan solo en origen y "
            f"{example['target_only_component_signatures']} solo en destino."
        )
    lines.extend(["", "## Impacto y criterio", ""])
    lines.extend(f"- {finding}" for finding in report["findings"])
    lines.extend(["", "## Validación", ""])
    if report["validation_errors"]:
        lines.extend(f"- ERROR: {error}" for error in report["validation_errors"])
    else:
        lines.append("- Todas las cantidades esperadas y relaciones navegación/catálogo son consistentes.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report, errors = build_report(args.root.resolve(), args.manifest.resolve())
    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else markdown(report)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
