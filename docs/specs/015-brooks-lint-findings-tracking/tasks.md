---
title: Brooks-Lint findings tracking tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

## Phase 1: Register Definition

- [x] T001 Define the durable Brooks findings register.
  - Requirements: Requirement 1, Requirement 3
  - Acceptance: Register schema includes stable IDs, mode, scope, severity,
    state, Symptom, Source, Consequence, Remedy, references, triage, and
    verification fields.
  - Evidence: Added `docs/reviews/brooks-lint/README.md` with the durable
    register schema, accepted mode-specific ID namespaces, mode-specific
    fields, state model, duplicate handling, and maintenance rules; D004 is
    accepted in `open-decisions.md`.

- [ ] T002 Decide how Brooks score history is handled.
  - Requirements: Requirement 4
  - Depends on: T001
  - Acceptance: `.brooks-lint-history.json` treatment is documented as committed
    artifact, ignored local telemetry, or optional supporting evidence.
  - Evidence:

## Phase 2: Seed Findings

- [ ] T003 Seed the register with the first Brooks architecture audit findings.
  - Requirements: Requirement 1, Requirement 2, Requirement 3
  - Depends on: T001
  - Acceptance: `BL-ARCH-001` through `BL-ARCH-004`, `BL-DEBT-001` through
    `BL-DEBT-004`, `BL-HEALTH-001` through `BL-HEALTH-005`, and
    `BL-TEST-001` through `BL-TEST-003` are recorded with current state,
    references, and mode-specific fields where applicable.
  - Evidence:

- [ ] T004 Add validation or documented maintenance rules for future Brooks runs.
  - Requirements: Requirement 2, Requirement 3, Requirement 4
  - Depends on: T001, T002, T003
  - Acceptance: Future Brooks skill runs have clear append/reconcile rules, and
    runtime validation is added only if D001 accepts it.
  - Evidence:

## Phase 3: Triage and Promotion

- [ ] T005 Triage seed findings into accepted, deferred, dismissed, or resolved.
  - Requirements: Requirement 2, Requirement 5
  - Depends on: T003
  - Acceptance: Each seed finding has a triage state and rationale.
  - Evidence:

- [ ] T006 Route accepted and deferred findings to tasks, backlog, roadmap, or
      explicit no-action decisions.
  - Requirements: Requirement 2, Requirement 5
  - Depends on: T005
  - Acceptance: No tracked seed finding remains without a destination or
    rationale.
  - Evidence:

## Phase 4: Verification and Closure

- [ ] T007 Validate lifecycle health and any runtime or plugin changes.
  - Requirements: Requirement 3, Requirement 4, Requirement 5
  - Depends on: T004, T006
  - Acceptance: Required validation commands pass and evidence is recorded.
  - Evidence:

- [ ] T008 Promote durable outcomes and prepare closure.
  - Requirements: Requirement 5
  - Depends on: T007
  - Acceptance: Register, backlog, roadmap, and closure targets are current.
  - Evidence:
