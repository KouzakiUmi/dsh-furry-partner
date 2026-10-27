# DSH Furry Partner · Umi

[简体中文](README.md) · [Documentation](docs/README.md) · [Identity and upgrade migration](docs/runtime-identity.md)

An animated Umi companion for DeepSeek Harness (DSH), with Chinese/English UI, 29 approved motion clips (including idle and enter/exit variants), real tool/session following, local companionship and an optional character voice. Current version **2.5.1-preview.8**, available as a pre-release, not yet published to npm.

## Build and install

### Download the prebuilt package

Download `dsh-furry-partner-2.5.1-preview.8.tgz` from [Releases](https://github.com/KouzakiUmi/dsh-furry-partner/releases), check it against the matching `.tgz.sha256`, then install:

```sh
dsh plugin --profile <profile> add "./dsh-furry-partner-2.5.1-preview.8.tgz"
```

The desktop app owns its `desktop` profile (the CLI refuses that profile), so install the local package through the app's plugin page instead of the command above.

### Build the package from this repository

```sh
python -m pip install -r tools/requirements-validation.txt
npm run build
npm test
npm run pack:release
```

Artifacts land in `dist/`: the tgz, its SHA-256, and a per-entry read-back report.

### Install directly from Git

The repository ships the built `lib/client.js`, so no build step is required first; the full clone is about 1.8 GB because the approved source artwork is committed:

```sh
dsh plugin --profile <profile> add "github:KouzakiUmi/dsh-furry-partner"
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
