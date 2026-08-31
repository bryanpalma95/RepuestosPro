#!/usr/bin/env python3
"""Audita cobertura, calidad de referencias y deriva entre JSON y SQLite.

El catálogo publicado (db.json) es la fuente efectiva para esta auditoría. La
comparación con db.sqlite es deliberadamente de solo lectura: nunca exporta ni
elimina registros.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import statistics
from collections import Counter, defaultdict
from pathlib import Path


PLACEHOLDER_RE = re.compile(
    r"\b(verificar|consultar|sin cambio|por modelo|por motor|seg[uú]n|"
    r"universal|posible|aprox|integrado|oem\b)\b",
    re.IGNORECASE,
)


def percentile(values: list[int], ratio: float) -> int:
    if not values:
        return 0
    return values[min(len(values) - 1, int((len(values) - 1) * ratio))]


def normalized_reference(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def vehicle_part_count(vehicle: dict) -> int:
    return sum(len(parts) for parts in vehicle.get("categories", {}).values())


def audit(repo: Path) -> dict:
    catalog = json.loads((repo / "db.json").read_text(encoding="utf-8"))
    compatibility = json.loads((repo / "db-compat.json").read_text(encoding="utf-8"))

    part_counts: list[int] = []
    part_counts_by_id: dict[str, int] = {}
    brand_counts: dict[str, list[int]] = defaultdict(list)
    status_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    placeholder_counts: Counter[str] = Counter()
    references_by_code: dict[str, set[str]] = defaultdict(set)
    no_reference_parts = 0
    source_links = 0
    invalid_statuses: Counter[str] = Counter()

    for vehicle_id, vehicle in catalog.items():
        count = vehicle_part_count(vehicle)
        part_counts.append(count)
        part_counts_by_id[vehicle_id] = count
        brand = str(vehicle.get("name", "")).split(maxsplit=1)[0]
        brand_counts[brand].append(count)

        for parts in vehicle.get("categories", {}).values():
            for part in parts:
                category_counts[str(part.get("cat", ""))] += 1
                source_links += len(part.get("links") or [])
                refs = part.get("refs") or []
                if not refs:
                    no_reference_parts += 1
                for ref in refs:
                    code = str(ref.get("r", "")).strip()
                    status = str(ref.get("s", "")).strip()
                    status_counts[status] += 1
                    if status not in {"confirmed", "verify"}:
                        invalid_statuses[status] += 1
                    if PLACEHOLDER_RE.search(code):
                        placeholder_counts[code] += 1
                        continue
                    normalized = normalized_reference(code)
                    if normalized:
                        references_by_code[normalized].add(vehicle_id)

    part_counts.sort()
    compatibility_keys = {
        normalized_reference(key) for key in compatibility if normalized_reference(key)
    }
    shared_references = {
        code: vehicles for code, vehicles in references_by_code.items() if len(vehicles) >= 2
    }

    sqlite_report: dict[str, object] = {"available": False}
    sqlite_path = repo / "db.sqlite"
    if sqlite_path.exists():
        connection = sqlite3.connect(
            sqlite_path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True
        )
        connection.execute("PRAGMA query_only = ON")
        sqlite_ids = {row[0] for row in connection.execute("SELECT id FROM vehicles")}
        sqlite_part_counts = dict(
            connection.execute(
                """
                SELECT v.id, COUNT(p.id)
                FROM vehicles v
                LEFT JOIN categories c ON c.vehicle_id = v.id
                LEFT JOIN parts p ON p.category_id = c.id
                GROUP BY v.id
                """
            )
        )
        connection.close()
        json_ids = set(catalog)
        overlap = sqlite_ids & json_ids
        sqlite_report = {
            "available": True,
            "vehicles": len(sqlite_ids),
            "json_vehicles": len(json_ids),
            "sqlite_only": sorted(sqlite_ids - json_ids),
            "json_only": sorted(json_ids - sqlite_ids),
            "overlap_with_different_part_count": sum(
                sqlite_part_counts.get(vehicle_id, 0) != part_counts_by_id[vehicle_id]
                for vehicle_id in overlap
            ),
            "safe_to_export": sqlite_ids == json_ids
            and all(
                sqlite_part_counts.get(vehicle_id, 0) == part_counts_by_id[vehicle_id]
                for vehicle_id in overlap
            ),
        }

    low_coverage = sorted(
        (
            {
                "vehicle_id": vehicle_id,
                "name": catalog[vehicle_id].get("name", ""),
                "parts": count,
            }
            for vehicle_id, count in part_counts_by_id.items()
        ),
        key=lambda item: (item["parts"], item["vehicle_id"]),
    )[:50]

    return {
        "catalog": {
            "vehicles": len(catalog),
            "parts": sum(part_counts),
            "references": sum(status_counts.values()),
            "reference_statuses": dict(status_counts),
            "invalid_statuses": dict(invalid_statuses),
            "parts_without_reference": no_reference_parts,
            "source_links": source_links,
            "parts_per_vehicle": {
                "min": part_counts[0] if part_counts else 0,
                "p10": percentile(part_counts, 0.10),
                "median": statistics.median(part_counts) if part_counts else 0,
                "p90": percentile(part_counts, 0.90),
                "max": part_counts[-1] if part_counts else 0,
            },
        },
        "compatibility": {
            "entries": len(compatibility),
            "unique_non_placeholder_references": len(references_by_code),
            "shared_references": len(shared_references),
            "shared_references_without_compatibility": sum(
                code not in compatibility_keys for code in shared_references
            ),
        },
        "brands": {
            brand: {
                "vehicles": len(values),
                "average_parts": round(statistics.mean(values), 2),
                "min_parts": min(values),
                "max_parts": max(values),
            }
            for brand, values in sorted(brand_counts.items())
        },
        "top_categories": category_counts.most_common(50),
        "top_placeholder_references": placeholder_counts.most_common(50),
        "lowest_coverage_vehicles": low_coverage,
        "sqlite_drift": sqlite_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Emite el informe completo como JSON")
    parser.add_argument("--strict", action="store_true", help="Falla ante estados inválidos o JSON ilegible")
    args = parser.parse_args()

    report = audit(args.repo.resolve())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        catalog = report["catalog"]
        compatibility = report["compatibility"]
        drift = report["sqlite_drift"]
        print(
            "Catálogo: {vehicles} vehículos | {parts} componentes | {references} referencias".format(
                **catalog
            )
        )
        print("Estados:", catalog["reference_statuses"])
        print("Cobertura por vehículo:", catalog["parts_per_vehicle"])
        print("Componentes sin referencia:", catalog["parts_without_reference"])
        print(
            "Compatibilidad: {entries} fichas | {shared_references_without_compatibility} "
            "referencias compartidas sin ficha".format(**compatibility)
        )
        print("SQLite:", drift)
        print("Vehículos con menor cobertura:")
        for item in report["lowest_coverage_vehicles"][:20]:
            print(f"  {item['parts']:>2}  {item['vehicle_id']}")

    if args.strict and report["catalog"]["invalid_statuses"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
