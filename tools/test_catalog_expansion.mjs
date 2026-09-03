import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import test from 'node:test';

const project = path.resolve('.');

function fixture() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'repuestospro-expansion-'));
  fs.mkdirSync(path.join(dir, 'research', 'catalog-expansion'), { recursive: true });
  for (const file of ['block-6-geely.json', 'block-7-mahindra.json', 'block-9-foton.json']) {
    fs.copyFileSync(path.join(project, 'research', 'catalog-expansion', file), path.join(dir, 'research', 'catalog-expansion', file));
  }
  fs.copyFileSync(path.join(project, 'tools', 'apply_brand_expansion.mjs'), path.join(dir, 'apply_brand_expansion.mjs'));
  fs.writeFileSync(path.join(dir, 'db-nav.json'), JSON.stringify({ Geely: { Coolray: ['2023'] } }));
  fs.writeFileSync(path.join(dir, 'db.json'), JSON.stringify({ 'geely-coolray-2023': { name: 'Geely Coolray — 2023', categories: {} } }));
  return dir;
}

test('la migración de marcas agrega solo candidatos trazables y conserva el modo dry-run', (t) => {
  const dir = fixture();
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const before = fs.readFileSync(path.join(dir, 'db.json'), 'utf8');
  const dryRun = JSON.parse(execFileSync(process.execPath, ['apply_brand_expansion.mjs'], { cwd: dir, encoding: 'utf8' }));
  assert.equal(dryRun.vehicles, 5);
  assert.equal(dryRun.candidateReferences, 10);
  assert.equal(fs.readFileSync(path.join(dir, 'db.json'), 'utf8'), before);

  const applied = JSON.parse(execFileSync(process.execPath, ['apply_brand_expansion.mjs', '--apply'], { cwd: dir, encoding: 'utf8' }));
  const nav = JSON.parse(fs.readFileSync(path.join(dir, 'db-nav.json'), 'utf8'));
  const db = JSON.parse(fs.readFileSync(path.join(dir, 'db.json'), 'utf8'));
  assert.deepEqual(nav.Mahindra['Pik Up'], ['2022']);
  assert.ok(db['geely-okavango-2023']);
  assert.ok(db['foton-tunland-g7-2024']);
  assert.equal(db['foton-tunland-g7-2024'].categories.Motor.length, 3);
  assert.equal(db['foton-tunland-g7-2024'].categories.Distribucion.length, 1);
  assert.ok(fs.existsSync(path.join(dir, applied.backupDir, 'migration-summary.json')));
});
