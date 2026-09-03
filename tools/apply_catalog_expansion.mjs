import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const apply = process.argv.includes('--apply');
const navPath = path.join(root, 'db-nav.json');
const dbPath = path.join(root, 'db.json');
const refsPath = path.join(root, 'research/catalog-expansion/block-5-referencias.json');
const nav = JSON.parse(fs.readFileSync(navPath, 'utf8'));
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
const referenceResearch = JSON.parse(fs.readFileSync(refsPath, 'utf8'));
const changes = [];

const slug = (value) => String(value)
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

function moveModel(fromBrand, fromModel, toBrand, toModel) {
  const years = nav[fromBrand]?.[fromModel];
  if (!years) throw new Error(`No existe ${fromBrand}/${fromModel} en db-nav.json`);
  nav[toBrand] ||= {};
  if (nav[toBrand][toModel]) throw new Error(`Destino ya existente: ${toBrand}/${toModel}`);

  nav[toBrand][toModel] = years;
  delete nav[fromBrand][fromModel];
  if (!Object.keys(nav[fromBrand]).length) delete nav[fromBrand];

  for (const year of years) {
    const oldKey = `${slug(fromBrand)}-${slug(fromModel)}-${year}`;
    const newKey = `${slug(toBrand)}-${slug(toModel)}-${year}`;
    if (!db[oldKey]) throw new Error(`Falta la ficha ${oldKey}`);
    if (db[newKey]) throw new Error(`La ficha destino ${newKey} ya existe`);
    db[newKey] = db[oldKey];
    db[newKey].name = `${toBrand} ${toModel} — ${year}`;
    delete db[oldKey];
  }
  changes.push({ type: 'move-model', from: `${fromBrand}/${fromModel}`, to: `${toBrand}/${toModel}`, years: years.length });
}

function addCandidateReference(candidate) {
  if (candidate.status !== 'candidate') throw new Error(`Estado de referencia no permitido: ${candidate.status}`);
  const year = String(candidate.años[0]);
  const key = `${slug(candidate.marca)}-${slug(candidate.modelo)}-${year}`;
  const vehicle = db[key];
  if (!vehicle) throw new Error(`No existe la ficha destino ${key}`);
  const parts = Object.values(vehicle.categories || {}).flat();
  const categoryAliases = {
    'filtro-de-aceite': ['filtro-aceite'],
    'filtro-de-aire': ['filtro-aire'],
    'bujia': ['bujia', 'bujias'],
    'pastillas-delanteras': ['pastillas-del', 'pastillas-freno-delanteras'],
    'pastillas-de-freno-delanteras': ['pastillas-del', 'pastillas-freno-delanteras']
  };
  const wanted = slug(candidate.categoria);
  const accepted = new Set([wanted, ...(categoryAliases[wanted] || [])]);
  const part = parts.find((item) => accepted.has(slug(item.cat)) || accepted.has(slug(item.name)));
  if (!part) throw new Error(`No se encontró ${candidate.categoria} en ${key}`);
  part.refs ||= [];
  const ref = String(candidate.referenciaOEM).trim();
  if (part.refs.some((item) => String(item.r).trim().toUpperCase() === ref.toUpperCase())) return;
  part.refs.push({ r: ref, s: 'candidate' });
  changes.push({ type: 'add-reference', vehicle: key, category: candidate.categoria, reference: ref, status: 'candidate' });
}

[
  ['Hyundai', 'Carnival', 'Kia', 'Carnival'],
  ['Hyundai', 'Cerato', 'Kia', 'Cerato'],
  ['Hyundai', 'Morning', 'Kia', 'Morning'],
  ['Hyundai', 'Rio', 'Kia', 'Rio'],
  ['Hyundai', 'Seltos', 'Kia', 'Seltos'],
  ['Hyundai', 'Soluto', 'Kia', 'Soluto'],
  ['Hyundai', 'Sorento', 'Kia', 'Sorento'],
  ['Hyundai', 'Sportage', 'Kia', 'Sportage'],
  ['Chery', 'Jetour X70', 'Jetour', 'X70'],
  ['Jeep', 'Durango', 'Dodge', 'Durango'],
  ['Jeep', 'Journey', 'Dodge', 'Journey'],
  ['Haval', 'Poer', 'GWM', 'Poer']
].forEach((operation) => moveModel(...operation));

referenceResearch.candidates.forEach(addCandidateReference);

const summary = {
  mode: apply ? 'apply' : 'dry-run',
  changes: changes.length,
  movedModels: changes.filter((item) => item.type === 'move-model').length,
  candidateReferences: changes.filter((item) => item.type === 'add-reference').length,
  details: changes
};

if (apply) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupDir = path.join(root, 'backups', `catalog-expansion-${stamp}`);
  fs.mkdirSync(backupDir, { recursive: true });
  fs.copyFileSync(navPath, path.join(backupDir, 'db-nav.json'));
  fs.copyFileSync(dbPath, path.join(backupDir, 'db.json'));
  fs.writeFileSync(navPath, JSON.stringify(nav), 'utf8');
  fs.writeFileSync(dbPath, JSON.stringify(db), 'utf8');
  fs.writeFileSync(path.join(backupDir, 'migration-summary.json'), JSON.stringify(summary, null, 2), 'utf8');
  summary.backupDir = path.relative(root, backupDir);
}

console.log(JSON.stringify(summary, null, 2));
