# DSH project boundaries

- This repository maintains the DSH product only. Use dsh-furry-partner for Host/Client identities, Cordis slot and package references, and /api/dsh-furry-partner for routes. The user explicitly authorized this migration on 2026-10-25. Preserve existing dsh-furry-partner:ui:v2 and :settings:v2 browser preferences.
- Do not add Pi entry points, a Pi SDK dependency, Pi installers, or Legacy simple-frame preparation logic. Shared animation modules are independent copies with source provenance.
- Preserve approved animation, palette, alpha, anchors, timing, and source approval records. Code changes do not authorize artwork generation or installation.
- Run npm run build and npm test after runtime changes. Verify release packages and matching version tags before publishing. Keep historical tags and source records intact.

## Release package contents

- `package.json` `files` lists what ships. Runtime code reads only `assets/animated` (catalog, hires frames, indexed), `assets/hires/umi` (fallback poses, watch, search, gestures), `assets/reactions/umi` (sheet indices), `assets/branding/title.json` + `umi-title.png`, `assets/illustration`, and `prompts`.
- Asset layering: `assets/animated/{hires,indexed}` holds the approved color derivatives the runtime serves; `Hi-Res/` (flat: `catalog.json`, `source-index.json`, `hires/`, `indexed/`) is the immutable pre-color frozen baseline used only by historical approval tests and `tools/verify-approved-color-consistency.py`. Nothing under `Hi-Res/` ships or is read at runtime.
- Excluded from the package but kept in the repository: `assets/animated/provenance/**` (approval evidence chain; tests read it from the working tree, runtime never does) and `assets/branding/umi-title-wave.webp` (dormant: `title.json` marks `qa.accepted: false`, so `loadTitleBranding` never serves it).
- Adding a new runtime asset means adding a positive `files` pattern; verify with `npm pack --dry-run --json` that entry count and total bytes match expectations, then unpack the built tgz and confirm the runtime loaders still resolve their files.
- Approved artwork is kept byte-exact by default. Reducing frame size by re-encoding changes approved pixels and hashes, so it needs explicit authorization plus updated approval records; it is not a packaging-only decision.
- `assets/animated/hires` was re-encoded to lossy WebP q90 with the user's authorization (2026-10-27). Alpha stays byte-identical to the approved pixels; RGB is bound by an alpha-weighted tolerance. The approved originals are recoverable: `Hi-Res/` holds the frozen baseline, and `assets/animated/provenance/lossy-q90-reencode.json` records every frame's before/after hash pair plus its measured PSNR. Re-encode with `scripts/reencode-approved-hires.py`, then run `node scripts/sync-adapted-hashes.mjs` after any edit to an already-adapted file.
