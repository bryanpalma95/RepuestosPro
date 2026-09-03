import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const apply = process.argv.includes('--apply');
const navPath = path.join(root, 'db-nav.json');
const dbPath = path.join(root, 'db.json');
const researchFiles = [
  'block-6-geely.json',
  'block-7-mahindra.json',
  'block-9-foton.json',
].map((file) => path.join(root, 'research', 'catalog-expansion', file));
const nav = JSON.parse(fs.readFileSync(navPath, 'utf8'));
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
const changes = [];

const slug = (value) => String(value)
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const sectionFor = (category) => {
  const normalized = slug(category);
  if (normalized.includes('correa')) return 'Distribucion';
  return 'Motor';
};

function buildVehicle(candidate, sources) {
  const sourceById = new Map(sources.map((source) => [source.id, source]));
  const categories = {};
  for (const part of candidate.parts) {
    const section = sectionFor(part.categoria);
    categories[section] ||= [];
    const source = sourceById.get(part.sourceId);
    if (!source) throw new Error(`No existe la fuente ${part.sourceId} para ${candidate.marca}/${candidate.modelo}`);
    categories[section].push({
      cat: part.categoria,
      name: `${part.categoria} OEM`,
      details: part.aplicabilidad,
      brands: 'OEM',
      refs: [{ r: String(part.referenciaOEM), s: 'candidate' }],
      links: [{ t: source.publisher, u: source.url }],
    });
  }
  return {
    name: `${candidate.marca} ${candidate.modelo} — ${candidate.años[0]}`,
    info: candidate.motorVersion,
    crossNote: 'Referencias candidatas: confirmar VIN, motor y versión antes de vender o instalar.',
    categories,
  };
}

function addCandidate(candidate, sources) {
  if (!Array.isArray(candidate.años) || candidate.años.length !== 1 || !Array.isArray(candidate.parts) || !candidate.parts.length) {
    throw new Error(`Candidato no integrable: ${candidate.marca}/${candidate.modelo}`);
  }
  if (candidate.parts.some((part) => part.status !== 'candidate')) {
    throw new Error(`Hay una referencia sin estado candidate en ${candidate.marca}/${candidate.modelo}`);
  }
  const year = String(candidate.años[0]);
  const key = `${slug(candidate.marca)}-${slug(candidate.modelo)}-${year}`;
  if (db[key] || nav[candidate.marca]?.[candidate.modelo]) {
    throw new Error(`El destino ya existe: ${candidate.marca}/${candidate.modelo}/${year}`);
  }
  nav[candidate.marca] ||= {};
  nav[candidate.marca][candidate.modelo] = [year];
  db[key] = buildVehicle(candidate, sources);
  changes.push({ type: 'add-vehicle', vehicle: key, candidateReferences: candidate.parts.length });
}

for (const researchFile of researchFiles) {
  const research = JSON.parse(fs.readFileSync(researchFile, 'utf8'));
  research.candidates.forEach((candidate) => addCandidate(candidate, research.sources));
}

const summary = {
  mode: apply ? 'apply' : 'dry-run',
  changes: changes.length,
  vehicles: changes.length,
  candidateReferences: changes.reduce((total, change) => total + change.candidateReferences, 0),
  details: changes,
};

if (apply) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupDir = path.join(root, 'backups', `brand-expansion-${stamp}`);
  fs.mkdirSync(backupDir, { recursive: true });
  fs.copyFileSync(navPath, path.join(backupDir, 'db-nav.json'));
  fs.copyFileSync(dbPath, path.join(backupDir, 'db.json'));
  fs.writeFileSync(navPath, JSON.stringify(nav), 'utf8');
  fs.writeFileSync(dbPath, JSON.stringify(db), 'utf8');
  fs.writeFileSync(path.join(backupDir, 'migration-summary.json'), JSON.stringify(summary, null, 2), 'utf8');
  summary.backupDir = path.relative(root, backupDir);
}

console.log(JSON.stringify(summary, null, 2));
