---
title: Brooks-Lint findings tracking tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-09
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

- [x] T002 Decide how Brooks score history is handled.
  - Requirements: Requirement 4
  - Depends on: T001
  - Acceptance: `.brooks-lint-history.json` treatment is documented as committed
    artifact, ignored local telemetry, or optional supporting evidence.
  - Evidence: Accepted D002 as optional supporting score-history evidence in
    `open-decisions.md`; documented the relationship between score history and
    the durable register in `docs/reviews/brooks-lint/README.md` and
    `change-impact.md`.

## Phase 2: Seed Findings

- [x] T003 Seed the register with the first Brooks architecture audit findings.
  - Requirements: Requirement 1, Requirement 2, Requirement 3
  - Depends on: T001
  - Acceptance: `BL-ARCH-001` through `BL-ARCH-004`, `BL-DEBT-001` through
    `BL-DEBT-004`, `BL-HEALTH-001` through `BL-HEALTH-005`, and
    `BL-TEST-001` through `BL-TEST-003` are recorded with current state,
    references, and mode-specific fields where applicable.
  - Evidence: Added `BL-ARCH-001` through `BL-ARCH-004`,
    `BL-DEBT-001` through `BL-DEBT-004`, `BL-HEALTH-001` through
    `BL-HEALTH-005`, and `BL-TEST-001` through `BL-TEST-003` to
    `docs/reviews/brooks-lint/README.md`; each seed finding preserves mode,
    scope, severity, state, symptom, source, consequence, remedy, repository
    references, Brooks attribution, pending triage rationale, pending
    destination, and pending verification.

- [x] T004 Add validation or documented maintenance rules for future Brooks runs.
  - Requirements: Requirement 2, Requirement 3, Requirement 4
  - Depends on: T001, T002, T003
  - Acceptance: Future Brooks skill runs have clear append/reconcile rules, and
    runtime validation is added only if D001 accepts it.
  - Evidence: Accepted D001 as Markdown-only first in `open-decisions.md`;
    retained register maintenance rules in `docs/reviews/brooks-lint/README.md`
    for stable IDs, repeated-run reconciliation, score-history handling,
    dismissal visibility, routing before closure, and verification before
    resolution. No runtime validation was added.

## Phase 3: Triage and Promotion

- [x] T005 Triage seed findings into accepted, deferred, dismissed, or resolved.
  - Requirements: Requirement 2, Requirement 5
  - Depends on: T003
  - Acceptance: Each seed finding has a triage state and rationale.
  - Evidence: Updated every seed finding in
    `docs/reviews/brooks-lint/README.md` from `needs-decision` to accepted,
    deferred, or dismissed with a concrete triage rationale.

- [x] T006 Route accepted and deferred findings to tasks, backlog, roadmap, or
      explicit no-action decisions.
  - Requirements: Requirement 2, Requirement 5
  - Depends on: T005
  - Acceptance: No tracked seed finding remains without a destination or
    rationale.
  - Evidence: Accepted D003 in `open-decisions.md`; routed drift findings to
    B016/R005, installer and distribution findings to B026, runtime
    modularization findings to B042, test fixture findings to B043, and
    subprocess-boundary findings to explicit no-action decisions in the
    register.

## Phase 4: Verification and Closure

- [x] T007 Validate lifecycle health and any runtime or plugin changes.
  - Requirements: Requirement 3, Requirement 4, Requirement 5
  - Depends on: T004, T006
  - Acceptance: Required validation commands pass and evidence is recorded.
  - Evidence: Full validation passed on 2026-06-11; see `verification.md`.

- [x] T008 Promote durable outcomes and prepare closure.
  - Requirements: Requirement 5
  - Depends on: T007
  - Acceptance: Register, backlog, roadmap, and closure targets are current.
  - Evidence: Durable outcomes were promoted to
    `docs/reviews/brooks-lint/README.md` and `docs/backlog/README.md`; roadmap
    links reuse existing R005. Closure log and archive index updates are
    prepared for the cleanup commit after the final spec commit.
