PRAGMA foreign_keys = ON;

BEGIN IMMEDIATE;

CREATE TABLE clients (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    branch_id TEXT REFERENCES branches(id) ON DELETE SET NULL,
    legacy_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL DEFAULT '',
    rut_normalized TEXT,
    phone TEXT,
    whatsapp TEXT,
    email TEXT,
    address TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    archived_at TEXT,
    UNIQUE (tenant_id, legacy_id)
);
CREATE UNIQUE INDEX clients_tenant_rut_unique ON clients(tenant_id, rut_normalized)
    WHERE rut_normalized IS NOT NULL AND rut_normalized <> '' AND archived_at IS NULL;

CREATE TABLE vehicles (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    client_id TEXT NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
    legacy_id TEXT NOT NULL,
    plate_normalized TEXT NOT NULL,
    vin_normalized TEXT,
    brand TEXT,
    model TEXT,
    model_year INTEGER,
    engine TEXT,
    displacement TEXT,
    fuel TEXT,
    transmission TEXT,
    mileage INTEGER,
    color TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    archived_at TEXT,
    UNIQUE (tenant_id, legacy_id)
);
CREATE UNIQUE INDEX vehicles_tenant_plate_unique ON vehicles(tenant_id, plate_normalized)
    WHERE archived_at IS NULL;
CREATE UNIQUE INDEX vehicles_tenant_vin_unique ON vehicles(tenant_id, vin_normalized)
    WHERE vin_normalized IS NOT NULL AND vin_normalized <> '' AND archived_at IS NULL;

CREATE TRIGGER vehicles_client_tenant_insert BEFORE INSERT ON vehicles BEGIN
    SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM clients WHERE id=NEW.client_id AND tenant_id=NEW.tenant_id)
    THEN RAISE(ABORT, 'vehicle client belongs to another tenant') END;
END;

CREATE TABLE workshop_services (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    legacy_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    base_price_minor INTEGER NOT NULL DEFAULT 0 CHECK (base_price_minor >= 0),
    estimated_minutes INTEGER CHECK (estimated_minutes IS NULL OR estimated_minutes >= 0),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (tenant_id, legacy_id)
);

CREATE TABLE work_orders (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    branch_id TEXT NOT NULL REFERENCES branches(id) ON DELETE RESTRICT,
    client_id TEXT NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
    vehicle_id TEXT NOT NULL REFERENCES vehicles(id) ON DELETE RESTRICT,
    legacy_id TEXT NOT NULL,
    identifier TEXT NOT NULL,
    status TEXT NOT NULL,
    opened_on TEXT,
    closed_at TEXT,
    mileage INTEGER,
    reported_problem TEXT,
    diagnosis TEXT,
    notes TEXT,
    services_subtotal_minor INTEGER NOT NULL DEFAULT 0,
    labor_subtotal_minor INTEGER NOT NULL DEFAULT 0,
    parts_subtotal_minor INTEGER NOT NULL DEFAULT 0,
    subtotal_minor INTEGER NOT NULL DEFAULT 0,
    discount_minor INTEGER NOT NULL DEFAULT 0,
    tax_basis_minor INTEGER NOT NULL DEFAULT 0,
    tax_percent REAL NOT NULL DEFAULT 0,
    tax_minor INTEGER NOT NULL DEFAULT 0,
    total_minor INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    legacy_snapshot_json TEXT NOT NULL,
    UNIQUE (tenant_id, legacy_id),
    UNIQUE (tenant_id, branch_id, identifier)
);
CREATE INDEX work_orders_tenant_status_idx ON work_orders(tenant_id, status, updated_at DESC);

CREATE TRIGGER work_orders_tenant_links_insert BEFORE INSERT ON work_orders BEGIN
    SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM branches WHERE id=NEW.branch_id AND tenant_id=NEW.tenant_id)
    THEN RAISE(ABORT, 'work order branch belongs to another tenant') END;
    SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM clients WHERE id=NEW.client_id AND tenant_id=NEW.tenant_id)
    THEN RAISE(ABORT, 'work order client belongs to another tenant') END;
    SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM vehicles WHERE id=NEW.vehicle_id AND tenant_id=NEW.tenant_id)
    THEN RAISE(ABORT, 'work order vehicle belongs to another tenant') END;
END;

CREATE TABLE work_order_lines (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    work_order_id TEXT NOT NULL REFERENCES work_orders(id) ON DELETE CASCADE,
    legacy_id TEXT NOT NULL,
    line_type TEXT NOT NULL CHECK (line_type IN ('service', 'labor', 'part')),
    service_id TEXT REFERENCES workshop_services(id) ON DELETE SET NULL,
    description TEXT NOT NULL,
    quantity REAL NOT NULL CHECK (quantity > 0),
    unit_price_minor INTEGER,
    subtotal_minor INTEGER NOT NULL CHECK (subtotal_minor >= 0),
    catalog_snapshot_json TEXT,
    position INTEGER NOT NULL,
    UNIQUE (work_order_id, legacy_id)
);

CREATE TABLE work_order_status_history (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    work_order_id TEXT NOT NULL REFERENCES work_orders(id) ON DELETE CASCADE,
    previous_status TEXT,
    new_status TEXT NOT NULL,
    changed_at TEXT NOT NULL,
    comment TEXT
);

CREATE TRIGGER work_order_lines_tenant_insert BEFORE INSERT ON work_order_lines BEGIN
    SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM work_orders WHERE id=NEW.work_order_id AND tenant_id=NEW.tenant_id)
    THEN RAISE(ABORT, 'work order line belongs to another tenant') END;
END;

CREATE TABLE legacy_import_runs (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    source_format TEXT NOT NULL,
    source_schema_version INTEGER NOT NULL,
    source_sha256 TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    counts_json TEXT NOT NULL,
    report_json TEXT NOT NULL,
    UNIQUE (tenant_id, source_sha256)
);

INSERT INTO schema_migrations(version, applied_at)
VALUES ('0002_workshop_core', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));

COMMIT;

