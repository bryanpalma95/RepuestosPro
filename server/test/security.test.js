import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { resolve } from 'node:path';
import { afterEach, beforeEach, test } from 'node:test';
import { createApi } from '../src/app.js';
import { RateLimiter } from '../src/rate-limit.js';
import { digestToken, hashPassword, verifyPassword } from '../src/security.js';
import { SecurityStore } from '../src/store.js';

const SECRET = 'test-only-session-secret-32-characters-long';
const NOW = '2026-01-01T00:00:00.000Z';
let store;
let server;
let baseUrl;

function seed() {
  const db = store.db;
  const ids = Object.fromEntries(['tenantA', 'tenantB', 'user', 'membershipA', 'membershipB', 'roleA', 'roleB', 'auditA', 'auditB'].map((key) => [key, randomUUID()]));
  db.prepare('INSERT INTO tenants(id,name,created_at,updated_at) VALUES (?,?,?,?)').run(ids.tenantA, 'Taller A', NOW, NOW);
  db.prepare('INSERT INTO tenants(id,name,created_at,updated_at) VALUES (?,?,?,?)').run(ids.tenantB, 'Taller B', NOW, NOW);
  db.prepare(`INSERT INTO users(id,email,display_name,password_hash,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?)`)
    .run(ids.user, 'owner@example.com', 'Owner', hashPassword('correct horse battery'), 'active', NOW, NOW);
  const membership = db.prepare('INSERT INTO memberships(id,tenant_id,user_id,status,created_at,updated_at) VALUES (?,?,?,?,?,?)');
  membership.run(ids.membershipA, ids.tenantA, ids.user, 'active', NOW, NOW);
  membership.run(ids.membershipB, ids.tenantB, ids.user, 'active', NOW, NOW);
  const role = db.prepare('INSERT INTO roles(id,tenant_id,code,name,created_at,updated_at) VALUES (?,?,?,?,?,?)');
  role.run(ids.roleA, ids.tenantA, 'viewer', 'Viewer A', NOW, NOW);
  role.run(ids.roleB, ids.tenantB, 'viewer', 'Viewer B', NOW, NOW);
  db.prepare('INSERT INTO permissions(code,description,created_at) VALUES (?,?,?)').run('audit.read', 'Leer auditoría', NOW);
  db.prepare('INSERT INTO role_permissions(role_id,permission_code,created_at) VALUES (?,?,?)').run(ids.roleA, 'audit.read', NOW);
  db.prepare('INSERT INTO membership_roles(membership_id,role_id,created_at) VALUES (?,?,?)').run(ids.membershipA, ids.roleA, NOW);
  const audit = db.prepare(`INSERT INTO audit_events(id,tenant_id,actor_user_id,action,entity_type,entity_id,occurred_at,source) VALUES (?,?,?,?,?,?,?,?)`);
  audit.run(ids.auditA, ids.tenantA, ids.user, 'test.created', 'test', randomUUID(), NOW, 'local');
  audit.run(ids.auditB, ids.tenantB, ids.user, 'test.created', 'test', randomUUID(), NOW, 'local');
  return ids;
}

async function request(path, options = {}) {
  return fetch(`${baseUrl}${path}`, { redirect: 'manual', ...options });
}

async function login(password = 'correct horse battery', extra = {}) {
  return request('/api/v1/auth/login', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'owner@example.com', password, ...extra }),
  });
}

beforeEach(async () => {
  store = new SecurityStore();
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0001_foundations.sql'));
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0002_security_hardening.sql'));
  seed();
  server = createApi({ store, sessionSecret: SECRET, limiter: new RateLimiter({ limit: 2 }) });
  await new Promise((resolveListen) => server.listen(0, '127.0.0.1', resolveListen));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

afterEach(async () => {
  await new Promise((resolveClose) => server.close(resolveClose));
  store.close();
});

test('Argon2id versionado valida la clave sin guardar texto reversible', () => {
  const hash = hashPassword('a sufficiently long password');
  assert.match(hash, /^\$argon2id\$v=19\$m=19456,t=2,p=1\$/);
  assert.equal(verifyPassword('a sufficiently long password', hash), true);
  assert.equal(verifyPassword('wrong password', hash), false);
});

test('login, me y logout usan cookie opaca revocable', async () => {
  const loggedIn = await login();
  assert.equal(loggedIn.status, 200);
  const cookie = loggedIn.headers.get('set-cookie');
  assert.match(cookie, /HttpOnly; Secure; SameSite=Strict/);
  assert.doesNotMatch(cookie, /owner@example\.com/);
  const token = /rp_session=([^;]+)/.exec(cookie)[1];
  assert.equal(store.db.prepare('SELECT token_digest FROM sessions').get().token_digest, digestToken(token, SECRET));
  assert.equal(await (await request('/api/v1/me', { headers: { cookie } })).json().then((body) => body.memberships.length), 2);
  assert.equal((await request('/api/v1/auth/logout', { method: 'POST', headers: { cookie } })).status, 204);
  assert.equal((await request('/api/v1/me', { headers: { cookie } })).status, 401);
  assert.equal((await request('/api/v1/me', { headers: { cookie: 'rp_session=%E0%A4%A' } })).status, 401);
});

test('DTO estricto y respuesta uniforme evitan entradas extra y enumeración básica', async () => {
  assert.equal((await login(undefined, { tenantId: randomUUID() })).status, 400);
  const wrong = await login('wrong password long');
  const missing = await request('/api/v1/auth/login', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email: 'missing@example.com', password: 'wrong password long' }) });
  assert.equal(wrong.status, 401);
  assert.equal(missing.status, 401);
  assert.deepEqual((await wrong.json()).message, (await missing.json()).message);
});

test('rate limit bloquea intentos reiterados', async () => {
  assert.equal((await login('wrong password long')).status, 401);
  assert.equal((await login('wrong password long')).status, 401);
  const limited = await login('wrong password long');
  assert.equal(limited.status, 429);
  assert.ok(Number(limited.headers.get('retry-after')) >= 1);
});

test('permiso y tenant se derivan de la membresía y las consultas quedan aisladas', () => {
  const ids = store.db.prepare('SELECT id FROM users').get();
  store.createSession({ userId: ids.id, digest: 'fixture-digest', ttlSeconds: 60 });
  const authenticated = store.sessionIdentity('fixture-digest');
  const tenantA = store.db.prepare("SELECT id FROM tenants WHERE name='Taller A'").get().id;
  const tenantB = store.db.prepare("SELECT id FROM tenants WHERE name='Taller B'").get().id;
  const allowed = store.requestContext(authenticated, tenantA, 'audit.read');
  assert.ok(allowed);
  assert.equal(store.listAuditEvents(allowed).length, 1);
  assert.equal(store.requestContext(authenticated, tenantB, 'audit.read'), null);
  assert.equal(store.requestContext(authenticated, tenantA, 'users.write'), null);
});

test('auditoría no admite UPDATE ni DELETE', () => {
  assert.throws(() => store.db.exec("UPDATE audit_events SET action='tampered'"), /immutable/);
  assert.throws(() => store.db.exec('DELETE FROM audit_events'), /immutable/);
});

