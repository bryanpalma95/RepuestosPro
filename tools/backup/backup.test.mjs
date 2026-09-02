import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { DatabaseSync } from 'node:sqlite';
import { createBackup, createScheduledBackup, verifyBackup } from './lib.mjs';

test('backup is consistent, checksummed and restorable', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'rp-backup-')); t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const source = path.join(root, 'source.sqlite'); const db = new DatabaseSync(source); db.exec('CREATE TABLE sample(value TEXT); INSERT INTO sample VALUES (\'preserved\')'); db.close();
  const result = createBackup({ source, destination: path.join(root, 'backups'), schemaVersion: 'test' });
  const verified = verifyBackup(result.manifestFile); assert.equal(verified.manifest.schemaVersion, 'test');
  const restored = new DatabaseSync(verified.databaseFile, { readOnly: true }); assert.equal(restored.prepare('SELECT value FROM sample').get().value, 'preserved'); restored.close();
  fs.appendFileSync(verified.databaseFile, 'tamper'); assert.throws(() => verifyBackup(result.manifestFile), /checksum/);
});

test('scheduled backup creates at most one verified copy per day', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'rp-scheduled-backup-')); t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const source = path.join(root, 'source.sqlite'); const db = new DatabaseSync(source); db.exec('CREATE TABLE sample(value TEXT); INSERT INTO sample VALUES (\'daily\')'); db.close();
  const destination = path.join(root, 'backups');
  const first = createScheduledBackup({ source, destination, now: new Date('2026-09-02T08:00:00.000Z') });
  const second = createScheduledBackup({ source, destination, now: new Date('2026-09-02T20:00:00.000Z') });
  assert.equal(first.created, true);
  assert.equal(second.created, false);
  assert.equal(fs.readdirSync(destination).filter((name) => name.endsWith('.manifest.json')).length, 1);
  assert.doesNotThrow(() => verifyBackup(first.manifestFile));
});
