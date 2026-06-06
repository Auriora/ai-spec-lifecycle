---
title: Codex hook dogfood tasks
doc_type: spec
artifact_type: tasks
status: archived
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

- [x] T002 Record representative hook evidence.
  - Depends on: T001
  - Files: `docs/specs/010-codex-hook-dogfood/verification.md`,
    `~/.codex/hooks.json`
  - Acceptance: Evidence covers quiet pass, useful finding, and template or
    no-target behavior.
  - Evidence: Representative hook payloads recorded in `verification.md`:
    quiet pass, useful finding, and no-target quiet behavior.

## Phase 2: Decision

- [x] T003 Decide hook policy.
  - Depends on: T002
  - Files: `docs/specs/010-codex-hook-dogfood/verification.md`,
    `docs/backlog/README.md`
  - Acceptance: Keep/refine/expand/remove/defer decision is recorded; any
    follow-up is routed.
  - Evidence: Policy decision recorded in `verification.md`: keep advisory
    hook globally enabled; do not promote blocking behavior.

- [x] T004 Validate and close or defer follow-up.
  - Depends on: T003
  - Files: `docs/specs/010-codex-hook-dogfood/verification.md`
  - Acceptance: Tests, spec lint, closure-check, and diff check are recorded.
  - Evidence: Focused hook tests, full regression tests, spec lint,
    closure-check, and diff check recorded in `verification.md`.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Traceability: traceability.md
- Verification: verification.md
