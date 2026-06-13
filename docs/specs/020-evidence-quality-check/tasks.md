---
title: Evidence quality check tasks
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

- [ ] T001 Add evidence quality runtime helper.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Helper returns task evidence records, diagnostics, and summary counts for concrete, vague, missing, waived, deferred, not-applicable, and not-run evidence.
  - Evidence: Pending.

- [ ] T002 Expose evidence quality through MCP.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: `evidence_quality_check` appears in `tools/list` and returns normalized structured output.
  - Evidence: Pending.

- [ ] T003 Add runtime and MCP tests.
  - Depends on: T001, T002
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover concrete, vague, missing, waived, deferred, documentation-only not-applicable, and unsupported not-run evidence.
  - Evidence: Pending.

- [ ] T004 Document evidence quality checks.
  - Depends on: T003
  - Files: `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Docs describe read-only behavior, classifications, and limitations.
  - Evidence: Pending.

- [ ] T005 Mirror bundles and validate.
  - Depends on: T004
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Source/bundle/cache parity and full validation pass.
  - Evidence: Pending.
