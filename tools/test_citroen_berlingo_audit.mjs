import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import test from 'node:test';

test('la auditoría de Berlingo bloquea la fusión cuando las variantes difieren', () => {
  const report = JSON.parse(execFileSync(process.execPath, ['tools/audit_citroen_berlingo.mjs'], { encoding: 'utf8' }));
  assert.equal(report.subject, 'Citroën Berlingo incorrectly duplicated under Peugeot');
  assert.equal(report.summary.automaticMigrationAllowed, false);
  assert.ok(report.summary.recordsInspected > 0);
  assert.ok(report.summary.blockedYears.length > 0);
  assert.ok(report.records.every((record) => record.conflicts.includes('motor-or-version')));
});
