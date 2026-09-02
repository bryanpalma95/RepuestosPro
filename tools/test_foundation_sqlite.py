#!/usr/bin/env python3
"""Pruebas de contrato para la migración fundacional de RepuestosPro Local."""

from __future__ import annotations

import sqlite3
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "database" / "migrations" / "sqlite" / "0001_foundations.sql"
NOW = "2026-09-01T12:00:00.000Z"


class FoundationMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(MIGRATION.read_text(encoding="utf-8"))
        self.db.execute(
            "INSERT INTO tenants(id,name,created_at,updated_at) VALUES (?,?,?,?)",
            ("tenant-a", "Taller A", NOW, NOW),
        )
        self.db.execute(
            "INSERT INTO tenants(id,name,created_at,updated_at) VALUES (?,?,?,?)",
            ("tenant-b", "Taller B", NOW, NOW),
        )
        self.db.execute(
            "INSERT INTO branches(id,tenant_id,name,code,created_at,updated_at) VALUES (?,?,?,?,?,?)",
            ("branch-a", "tenant-a", "Casa matriz A", "MATRIZ", NOW, NOW),
        )
        self.db.execute(
            "INSERT INTO branches(id,tenant_id,name,code,created_at,updated_at) VALUES (?,?,?,?,?,?)",
            ("branch-b", "tenant-b", "Casa matriz B", "MATRIZ", NOW, NOW),
        )
        self.db.execute(
            "INSERT INTO users(id,email,display_name,status,created_at,updated_at) VALUES (?,?,?,?,?,?)",
            ("user-a", "owner@example.test", "Owner", "active", NOW, NOW),
        )
        self.db.execute(
            "INSERT INTO memberships(id,tenant_id,user_id,default_branch_id,created_at,updated_at) VALUES (?,?,?,?,?,?)",
            ("membership-a", "tenant-a", "user-a", "branch-a", NOW, NOW),
        )
        self.db.execute(
            "INSERT INTO roles(id,tenant_id,code,name,created_at,updated_at) VALUES (?,?,?,?,?,?)",
            ("role-a", "tenant-a", "owner", "Propietario", NOW, NOW),
        )
        self.db.execute(
            "INSERT INTO roles(id,tenant_id,code,name,created_at,updated_at) VALUES (?,?,?,?,?,?)",
            ("role-b", "tenant-b", "owner", "Propietario", NOW, NOW),
        )

    def tearDown(self) -> None:
        self.db.close()

    def test_migration_is_registered_and_integral(self) -> None:
        version = self.db.execute("SELECT version FROM schema_migrations").fetchone()[0]
        self.assertEqual(version, "0001_foundations")
        self.assertEqual(self.db.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_membership_cannot_reference_branch_from_another_tenant(self) -> None:
        with self.assertRaisesRegex(sqlite3.IntegrityError, "another tenant"):
            self.db.execute(
                "UPDATE memberships SET default_branch_id=? WHERE id=?",
                ("branch-b", "membership-a"),
            )

    def test_role_assignment_cannot_cross_tenants(self) -> None:
        with self.assertRaisesRegex(sqlite3.IntegrityError, "different tenants"):
            self.db.execute(
                "INSERT INTO membership_roles(membership_id,role_id,created_at) VALUES (?,?,?)",
                ("membership-a", "role-b", NOW),
            )

    def test_counter_cannot_cross_tenants(self) -> None:
        with self.assertRaisesRegex(sqlite3.IntegrityError, "another tenant"):
            self.db.execute(
                "INSERT INTO tenant_counters(tenant_id,branch_id,counter_type,counter_year,updated_at) VALUES (?,?,?,?,?)",
                ("tenant-a", "branch-b", "work_order", 2026, NOW),
            )

    def test_audit_event_preserves_previous_and_new_values(self) -> None:
        self.db.execute(
            """
            INSERT INTO audit_events(
                id,tenant_id,branch_id,actor_user_id,action,entity_type,entity_id,
                occurred_at,source,previous_value_json,new_value_json
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                "audit-1", "tenant-a", "branch-a", "user-a", "work_order.closed",
                "work_order", "order-1", NOW, "local", '{"status":"repair"}',
                '{"status":"delivered"}',
            ),
        )
        event = self.db.execute(
            "SELECT previous_value_json,new_value_json FROM audit_events WHERE id='audit-1'"
        ).fetchone()
        self.assertEqual(event, ('{"status":"repair"}', '{"status":"delivered"}'))


if __name__ == "__main__":
    unittest.main()
