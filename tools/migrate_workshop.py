#!/usr/bin/env python3
"""Prevalida e importa un respaldo LocalStorage de Taller a SQLite de forma segura."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "database" / "migrations" / "sqlite"
FORMAT = "repuestospro-workshop-backup"
SUPPORTED_VERSIONS = {1, 2, 3}
NAMESPACE = uuid.UUID("6dd6cd50-e39f-4dbe-893b-f6a496ae7905")


class MigrationError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    # JSON.stringify serializa 1.0 y -0.0 como 1 y 0; el respaldo web calcula el hash
    # sobre esa representación, no sobre el texto (posiblemente indentado) del archivo.
    def javascript_numbers(item: Any) -> Any:
        if isinstance(item, float) and item.is_integer():
            return int(item)
        if isinstance(item, list):
            return [javascript_numbers(child) for child in item]
        if isinstance(item, dict):
            return {key: javascript_numbers(child) for key, child in item.items()}
        return item
    return json.dumps(javascript_numbers(value), ensure_ascii=False, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def stable_id(tenant_id: str, kind: str, legacy_id: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{tenant_id}:{kind}:{legacy_id}"))


def money(value: Any) -> int:
    try:
        number = float(value or 0)
    except (TypeError, ValueError) as error:
        raise MigrationError(f"Monto inválido: {value!r}") from error
    if number < 0 or number != number or number in (float("inf"), float("-inf")):
        raise MigrationError(f"Monto inválido: {value!r}")
    return round(number)


def calculate_totals(order: dict[str, Any]) -> dict[str, int | float]:
    def line_sum(field: str) -> int:
        total = 0
        for line in order.get(field, []) if isinstance(order.get(field, []), list) else []:
            if isinstance(line, dict):
                subtotal = line.get("subtotal")
                if subtotal is None:
                    subtotal = float(line.get("cantidad") or 1) * float(line.get("precioUnitario") or 0)
                total += money(subtotal)
        return total
    services = line_sum("servicios"); labor = line_sum("manoObra"); parts = line_sum("repuestos")
    subtotal = services + labor + parts
    discount = min(money(order.get("descuento")), subtotal)
    basis = subtotal - discount
    tax_percent = min(100.0, max(0.0, float(order.get("impuestoPorcentaje") or 0)))
    tax = round(basis * tax_percent / 100)
    return {"serviciosSubtotal": services, "manoObraSubtotal": labor, "repuestosSubtotal": parts,
            "subtotal": subtotal, "descuento": discount, "baseImponible": basis,
            "impuestoPorcentaje": tax_percent, "impuesto": tax, "total": basis + tax}


def load_source(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = path.read_text(encoding="utf-8")
    document = json.loads(raw)
    if not isinstance(document, dict):
        raise MigrationError("El origen debe ser un objeto JSON.")
    if document.get("format") == FORMAT:
        data = document.get("data")
        checksum = document.get("checksum", {})
        if not isinstance(data, dict):
            raise MigrationError("El envelope no contiene un payload válido.")
        if checksum.get("algorithm") != "SHA-256" or not checksum.get("value"):
            raise MigrationError("El envelope no contiene un checksum SHA-256.")
        actual = sha256_text(canonical_json(data))
        if actual.lower() != str(checksum["value"]).lower():
            raise MigrationError("El checksum del respaldo no coincide con su payload.")
        metadata = {"format": FORMAT, "source_sha256": actual, "checksum_verified": True}
    else:
        data = document
        metadata = {
            "format": "repuestospro-workshop-localstorage",
            "source_sha256": sha256_text(canonical_json(data)),
            "checksum_verified": False,
        }
    return data, metadata


def validate(data: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    version = data.get("version", 1)
    if version not in SUPPORTED_VERSIONS:
        errors.append(f"Versión de esquema no soportada: {version!r}")
    collections: dict[str, list[dict[str, Any]]] = {}
    for name in ("clients", "vehicles", "services", "workOrders"):
        value = data.get(name, [])
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            errors.append(f"{name} debe ser una lista de objetos.")
            collections[name] = []
        else:
            collections[name] = value
        ids = [str(item.get("id", "")) for item in collections[name]]
        if any(not item_id for item_id in ids):
            errors.append(f"{name} contiene registros sin id legado.")
        if len(ids) != len(set(ids)):
            errors.append(f"{name} contiene ids legados duplicados.")

    client_ids = {str(item.get("id")) for item in collections["clients"]}
    vehicle_ids = {str(item.get("id")) for item in collections["vehicles"]}
    service_ids = {str(item.get("id")) for item in collections["services"]}
    for vehicle in collections["vehicles"]:
        if str(vehicle.get("clienteId")) not in client_ids:
            errors.append(f"Vehículo {vehicle.get('id')} referencia un cliente inexistente.")
    expected_lines = 0
    for order in collections["workOrders"]:
        if str(order.get("clienteId")) not in client_ids:
            errors.append(f"OT {order.get('id')} referencia un cliente inexistente.")
        if str(order.get("vehiculoId")) not in vehicle_ids:
            errors.append(f"OT {order.get('id')} referencia un vehículo inexistente.")
        for field in ("servicios", "manoObra", "repuestos"):
            lines = order.get(field, [])
            if not isinstance(lines, list):
                errors.append(f"OT {order.get('id')}: {field} no es una lista.")
                continue
            expected_lines += len(lines)
            for line in lines:
                if not isinstance(line, dict) or not line.get("id"):
                    errors.append(f"OT {order.get('id')}: línea {field} inválida o sin id.")
                if field == "servicios" and line.get("servicioId") and str(line["servicioId"]) not in service_ids:
                    warnings.append(f"OT {order.get('id')}: servicio {line['servicioId']} no existe; se conserva snapshot.")
        try:
            recalculated = calculate_totals(order)
            stored = order.get("totales")
            if isinstance(stored, dict):
                for field in ("serviciosSubtotal", "manoObraSubtotal", "repuestosSubtotal", "subtotal", "descuento", "baseImponible", "impuesto", "total"):
                    if money(stored.get(field)) != recalculated[field]:
                        errors.append(f"OT {order.get('id')}: total {field} no coincide con sus líneas.")
        except (MigrationError, TypeError, ValueError) as error:
            errors.append(f"OT {order.get('id')}: no fue posible recalcular totales ({error}).")
    counts = {name: len(value) for name, value in collections.items()}
    counts["workOrderLines"] = expected_lines
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": counts,
        "schemaVersion": version,
        **metadata,
    }


def apply_migrations(db: sqlite3.Connection) -> None:
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")
    db.execute("PRAGMA busy_timeout = 5000")
    existing = set()
    if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_migrations'").fetchone():
        existing = {row[0] for row in db.execute("SELECT version FROM schema_migrations")}
    for migration in sorted(MIGRATIONS.glob("*.sql")):
        version = migration.stem
        if version not in existing:
            db.executescript(migration.read_text(encoding="utf-8"))


def create_backup(db_path: Path, backup_dir: Path) -> Path | None:
    if not db_path.exists():
        return None
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = backup_dir / f"{db_path.stem}.pre-import-{stamp}{db_path.suffix}"
    source = sqlite3.connect(db_path)
    destination = sqlite3.connect(target)
    try:
        source.backup(destination)
        if destination.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise MigrationError("El respaldo SQLite no superó integrity_check.")
    finally:
        destination.close()
        source.close()
    manifest = target.with_suffix(target.suffix + ".sha256")
    manifest.write_text(hashlib.sha256(target.read_bytes()).hexdigest() + "  " + target.name + "\n", encoding="ascii")
    return target


def _timestamp(record: dict[str, Any], field: str, fallback: str) -> str:
    return str(record.get(field) or fallback)


def import_sqlite(data: dict[str, Any], report: dict[str, Any], db_path: Path, tenant_name: str, backup_dir: Path) -> dict[str, Any]:
    if not report["valid"]:
        raise MigrationError("No se puede importar un origen inválido.")
    tenant_id = stable_id("global", "tenant", tenant_name)
    branch_id = stable_id(tenant_id, "branch", "MATRIZ")
    run_id = stable_id(tenant_id, "import", report["source_sha256"])
    backup = create_backup(db_path, backup_dir)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(db_path)
    now = utc_now()
    try:
        apply_migrations(db)
        if db.execute("SELECT 1 FROM legacy_import_runs WHERE tenant_id=? AND source_sha256=?", (tenant_id, report["source_sha256"])).fetchone():
            raise MigrationError("Este respaldo ya fue importado para el tenant destino.")
        db.execute("BEGIN IMMEDIATE")
        db.execute("INSERT OR IGNORE INTO tenants(id,name,created_at,updated_at) VALUES (?,?,?,?)", (tenant_id, tenant_name, now, now))
        db.execute("INSERT OR IGNORE INTO branches(id,tenant_id,name,code,created_at,updated_at) VALUES (?,?,?,?,?,?)", (branch_id, tenant_id, "Casa matriz", "MATRIZ", now, now))
        client_map: dict[str, str] = {}
        for item in data.get("clients", []):
            legacy = str(item["id"]); item_id = stable_id(tenant_id, "client", legacy); client_map[legacy] = item_id
            db.execute("""INSERT INTO clients(
                id,tenant_id,branch_id,legacy_id,first_name,last_name,rut_normalized,phone,whatsapp,email,
                address,notes,created_at,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                item_id, tenant_id, branch_id, legacy, str(item.get("nombre") or "Sin nombre"), str(item.get("apellido") or ""),
                item.get("rut") or None, item.get("telefono") or None, item.get("whatsapp") or None, item.get("email") or None,
                item.get("direccion") or None, item.get("notas") or None, _timestamp(item, "createdAt", now), _timestamp(item, "updatedAt", now)))
        vehicle_map: dict[str, str] = {}
        for item in data.get("vehicles", []):
            legacy = str(item["id"]); item_id = stable_id(tenant_id, "vehicle", legacy); vehicle_map[legacy] = item_id
            db.execute("""INSERT INTO vehicles(
                id,tenant_id,client_id,legacy_id,plate_normalized,vin_normalized,brand,model,model_year,engine,
                displacement,fuel,transmission,mileage,color,notes,created_at,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                item_id, tenant_id, client_map[str(item["clienteId"])], legacy, str(item.get("patente") or "SIN-" + legacy),
                item.get("vin") or None, item.get("marca"), item.get("modelo"), item.get("anio"), item.get("motor"), item.get("cilindrada"),
                item.get("combustible"), item.get("transmision"), item.get("kilometraje"), item.get("color"), item.get("notas"),
                _timestamp(item, "createdAt", now), _timestamp(item, "updatedAt", now)))
        service_map: dict[str, str] = {}
        for item in data.get("services", []):
            legacy = str(item["id"]); item_id = stable_id(tenant_id, "service", legacy); service_map[legacy] = item_id
            db.execute("""INSERT INTO workshop_services(
                id,tenant_id,legacy_id,name,description,base_price_minor,estimated_minutes,active,created_at,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?)""", (
                item_id, tenant_id, legacy, str(item.get("nombre") or "Servicio"), item.get("descripcion"), money(item.get("precioBase")),
                item.get("duracionEstimada"), 1 if item.get("activo") else 0, _timestamp(item, "createdAt", now), _timestamp(item, "updatedAt", now),))
        inserted_lines = 0
        for order in data.get("workOrders", []):
            legacy = str(order["id"]); order_id = stable_id(tenant_id, "work_order", legacy)
            totals = calculate_totals(order)
            db.execute("""INSERT INTO work_orders(
                id,tenant_id,branch_id,client_id,vehicle_id,legacy_id,identifier,status,opened_on,closed_at,mileage,
                reported_problem,diagnosis,notes,services_subtotal_minor,labor_subtotal_minor,parts_subtotal_minor,
                subtotal_minor,discount_minor,tax_basis_minor,tax_percent,tax_minor,total_minor,created_at,updated_at,
                legacy_snapshot_json
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                order_id, tenant_id, branch_id, client_map[str(order["clienteId"])], vehicle_map[str(order["vehiculoId"])], legacy,
                str(order.get("identificador") or legacy), str(order.get("estado") or "Presupuesto"), order.get("fecha"), order.get("closedAt") or None,
                order.get("kilometraje"), order.get("problemaReportado"), order.get("diagnostico"), order.get("notas"),
                money(totals.get("serviciosSubtotal")), money(totals.get("manoObraSubtotal")), money(totals.get("repuestosSubtotal")),
                money(totals.get("subtotal")), money(totals.get("descuento", order.get("descuento"))), money(totals.get("baseImponible")),
                float(totals.get("impuestoPorcentaje", order.get("impuestoPorcentaje", 0)) or 0), money(totals.get("impuesto")), money(totals.get("total")),
                _timestamp(order, "createdAt", now), _timestamp(order, "updatedAt", now), canonical_json(order)))
            for field, line_type in (("servicios", "service"), ("manoObra", "labor"), ("repuestos", "part")):
                for position, line in enumerate(order.get(field, [])):
                    line_legacy = str(line["id"]); line_id = stable_id(tenant_id, f"line:{legacy}", line_legacy)
                    snapshot = line.get("catalogSnapshot") if line_type == "part" else None
                    description = line.get("descripcion") or (snapshot or {}).get("name") or "Línea importada"
                    service_id = service_map.get(str(line.get("servicioId"))) if line_type == "service" else None
                    unit = None if line.get("precioUnitario") is None else money(line.get("precioUnitario"))
                    db.execute("INSERT INTO work_order_lines VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                        line_id, tenant_id, order_id, line_legacy, line_type, service_id, description, float(line.get("cantidad") or 1),
                        unit, money(line.get("subtotal")), canonical_json(snapshot) if snapshot is not None else None, position))
                    inserted_lines += 1
            db.execute("INSERT INTO work_order_status_history VALUES (?,?,?,?,?,?,?)", (
                stable_id(tenant_id, "status", legacy), tenant_id, order_id, None, str(order.get("estado") or "Presupuesto"),
                _timestamp(order, "updatedAt", now), "Estado inicial importado desde LocalStorage"))
        actual = {"clients": db.execute("SELECT count(*) FROM clients WHERE tenant_id=?", (tenant_id,)).fetchone()[0],
                  "vehicles": db.execute("SELECT count(*) FROM vehicles WHERE tenant_id=?", (tenant_id,)).fetchone()[0],
                  "services": db.execute("SELECT count(*) FROM workshop_services WHERE tenant_id=?", (tenant_id,)).fetchone()[0],
                  "workOrders": db.execute("SELECT count(*) FROM work_orders WHERE tenant_id=?", (tenant_id,)).fetchone()[0],
                  "workOrderLines": inserted_lines}
        if actual != report["counts"]:
            raise MigrationError(f"La conciliación de conteos falló: esperado {report['counts']}, obtenido {actual}")
        if db.execute("PRAGMA foreign_key_check").fetchall():
            raise MigrationError("La verificación de claves foráneas falló.")
        final_report = {**report, "destinationCounts": actual, "tenantId": tenant_id, "branchId": branch_id}
        db.execute("INSERT INTO legacy_import_runs VALUES (?,?,?,?,?,?,?,?)", (run_id, tenant_id, report["format"], report["schemaVersion"], report["source_sha256"], now, canonical_json(actual), canonical_json(final_report)))
        db.commit()
        final_report.update({"applied": True, "backup": str(backup) if backup else None, "integrity": "ok"})
        return final_report
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="JSON crudo de LocalStorage o envelope de respaldo")
    parser.add_argument("--database", type=Path, default=ROOT / "repuestospro-local.sqlite")
    parser.add_argument("--tenant-name", default="Mi taller")
    parser.add_argument("--backup-dir", type=Path, default=ROOT / "backups")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--apply", action="store_true", help="Confirma la escritura; sin esta opción solo previsualiza")
    args = parser.parse_args()
    data, metadata = load_source(args.source)
    report = validate(data, metadata)
    if args.apply and report["valid"]:
        report = import_sqlite(data, report, args.database, args.tenant_name, args.backup_dir)
    else:
        report["applied"] = False
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, sqlite3.Error, MigrationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

