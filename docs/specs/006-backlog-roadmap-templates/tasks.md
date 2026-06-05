---
title: Backlog and roadmap templates tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Tasks

**Input**: `requirements.md`, `design.md`, `docs/backlog/README.md`,
`docs/design/spec-lifecycle-management.md`, and
`skills/spec-lifecycle-manager/`.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
T004 -> T005
T005 -> T006
T006 -> T007
```

## Phase 1: Spec Baseline

- [x] T001 Create backlog and roadmap template implementation spec.
  - Depends on: none
  - Files: `docs/specs/006-backlog-roadmap-templates/`
  - Acceptance: Requirements, design, tasks, traceability, and verification
    describe backlog/roadmap templates and deferred-work routing.
  - Evidence: Spec package created.

## Phase 2: Durable Templates

- [x] T002 Add backlog durable template.
  - Depends on: T001
  - Files:
    `skills/spec-lifecycle-manager/references/durable-doc-templates/backlog.md`
  - Acceptance: Template includes item fields, status guidance, promotion
    links, and maintenance rules.
  - Evidence: Backlog template added with required fields and routing notes.

- [x] T003 Add roadmap durable template.
  - Depends on: T002
  - Files:
    `skills/spec-lifecycle-manager/references/durable-doc-templates/roadmap.md`
  - Acceptance: Template includes horizons, dependencies, exit criteria,
    ownership, evidence, and review cadence.
  - Evidence: Roadmap template added with required fields and review guidance.

- [x] T004 Update durable template index and routing references.
  - Depends on: T003
  - Files:
    `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md`,
    `skills/spec-lifecycle-manager/references/document-routing-and-expert-review.md`
  - Acceptance: Backlog and roadmap templates are discoverable and routing
    guidance distinguishes them from specs, changelogs, and closure logs.
  - Evidence: Durable template README and routing reference updated.

## Phase 3: Skill And Durable Lifecycle Guidance

- [x] T005 Update skill deferred-work guidance.
  - Depends on: T004
  - Files: `skills/spec-lifecycle-manager/SKILL.md`
  - Acceptance: Promotion and closure guidance tells agents how to choose
    backlog, roadmap, issue tracker, or follow-up spec destinations.
  - Evidence: Skill promotion guidance includes deferred-work routing rules.

- [x] T006 Promote lifecycle docs and backlog item status.
  - Depends on: T005
  - Files: `docs/design/spec-lifecycle-management.md`, `docs/README.md`,
    `docs/backlog/README.md`
  - Acceptance: Durable docs describe backlog/roadmap roles, and B001 no
    longer appears as unpromoted work.
  - Evidence: Lifecycle docs and docs index updated; B001 marked promoted to
    spec 006 and implemented by this template update.

## Phase 4: Validation

- [x] T007 Validate and record evidence.
  - Depends on: T006
  - Files: `docs/specs/006-backlog-roadmap-templates/verification.md`
  - Acceptance: Spec lint, closure-check, runtime tests, and whitespace check
    pass or record explicit residual risk.
  - Evidence: Verification records passing lint, closure-check, unit tests,
    and `git diff --check`.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Traceability: traceability.md
- Verification: verification.md
