---
title: Closure risk review tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003 -> T004 -> T005

## Tasks

- [ ] T001 Add closure risk runtime helper.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Helper aggregates closure, promotion, validation, evidence, decision, stale-active-doc, and historical-recoverability signals into risk findings.
  - Evidence: Pending.

- [ ] T002 Expose closure risk through MCP.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: `closure_risk_review` appears in `tools/list` and returns normalized structured output.
  - Evidence: Pending.

- [ ] T003 Add closure risk tests.
  - Depends on: T001, T002
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover low-risk closure, weak evidence, missing durable promotion, stale active documentation, Git-history recoverability, and blind spots.
  - Evidence: Pending.

- [ ] T004 Document closure risk review.
  - Depends on: T003
  - Files: `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Docs define inputs, risk levels, findings, blind spots, and limitations.
  - Evidence: Pending.

- [ ] T005 Mirror bundles and validate.
  - Depends on: T004
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Full validation and parity checks pass.
  - Evidence: Pending.
