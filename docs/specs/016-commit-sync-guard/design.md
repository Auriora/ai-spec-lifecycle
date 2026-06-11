---
title: Commit sync guard design
doc_type: design
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Technical Design

## Overview

Add a read-only `sync-guard` command to
`skills/spec-lifecycle-manager/scripts/spec_runtime.py` for this
`agent-dev-lifecycle` package repository.

The command returns one JSON payload with:

- `source_bundle_parity`
- `bundle_cache_parity`
- `reload_advisory`
- `commit_evidence`
- `findings`
- `summary`
- `recommendations`

The guard is advisory. It does not call the installer, copy files, update Codex
configuration, remove old skill installs, or reload MCP processes.

When the command is run outside the Spec Lifecycle Manager package repository,
it returns `status: "not_applicable"` with missing package-maintainer paths and
does not emit drift findings.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
| --- | --- | --- | --- |
| Requirement 1 | AC1-AC3 | Manifest/hash comparison between source and bundled skill. | Fixture-backed runtime tests and existing plugin parity test. |
| Requirement 1A | AC1-AC3 | Repository applicability check before parity checks. | Fixture-backed non-package repository test. |
| Requirement 2 | AC1-AC3 | Cache candidate discovery under `$CODEX_HOME/plugins/cache`. | Fixture-backed runtime tests with temp Codex home. |
| Requirement 3 | AC1-AC3 | Reload advisory derived from parity state. | Unit tests and command output shape checks. |
| Requirement 4 | AC1-AC3 | Recent Git commit path classification. | Runtime command test against current Git history shape. |

## High-Level Design

### System Architecture

`spec_runtime.py` remains the single CLI implementation surface. The new
command composes local filesystem inspection and optional Git history
inspection into a JSON report.

### Components and Changes

- Runtime command parser: add `sync-guard`.
- Applicability helper: confirm this is the package-maintainer repository.
- Parity helpers: build file manifests and content hashes.
- Installed cache discovery: find candidate plugin cache directories.
- Reload advisory: derive whether reload is recommended from parity state.
- Commit evidence review: classify recent commits that touched the source
  skill.

### Data Models

The command returns dictionaries with stable keys rather than introducing a new
schema module. Each check includes `status`, `details`, and any `findings`
needed by the top-level summary.

### Data Flow

```text
repo root
  -> check repository applicability
  -> derive source, bundle, plugin, codex home, cache candidates
  -> compare source skill to bundled skill
  -> compare bundled plugin to selected installed cache candidate
  -> derive reload advisory from parity state
  -> inspect recent git commits when available
  -> aggregate findings, summary, and recommendations
```

## Path Model

Default paths are derived from the repository root:

| Role | Default path |
| --- | --- |
| Source skill | `skills/spec-lifecycle-manager/` |
| Bundled plugin | `plugins/spec-lifecycle-manager/` |
| Bundled plugin skill | `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/` |
| Codex home | `$CODEX_HOME` or `~/.codex` |
| Installed cache candidates | `$CODEX_HOME/plugins/cache/*/spec-lifecycle-manager/*/` |

The command accepts `--codex-home` so tests and local validation can use a
fixture directory without reading the real Codex home.

The applicability check requires these repository-owned paths before parity
checks run:

- `skills/spec-lifecycle-manager/SKILL.md`
- `plugins/spec-lifecycle-manager/.codex-plugin/plugin.json`
- `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md`
- `scripts/install-spec-lifecycle-manager-package.sh`
- `packaging/spec-lifecycle-manager/package-manifest.json`

## Parity Algorithm

Parity compares file manifests and SHA-256 hashes. It excludes generated and
local-only artifacts:

- `__pycache__/`
- `*.pyc`
- `.DS_Store`

The source-to-bundle check compares the source skill directory with the bundled
plugin skill directory.

The bundle-to-cache check compares `plugins/spec-lifecycle-manager/` with the
selected installed cache candidate. If multiple candidates exist, select the
newest by modification time and report all candidates.

## MCP Reload Advisory

The advisory recommends reload when:

- source/bundle parity is not `in_sync`; sync and install are needed before
  relying on MCP or hook code; or
- bundle/cache parity is not `in_sync`; reload Codex after install so
  plugin-scoped MCP and hooks use the refreshed package.

The guard does not enumerate running processes. Reload need is an operational
advisory derived from package/cache evidence, not host process state.

## Commit Evidence Algorithm

The command runs:

```bash
git log --name-only --format=%H%x09%s -n <N>
```

Default `N` is 5. For each recent commit touching
`skills/spec-lifecycle-manager/`, it reports whether the same commit touched
any sync evidence path:

- `plugins/spec-lifecycle-manager/`
- `packaging/spec-lifecycle-manager/`
- `scripts/install-spec-lifecycle-manager-package.sh`
- `docs/reference/spec-lifecycle-manager-mcp-install.md`
- `docs/reference/spec-lifecycle-runtime.md`

This is a reminder check, not proof that install happened.

## Low-Level Design

### Algorithms and Logic

```text
sync_guard(repo_root, codex_home, commits):
    source_bundle = compare_trees(source_skill, bundled_skill)
    cache = discover newest cache candidate
    bundle_cache = compare_trees(bundled_plugin, cache) or missing
    reload = derive reload advisory from parity state
    commits = inspect recent git commits for source and evidence paths
    findings = aggregate non-clean states
    return payload
```

### Function Signatures and Interfaces

```text
sync_guard(repo_root: Path, codex_home: Path | None, commit_count: int) -> dict[str, Any]
sync_guard_applicability(repo_root: Path) -> dict[str, Any]
compare_trees(left: Path, right: Path) -> dict[str, Any]
discover_plugin_cache_candidates(codex_home: Path) -> list[Path]
reload_advisory(source_bundle: dict[str, Any], bundle_cache: dict[str, Any]) -> dict[str, Any]
commit_sync_evidence(repo_root: Path, commit_count: int) -> dict[str, Any]
```

### Error Handling

Missing paths and unavailable Git inspection return structured payload sections
with `status: "missing"` or `status: "unknown"`. Unexpected filesystem errors
are reported as findings instead of mutating state.

### Security, Trust, and Access

The command reads local files and Git metadata only. It does not inspect OS
process tables, execute repo validation commands beyond `git log`, read file
contents outside selected parity trees, or write to Codex home.

### Migration and Compatibility

Existing runtime commands and MCP tools are unchanged. The first implementation
is CLI-only; MCP exposure can be added later if dogfooding shows it should be a
primary agent-facing tool.

## CLI

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .
```

Optional arguments:

- `--codex-home <path>`
- `--commits <N>`

## Risks

- Cache candidate selection is deterministic but cannot prove which cache Codex
  has loaded after a client restart.
- Commit evidence shows whether relevant files changed together; it does not
  prove the installer ran.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
| --- | --- | --- | --- |
| Focused sync guard tests | Requirements 1-4 | `verification.md`, task evidence | Reload state remains advisory rather than proof of a specific client session. |
| Full unittest suite | Runtime regression | `verification.md` | None expected. |
| Manual `sync-guard` run | Local package state | `verification.md` | Installed Codex cache may differ by user home. |

## Operational Considerations

Add the command to install validation docs so agents run it after package
changes and before claiming install parity. Reload remains a manual operator
step.

## Open Questions

- Should the guard become an MCP tool after CLI dogfooding?

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: `change-impact.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
