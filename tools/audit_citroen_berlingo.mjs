import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const nav = JSON.parse(fs.readFileSync(path.join(root, 'db-nav.json'), 'utf8'));
const db = JSON.parse(fs.readFileSync(path.join(root, 'db.json'), 'utf8'));
const sourceBrand = 'Peugeot';
const sourceModels = ['Berlingo', 'Citroen Berlingo'];

const slug = (value) => String(value)
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

function vehicleKey(model, year) {
  return `${slug(sourceBrand)}-${slug(model)}-${year}`;
}

function partSignature(part) {
  return JSON.stringify({
    category: part.cat,
    references: (part.refs || []).map((reference) => ({ r: reference.r, s: reference.s })),
    details: part.details,
  });
}

const yearSets = sourceModels.map((model) => new Set(nav[sourceBrand]?.[model] || []));
const years = [...new Set(yearSets.flatMap((set) => [...set]))].sort();
const records = years.map((year) => {
  const variants = sourceModels.map((model) => {
    const key = vehicleKey(model, year);
    const vehicle = db[key];
    const parts = Object.values(vehicle?.categories || {}).flat();
    return {
      sourceModel: model,
      key,
      presentInNavigation: yearSets[sourceModels.indexOf(model)].has(year),
      vehicleFound: Boolean(vehicle),
      info: vehicle?.info || null,
      partCount: parts.length,
      partSignatures: parts.map(partSignature).sort(),
    };
  });
  const [first, second] = variants;
  const conflicts = [];
  if (!variants.every((variant) => variant.presentInNavigation && variant.vehicleFound)) conflicts.push('missing-record');
  if (first.info !== second.info) conflicts.push('motor-or-version');
  if (JSON.stringify(first.partSignatures) !== JSON.stringify(second.partSignatures)) conflicts.push('part-content');
  return { year, variants, conflicts, migration: conflicts.length ? 'blocked' : 'needs-vin-review' };
});

const report = {
  generatedAt: new Date().toISOString(),
  subject: 'Citroën Berlingo incorrectly duplicated under Peugeot',
  source: { brand: sourceBrand, models: sourceModels },
  summary: {
    years: years.length,
    recordsInspected: records.reduce((total, record) => total + record.variants.length, 0),
    blockedYears: records.filter((record) => record.migration === 'blocked').map((record) => record.year),
    automaticMigrationAllowed: false,
  },
  requiredEvidence: [
    'VIN de cada unidad o lote de unidades.',
    'Consulta EPC Stellantis o concesionario autorizado que vincule VIN, motor y referencia OEM.',
    'Regla de reconciliación aprobada para artículos contradictorios antes de crear una ficha Citroën Berlingo canónica.',
  ],
  records,
};

if (process.argv.includes('--write')) {
  const output = path.join(root, 'research', 'catalog-expansion', 'berlingo-audit.json');
  fs.writeFileSync(output, JSON.stringify(report, null, 2));
  report.output = path.relative(root, output);
}

console.log(JSON.stringify(report, null, 2));
