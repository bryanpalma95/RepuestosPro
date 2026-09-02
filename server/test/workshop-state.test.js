import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { afterEach, beforeEach, test } from 'node:test';
import { createApi } from '../src/app.js';
import { SecurityStore } from '../src/store.js';

const SECRET = 'test-only-session-secret-32-characters-long';
let store;
let server;
let baseUrl;

beforeEach(async () => {
  store = new SecurityStore();
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0001_foundations.sql'));
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0003_local_workshop_state.sql'));
  server = createApi({ store, sessionSecret: SECRET, localMode: true });
  await new Promise((resolveListen) => server.listen(0, '127.0.0.1', resolveListen));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

afterEach(async () => {
  await new Promise((resolveClose) => server.close(resolveClose));
  store.close();
});

test('el modo local guarda y recupera el estado del Taller en SQLite', async () => {
  const state = {
    version: 4,
    clients: [{ id: 'cli-test', nombre: 'Prueba' }],
    vehicles: [], services: [], workOrders: [], pendingParts: []
  };
  const saved = await fetch(`${baseUrl}/api/v1/local/workshop-state`, {
    method: 'PUT', headers: { 'content-type': 'application/json' }, body: JSON.stringify(state)
  });
  assert.equal(saved.status, 200);
  const loaded = await fetch(`${baseUrl}/api/v1/local/workshop-state`).then((response) => response.json());
  assert.deepEqual(loaded.state, state);
  assert.equal(store.db.prepare('SELECT COUNT(*) total FROM local_workshop_state').get().total, 1);
});

test('el modo local rechaza estados incompletos', async () => {
  const response = await fetch(`${baseUrl}/api/v1/local/workshop-state`, {
    method: 'PUT', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ clients: [] })
  });
  assert.equal(response.status, 400);
});
