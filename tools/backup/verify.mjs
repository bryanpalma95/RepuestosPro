import { verifyBackup } from './lib.mjs';

try {
  const manifest = process.argv[2];
  if (!manifest) throw new Error('Usage: node tools/backup/verify.mjs <manifest.json>');
  const result = verifyBackup(manifest);
  console.log(JSON.stringify({ status: 'ok', database: result.databaseFile, schemaVersion: result.manifest.schemaVersion }));
} catch (error) { console.error(JSON.stringify({ status: 'error', message: error.message })); process.exitCode = 1; }

