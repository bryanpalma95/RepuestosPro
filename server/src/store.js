import { randomUUID } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const isoNow = () => new Date().toISOString();

export class SecurityStore {
  constructor(filename = ':memory:') {
    this.db = new DatabaseSync(filename);
    this.db.exec('PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;');
  }

  migrate(migrationPath) {
    const version = basename(migrationPath, '.sql');
    const hasTable = this.db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_migrations'").get();
    if (hasTable && this.db.prepare('SELECT 1 FROM schema_migrations WHERE version=?').get(version)) return false;
    this.db.exec(readFileSync(migrationPath, 'utf8'));
    return true;
  }
  close() { this.db.close(); }

  findLoginIdentity(email) {
    return this.db.prepare(`SELECT id, email, display_name, password_hash, status FROM users WHERE email = ? COLLATE NOCASE`).get(email);
  }

  createSession({ userId, digest, ttlSeconds, ipAddress, userAgent }) {
    const now = isoNow();
    const expires = new Date(Date.now() + ttlSeconds * 1000).toISOString();
    const id = randomUUID();
    this.db.prepare(`INSERT INTO sessions(id,user_id,token_digest,created_at,expires_at,ip_address,user_agent) VALUES (?,?,?,?,?,?,?)`)
      .run(id, userId, digest, now, expires, ipAddress ?? null, String(userAgent ?? '').slice(0, 512) || null);
    return { id, expires };
  }

  sessionIdentity(digest) {
    const user = this.db.prepare(`
      SELECT u.id, u.email, u.display_name FROM sessions s
      JOIN users u ON u.id=s.user_id
      WHERE s.token_digest=? AND s.revoked_at IS NULL AND s.expires_at>? AND u.status='active'
    `).get(digest, isoNow());
    if (!user) return null;
    const memberships = this.db.prepare(`
      SELECT m.id, m.tenant_id, t.name tenant_name, m.default_branch_id
      FROM memberships m JOIN tenants t ON t.id=m.tenant_id
      WHERE m.user_id=? AND m.status='active' AND t.status='active' ORDER BY m.created_at
    `).all(user.id).map((membership) => ({
      ...membership,
      permissions: this.db.prepare(`
        SELECT DISTINCT rp.permission_code code FROM membership_roles mr
        JOIN roles r ON r.id=mr.role_id AND r.tenant_id=?
        JOIN role_permissions rp ON rp.role_id=r.id
        WHERE mr.membership_id=? ORDER BY rp.permission_code
      `).all(membership.tenant_id, membership.id).map((row) => row.code),
    }));
    return { user, memberships };
  }

  revokeSession(digest) {
    return this.db.prepare(`UPDATE sessions SET revoked_at=? WHERE token_digest=? AND revoked_at IS NULL`).run(isoNow(), digest).changes > 0;
  }

  getLocalWorkshopState() {
    const row = this.db.prepare(`SELECT schema_version, state_json, updated_at FROM local_workshop_state WHERE id=1`).get();
    if (!row) return null;
    return { schemaVersion: row.schema_version, state: JSON.parse(row.state_json), updatedAt: row.updated_at };
  }

  saveLocalWorkshopState(state) {
    const updatedAt = new Date().toISOString();
    const schemaVersion = Number(state?.version) || 1;
    this.db.prepare(`
      INSERT INTO local_workshop_state(id,schema_version,state_json,updated_at) VALUES (1,?,?,?)
      ON CONFLICT(id) DO UPDATE SET schema_version=excluded.schema_version,state_json=excluded.state_json,updated_at=excluded.updated_at
    `).run(schemaVersion, JSON.stringify(state), updatedAt);
    return { schemaVersion, updatedAt };
  }

  requestContext(identity, tenantId, permission) {
    const membership = identity?.memberships.find((item) => item.tenant_id === tenantId);
    if (!membership || !membership.permissions.includes(permission)) return null;
    return Object.freeze({ userId: identity.user.id, tenantId, membershipId: membership.id, branchId: membership.default_branch_id, permissions: membership.permissions });
  }

  listAuditEvents(context) {
    return this.db.prepare(`SELECT * FROM audit_events WHERE tenant_id=? ORDER BY occurred_at DESC`).all(context.tenantId);
  }
}
