import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('research/catalog-expansion');
const files = fs.existsSync(root)
  ? fs.readdirSync(root).filter((name) => /^block-[1-5].*\.json$/i.test(name)).sort()
  : [];

if (!files.length) {
  console.error('No hay bloques para validar en research/catalog-expansion.');
  process.exitCode = 1;
} else {
  const seen = new Map();
  let errors = 0;
  let warnings = 0;

  for (const file of files) {
    const fullPath = path.join(root, file);
    let block;
    try {
      block = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
    } catch (error) {
      console.error(`${file}: JSON inválido (${error.message})`);
      errors += 1;
      continue;
    }

    if (!Array.isArray(block.sources) || !Array.isArray(block.candidates) || !Array.isArray(block.unresolved)) {
      console.error(`${file}: debe contener sources, candidates y unresolved como listas.`);
      errors += 1;
      continue;
    }

    const sourceIds = new Set(block.sources.map((source) => source?.id).filter(Boolean));
    block.candidates.forEach((candidate, index) => {
      const label = `${file}#${index + 1}`;
      const confidence = candidate?.confidence;
      const textualConfidence = String(confidence || '').toLowerCase();
      const confidenceIsValid = (typeof confidence === 'number' && confidence >= 0 && confidence <= 1)
        || ['high', 'medium', 'low', 'alta', 'media', 'baja'].includes(textualConfidence);
      if (!confidenceIsValid) {
        console.error(`${label}: confidence inválido o ausente.`);
        errors += 1;
      }
      const evidence = candidate?.evidencia || candidate?.evidence;
      if (!evidence || (Array.isArray(evidence) && evidence.length === 0)) {
        console.error(`${label}: falta evidencia.`);
        errors += 1;
      }
      const evidenceItems = Array.isArray(evidence) ? evidence : [evidence];
      const citedIds = evidenceItems
        .map((item) => typeof item === 'string' ? item : item?.sourceId || item?.id)
        .filter(Boolean);
      const hasDeclaredSource = citedIds.some((id) => sourceIds.has(id));
      if (!hasDeclaredSource) {
        if (candidate?.status === 'unverified-local-audit') {
          console.warn(`${label}: auditoría local retenida sin fuente externa; no integrar automáticamente.`);
          warnings += 1;
        } else {
          console.error(`${label}: ninguna evidencia apunta a un sourceId declarado.`);
          errors += 1;
        }
      }

      const key = [candidate?.marca, candidate?.modelo, candidate?.años || candidate?.anios, candidate?.referenciaOEM, candidate?.issueType]
        .map((value) => JSON.stringify(value ?? '').toLowerCase())
        .join('|');
      if (seen.has(key)) {
        console.warn(`${label}: revisar posible solapamiento con ${seen.get(key)}.`);
        warnings += 1;
      } else {
        seen.set(key, label);
      }
    });
  }

  if (errors) {
    console.error(`Validación terminada con ${errors} problema(s).`);
    process.exitCode = 1;
  } else {
    console.log(`${files.length} bloque(s) válidos; ${seen.size} claves de candidato y ${warnings} advertencia(s) de solapamiento.`);
  }
}
