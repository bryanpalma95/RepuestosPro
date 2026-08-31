#!/usr/bin/env python3
"""Pruebas unitarias para sqlite_json_reconcile.py (solo biblioteca estandar)."""

from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from sqlite_json_reconcile import build_report, file_sha256


SCHEMA = """
CREATE TABLE vehicles(id TEXT PRIMARY KEY,name TEXT NOT NULL,info TEXT,cross_note TEXT);
CREATE TABLE categories(id INTEGER PRIMARY KEY,vehicle_id TEXT,name TEXT,sort_order INTEGER);
CREATE TABLE parts(id INTEGER PRIMARY KEY,category_id INTEGER,cat_label TEXT,name TEXT,
                  details TEXT,brands TEXT,interval_info TEXT);
CREATE TABLE part_refs(id INTEGER PRIMARY KEY,part_id INTEGER,reference TEXT,status TEXT);
CREATE TABLE part_links(id INTEGER PRIMARY KEY,part_id INTEGER,label TEXT,url TEXT);
"""


def vehicle(part_name: str = "Filtro") -> dict:
    return {
        "name": "Marca Modelo 2020",
        "info": "Motor X",
        "crossNote": "",
        "categories": {
            "Motor": [
                {
                    "cat": "MOTOR",
                    "name": part_name,
                    "details": "Detalle",
                    "brands": "Proveedor",
                    "refs": [{"r": "ABC-1", "s": "confirmed"}],
                    "links": [{"t": "Fuente", "u": "https://example.test"}],
                }
            ]
        },
    }


class ReconcileTests(unittest.TestCase):
    def make_sources(self, root: Path, json_part_name: str = "Filtro") -> tuple[Path, Path]:
        json_path = root / "db.json"
        sqlite_path = root / "db.sqlite"
        json_path.write_text(
            json.dumps({"marca-modelo-2020": vehicle(json_part_name)}), encoding="utf-8"
        )
        connection = sqlite3.connect(sqlite_path)
        connection.executescript(SCHEMA)
        connection.execute(
            "INSERT INTO vehicles VALUES (?,?,?,?)",
            ("marca-modelo-2020", "Marca Modelo 2020", "Motor X", ""),
        )
        connection.execute("INSERT INTO categories VALUES (1,?,?,0)", ("marca-modelo-2020", "Motor"))
        connection.execute(
            "INSERT INTO parts VALUES (1,1,?,?,?,?,NULL)",
            ("MOTOR", "Filtro", "Detalle", "Proveedor"),
        )
        connection.execute("INSERT INTO part_refs VALUES (1,1,'ABC-1','confirmed')")
        connection.execute(
            "INSERT INTO part_links VALUES (1,1,'Fuente','https://example.test')"
        )
        connection.commit()
        connection.close()
        return json_path, sqlite_path

    def test_equivalent_sources_are_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            json_path, sqlite_path = self.make_sources(Path(temp))
            hashes = (file_sha256(json_path), file_sha256(sqlite_path))
            report = build_report(json_path, sqlite_path)
            self.assertEqual("equivalent", report["safety"]["decision"])
            self.assertTrue(report["safety"]["safe_to_replace_json_from_sqlite"])
            self.assertEqual(hashes, (file_sha256(json_path), file_sha256(sqlite_path)))

    def test_drift_is_classified_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            json_path, sqlite_path = self.make_sources(Path(temp), "Filtro enriquecido")
            hashes = (file_sha256(json_path), file_sha256(sqlite_path))
            report = build_report(json_path, sqlite_path)
            drift = report["drift"]
            self.assertEqual("blocked", report["safety"]["decision"])
            self.assertEqual(1, drift["different_common_vehicles"])
            self.assertEqual(1, drift["json_only_part_occurrences_in_common_vehicles"])
            self.assertEqual(1, drift["sqlite_only_part_occurrences_in_common_vehicles"])
            self.assertEqual(1, len(drift["vehicle_summaries"]))
            self.assertEqual(1, drift["vehicle_details_included"])
            self.assertEqual(hashes, (file_sha256(json_path), file_sha256(sqlite_path)))


if __name__ == "__main__":
    unittest.main()
