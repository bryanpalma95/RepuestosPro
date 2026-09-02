import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';

function repository() {
  const values = new Map();
  const window = {
    crypto: webcrypto,
    TextEncoder,
    localStorage: {
      getItem: (key) => values.has(key) ? values.get(key) : null,
      setItem: (key, value) => values.set(key, value),
    },
  };
  vm.runInNewContext(fs.readFileSync(new URL('../taller-repository.js', import.meta.url), 'utf8'), { window });
  return new window.TallerData.LocalWorkshopRepository();
}

test('artículos nuevos se deduplican y exportan sin datos personales', async () => {
  const repo = repository();
  const vehicle = { marca: 'Toyota', modelo: 'Yaris', anio: 2020, motor: '2NR-FE', patente: 'SECRET1' };
  const first = await repo.queuePendingPart({ name: 'Filtro de aceite', brand: 'Denso', reference: 'abc-123', vehicle });
  const second = await repo.queuePendingPart({ name: 'Filtro de aceite', brand: 'Denso', reference: 'ABC-123', vehicle });
  assert.equal(first.id, second.id);
  assert.equal(second.occurrences, 2);
  const batch = await repo.exportPendingParts();
  assert.equal(batch.items.length, 1);
  assert.equal(batch.items[0].vehicle.patente, undefined);
  assert.equal(JSON.stringify(batch).includes('SECRET1'), false);
  const localResults = await repo.searchLocalParts('A', vehicle, 'compatible');
  assert.equal(localResults.length, 1);
  assert.equal(localResults[0].name, 'Filtro de aceite');
  assert.equal(localResults[0].category, 'Local · pendiente');
});

test('una actualización válida enriquece el pendiente', async () => {
  const repo = repository();
  const pending = await repo.queuePendingPart({ name: 'Filtro', vehicle: { marca: 'Kia', modelo: 'Rio', anio: 2018 } });
  const result = await repo.importEnrichmentPackage({
    format: 'repuestospro-enrichment-update', version: 1,
    items: [{ pendingId: pending.id, name: 'Filtro de aceite', references: [{ code: '26300-35505', status: 'verified' }], compatibilityConfirmed: true }],
  });
  assert.equal(result.updated, 1);
  const [item] = await repo.listPendingParts();
  assert.equal(item.status, 'enriched');
  assert.equal(item.enrichment.references[0].code, '26300-35505');
});
