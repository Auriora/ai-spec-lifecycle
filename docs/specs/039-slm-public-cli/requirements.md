---
title: Public slm CLI requirements
doc_type: spec
artifact_type: requirements
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Requirements

## Introduction

Spec Lifecycle Manager currently exposes structured lifecycle behavior through
MCP and a JSON-oriented recovery runtime, while the repository-local `slc`
command is maintainer tooling for validation, packaging, synchronization, and
release work. Users need a short, packaged, read-only command for inspecting
specs, tasks, requirements, and closed history without learning internal
runtime commands or reading raw JSON.

This spec introduces `slm` as that public CLI. It keeps `slc` as the separate
repository-maintenance command and deliberately does not preserve the existing
long installer executable names as compatibility aliases because they are not
in use.

## Goals

- Provide a short public `slm` executable from the release package.
- Present active specs and their distinct status, health, progress, and next
  task signals without inventing one misleading aggregate state.
- Provide task, requirement, and historical-spec views with predictable
  filters and stable machine-readable output.
- Reuse the shared lifecycle core so CLI and MCP/runtime interpretations do not
  drift.
- Keep the first public CLI release strictly read-only and cross-platform.
- Preserve the existing repository-local `slc` maintainer workflow.

## Non-Goals

- Add task-state, spec creation, closure, archive, promotion, or other write
  commands to `slm`.
- Rename, package, or broaden the repository-local `slc` maintainer CLI.
- Add a new MCP tool when an existing core or MCP surface already owns the
  underlying lifecycle meaning.
- Preserve `spec-lifecycle-manager` or `ai-spec-lifecycle` as executable
  compatibility aliases.
- Treat structural health as proof of implementation, validation, promotion,
  or closure readiness.
- Recreate removed spec packages in order to display history.
- Add a third-party table, colour, or terminal UI dependency.

## Glossary

| Term | Definition |
|------|------------|
| `slm` | Public, packaged, read-only Spec Lifecycle Manager CLI. |
| `slc` | Existing repository-local maintainer CLI for development, validation, packaging, synchronization, and release operations. |
| pending | Literal task marker `[ ]`; it does not mean every unfinished task. |
| open | Non-terminal task states that still need implementation, review, or intervention. |
| next | The dependency-aware task selected by the existing `next_task` lifecycle contract. |
| history | Closed-spec records from the archive index and closure log, including removed and retained archived dispositions. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `README.md` | Documents packaged installation, the current long installer command, and the Codex/Claude plugin surfaces. | high | Must describe `slm install` and the public inspection commands after promotion. |
| `docs/reference/spec-lifecycle-runtime.md` | Defines runtime commands, lifecycle state semantics, task markers, requirement priorities, archive behavior, and MCP-first boundaries. | high | Remains the detailed runtime authority. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Defines package layout, interpreter selection, installation, and cross-platform constraints. | high | Must include the public CLI and executable migration. |
| `docs/design/spec-lifecycle-management.md` | Defines the lifecycle architecture and MCP/runtime responsibilities. | high | Must record the public read-only presentation boundary. |
| `tools/devcli/` | Implements the repository-local Typer-based `slc` maintainer CLI. | high | Remains repo-local and is not the packaged public CLI. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Owns spec scanning, resolution, task state, next-task selection, requirements parsing, and archive semantics. | high | Public views must compose these contracts instead of reparsing Markdown independently. |
| `packaging/spec-lifecycle-manager/npm-install.js` and `package.json` | Expose the current package installer binaries and Python resolution path. | high | Must become or route through the `slm` dispatcher. |

## Durable Impact

See `change-impact.md` for the complete rename, packaging, runtime, and
documentation delta.

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| requirements/reference | modify | `README.md` | Make `slm` the public command and document the read-only views. |
| design | modify | `docs/design/spec-lifecycle-management.md` | Add the public CLI boundary and shared-core ownership. |
| runtime reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document commands, filters, state semantics, JSON output, and exit behavior. |
| install/reference | modify | `docs/reference/spec-lifecycle-manager-mcp-install.md` | Document the packaged `slm` executable and removal of old bin aliases. |
| package contract | modify | `package.json`, package manifests, package tests | Ship one `slm` bin with `install` and read-only inspection commands. |

## Staged Readiness

- **Current stage:** tasks
- **Next stage:** reconcile and implement
- **Ready to implement when:** package lint passes, the public command and
  output contracts remain traceable through design and tasks, and the selected
  implementation task has bounded context.
- **Design-first exception:** no
- **Optional artifacts included:** `canonical-context.md`, `change-impact.md`,
  `quickstart.md`, `traceability.md`, `verification.md`
- **Downstream review needed:** design, tasks, traceability, verification, and
  package/release review

## Requirements

### Requirement 1: Public executable identity

**User Story:** As a Spec Lifecycle Manager user, I want a short `slm` command,
so that routine lifecycle inspection is easy to discover and type.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN the released package is installed, WHEN the user invokes `slm
   --help`, THEN THE SYSTEM SHALL display the public lifecycle commands and the
   `install` command.
2. WHERE repository development tooling is used, THE SYSTEM SHALL retain `slc`
   as the distinct maintainer CLI and SHALL NOT package it as the public CLI.
3. WHEN the package bin contract is updated, THEN THE SYSTEM SHALL expose
   `slm` as the sole executable and SHALL remove the unused
   `spec-lifecycle-manager` and `ai-spec-lifecycle` executable aliases.
4. GIVEN the package name is invoked through npm or npx, WHEN its sole bin is
   selected, THEN THE SYSTEM SHALL route to the same `slm` command surface.

### Requirement 2: Active spec inventory

**User Story:** As a maintainer, I want to list active specs and their distinct
state signals, so that I can orient without confusing health with readiness.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a lifecycle-enabled repository, WHEN the user runs `slm specs`, THEN
   THE SYSTEM SHALL list active spec ID, declared status, structural health,
   completed/total task progress, and next runnable task where available.
2. WHERE no active specs exist, THE SYSTEM SHALL return a successful empty
   result with a concise explanation rather than treating absence as an error.
3. WHERE multiple state dimensions differ, THE SYSTEM SHALL display them as
   separate fields and SHALL NOT collapse them into an undocumented synthetic
   state.
4. WHEN the user runs bare `slm`, THEN THE SYSTEM SHALL behave as `slm specs`.
5. WHEN `--all` is supplied, THEN THE SYSTEM SHALL include active and historic
   records with an explicit lifecycle/disposition field.

### Requirement 3: Deterministic spec selection

**User Story:** As a user, I want concise but unambiguous spec references, so
that I can inspect the intended package without copying full paths.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a spec-taking command, WHEN the user supplies a full ID, unique
   numeric prefix, slug, or package path, THEN THE SYSTEM SHALL resolve it
   through the shared spec-resolution contract.
2. GIVEN no spec argument and exactly one active spec, WHEN the command runs,
   THEN THE SYSTEM SHALL select that spec.
3. GIVEN no spec argument and multiple active specs, WHEN the command runs,
   THEN THE SYSTEM SHALL exit without guessing and list concise candidate IDs.
4. GIVEN an ambiguous, historic-only, or missing reference where an active
   package is required, THEN THE SYSTEM SHALL return an actionable error that
   distinguishes those cases.

### Requirement 4: Task inventory and filters

**User Story:** As a maintainer, I want task listings filtered by truthful
state, so that I can review completed work, pending work, all open work, or the
next runnable task.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a selected active spec, WHEN the user runs `slm tasks [SPEC]`, THEN
   THE SYSTEM SHALL list task ID, marker, normalized state, dependencies,
   linked requirements, and summary.
2. WHEN `--complete` is supplied, THEN THE SYSTEM SHALL include only `[x]`
   complete tasks.
3. WHEN `--pending` is supplied, THEN THE SYSTEM SHALL include only literal
   `[ ]` pending tasks.
4. WHEN `--open` is supplied, THEN THE SYSTEM SHALL include non-terminal
   pending, in-progress, partial, review-needed, and attention tasks, and SHALL
   exclude complete, routed, no-op, and deferred outcomes.
5. WHEN one or more compatible task-state selectors are supplied from
   `--complete`, `--pending`, `--open`, or repeatable `--state STATE`, THEN THE
   SYSTEM SHALL include the union of their normalized state sets, and duplicate
   selectors SHALL NOT duplicate records.
6. WHEN `--next` is supplied, THEN THE SYSTEM SHALL return the same
   dependency-aware selection as the existing `next_task` contract and SHALL
   be mutually exclusive with task-state filters.
7. WHEN the user runs `slm next [SPEC]`, THEN THE SYSTEM SHALL behave as `slm
   tasks [SPEC] --next`.

### Requirement 5: Requirement inventory and priority

**User Story:** As a maintainer, I want requirements and their priorities in a
compact view, so that I can understand scope before selecting work.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a selected active spec, WHEN the user runs `slm requirements [SPEC]`,
   THEN THE SYSTEM SHALL list requirement ID, canonical priority, title, and
   linked task IDs where traceability exists.
2. WHERE a requirement has no accepted priority, THE SYSTEM SHALL display
   `unspecified` without treating compatibility input as invalid.
3. WHEN `--priority must-have`, `--priority should-have`, or `--priority
   could-have` is supplied, THEN THE SYSTEM SHALL return only requirements with
   that canonical priority.
4. WHEN `--missing-priority` is supplied, THEN THE SYSTEM SHALL return only
   requirements without an accepted canonical priority.
5. WHERE invalid or shorthand priority text exists, THE SYSTEM SHALL preserve
   the shared parser's diagnostic/canonicalization semantics rather than
   inventing a CLI-only interpretation.

### Requirement 6: Closed and historic spec inventory

**User Story:** As a maintainer, I want to list closed specs even when their
packages were removed, so that delivery history remains discoverable.

**Priority:** must-have

#### Acceptance Criteria

1. WHEN the user runs `slm history`, THEN THE SYSTEM SHALL list closed spec ID,
   title, disposition, final spec commit, and cleanup commit where recorded.
2. THE SYSTEM SHALL source historic records from the validated archive index
   and closure log and SHALL NOT require removed package directories to exist.
3. WHEN `--archived` or `--removed` is supplied, THEN THE SYSTEM SHALL filter
   by the corresponding retained or removed disposition; WHEN both are
   supplied, THEN THE SYSTEM SHALL return the union without duplicate records.
4. WHEN `--limit N` is supplied, THEN THE SYSTEM SHALL return at most the most
   recent `N` records in durable record order.
5. WHERE archive metadata is malformed, THE SYSTEM SHALL surface the existing
   archive diagnostics and SHALL NOT silently present invalid history as
   authoritative.

### Requirement 7: Human and machine output contracts

**User Story:** As a person or automation author, I want readable terminal
tables and stable JSON, so that the same command is useful interactively and in
scripts.

**Priority:** must-have

#### Acceptance Criteria

1. WHEN stdout is used without `--json`, THEN THE SYSTEM SHALL render concise
   plain-text tables or empty-state messages without a third-party UI
   dependency.
2. WHEN `--json` is supplied, THEN THE SYSTEM SHALL emit one valid JSON
   document containing schema version, command, repository root, records, and
   summary metadata.
3. THE SYSTEM SHALL derive table and JSON output from the same normalized
   records so that presentation modes cannot disagree about selection or
   state.
4. THE SYSTEM SHALL keep repository-owned paths repo-relative in user-facing
   output and SHALL avoid plugin-cache paths except in explicit diagnostics.
5. GIVEN identical repository state and arguments, THEN THE SYSTEM SHALL emit
   deterministic record ordering and JSON field meaning.

### Requirement 8: Repository discovery and failures

**User Story:** As a user working in nested directories, I want predictable
repository discovery and actionable failures, so that I do not have to run the
CLI only from the root.

**Priority:** should-have

#### Acceptance Criteria

1. GIVEN a working directory inside a repository, WHEN an `slm` inspection
   command runs, THEN THE SYSTEM SHALL discover the repository root according
   to the existing lifecycle root contract.
2. WHEN `-C PATH` or `--repo PATH` is supplied, THEN THE SYSTEM SHALL use the
   explicit repository root.
3. WHERE repository discovery, Python resolution, spec selection, or input
   validation fails, THE SYSTEM SHALL write a concise actionable error to
   stderr and return a non-zero exit code.
4. WHEN an inspection succeeds, including a valid empty result, THE SYSTEM
   SHALL return exit code zero.

### Requirement 9: Read-only and packaged operation

**User Story:** As a user, I want inspection commands to be safe and available
from the supported package, so that querying lifecycle state cannot modify my
repository.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN any `specs`, `tasks`, `next`, `requirements`, or `history` invocation,
   THEN THE SYSTEM SHALL NOT modify spec files, durable docs, configuration,
   plugin state, caches inside the repository, or Git state.
2. GIVEN the release tarball is installed on Windows, macOS, or Linux with a
   supported Node and Python runtime, WHEN `slm` is invoked, THEN THE SYSTEM
   SHALL resolve Python through the existing package interpreter contract and
   run without the repo-local Typer environment.
3. WHEN `slm install` is invoked, THEN THE SYSTEM SHALL preserve the existing
   package-owned Codex installation behavior.
4. THE SYSTEM SHALL ship the public CLI implementation, shared runtime modules,
   and tests through the package contract and SHALL verify the executable from
   a built tarball rather than a development checkout.

## Correctness Properties

- **CP-001:** For every task record, exactly one normalized state is derived
  from its persisted marker, and shorthand filters select only records in their
  defined state sets.
- **CP-002:** `slm tasks SPEC --next` and `slm next SPEC` select the same task
  ID and blocker outcome as the shared `next_task` contract for identical
  repository state.
- **CP-003:** Human table and JSON presentations contain the same normalized
  record set in the same deterministic order.
- **CP-004:** No read-only command changes the repository worktree or lifecycle
  artifacts.
- **CP-005:** An ambiguous or absent selection with multiple active specs never
  chooses a spec implicitly.
- **CP-006:** Historic output is a projection of validated durable closure
  records and never depends on recreating removed package content.
- **CP-007:** Requirement priority display uses the shared canonical parser;
  missing priority maps to `unspecified` and does not become a fourth persisted
  priority.

## Technical Context

- **Language/Version:** Node.js 18+ package dispatcher; Python 3.10+ standard
  library lifecycle runtime; Python 3.12+ remains acceptable for repo-local
  `slc` development.
- **Primary Dependencies:** Existing lifecycle core, package interpreter
  resolver, npm package contract, `unittest`, and Node's built-in test runner.
- **Target Platform:** Windows, macOS, and Linux terminals and automation.
- **Constraints:** No packaged Typer dependency; no Markdown re-parser outside
  the shared core; no writes from inspection commands; repo-relative output.
- **Performance Goals:** One repository scan per invocation where practical;
  avoid repeated full lint or closure checks merely to render a list; remain
  responsive for repositories with hundreds of active and historic specs.

## Success Criteria

- **SC-001:** A tarball-installed `slm` can render active specs, filtered tasks,
  requirements with priorities, next task, and history on all supported
  platforms.
- **SC-002:** Focused and full tests prove task-filter partitions, selection
  ambiguity, requirement priority behavior, durable history sourcing, JSON
  parity, and read-only worktree preservation.
- **SC-003:** `package.json` exposes `slm` as its sole bin, `slm install`
  preserves installation, and package validation confirms all public CLI files
  are present.
- **SC-004:** README, runtime, design, and installation references describe the
  accepted public CLI and clearly distinguish it from `slc` and MCP.

## Related Artifacts

- Change Impact: `change-impact.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
- Quickstart: `quickstart.md`
