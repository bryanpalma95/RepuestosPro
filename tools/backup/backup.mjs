import { createBackup, enforceRetention } from './lib.mjs';

try {
  const source = process.env.DATABASE_PATH || './var/data/repuestospro.sqlite';
  const destination = process.env.BACKUP_DIR || './var/backups';
  const retention = Number(process.env.BACKUP_RETENTION || 14);
  const result = createBackup({ source, destination, schemaVersion: process.env.RP_SCHEMA_VERSION || '0002_security_hardening' });
  enforceRetention(destination, retention);
  console.log(JSON.stringify({ status: 'ok', manifest: result.manifestFile, checksum: result.manifest.sha256 }));
} catch (error) { console.error(JSON.stringify({ status: 'error', message: error.message })); process.exitCode = 1; }
