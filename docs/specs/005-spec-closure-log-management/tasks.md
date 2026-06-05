---
title: Spec closure log management tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Tasks

**Input**: `requirements.md`, `design.md`,
`docs/design/spec-lifecycle-management.md`, and
`skills/spec-lifecycle-manager/`.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
T004 -> T005
T004 -> T006
T005 + T006 -> T007
```

## Phase 1: Spec And Decision Baseline

- [x] T001 Create closure-log implementation spec.
  - Depends on: none
  - Files: `docs/specs/005-spec-closure-log-management/`
  - Acceptance: Requirements, design, and tasks describe Git-backed spec
    closure, closure-log roles, and implementation path.
  - Evidence: This spec package created.

- [x] T002 Decide default closure log path and document class.
  - Depends on: T001
  - Files: `docs/specs/005-spec-closure-log-management/design.md`,
    `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md`
  - Acceptance: Decision records whether the default is
    `docs/history/spec-closure-log.md`, `docs/changelog/spec-lifecycle.md`,
    or another path, and whether the template uses `doc_type: history` or a
    new durable class.
  - Evidence: Design records fallback default
    `docs/history/spec-closure-log.md` with `doc_type: history`; durable
    template README documents the class.

## Phase 2: Template And Skill Updates

- [x] T003 Add spec closure log durable template.
  - Depends on: T002
  - Files:
    `skills/spec-lifecycle-manager/references/durable-doc-templates/spec-closure-log.md`,
    `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md`
  - Acceptance: Template includes required closure fields, explains Git-backed
    archival, and distinguishes closure records from product changelogs.
  - Evidence: `spec-closure-log.md` durable template added with required
    closure fields, final spec commit guidance, closure actions, and changelog
    boundary; durable template README documents default path and class.

- [x] T004 Update skill close and promotion guidance.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/SKILL.md`,
    `skills/spec-lifecycle-manager/references/document-routing-and-expert-review.md`,
    `skills/spec-lifecycle-manager/references/durable-doc-templates/document-lifecycle.md`,
    `skills/spec-lifecycle-manager/references/spec-package/verification.md`
  - Acceptance: Close workflow requires a final spec commit before removal,
    updates the closure log, distinguishes remove/archive/retain actions, and
    records closure evidence.
  - Evidence: Skill close guidance now requires final spec commit before
    removal, closure log entry, cleanup action, and closure reporting;
    routing, lifecycle, and verification references include closure-log fields.

## Phase 3: Durable Docs And Validation

- [x] T005 Promote lifecycle design changes.
  - Depends on: T004
  - Files: `docs/design/spec-lifecycle-management.md`, `docs/README.md`
  - Acceptance: Durable docs describe the closure-log model, active index
    boundary, Git-backed archive, and changelog boundary.
  - Evidence: `docs/design/spec-lifecycle-management.md` describes fallback
    closure log path, `doc_type: history`, two-commit Git-backed archive flow,
    closure actions, active-index boundary, and changelog boundary; docs index
    notes closure-log discoverability.

- [x] T006 Add validation coverage.
  - Depends on: T004
  - Files: `docs/specs/002-spec-lifecycle-validation/requirements.md`,
    `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`,
    fixture docs as needed
  - Acceptance: Validation requirements and evidence cover closure-log
    template presence, final spec commit guidance, and active index cleanup.
  - Evidence: Validation requirements include closure-log static consistency;
    validation evidence records closure-log template and final spec commit
    guidance checks.

## Phase 4: Dogfood And Close

- [x] T007 Dogfood closure-log workflow on a completed spec.
  - Depends on: T005, T006
  - Files: `docs/specs/005-spec-closure-log-management/`,
    `docs/history/spec-closure-log.md`,
    `docs/specs/004-spec-management-mcp/`
  - Acceptance: A real or fixture close flow records final spec commit, closure
    action, durable destinations, verification summary, residual risks, and
    follow-up.
  - Evidence: Closure log entry for 004 records final spec commit `86687b6`,
    closure action `retained-as-history`, durable destinations, verification
    summary, residual risks, and follow-up; 004 frontmatter status changed to
    `archived`.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
