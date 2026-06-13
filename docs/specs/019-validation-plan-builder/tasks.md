---
title: Validation plan builder tasks
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

- [ ] T001 Add runtime validation plan helper.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Helper returns deterministic plan items from changed files and optional task context, including `not_applicable` versus `not_run` classification, planned/executed/blocked/inspection-only validation state, and a validation contract when task evidence can support one.
  - Evidence: Pending.

- [ ] T002 Expose validation planning through MCP.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: `tools/list` exposes `validation_plan`; `tools/call` returns normalized structured content.
  - Evidence: Pending.

- [ ] T003 Add tests for planner behavior.
  - Depends on: T001, T002
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover file classification, package changes, spec changes, documentation-only changes, skipped-noise prevention, validation-contract gaps, planned-versus-executed validation state, and MCP schema/call output.
  - Evidence: Pending.

- [ ] T004 Document the validation planner.
  - Depends on: T003
  - Files: `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Runtime docs describe command/tool inputs, output fields, validation contract fields, validation state semantics, and read-only behavior.
  - Evidence: Pending.

- [ ] T005 Mirror bundles and validate.
  - Depends on: T004
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Source, Codex bundle, Claude bundle, package contract, sync guard, full tests, scan, archive index, prompts, and whitespace checks pass.
  - Evidence: Pending.
