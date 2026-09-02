PRAGMA foreign_keys = ON;

BEGIN IMMEDIATE;

CREATE TABLE local_workshop_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    schema_version INTEGER NOT NULL,
    state_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

INSERT INTO schema_migrations(version, applied_at)
VALUES ('0003_local_workshop_state', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));

COMMIT;
