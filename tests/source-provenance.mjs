import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
const root = new URL('../', import.meta.url);
const source = JSON.parse(readFileSync(new URL('SOURCE-PROVENANCE.json', root), 'utf8'));
const modified = new Set(source.localAdaptations || []);
let checked = 0;
for (const [path, digest] of Object.entries(source.copiedFileSha256)) {
  assert.ok(!path.startsWith('/') && !path.split('/').includes('..'));
  const file = new URL(path, root);
  assert.ok(existsSync(file), `Missing extracted source: ${path}`);
  if (modified.has(path)) continue;
  assert.equal(createHash('sha256').update(readFileSync(file)).digest('hex'), digest, `Extracted source bytes changed: ${path}`);
  checked++;
}
console.log(`Standalone source provenance: ${checked} original file hashes and all extracted source paths passed.`);
