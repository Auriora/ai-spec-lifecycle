<!--
Copyright 2026 Auriora

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Agent Development Lifecycle

This repository maintains the `spec-lifecycle-manager` Codex plugin, its
repo-owned skill source, runtime helpers, MCP prompt definitions, fallback
templates, and durable documentation for the lifecycle model.

The lifecycle model treats implementation specs as temporary delivery
scaffolding. Active work lives in `docs/specs/[###-slug]/`; accepted behavior is
promoted into durable docs before a spec is closed and removed or archived.

## Repository Layout

- `skills/spec-lifecycle-manager/`: canonical skill source.
- `skills/spec-lifecycle-manager/scripts/`: Python runtime helpers and MCP
  server implementation.
- `skills/spec-lifecycle-manager/prompts/`: MCP prompt definitions.
- `skills/spec-lifecycle-manager/references/`: fallback spec-package and
  durable-doc templates.
- `plugins/spec-lifecycle-manager/`: bundled Codex and Claude plugin copies.
- `packaging/spec-lifecycle-manager/`: npm packaging and installer support.
- `docs/`: durable design, governance, reference, backlog, roadmap, and history
  documentation.
- `docs/specs/`: active implementation specs, when present.
- `tests/`: `unittest` and Node runtime coverage with fixtures under
  `tests/fixtures/`.

## Start Here

- `docs/README.md`: documentation index and lifecycle overview.
- `docs/design/spec-lifecycle-management.md`: current lifecycle design.
- `docs/reference/spec-lifecycle-runtime.md`: runtime and MCP tool reference.
- `docs/reference/spec-lifecycle-manager-mcp-install.md`: MCP installation
  guidance.
- `docs/history/spec-closure-log.md`: narrative history for closed specs.
- `docs/history/spec-archive-index.md`: compact archive lookup for closed specs.
- `AGENTS.md`: repository instructions for coding agents.

## Validation

Run the full Python test suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

Run the repository validation bundle:

```bash
npm run validate
```

Run focused lifecycle checks:

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts
git diff --check
```

In Codex sessions where the `spec-lifecycle-manager` MCP server is available,
prefer the MCP tools for lifecycle context and use the direct Python commands
for CI, recovery, and runtime debugging.

## Releases

Use the local developer CLI to prepare release notes from Git evidence before
tagging a release:

```bash
slc release notes \
  --from v0.3.0 \
  --to HEAD \
  --version 0.2.1 \
  --output docs/release-notes/v0.3.0-draft.md \
  --evidence-output docs/release-notes/v0.3.0-evidence.json \
  --agent-instructions docs/release-notes/v0.3.0-agent.md
```

Review the generated evidence and write the final release note to
`docs/release-notes/vX.Y.Z.md`. The GitHub release workflow requires that file
for tag builds and publishes the packed npm tarball to the matching GitHub
release. npm publishing remains guarded by manual `workflow_dispatch` plus the
`NPM_TOKEN` secret.

## Install

The supported distribution path is the npm package tarball attached to GitHub
releases. The package installs the bundled plugin; do not install by cloning
this repository and copying files with `rsync`.

Install the latest released package globally:

```bash
npm install -g https://github.com/Auriora/ai-spec-lifecycle/releases/download/v0.3.0/auriora-ai-spec-lifecycle-0.3.0.tgz
```

### Codex

Install or refresh the Codex plugin from the npm package:

```bash
spec-lifecycle-manager install
```

The installer resolves Python 3.10+, installs the self-contained Codex plugin,
removes old managed standalone skill/MCP/hook entries, registers the local
marketplace entry, and runs `codex plugin add`.

Use a custom Codex home when needed:

```bash
spec-lifecycle-manager install --codex-home ~/.codex
```

Confirm the plugin is available:

```bash
codex plugin list
```

### Claude Code

For a version-pinned install without cloning the repository:

```bash
claude plugin marketplace add https://raw.githubusercontent.com/Auriora/ai-spec-lifecycle/main/packaging/spec-lifecycle-manager/marketplace-pinned.json
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

Confirm the plugin is installed and enabled:

```bash
claude plugin list
```

For offline or tarball-based Claude installs, unpack the same release tarball
and use its bundled marketplace:

```bash
tar -xzf auriora-ai-spec-lifecycle-0.3.0.tgz
claude plugin marketplace add ./package
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

## Local Development

The repo copy under `skills/spec-lifecycle-manager/` is the source of truth.
Installed copies and bundled plugin copies are generated or mirrored artifacts
that must stay in sync with the source skill.

Run the MCP server directly from source only while developing this repo:

```bash
python3 skills/spec-lifecycle-manager/scripts/spec_mcp_server.py "$PWD"
```

## License

This project is licensed under the GNU General Public License v3.0 or later.
See `LICENSE` for the full license text.
