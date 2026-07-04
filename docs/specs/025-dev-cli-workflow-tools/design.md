---
title: Developer CLI workflow tools design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Technical Design

## Overview

The developer CLI should be a Python Typer package under `tools/devcli` with a
project-specific `slc` entry point. It should orchestrate existing repository
commands for validation, package checks, local install, bundle sync, spec
lifecycle checks, and release preflight.

The CLI is not a lifecycle runtime. `spec_runtime.py`, package metadata, npm
scripts, and installer scripts remain authoritative. The CLI improves
discoverability, sequencing, dry-run behavior, and failure reporting.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 CLI identity | AC1-AC4 | Package identity and command groups | CLI help and metadata tests |
| Requirement 2 runner | AC1-AC4 | Shared runner | Runner unit tests |
| Requirement 3 validation | AC1-AC4 | `slc check` | Command plan tests |
| Requirement 4 sync | AC1-AC4 | `slc sync` | Copy-plan and sync-guard tests |
| Requirement 5 package/install | AC1-AC4 | `slc package` | Package command tests |
| Requirement 6 status/doctor | AC1-AC4 | `slc plugin`, `slc doctor` | Mocked Codex/tool tests |
| Requirement 7 spec wrappers | AC1-AC5 | `slc spec` | Spec command tests |
| Requirement 8 release preflight | AC1-AC4 | `slc release preflight` | Preflight tests |
| Requirement 9 docs | AC1-AC3 | Operational docs | Documentation review |
| Requirement 10 tests | AC1-AC4 | Test strategy | CLI test command |

## Correctness Property Coverage

| Property | Design Behavior | Validation Direction | Notes |
|----------|-----------------|----------------------|-------|
| CP-001 | Command plans are built from explicit ordered `CommandSpec` stages. | Unit tests assert argv order. | |
| CP-002 | Runner stops dependent plans on first failure. | Failure propagation tests. | Independent aggregated checks can be added later if needed. |
| CP-003 | Dry-run uses runner rendering or authoritative dry-run flags. | Dry-run tests and install pass-through tests. | |
| CP-004 | Repo utility normalizes in-repo paths for display. | Path handling tests. | Mirrors repo-wide path policy. |
| CP-005 | Spec wrappers shell out to `spec_runtime.py`. | Command plan tests. | No duplicate parsing. |

## High-Level Design

### System Architecture

```text
tools/devcli/
  pyproject.toml
  src/auriora_dev/
    cli.py
    runner.py
    repo.py
    commands/
      check.py
      package.py
      plugin.py
      release.py
      spec.py
      sync.py
      doctor.py
  tests/
```

### Command Groups

```text
slc
  check
  doctor
  package
    check
    pack
    install-local
  plugin
    status
  release
    preflight
  spec
    scan
    summary
    lint
    archive-index
    prompts
  sync
    bundles
    guard
```

### Components and Changes

- `tools/devcli/pyproject.toml`
  - Rename package metadata from template names to repository-specific names.
  - Change primary entry point from `proj` to `slc`.
- `runner.py`
  - Provide shared command execution, dry-run rendering, mutation labels,
    elapsed time, and failure propagation.
- `repo.py`
  - Discover repo root from `pyproject.toml`, `package.json`,
    `scripts/install-spec-lifecycle-manager-package.sh`, and `.git`.
  - Normalize user-facing display paths.
- `commands/check.py`
  - Build validation command plan.
- `commands/package.py`
  - Wrap package contract, npm dry-run, and local installer.
- `commands/sync.py`
  - Sync source skill files into bundled plugin copies and run sync guard.
- `commands/plugin.py`
  - Read-only Codex plugin status.
- `commands/spec.py`
  - Wrap `spec_runtime.py` lifecycle commands.
- `commands/release.py`
  - Read-only release preflight.
- `commands/doctor.py`
  - Read-only local tool diagnostics.

### Data Flow

```text
CLI args
  -> Typer command handler
  -> repo root resolution
  -> command plan construction
  -> shared runner dry-run or execution
  -> per-stage summary
  -> process exit code
```

## Low-Level Design

### Package Identity

**Resolved 2026-07-04:** primary command is `slc`; package metadata uses
`slc-devcli`; no temporary `proj` alias is retained.

```toml
[project]
name = "slc-devcli"
description = "Stable developer CLI for the spec lifecycle tooling"

[project.scripts]
slc = "auriora_dev.cli:app"
```

`proj` is removed, not aliased, per the non-goal against retaining
template-specific naming.

### Shared Runner

```python
@dataclass(frozen=True)
class CommandSpec:
    label: str
    argv: tuple[str, ...]
    cwd: Path
    mutates: bool = False
    timeout_seconds: int | None = None
```

Runner behavior:

- print command label and argv before execution;
- render command plans in dry-run mode;
- stream stdout/stderr by default;
- stop dependent stages on first non-zero exit;
- report cwd, exit code, and elapsed time;
- use argv arrays, not shell strings.

### Repository Root Discovery

Root discovery should:

- accept `--repo-root` for all commands;
- walk upward from cwd and package location;
- require markers such as `package.json`,
  `scripts/install-spec-lifecycle-manager-package.sh`, `skills/spec-lifecycle-manager/`,
  or `.git`;
- fail clearly when no repository root is found.

### `slc check`

Default command plan:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .
npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json
git diff --check
```

Focused flags can disable stages, but output must say the scope is reduced.

### `slc sync`

`slc sync bundles` should sync source skill files into:

```text
plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/
plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/
```

The first implementation can copy the entire source skill tree or a documented
allowlist. After copying, it should run:

```text
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .
```

`slc sync guard` should run:

```text
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .
```

### `slc package`

`slc package check` plan:

```text
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .
npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .
```

`slc package pack` can initially wrap npm dry-run only; producing a real tarball
should require `--write` or an explicit non-dry-run flag.

`slc package install-local` should invoke:

```text
scripts/install-spec-lifecycle-manager-package.sh [supported options]
```

Supported pass-through options should match the installer, including
`--source`, `--marketplace-name`, `--codex-home`, and `--dry-run` when present.

### `slc plugin status`

Read-only command:

```text
codex plugin list
```

The command should tolerate missing Codex CLI and report degraded status.
Detailed installed-cache parity belongs to `slc sync guard`.

### `slc spec`

Spec wrappers should invoke:

```text
skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .
skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .
skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts
skills/spec-lifecycle-manager/scripts/spec_runtime.py summary <path>
skills/spec-lifecycle-manager/scripts/spec_runtime.py lint <path>
```

No wrapper should parse spec files directly.

### `slc release preflight`

Initial release preflight is local and non-mutating:

- check working tree status;
- run `slc package check`;
- inspect `package.json` version and package metadata;
- report active spec state, especially `022-npm-publish-release-workflow`;
- report whether publish/release commands are intentionally out of scope.

No push, tag, npm publish, or GitHub release creation is allowed in this spec's
first implementation.

## Error Handling

- Usage errors should use Typer defaults.
- External command failures should return the external exit code when
  practical.
- Missing optional tools should report `unavailable` or `degraded` status.
- Mutating commands should print mutation scope before execution.
- User-facing paths should be repo-relative for in-repo files.

## Security, Trust, and Access

- Do not read npm or GitHub credentials.
- Do not write user-level Codex config except by invoking the authoritative
  installer command the user explicitly requested.
- Do not run external release mutations in the first implementation.
- Use subprocess argv lists instead of shell strings.
- Tests must not require local Codex, GitHub, npm credentials, or writable
  user-level config.

## Migration and Compatibility

- The placeholder `proj` CLI is template scaffolding and can be removed.
- Existing scripts remain supported and documented as authoritative.
- CLI docs should present `slc` as a convenience wrapper, not the only path.
- Active spec `022` remains the owner of actual release automation and npm
  publish behavior.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| CLI unit tests | command composition, dry-run, failure propagation, path handling | `verification.md`, task evidence | Does not prove real local Codex state. |
| Full unit suite | existing runtime and package behavior | `verification.md` | Slow but local. |
| `package-contract .` | source/bundle parity and package metadata | `verification.md` | Installed cache checked by sync guard. |
| `sync-guard .` | installed cache and commit sync evidence | `verification.md` | Requires local installed cache for full signal. |
| npm pack dry-run | package payload | `verification.md` | Does not publish. |

## Downstream Task Guidance

- Implement CLI foundation before adding command wrappers.
- Add tests as each command group is added.
- Keep release mutation out of scope until `022` defines publish behavior.
- Update durable docs before closing the spec.

## Operational Considerations

- Keep CLI dependencies isolated to `tools/devcli`.
- Keep long-running validation opt-in and clearly labeled.
- Use dry-run-first defaults for package and release workflows where possible.
- Keep generated artifacts and caches out of Git.

## Open Questions

- Should `slc package pack` ever create a real tarball, or should it remain
  dry-run-only until release workflow `022` lands?
- Should `slc sync bundles` copy the full skill tree or a narrower allowlist?
- Should CLI tests use pytest, Typer's testing helper, or standard-library
  unittest with direct function tests?

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: `change-impact.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
