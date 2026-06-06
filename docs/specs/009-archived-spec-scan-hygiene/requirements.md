---
title: Archived spec scan hygiene requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Requirements

## Introduction

Archived spec packages are historical delivery records. They may predate the
current spec lint expectations, so default repository scans should not report
active health failures solely because an archived package no longer matches the
latest authoring template.

## Goals

- Keep archived specs visible in repository inventory.
- Exclude archived specs from active-health lint by default.
- Provide an explicit audit mode for archived package lint.
- Document the behavior for CLI, MCP, hooks, and future agents.
- Add regression tests for default scan and audit scan behavior.

## Non-Goals

- Migrate old archived specs to the current template.
- Disable direct lint or closure checks for archived packages.
- Remove archived packages from the repository.
- Change the closure-log or Git-backed archive implementation.

## Glossary

| Term | Definition |
|------|------------|
| Active health | Scan health for packages that are still active delivery work. |
| Archived lint audit | Explicit scan mode that runs authoring lint against archived packages. |
| Historical package | A retained spec package marked `archived`, `closed`, or `superseded`. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/reference/spec-lifecycle-runtime.md` | Runtime scan reports package health and notes archived specs are detected but not migrated. | high | Needs default active-health semantics. |
| `docs/design/spec-lifecycle-management.md` | Archived specs should remain historical unless resumed. | high | Needs scan-health policy. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | `scan_specs` currently lints every discovered package. | high | Old archived packages can surface current-template diagnostics. |

## Requirements

### Requirement 1: Active-Health Scan Boundary

**User Story:** As a maintainer, I want default scans to separate active and
archived package health, so that historical records do not look like active
implementation failures.

#### Acceptance Criteria

1. GIVEN a package has an archived lifecycle status, WHEN default scan runs,
   THEN the package SHALL remain in the inventory with archived lifecycle
   metadata.
2. GIVEN default scan runs, WHEN an archived package predates current lint
   expectations, THEN the scan SHALL skip authoring lint for that package.
3. WHERE scan summary is reported, THE SYSTEM SHALL count active and archived
   packages separately and SHALL report active pass, warning, and error counts.

### Requirement 2: Explicit Archived Audit

**User Story:** As a maintainer, I want an explicit archived lint audit mode,
so that historical packages can still be checked when intentionally reviewing
old records.

#### Acceptance Criteria

1. GIVEN an operator requests archived lint inclusion, WHEN scan runs, THEN the
   runtime SHALL lint archived packages and report their diagnostics in health.
2. GIVEN a package is linted directly, WHEN it is archived, THEN direct lint
   SHALL remain strict and SHALL not silently skip diagnostics.
3. IF the MCP scan tool is used, THEN it SHALL expose the archived audit option.

### Requirement 3: Documentation And Guidance

**User Story:** As an agent using the skill, I want clear guidance about
archived scan behavior, so that I do not migrate or fail old packages during
active implementation work.

#### Acceptance Criteria

1. GIVEN runtime guidance is read, WHEN scan behavior is described, THEN it
   SHALL state that archived packages are excluded from active-health lint by
   default.
2. WHERE explicit audits are documented, THE SYSTEM SHALL name the CLI flag and
   MCP argument.
3. IF a historical package must be modernized, THEN the guidance SHALL require
   a separate migration or resumption decision instead of automatic migration.

### Requirement 4: Validation Coverage

**User Story:** As a maintainer, I want automated tests for archived scan
hygiene, so that future runtime changes do not reintroduce noisy active scans.

#### Acceptance Criteria

1. GIVEN regression tests run, WHEN default scan is tested, THEN archived
   packages SHALL show skipped archived health.
2. GIVEN regression tests run, WHEN archived audit mode is tested, THEN old
   archived diagnostics SHALL be visible.
3. WHERE MCP scan is tested, THE SYSTEM SHALL cover the archived audit option.

## Correctness Properties

- Archived packages remain discoverable in every scan mode.
- Default scan active-error counts are unaffected by archived package lint
  diagnostics.
- Explicit archived audit mode returns the same kind of health diagnostics that
  active scan health returns.
- Direct lint behavior is status independent.

## Technical Context

The implementation affects the dependency-free runtime and MCP adapter:
`skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
`skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, and regression
tests under `tests/runtime/`.

## Success Criteria

- Default `scan` reports archived packages as skipped from active authoring
  lint.
- `scan --include-archived-lint` exposes diagnostics for old archived specs.
- MCP `scan_specs` accepts `include_archived_lint`.
- Runtime tests pass and durable docs describe the behavior.
