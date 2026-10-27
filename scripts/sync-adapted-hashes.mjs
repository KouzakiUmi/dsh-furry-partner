#!/usr/bin/env node
// Rebind the current hashes of adapted files in SOURCE-PROVENANCE.json.
// Run after editing any file already listed in localAdaptations.
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const path = new URL('SOURCE-PROVENANCE.json', root);
const doc = JSON.parse(readFileSync(path, 'utf8'));
let changed = 0;
for (const rel of doc.localAdaptations || []) {
  const bytes = readFileSync(new URL(rel, root));
  const digest = createHash('sha256').update(bytes).digest('hex');
  if (doc.adaptedFileSha256[rel] !== digest) {
    doc.adaptedFileSha256[rel] = digest;
    console.log(`rebound ${rel}`);
    changed++;
  }
}
if (changed > 0) {
  writeFileSync(path, `${JSON.stringify(doc, null, 2)}\n`, 'utf8');
  console.log(`${changed} adapted hash(es) updated`);
} else {
  console.log('all adapted hashes already current');
}
