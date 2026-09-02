PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

CREATE TRIGGER audit_events_immutable_update
BEFORE UPDATE ON audit_events
BEGIN
  SELECT RAISE(ABORT, 'audit events are immutable');
END;

CREATE TRIGGER audit_events_immutable_delete
BEFORE DELETE ON audit_events
BEGIN
  SELECT RAISE(ABORT, 'audit events are immutable');
END;

INSERT INTO schema_migrations(version, applied_at)
VALUES ('0002_security_hardening', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
COMMIT;

