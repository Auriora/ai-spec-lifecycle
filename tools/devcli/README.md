# Dev CLI

This package provides the `slc` developer interface for Spec Lifecycle tooling.
It is a thin wrapper over repository-owned scripts, npm commands, and
`skills/spec-lifecycle-manager/scripts/spec_runtime.py`; it should not duplicate
the lifecycle runtime.

## Install

```bash
pip install --no-build-isolation -e tools/devcli
```

## Commands

The current command identity is `slc`. No `proj` compatibility alias is
retained.

```bash
slc check
slc sync bundles --dry-run
slc sync guard
slc package check
slc package pack
slc package install-local --dry-run
slc plugin status
slc doctor
slc spec scan
slc spec archive-index
slc spec prompts
slc spec lint docs/specs/025-dev-cli-workflow-tools
slc release preflight --allow-dirty
```

Command implementations live in `src/auriora_dev/cli.py` and
`src/auriora_dev/commands/`. Shared command planning and repository path
helpers live in:

- `src/auriora_dev/runner.py`
- `src/auriora_dev/repo.py`

## Mutation Boundaries

Read-only commands should only inspect repository state or render command
plans. Mutating commands, such as bundle sync or local plugin install, must
state the underlying authoritative command and use dry-run behavior when that
command supports it. Tests should mock external commands or use safe dry-run
paths so they do not require Codex, npm publish credentials, GitHub
credentials, or writable user-level config.

Run focused CLI tests with:

```bash
npm run test:devcli
```

Task files use grouped Kiro-style checklists with `[ ]`, `[-]`, and `[x]`,
plus numbered tasks and sub-tasks.
