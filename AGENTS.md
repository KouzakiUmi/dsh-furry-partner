# DSH project boundaries

- This repository maintains the DSH product only. Preserve the existing Host/Client IDs, Cordis slot ID, API paths, and settings keys unless the user explicitly authorizes a migration.
- Do not add Pi entry points, a Pi SDK dependency, Pi installers, or Legacy simple-frame preparation logic. Shared animation modules are independent copies with source provenance.
- Preserve approved animation, palette, alpha, anchors, timing, and source approval records. Code changes do not authorize artwork generation or installation.
- Run npm run build and npm test after runtime changes. Verify release packages and matching version tags before publishing. Keep historical tags and source records intact.
