# DSH Furry Partner · Umi

[简体中文](README.md) · [Documentation](docs/README.md) · [Identity and upgrade migration](docs/runtime-identity.md)

An animated Umi companion for DeepSeek Harness (DSH), with Chinese/English UI, 29 complete clips, real tool/session following, local companionship and an optional character voice. Current source is **2.5.1-preview.7**, not yet published as a Release.

## Build and install

```sh
python -m pip install -r tools/requirements-validation.txt
npm run build
npm test
npm run pack:release
```

Save work and disable the old plugin before installing the generated package from dist. Check the installed DSH version's command help for available options:

```sh
dsh plugin --profile desktop add "./dsh-furry-partner-2.5.1-preview.7.tgz"
```

Restart DSH after installation. Only the illustrated full-animation style is exposed; historical pixel preferences migrate to illustration. Build and test commands do not install the plugin or modify a live DSH configuration.

## Canonical runtime identity

| Component | Value |
| --- | --- |
| Package, Host and client module ID | `dsh-furry-partner` |
| Client plugin | `dsh-furry-partner/client` |
| Cordis id / name | `dsh-furry-partner` / `dsh-furry-partner` |
| Host API prefix | `/api/dsh-furry-partner/` |
| Settings slot key | `plugins.bundle.config:dsh-furry-partner` |
| Browser preference keys | `dsh-furry-partner:ui:v2`, `dsh-furry-partner:settings:v2` |

Replace the previous Cordis entry rather than loading both identities. Update Host and Client together, then reload. Old API aliases are not retained. Existing DSH browser keys are unchanged; back up file configuration before an upgrade. See [migration steps](docs/runtime-identity.md).

## Development and provenance

Use Node.js 24 and Python. The runtime has no dependency on another host SDK, adjacent repository or old work directory. Build generates lib/client.js from reviewed modules; do not edit that bundle directly. Tests cover Host/Client, session following, playback timing, failures, interactions, names/routes and source provenance. Packaging reads every archive entry back and emits SHA-256 and audit reports.

Code/docs are Apache-2.0; character artwork remains ARR under [ASSET_LICENSE](ASSET_LICENSE.md). SOURCE-PROVENANCE.json retains original source hashes and separately binds adapted code hashes. Approved assets and records remain unchanged. Original repository names are provenance facts, not active runtime identities. Unused historical host system prompts are archived under docs/history/source-prompts and excluded from the runtime package.

The [original project](https://github.com/KouzakiUmi/pi-furry-partner) maintains its terminal editions separately. The repositories do not share mutable runtime code.
