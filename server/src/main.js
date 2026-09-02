import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { createApi } from './app.js';
import { SecurityStore } from './store.js';

const sessionSecret = process.env.SESSION_SECRET;
if (!sessionSecret || sessionSecret.length < 32) throw new Error('SESSION_SECRET debe tener al menos 32 caracteres');
const databasePath = process.env.DATABASE_PATH ?? 'repuestospro.sqlite';
if (databasePath !== ':memory:') mkdirSync(dirname(resolve(databasePath)), { recursive: true });
const store = new SecurityStore(databasePath);
if (process.env.RUN_MIGRATIONS === '1') {
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0001_foundations.sql'));
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0002_workshop_core.sql'));
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0002_security_hardening.sql'));
  store.migrate(resolve(import.meta.dirname, '../../database/migrations/sqlite/0003_local_workshop_state.sql'));
}
const port = Number(process.env.PORT ?? 3000);
const staticRoot = resolve(import.meta.dirname, '../..');
createApi({ store, sessionSecret, staticRoot }).listen(port, '127.0.0.1', () => console.log(`RepuestosPro listo en http://127.0.0.1:${port}`));
