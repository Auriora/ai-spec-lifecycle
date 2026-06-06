---
title: Operating model governance adoption tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004 -> T005 -> T006
```

## Phase 1: Spec And Governance

- [x] T001 Create focused governance adoption spec.
  - Depends on: none
  - Files: `docs/specs/012-operating-model-governance-adoption/`
  - Acceptance: Spec package defines requirements, design, tasks,
    traceability, and verification for R003/B005.
  - Evidence: Spec package created from roadmap/backlog sources.

- [x] T002 Adopt selected operating-model rules in governance.
  - Depends on: T001
  - Files: `docs/governance/constitution.md`
  - Acceptance: Constitution includes enforceable rules for spec context, risk
    gates, bounded parallel work, evidence, and durable promotion.
  - Evidence: Constitution updated; flexible workflow mechanics left in design
    guidance.

- [x] T003 Record operating-model adoption boundary.
  - Depends on: T002
  - Files: `docs/design/coding-agent-operating-model.md`
  - Acceptance: Design doc explains which rules became governance and what
    remains guidance.
  - Evidence: Operating-model dogfood decision updated.

## Phase 2: Planning And Validation

- [x] T004 Update roadmap and backlog status.
  - Depends on: T003
  - Files: `docs/roadmap/README.md`, `docs/backlog/README.md`
  - Acceptance: R003 and B005 are marked complete with evidence.
  - Evidence: Planning docs updated.

- [x] T005 Validate the governance adoption.
  - Depends on: T004
  - Files: `docs/specs/012-operating-model-governance-adoption/verification.md`
  - Acceptance: Lint, scan, archive-index validation, full tests, and diff
    hygiene pass or record residual risk.
  - Evidence: Verification commands recorded.

- [ ] T006 Close spec 012.
  - Depends on: T005
  - Files: `docs/specs/012-operating-model-governance-adoption/`,
    `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md`
  - Acceptance: Final spec commit and cleanup commit are recorded; spec is
    archived as retained history.
  - Evidence: Pending.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
