---
title: Developer CLI workflow tools requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Requirements

## Introduction

This repository has repeated maintainer workflows for validation, source-to-bundle
sync, local plugin install, installed cache verification, package dry-runs,
spec lifecycle checks, and release preflight. Today those workflows are spread
across direct `spec_runtime.py` commands, npm scripts, shell scripts, package
metadata, runbooks, and terminal history.

The new `tools/` scaffold should become a small repository-owned developer CLI
that makes those workflows easy to repeat without creating a second lifecycle
runtime, installer, packager, or release system.

## Goals

- Provide a project-specific CLI entry point for `agent-dev-lifecycle`
  maintainer workflows.
- Replace template `proj` commands with commands that run real repository
  workflows.
- Keep CLI commands thin, explicit wrappers over authoritative scripts,
  package metadata, and `spec_runtime.py`.
- Make validation, bundle sync, local install, package preflight, spec checks,
  and release preflight easier to run safely.
- Make mutating commands explicit and dry-run-friendly where the underlying
  workflow supports it.
- Test command composition and failure behavior without requiring local Codex,
  npm credentials, GitHub credentials, or user-level config mutation.

## Non-Goals

- Do not duplicate lifecycle parsing, linting, closure, package-contract, or
  sync-guard logic from `spec_runtime.py`.
- Do not duplicate installer logic from
  `scripts/install-spec-lifecycle-manager-package.sh`.
- Do not implement a second MCP server, hook runner, or plugin packager.
- Do not publish npm packages, push tags, create GitHub releases, or mutate
  GitHub state in the first implementation slice.
- Do not add broad project scaffolding unrelated to this repository's
  lifecycle-plugin maintenance workflows.
- Do not retain template-specific `proj` naming or `docs/spec` assumptions.

## Glossary

| Term | Definition |
|------|------------|
| Developer CLI | Repository-owned command-line interface under `tools/devcli` for local maintainers and agents. |
| Authoritative command | Existing command that owns behavior, such as `spec_runtime.py package-contract .`, `npm pack --dry-run --json`, or `scripts/install-spec-lifecycle-manager-package.sh`. |
| Wrapper command | CLI command that validates options, runs authoritative commands, and reports stage status. |
| Dry run | Mode that prints planned commands or invokes authoritative dry-run behavior without unsupported mutation. |
| Bundle sync | Copying source skill changes into bundled Codex and Claude plugin copies, then validating parity. |
| External release state | npm registry, GitHub releases, Git tags pushed to remotes, and other state outside the local checkout. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `AGENTS.md` | Defines repo structure, validation commands, lifecycle MCP preference, and repo-relative path policy. | high | CLI docs and output should follow the same path policy. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime commands, hook behavior, sync guard, package contract, and path policy. | high | `spec_runtime.py` remains the lifecycle engine. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Documents plugin install, npm package shape, hook policy, and validation checklist. | high | CLI should wrap this workflow, not replace it. |
| `docs/specs/022-npm-publish-release-workflow/` | Active spec for CI/CD, guarded npm publish, release evidence, and install verification. | high | Release-push and publish behavior belongs there, not in this CLI spec's first slice. |
| `package.json` | Defines npm package metadata, validation script, and pack dry-run command. | high | CLI package commands should invoke these commands or equivalent authoritative scripts. |
| `scripts/install-spec-lifecycle-manager-package.sh` | Owns local plugin install and old standalone config cleanup. | high | CLI install command should pass through supported options. |
| `tools/README.md`, `tools/devcli/README.md`, `tools/devcli/pyproject.toml` | New generic CLI scaffold with placeholder `proj` command and template text. | high | Must be replaced with project-specific identity and commands. |
| `../agent-workbench/docs/specs/028-dev-cli-workflow-tools/` | Reference pattern for a thin repository-owned developer CLI. | medium | Input pattern only; commands must be adapted to this repository. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| agent instructions | clarify | `AGENTS.md` | Add CLI usage only if it becomes a standard workflow. |
| runtime reference | clarify | `docs/reference/spec-lifecycle-runtime.md` | Document CLI convenience wrappers after implementation. |
| install runbook | modify | `docs/reference/spec-lifecycle-manager-mcp-install.md` | Add CLI commands while preserving authoritative underlying commands. |
| package metadata | modify | `tools/devcli/pyproject.toml`, possibly `package.json` | Add project-specific CLI metadata and test command. |
| active release workflow | unchanged | `docs/specs/022-npm-publish-release-workflow/` | Keep publish and release automation there. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** CLI identity, authoritative command boundaries,
  mutation boundaries, and test safety are clear.
- **Design-first exception:** no.
- **Optional artifacts recommended:** `change-impact.md`
- **Downstream review needed:** tasks, traceability, verification

## Requirements

### Requirement 1: Project-Specific CLI Identity

**User Story:** As a maintainer, I want a repository-specific command name and
help text, so that CLI commands clearly belong to `agent-dev-lifecycle`.

#### Acceptance Criteria

1. GIVEN the CLI package, WHEN it is installed editable from `tools/devcli`,
   THEN it SHALL expose a primary project-specific command such as `slc`.
2. WHEN a user runs the CLI with no arguments or `--help`, THEN it SHALL show
   lifecycle, package, sync, install, and release-preflight command groups.
3. WHEN package metadata is inspected, THEN it SHALL use repository-specific
   package name, description, and script entry point.
4. IF a compatibility alias is retained, THEN it SHALL be documented as
   temporary and SHALL NOT be the primary command in docs.

### Requirement 2: Shared Command Runner

**User Story:** As a CLI maintainer, I want one command execution layer, so
that every wrapper reports commands, failures, and dry-runs consistently.

#### Acceptance Criteria

1. GIVEN a wrapper command, WHEN it invokes an external command, THEN it SHALL
   use a shared runner that records label, argv, cwd, exit code, elapsed time,
   and mutation classification.
2. IF a dependent command fails, THEN subsequent dependent stages SHALL stop
   and the CLI SHALL return a non-zero exit code.
3. WHEN `--dry-run` is passed, THEN the CLI SHALL print planned commands or
   call authoritative dry-run modes without unsupported mutation.
4. WHEN command output is streamed, THEN failed command output SHALL remain
   visible enough to debug the failure.

### Requirement 3: Local Validation Wrapper

**User Story:** As a developer preparing a change, I want one validation
command, so that I can run the expected local checks without remembering every
runtime and package command.

#### Acceptance Criteria

1. GIVEN `slc check`, WHEN it runs, THEN it SHALL run the full unit suite,
   lifecycle scan, archive-index validation, prompt validation,
   package-contract validation, npm package dry-run, and `git diff --check` by
   default.
2. WHEN focused options are provided, THEN the CLI MAY run a reduced subset and
   SHALL make the reduced scope explicit.
3. IF any validation stage fails, THEN the CLI SHALL report the failed stage
   and return non-zero.
4. WHEN all stages pass, THEN the CLI SHALL summarize passed stages.

### Requirement 4: Bundle Sync Wrapper

**User Story:** As a maintainer changing skill source, I want one sync command,
so that source, bundled Codex plugin, and Claude plugin copies stay aligned.

#### Acceptance Criteria

1. GIVEN `slc sync bundles`, WHEN it runs, THEN it SHALL copy supported source
   skill files into bundled Codex and Claude plugin locations or report the
   planned copy operations in dry-run mode.
2. WHEN sync completes, THEN it SHALL run or recommend `sync-guard` to confirm
   source, bundle, installed cache, and commit evidence state.
3. IF bundled copies drift, THEN the command SHALL return non-zero or surface
   the drift clearly.
4. The command SHALL use repo-relative paths in all user-facing output.

### Requirement 5: Package And Install Wrappers

**User Story:** As a local Codex user, I want package and install commands, so
that I can refresh the local plugin install predictably.

#### Acceptance Criteria

1. GIVEN `slc package check`, WHEN it runs, THEN it SHALL run
   `package-contract`, npm pack dry-run, and `sync-guard`.
2. GIVEN `slc package install-local`, WHEN it runs, THEN it SHALL invoke
   `scripts/install-spec-lifecycle-manager-package.sh` with supported
   pass-through options.
3. WHEN users pass `--dry-run` to install-local, THEN the CLI SHALL use the
   installer dry-run rather than simulating installer behavior in Python.
4. WHEN install succeeds, THEN the CLI SHALL print the next verification
   command, such as `slc sync guard` or `slc plugin status`.

### Requirement 6: Plugin Status And Doctor

**User Story:** As a maintainer, I want read-only local diagnostics, so that I
can tell whether the installed plugin and local toolchain are usable.

#### Acceptance Criteria

1. GIVEN `slc plugin status`, WHEN it runs, THEN it SHALL inspect
   `codex plugin list` when available and report whether
   `spec-lifecycle-manager` appears installed.
2. IF Codex CLI is unavailable, THEN the command SHALL report a degraded status
   instead of pretending plugin state is known.
3. GIVEN `slc doctor`, WHEN it runs, THEN it SHALL report Python, Node, npm,
   Codex CLI availability, package metadata presence, and editable CLI install
   guidance.
4. Doctor SHALL be read-only by default.

### Requirement 7: Spec Lifecycle Wrappers

**User Story:** As an agent working on this repository, I want short wrappers
for spec lifecycle checks, so that I can use the repository's active spec
layout without remembering helper paths.

#### Acceptance Criteria

1. GIVEN `slc spec scan`, WHEN it runs, THEN it SHALL invoke
   `spec_runtime.py scan .`.
2. GIVEN `slc spec archive-index`, WHEN it runs, THEN it SHALL invoke
   `spec_runtime.py archive-index .`.
3. GIVEN `slc spec prompts`, WHEN it runs, THEN it SHALL invoke
   `spec_runtime.py prompts`.
4. GIVEN `slc spec lint <path>` or `slc spec summary <path>`, WHEN it runs,
   THEN it SHALL invoke the matching `spec_runtime.py` command.
5. The CLI SHALL NOT implement a second spec parser.

### Requirement 8: Release Preflight

**User Story:** As a maintainer preparing a release, I want a guarded preflight,
so that metadata, validation, package contents, and local state are checked
before any external release action.

#### Acceptance Criteria

1. GIVEN `slc release preflight`, WHEN it runs, THEN it SHALL check working
   tree status, package metadata, package validation, npm dry-run, and current
   active spec state.
2. IF the working tree is dirty, THEN the command SHALL report the dirty state
   and require an explicit flag to continue.
3. The first implementation SHALL NOT push commits or tags, publish npm,
   create GitHub releases, or mutate external release state.
4. Future push or publish commands SHALL be separate commands with explicit
   flags and human-controlled credentials.

### Requirement 9: Documentation And Mutation Boundaries

**User Story:** As a new contributor or agent, I want CLI docs that identify
underlying commands and mutation boundaries, so that I can use the CLI safely.

#### Acceptance Criteria

1. WHEN the CLI is implemented, THEN `tools/README.md` and
   `tools/devcli/README.md` SHALL document install, command groups, examples,
   and mutation boundaries.
2. WHEN CLI commands wrap install or package runbooks, THEN
   `docs/reference/spec-lifecycle-manager-mcp-install.md` SHALL mention the
   CLI as a convenience wrapper while preserving authoritative commands.
3. WHEN package metadata or scripts change, THEN documentation SHALL stay in
   sync with the chosen command name.

### Requirement 10: Tests And CI Safety

**User Story:** As a maintainer, I want CLI tests that do not mutate local
Codex, npm, GitHub, or plugin state, so that validation is safe in CI and local
sessions.

#### Acceptance Criteria

1. GIVEN CLI unit tests, WHEN they run, THEN external commands SHALL be mocked
   or executed only in safe dry-run modes.
2. Tests SHALL cover command composition, failure propagation, dry-run output,
   pass-through options, and repo-relative path handling.
3. CI integration SHALL NOT require a real Codex installation, npm publish
   credentials, GitHub credentials, or writable user-level Codex config.
4. Repository validation SHALL include the CLI tests once the CLI is active.

## Correctness Properties

- **CP-001:** Wrapper commands invoke documented authoritative commands in a
  deterministic order.
- **CP-002:** Failed dependent stages stop later dependent stages.
- **CP-003:** Dry-run mode does not mutate plugin installs, package metadata,
  external release state, or user-level Codex config beyond authoritative
  dry-run behavior.
- **CP-004:** User-facing CLI output uses repo-relative paths for in-repo files
  and absolute paths only for out-of-repo files.
- **CP-005:** Spec lifecycle wrappers call `spec_runtime.py` and do not parse
  spec packages independently.

## Technical Context

- **Language/Version:** Python 3.12 currently declared by `tools/devcli`.
- **Primary Dependencies:** Typer scaffold currently declares
  `typer>=0.12,<1.0`; test dependency decision remains open.
- **Target Platform:** Local maintainer checkout on Linux-like systems with
  Python, Node/npm, Git, and optional Codex CLI.
- **Constraints:** No local Codex mutation in tests; no external release
  mutation in first implementation; keep repo-relative path policy.
- **Performance Goals:** CLI startup and dry-run output should be fast enough
  for frequent local use; long-running validation is acceptable when explicit.

## Success Criteria

- **SC-001:** `slc --help` exposes project-specific command groups and no
  template placeholder commands.
- **SC-002:** `slc check`, `slc package check`, `slc package install-local`,
  `slc sync guard`, `slc plugin status`, `slc spec scan`, and
  `slc release preflight` are implemented or explicitly staged.
- **SC-003:** CLI tests cover command composition and no-mutation dry-run
  behavior.
- **SC-004:** Durable docs describe command usage, mutation boundaries, and
  authoritative underlying commands.

## Related Artifacts

- Change Impact: `change-impact.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
