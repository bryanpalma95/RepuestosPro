import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';

export const sha256 = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');

export function createBackup({ source, destination, schemaVersion = 'unknown', now = new Date() }) {
  if (!fs.existsSync(source)) throw new Error(`Database does not exist: ${source}`);
  fs.mkdirSync(destination, { recursive: true });
  const stamp = now.toISOString().replace(/[:.]/g, '-');
  const base = `repuestospro-${stamp}`;
  const databaseFile = path.join(destination, `${base}.sqlite`);
  const sourceDb = new DatabaseSync(source, { readOnly: true });
  try {
    sourceDb.exec(`VACUUM INTO '${databaseFile.replaceAll("'", "''")}'`);
  } finally { sourceDb.close(); }
  const check = new DatabaseSync(databaseFile, { readOnly: true });
  try { if (check.prepare('PRAGMA integrity_check').get().integrity_check !== 'ok') throw new Error('Backup integrity check failed'); }
  finally { check.close(); }
  const manifest = { format: 'repuestospro-local-backup', backupVersion: 1, createdAt: now.toISOString(), schemaVersion, database: path.basename(databaseFile), sha256: sha256(databaseFile) };
  const manifestFile = path.join(destination, `${base}.manifest.json`);
  fs.writeFileSync(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`, { flag: 'wx' });
  return { databaseFile, manifestFile, manifest };
}

export function verifyBackup(manifestFile) {
  const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
  if (manifest.format !== 'repuestospro-local-backup' || manifest.backupVersion !== 1) throw new Error('Unsupported backup manifest');
  if (path.basename(manifest.database) !== manifest.database) throw new Error('Unsafe database path in manifest');
  const databaseFile = path.join(path.dirname(manifestFile), manifest.database);
  if (sha256(databaseFile) !== manifest.sha256) throw new Error('Backup checksum mismatch');
  const db = new DatabaseSync(databaseFile, { readOnly: true });
  try { if (db.prepare('PRAGMA integrity_check').get().integrity_check !== 'ok') throw new Error('Backup integrity check failed'); }
  finally { db.close(); }
  return { manifest, databaseFile };
}

export function enforceRetention(directory, keep) {
  const manifests = fs.readdirSync(directory).filter((name) => name.endsWith('.manifest.json')).sort().reverse();
  for (const name of manifests.slice(keep)) {
    const manifestFile = path.join(directory, name);
    const { databaseFile } = verifyBackup(manifestFile);
    fs.rmSync(databaseFile); fs.rmSync(manifestFile);
  }
}

export function createScheduledBackup({ source, destination, schemaVersion = 'unknown', retention = 14, now = new Date() }) {
  fs.mkdirSync(destination, { recursive: true });
  const day = now.toISOString().slice(0, 10);
  const existing = fs.readdirSync(destination).find((name) => name.startsWith(`repuestospro-${day}T`) && name.endsWith('.manifest.json'));
  if (existing) return { created: false, manifestFile: path.join(destination, existing) };
  const result = createBackup({ source, destination, schemaVersion, now });
  enforceRetention(destination, retention);
  return { created: true, ...result };
}
