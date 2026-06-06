---
title: Codex hook dogfood tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

**Input**: Installed Codex hook configuration, runtime hook wrapper, and
dogfood evidence from real or representative edits.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
```

## Phase 1: Dogfood Setup

- [x] T001 Create Codex hook dogfood spec.
  - Depends on: none
  - Files: `docs/specs/010-codex-hook-dogfood/`
  - Acceptance: Requirements, design, tasks, traceability, and verification
    exist for dogfood evaluation.
  - Evidence: Spec package created.

- [ ] T002 Record representative hook evidence.
  - Depends on: T001
  - Files: `docs/specs/010-codex-hook-dogfood/verification.md`,
    `~/.codex/hooks.json`
  - Acceptance: Evidence covers quiet pass, useful finding, and template or
    no-target behavior.
  - Evidence: Pending.

## Phase 2: Decision

- [ ] T003 Decide hook policy.
  - Depends on: T002
  - Files: `docs/specs/010-codex-hook-dogfood/verification.md`,
    `docs/backlog/README.md`
  - Acceptance: Keep/refine/expand/remove/defer decision is recorded; any
    follow-up is routed.
  - Evidence: Pending.

- [ ] T004 Validate and close or defer follow-up.
  - Depends on: T003
  - Files: `docs/specs/010-codex-hook-dogfood/verification.md`
  - Acceptance: Tests, spec lint, closure-check, and diff check are recorded.
  - Evidence: Pending.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Traceability: traceability.md
- Verification: verification.md
