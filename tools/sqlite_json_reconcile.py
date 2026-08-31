#!/usr/bin/env python3
"""Compara db.sqlite con db.json y produce un plan de reconciliacion seguro.

Esta herramienta es deliberadamente de solo lectura respecto de las fuentes.
No exporta, importa, actualiza ni elimina datos. Si se solicita ``--output``, el
unico archivo escrito es el informe indicado por el operador.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def part_signature(part: dict[str, Any]) -> str:
    """Firma estable que conserva duplicados y el orden interno de refs/links."""
    normalized = {
        "cat": part.get("cat", ""),
        "name": part.get("name", ""),
        "details": part.get("details", ""),
        "brands": part.get("brands", ""),
        "refs": part.get("refs") or [],
        "links": part.get("links") or [],
    }
    if part.get("interval"):
        normalized["interval"] = part["interval"]
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def part_label(signature: str) -> dict[str, Any]:
    part = json.loads(signature)
    return {
        "cat": part["cat"],
        "name": part["name"],
        "refs": [ref.get("r", "") for ref in part["refs"][:5]],
    }


def catalog_counts(catalog: dict[str, Any]) -> dict[str, int]:
    categories = parts = refs = links = 0
    for vehicle in catalog.values():
        vehicle_categories = vehicle.get("categories") or {}
        categories += len(vehicle_categories)
        for part_list in vehicle_categories.values():
            parts += len(part_list)
            refs += sum(len(part.get("refs") or []) for part in part_list)
            links += sum(len(part.get("links") or []) for part in part_list)
    return {
        "vehicles": len(catalog),
        "categories": categories,
        "parts": parts,
        "references": refs,
        "links": links,
    }


def load_sqlite_projection(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    # mode=ro + PRAGMA query_only impiden escrituras incluso si el codigo cambia.
    uri = path.resolve().as_uri() + "?mode=ro&immutable=1"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    foreign_key_issues = [tuple(row) for row in connection.execute("PRAGMA foreign_key_check")]

    vehicles = connection.execute("SELECT * FROM vehicles ORDER BY id").fetchall()
    categories = connection.execute(
        "SELECT id, vehicle_id, name, sort_order FROM categories ORDER BY id"
    ).fetchall()
    parts = connection.execute(
        "SELECT id, category_id, cat_label, name, details, brands, interval_info "
        "FROM parts ORDER BY id"
    ).fetchall()
    refs = connection.execute(
        "SELECT part_id, reference, status FROM part_refs ORDER BY id"
    ).fetchall()
    links = connection.execute(
        "SELECT part_id, label, url FROM part_links ORDER BY id"
    ).fetchall()
    connection.close()

    refs_by_part: dict[int, list[dict[str, str]]] = {}
    for row in refs:
        refs_by_part.setdefault(row["part_id"], []).append(
            {"r": row["reference"], "s": row["status"]}
        )
    links_by_part: dict[int, list[dict[str, str]]] = {}
    for row in links:
        links_by_part.setdefault(row["part_id"], []).append(
            {"t": row["label"], "u": row["url"]}
        )

    parts_by_category: dict[int, list[dict[str, Any]]] = {}
    for row in parts:
        item: dict[str, Any] = {
            "cat": row["cat_label"],
            "name": row["name"],
            "details": row["details"] or "",
            "brands": row["brands"] or "",
            "refs": refs_by_part.get(row["id"], []),
            "links": links_by_part.get(row["id"], []),
        }
        if row["interval_info"]:
            item["interval"] = row["interval_info"]
        parts_by_category.setdefault(row["category_id"], []).append(item)

    categories_by_vehicle: dict[str, list[sqlite3.Row]] = {}
    for row in categories:
        categories_by_vehicle.setdefault(row["vehicle_id"], []).append(row)
    for rows in categories_by_vehicle.values():
        rows.sort(key=lambda row: (row["sort_order"], row["name"]))

    catalog: dict[str, Any] = {}
    for vehicle in vehicles:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for category in categories_by_vehicle.get(vehicle["id"], []):
            category_parts = parts_by_category.get(category["id"], [])
            if category_parts:
                grouped[category["name"]] = category_parts
        catalog[vehicle["id"]] = {
            "name": vehicle["name"],
            "info": vehicle["info"] or "",
            "crossNote": vehicle["cross_note"] or "",
            "categories": grouped,
        }

    return catalog, {
        "integrity_check": integrity,
        "foreign_key_issues": foreign_key_issues,
    }


def compare_vehicle(
    vehicle_id: str,
    json_vehicle: dict[str, Any],
    sqlite_vehicle: dict[str, Any],
    sample_limit: int,
) -> dict[str, Any] | None:
    metadata_fields = ("name", "info", "crossNote")
    metadata_differences = {
        field: {"json": json_vehicle.get(field, ""), "sqlite": sqlite_vehicle.get(field, "")}
        for field in metadata_fields
        if json_vehicle.get(field, "") != sqlite_vehicle.get(field, "")
    }
    json_categories = json_vehicle.get("categories") or {}
    sqlite_categories = sqlite_vehicle.get("categories") or {}
    category_names = set(json_categories) | set(sqlite_categories)
    category_differences: list[dict[str, Any]] = []
    json_only_total = sqlite_only_total = 0

    for category in sorted(category_names):
        json_counter = Counter(part_signature(part) for part in json_categories.get(category, []))
        sqlite_counter = Counter(part_signature(part) for part in sqlite_categories.get(category, []))
        json_only = json_counter - sqlite_counter
        sqlite_only = sqlite_counter - json_counter
        json_only_count = sum(json_only.values())
        sqlite_only_count = sum(sqlite_only.values())
        if not json_only_count and not sqlite_only_count:
            continue
        json_only_total += json_only_count
        sqlite_only_total += sqlite_only_count
        category_differences.append(
            {
                "category": category,
                "json_parts": len(json_categories.get(category, [])),
                "sqlite_parts": len(sqlite_categories.get(category, [])),
                "json_only_occurrences": json_only_count,
                "sqlite_only_occurrences": sqlite_only_count,
                "json_only_samples": [
                    {**part_label(signature), "occurrences": count}
                    for signature, count in list(json_only.items())[:sample_limit]
                ],
                "sqlite_only_samples": [
                    {**part_label(signature), "occurrences": count}
                    for signature, count in list(sqlite_only.items())[:sample_limit]
                ],
            }
        )

    if not metadata_differences and not category_differences:
        return None
    return {
        "vehicle_id": vehicle_id,
        "metadata_differences": metadata_differences,
        "json_only_part_occurrences": json_only_total,
        "sqlite_only_part_occurrences": sqlite_only_total,
        "category_differences": category_differences,
    }


def build_report(
    json_path: Path,
    sqlite_path: Path,
    sample_limit: int = 3,
    vehicle_detail_limit: int = 25,
) -> dict[str, Any]:
    source_hashes_before = {
        "json_sha256": file_sha256(json_path),
        "sqlite_sha256": file_sha256(sqlite_path),
    }
    json_catalog = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(json_catalog, dict):
        raise ValueError("db.json debe contener un objeto en la raiz")
    sqlite_catalog, sqlite_health = load_sqlite_projection(sqlite_path)

    json_ids = set(json_catalog)
    sqlite_ids = set(sqlite_catalog)
    common_ids = json_ids & sqlite_ids
    vehicle_differences = []
    for vehicle_id in sorted(common_ids):
        difference = compare_vehicle(
            vehicle_id, json_catalog[vehicle_id], sqlite_catalog[vehicle_id], sample_limit
        )
        if difference:
            vehicle_differences.append(difference)

    json_only_parts = sum(item["json_only_part_occurrences"] for item in vehicle_differences)
    sqlite_only_parts = sum(item["sqlite_only_part_occurrences"] for item in vehicle_differences)
    json_only_vehicle_parts = sum(
        catalog_counts({vehicle_id: json_catalog[vehicle_id]})["parts"]
        for vehicle_id in json_ids - sqlite_ids
    )
    sqlite_only_vehicle_parts = sum(
        catalog_counts({vehicle_id: sqlite_catalog[vehicle_id]})["parts"]
        for vehicle_id in sqlite_ids - json_ids
    )
    exact = not (json_ids ^ sqlite_ids) and not vehicle_differences
    vehicle_summaries = [
        {
            "vehicle_id": item["vehicle_id"],
            "metadata_differences": sorted(item["metadata_differences"]),
            "json_only_part_occurrences": item["json_only_part_occurrences"],
            "sqlite_only_part_occurrences": item["sqlite_only_part_occurrences"],
            "different_categories": len(item["category_differences"]),
        }
        for item in vehicle_differences
    ]
    vehicle_differences.sort(
        key=lambda item: (
            item["json_only_part_occurrences"] + item["sqlite_only_part_occurrences"],
            item["vehicle_id"],
        ),
        reverse=True,
    )
    detailed_vehicles = (
        vehicle_differences
        if vehicle_detail_limit < 0
        else vehicle_differences[:vehicle_detail_limit]
    )

    source_hashes_after = {
        "json_sha256": file_sha256(json_path),
        "sqlite_sha256": file_sha256(sqlite_path),
    }
    if source_hashes_before != source_hashes_after:
        raise RuntimeError("Una fuente cambio durante la auditoria; descarte el informe y repita")

    return {
        "schema_version": 1,
        "safety": {
            "mode": "read-only",
            "sources_unchanged_during_run": True,
            "safe_to_replace_json_from_sqlite": exact,
            "decision": "equivalent" if exact else "blocked",
            "reason": (
                "Las proyecciones son equivalentes."
                if exact
                else "Una exportacion SQLite -> JSON agregaria, cambiaria o perderia datos."
            ),
        },
        "sources": {
            "json": str(json_path.resolve()),
            "sqlite": str(sqlite_path.resolve()),
            **source_hashes_after,
        },
        "sqlite_health": sqlite_health,
        "counts": {
            "json": catalog_counts(json_catalog),
            "sqlite_projection": catalog_counts(sqlite_catalog),
        },
        "drift": {
            "json_only_vehicle_ids": sorted(json_ids - sqlite_ids),
            "sqlite_only_vehicle_ids": sorted(sqlite_ids - json_ids),
            "common_vehicles": len(common_ids),
            "exact_common_vehicles": len(common_ids) - len(vehicle_differences),
            "different_common_vehicles": len(vehicle_differences),
            "json_only_part_occurrences_in_common_vehicles": json_only_parts,
            "sqlite_only_part_occurrences_in_common_vehicles": sqlite_only_parts,
            "parts_in_json_only_vehicles": json_only_vehicle_parts,
            "parts_in_sqlite_only_vehicles": sqlite_only_vehicle_parts,
            "different_categories": sum(
                len(item["category_differences"]) for item in vehicle_differences
            ),
            "vehicle_summaries": vehicle_summaries,
            "vehicle_details_included": len(detailed_vehicles),
            "vehicle_details_omitted": len(vehicle_differences) - len(detailed_vehicles),
            "vehicle_details": detailed_vehicles,
        },
        "migration_plan": {
            "status": "ready" if exact else "review-required",
            "effective_canonical_source": "db.json",
            "steps": [
                "Congelar hashes de ambas fuentes y revisar IDs exclusivos.",
                "Clasificar cada diferencia como agregar a SQLite, conservar solo en JSON o corregir.",
                "Aplicar cambios futuros en una copia transaccional de SQLite, nunca sobre el original.",
                "Proyectar la copia a un archivo temporal y exigir equivalencia exacta con db.json.",
                "Reemplazar una fuente solo tras revision humana, respaldo y pruebas del catalogo/Taller.",
            ],
            "prohibited_while_blocked": [
                "python export_db.py",
                "python export_db_fast.py",
                "borrados automaticos en cualquiera de las fuentes",
            ],
        },
    }


def print_summary(report: dict[str, Any]) -> None:
    counts = report["counts"]
    drift = report["drift"]
    print("Reconciliacion SQLite <-> JSON (solo lectura)")
    print("Decision:", report["safety"]["decision"])
    print("JSON:", counts["json"])
    print("SQLite proyectado:", counts["sqlite_projection"])
    print(
        "Vehiculos: JSON-only {json_only} | SQLite-only {sqlite_only} | "
        "comunes distintos {different}".format(
            json_only=len(drift["json_only_vehicle_ids"]),
            sqlite_only=len(drift["sqlite_only_vehicle_ids"]),
            different=drift["different_common_vehicles"],
        )
    )
    print(
        "Componentes en vehiculos comunes: solo JSON {json_only} | solo SQLite {sqlite_only}".format(
            json_only=drift["json_only_part_occurrences_in_common_vehicles"],
            sqlite_only=drift["sqlite_only_part_occurrences_in_common_vehicles"],
        )
    )
    if report["safety"]["decision"] == "blocked":
        print("BLOQUEADO: no ejecutar export_db.py ni export_db_fast.py")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--json", dest="json_path", type=Path, default=root / "db.json")
    parser.add_argument("--sqlite", dest="sqlite_path", type=Path, default=root / "db.sqlite")
    parser.add_argument("--output", type=Path, help="Escribe solamente el informe JSON indicado")
    parser.add_argument("--sample-limit", type=int, default=3)
    parser.add_argument(
        "--vehicle-detail-limit",
        type=int,
        default=25,
        help="Vehiculos con detalle de categorias; -1 incluye todos (por defecto: 25)",
    )
    parser.add_argument(
        "--fail-on-drift", action="store_true", help="Retorna codigo 2 si las fuentes difieren"
    )
    args = parser.parse_args()
    if args.sample_limit < 0:
        parser.error("--sample-limit no puede ser negativo")

    report = build_report(
        args.json_path.resolve(),
        args.sqlite_path.resolve(),
        args.sample_limit,
        args.vehicle_detail_limit,
    )
    print_summary(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("Informe escrito:", args.output.resolve())
    if args.fail_on_drift and report["safety"]["decision"] != "equivalent":
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, sqlite3.Error, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
