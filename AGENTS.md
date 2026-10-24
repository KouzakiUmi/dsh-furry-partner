# DSH project boundaries

- This repository maintains the DSH product only. Use dsh-furry-partner for Host/Client identities, Cordis slot and package references, and /api/dsh-furry-partner for routes. The user explicitly authorized this migration on 2026-10-25. Preserve existing dsh-furry-partner:ui:v2 and :settings:v2 browser preferences.
- Do not add Pi entry points, a Pi SDK dependency, Pi installers, or Legacy simple-frame preparation logic. Shared animation modules are independent copies with source provenance.
- Preserve approved animation, palette, alpha, anchors, timing, and source approval records. Code changes do not authorize artwork generation or installation.
- Run npm run build and npm test after runtime changes. Verify release packages and matching version tags before publishing. Keep historical tags and source records intact.
