#!/usr/bin/env python3
"""Pruebas de prevalidación, integridad, respaldo y rollback del importador Taller."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from migrate_workshop import FORMAT, MigrationError, canonical_json, import_sqlite, load_source, validate


def fixture() -> dict:
    return {
        "version": 3,
        "clients": [{"id": "cli-1", "nombre": "Ana", "apellido": "Pérez", "rut": "12345678-5"}],
        "vehicles": [{"id": "veh-1", "clienteId": "cli-1", "patente": "ABCD12", "marca": "Kia", "modelo": "Rio"}],
        "services": [{"id": "srv-1", "nombre": "Cambio aceite", "precioBase": 20000, "activo": True}],
        "workOrders": [{
            "id": "ot-1", "identificador": "OT-2026-0001", "clienteId": "cli-1", "vehiculoId": "veh-1",
            "estado": "Pendiente", "servicios": [{"id": "line-1", "servicioId": "srv-1", "descripcion": "Cambio aceite", "cantidad": 1, "precioUnitario": 20000, "subtotal": 20000}],
            "manoObra": [], "repuestos": [{"id": "part-1", "cantidad": 1, "precioUnitario": 5000, "subtotal": 5000,
                "catalogSnapshot": {"catalogId": "catalog-1", "name": "Filtro", "references": [{"code": "26300", "status": "verify"}], "compatibilityConfirmed": False}}],
            "descuento": 0, "impuestoPorcentaje": 0,
            "totales": {"serviciosSubtotal": 20000, "manoObraSubtotal": 0, "repuestosSubtotal": 5000, "subtotal": 25000, "descuento": 0, "baseImponible": 25000, "impuestoPorcentaje": 0, "impuesto": 0, "total": 25000}
        }]
    }


class WorkshopMigrationTests(unittest.TestCase):
    def make_source(self, root: Path, data: dict | None = None, checksum: str | None = None) -> Path:
        payload = data or fixture()
        digest = checksum or hashlib.sha256(canonical_json(payload).encode()).hexdigest()
        source = root / "backup.json"
        source.write_text(json.dumps({"format": FORMAT, "backupVersion": 1, "checksum": {"algorithm": "SHA-256", "value": digest}, "data": payload}, ensure_ascii=False), encoding="utf-8")
        return source

    def test_checksum_is_verified_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(MigrationError, "checksum"):
                load_source(self.make_source(Path(temp), checksum="0" * 64))

    def test_broken_reference_blocks_preview(self) -> None:
        data = fixture(); data["vehicles"][0]["clienteId"] = "missing"
        report = validate(data, {"format": FORMAT, "source_sha256": "abc", "checksum_verified": True})
        self.assertFalse(report["valid"])
        self.assertTrue(any("cliente inexistente" in error for error in report["errors"]))

    def test_incorrect_legacy_total_blocks_import(self) -> None:
        data = fixture(); data["workOrders"][0]["totales"]["total"] = 999
        report = validate(data, {"format": FORMAT, "source_sha256": "abc", "checksum_verified": True})
        self.assertFalse(report["valid"])
        self.assertTrue(any("total total" in error for error in report["errors"]))

    def test_import_preserves_counts_snapshots_and_verify_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); data, metadata = load_source(self.make_source(root)); report = validate(data, metadata)
            result = import_sqlite(data, report, root / "local.sqlite", "Taller fixture", root / "backups")
            self.assertTrue(result["applied"])
            self.assertEqual(report["counts"], result["destinationCounts"])
            db = sqlite3.connect(root / "local.sqlite")
            snapshot = json.loads(db.execute("SELECT catalog_snapshot_json FROM work_order_lines WHERE line_type='part'").fetchone()[0])
            self.assertEqual("verify", snapshot["references"][0]["status"])
            self.assertEqual([], db.execute("PRAGMA foreign_key_check").fetchall())
            db.close()

    def test_existing_database_gets_verified_backup_and_duplicate_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = self.make_source(root); data, metadata = load_source(source); report = validate(data, metadata)
            database = root / "local.sqlite"; backup_dir = root / "backups"
            import_sqlite(data, report, database, "Taller fixture", backup_dir)
            with self.assertRaisesRegex(MigrationError, "ya fue importado"):
                import_sqlite(data, report, database, "Taller fixture", backup_dir)
            backups = list(backup_dir.glob("*.sqlite"))
            self.assertTrue(backups)
            self.assertTrue(backups[0].with_suffix(".sqlite.sha256").exists())
            db = sqlite3.connect(database)
            self.assertEqual(1, db.execute("SELECT count(*) FROM legacy_import_runs").fetchone()[0])
            db.close()


if __name__ == "__main__":
    unittest.main()

