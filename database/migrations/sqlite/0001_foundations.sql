PRAGMA foreign_keys = ON;

BEGIN IMMEDIATE;

CREATE TABLE schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE tenants (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    rut TEXT,
    legal_name TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'archived')),
    timezone TEXT NOT NULL DEFAULT 'America/Santiago',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    archived_at TEXT
);

CREATE UNIQUE INDEX tenants_rut_unique
    ON tenants(rut) WHERE rut IS NOT NULL AND rut <> '';

CREATE TABLE branches (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    address TEXT,
    comuna TEXT,
    region TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (tenant_id, code)
);

CREATE INDEX branches_tenant_status_idx ON branches(tenant_id, status);

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL COLLATE NOCASE,
    display_name TEXT NOT NULL,
    password_hash TEXT,
    status TEXT NOT NULL DEFAULT 'invited' CHECK (status IN ('invited', 'active', 'locked', 'disabled')),
    email_verified_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE UNIQUE INDEX users_email_unique ON users(email COLLATE NOCASE);

CREATE TABLE memberships (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    default_branch_id TEXT REFERENCES branches(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('invited', 'active', 'suspended', 'revoked')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (tenant_id, user_id)
);

CREATE INDEX memberships_user_status_idx ON memberships(user_id, status);
CREATE INDEX memberships_tenant_status_idx ON memberships(tenant_id, status);

CREATE TRIGGER memberships_branch_tenant_insert
BEFORE INSERT ON memberships
WHEN NEW.default_branch_id IS NOT NULL
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM branches
        WHERE id = NEW.default_branch_id AND tenant_id = NEW.tenant_id
    ) THEN RAISE(ABORT, 'default branch belongs to another tenant') END;
END;

CREATE TRIGGER memberships_branch_tenant_update
BEFORE UPDATE OF tenant_id, default_branch_id ON memberships
WHEN NEW.default_branch_id IS NOT NULL
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM branches
        WHERE id = NEW.default_branch_id AND tenant_id = NEW.tenant_id
    ) THEN RAISE(ABORT, 'default branch belongs to another tenant') END;
END;

CREATE TABLE roles (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    is_system INTEGER NOT NULL DEFAULT 0 CHECK (is_system IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (tenant_id, code)
);

CREATE TABLE permissions (
    code TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE role_permissions (
    role_id TEXT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_code TEXT NOT NULL REFERENCES permissions(code) ON DELETE CASCADE,
    created_at TEXT NOT NULL,
    PRIMARY KEY (role_id, permission_code)
);

CREATE TABLE membership_roles (
    membership_id TEXT NOT NULL REFERENCES memberships(id) ON DELETE CASCADE,
    role_id TEXT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL,
    PRIMARY KEY (membership_id, role_id)
);

CREATE TRIGGER membership_roles_same_tenant_insert
BEFORE INSERT ON membership_roles
BEGIN
    SELECT CASE WHEN (
        SELECT tenant_id FROM memberships WHERE id = NEW.membership_id
    ) <> (
        SELECT tenant_id FROM roles WHERE id = NEW.role_id
    ) THEN RAISE(ABORT, 'membership and role belong to different tenants') END;
END;

CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_digest TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    last_seen_at TEXT,
    revoked_at TEXT,
    ip_address TEXT,
    user_agent TEXT
);

CREATE INDEX sessions_user_active_idx ON sessions(user_id, expires_at, revoked_at);

CREATE TABLE password_reset_tokens (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_digest TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    used_at TEXT
);

CREATE INDEX password_reset_user_idx ON password_reset_tokens(user_id, expires_at);

CREATE TABLE tenant_counters (
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id TEXT NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    counter_type TEXT NOT NULL,
    counter_year INTEGER NOT NULL,
    current_value INTEGER NOT NULL DEFAULT 0 CHECK (current_value >= 0),
    updated_at TEXT NOT NULL,
    PRIMARY KEY (tenant_id, branch_id, counter_type, counter_year)
);

CREATE TRIGGER tenant_counters_branch_tenant_insert
BEFORE INSERT ON tenant_counters
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM branches
        WHERE id = NEW.branch_id AND tenant_id = NEW.tenant_id
    ) THEN RAISE(ABORT, 'counter branch belongs to another tenant') END;
END;

CREATE TABLE audit_events (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    branch_id TEXT REFERENCES branches(id) ON DELETE SET NULL,
    actor_user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    request_id TEXT,
    source TEXT NOT NULL CHECK (source IN ('cloud', 'local', 'migration', 'system')),
    previous_value_json TEXT,
    new_value_json TEXT,
    ip_address TEXT,
    user_agent TEXT
);

CREATE INDEX audit_events_entity_idx
    ON audit_events(tenant_id, entity_type, entity_id, occurred_at DESC);
CREATE INDEX audit_events_actor_idx
    ON audit_events(tenant_id, actor_user_id, occurred_at DESC);

CREATE TRIGGER audit_events_branch_tenant_insert
BEFORE INSERT ON audit_events
WHEN NEW.branch_id IS NOT NULL
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM branches
        WHERE id = NEW.branch_id AND tenant_id = NEW.tenant_id
    ) THEN RAISE(ABORT, 'audit branch belongs to another tenant') END;
END;

INSERT INTO schema_migrations(version, applied_at)
VALUES ('0001_foundations', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));

COMMIT;
