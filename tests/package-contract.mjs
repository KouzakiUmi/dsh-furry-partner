import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
const root = new URL('../', import.meta.url);
const pkg = JSON.parse(readFileSync(new URL('package.json', root), 'utf8'));
assert.equal(pkg.name, 'dsh-furry-partner');
assert.ok(!pkg.pi);
assert.equal(pkg.main, './lib/index.js');
assert.equal(pkg.dsh.bundle.patch, './cordis.patch.yml');
const patch = readFileSync(new URL('cordis.patch.yml', root), 'utf8');
assert.match(patch, /id:\s*dsh-furry-partner/);
assert.match(patch, /name:\s*dsh-furry-partner/);
assert.equal((await import(pkg.name)).name, 'dsh-furry-partner', 'The renamed package resolves to the DSH Host identity');
for (const name of ['index.ts', 'install.ps1', 'uninstall.ps1', 'tests/pi-runtime.mjs']) assert.ok(!existsSync(new URL(name, root)), name);
const provenance = JSON.parse(readFileSync(new URL('SOURCE-PROVENANCE.json', root), 'utf8'));
assert.equal(provenance.runtimeCompatibility.hostPluginId, 'dsh-furry-partner');
assert.ok(!Object.keys(pkg.dependencies || {}).some(name => name.includes('pi-coding-agent') || name.includes('pi-tui')));
for (const entry of readdirSync(new URL('lib/', root))) {
  if (!/\.(?:js|mjs)$/.test(entry)) continue;
  const code = readFileSync(new URL(`lib/${entry}`, root), 'utf8');
  assert.doesNotMatch(code, /pi-furry-partner|pi-system-|pi-motion-|\/api\/furry-partner/, `Obsolete runtime identity in ${entry}`);
}
console.log('Standalone DSH package: independent package/repository, canonical DSH identities, no Pi entry point/installer/SDK, and source provenance passed.');
