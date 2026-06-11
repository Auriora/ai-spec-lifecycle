---
title: GHCR distribution packaging tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-11
---

# GHCR Distribution Packaging Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004 -> T005
```

## Tasks

- [x] T001 Define focused GHCR packaging spec.
  - Depends on: none
  - Requirement: Requirement 1; Requirement 2; Requirement 3; Requirement 4
  - Files: `docs/specs/017-ghcr-distribution-packaging/`
  - Acceptance: Spec defines package contract, layout, validation, provenance,
    docs, and non-goals for registry publishing.
  - Evidence: Created this spec package.

- [x] T002 Add GHCR package contract artifacts.
  - Depends on: T001
  - Requirement: Requirements 1, 3
  - Files: `packaging/spec-lifecycle-manager/ghcr-package.json`,
    `packaging/spec-lifecycle-manager/Containerfile`
  - Acceptance: Contract defines package name, image reference, version source,
    payload root, required paths, labels, compatibility, and publish status.
  - Evidence: Added `packaging/spec-lifecycle-manager/ghcr-package.json`,
    `packaging/spec-lifecycle-manager/Containerfile`, and GHCR distribution
    metadata in `packaging/spec-lifecycle-manager/package-manifest.json`.

- [x] T003 Add deterministic package contract validation.
  - Depends on: T002
  - Requirement: Requirement 1; Requirement 2; Requirement 3
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `package-contract` reports package metadata, required path
    status, source/bundle parity, provenance, diagnostics, and summary.
  - Evidence: Added `package-contract` runtime command in source and bundled
    `spec_runtime.py`; focused `tests.runtime.test_spec_runtime` passed.

- [x] T004 Promote install and distribution docs.
  - Depends on: T003
  - Requirement: Requirement 4
  - Files: `docs/reference/spec-lifecycle-manager-mcp-install.md`,
    `docs/reference/spec-lifecycle-runtime.md`, `docs/backlog/README.md`
  - Acceptance: Docs describe local install as supported, GHCR as
    contract-ready and not yet published, and list validation commands.
  - Evidence: Updated `docs/reference/spec-lifecycle-runtime.md`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`, and
    `docs/backlog/README.md`.

- [x] T005 Validate and prepare closure.
  - Depends on: T004
  - Requirement: Requirement 1; Requirement 2; Requirement 3; Requirement 4
  - Files: `docs/specs/017-ghcr-distribution-packaging/verification.md`
  - Acceptance: Focused tests, full tests, package-contract, sync-guard, spec
    lint, closure check, and whitespace validation are recorded.
  - Evidence: Focused runtime tests passed; full unittest suite passed;
    `package-contract` passed; `sync-guard` reported source/bundle in sync and
    installed cache drift pending reinstall; spec lint, closure check, archive
    index, prompt validation, and whitespace checks passed.
