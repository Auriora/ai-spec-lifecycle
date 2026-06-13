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

- [x] T001 Add closure risk runtime helper.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Helper aggregates closure, promotion, validation, evidence, decision, stale-active-doc, and historical-recoverability signals into risk findings.
  - Evidence: skills/spec-lifecycle-manager/scripts/spec_runtime.py CLI smoke returned risk_level=high, findings=8, blind_spots=0, advisory=true, mutates_files=false for the selected spec package.
  - Status: Runtime helper and CLI aggregate closure, promotion, validation, evidence, decision, active-doc, and archive recovery signals.
- [x] T002 Expose closure risk through MCP.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: `closure_risk_review` appears in `tools/list` and returns normalized structured output.
  - Evidence: skills/spec-lifecycle-manager/scripts/spec_mcp_server.py MCP smoke printed tool=True and payload high True False True for tool_definitions, call_tool, advisory, mutates_files, and signals checks.
  - Status: MCP tool registration and dispatch are implemented.
- [x] T003 Add closure risk tests.
  - Depends on: T001, T002
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover low-risk closure, weak evidence, missing durable promotion, stale active documentation, Git-history recoverability, and blind spots.
  - Evidence: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server ran 111 tests OK.
  - Status: Runtime and MCP coverage exercise risk levels, findings, blind spots, recovery signals, and structured output.
- [x] T004 Document closure risk review.
  - Depends on: T003
  - Files: `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Docs define inputs, risk levels, findings, blind spots, and limitations.
  - Evidence: Updated docs/reference/spec-lifecycle-runtime.md with closure risk CLI/MCP inputs, risk levels, findings, blind spots, read-only behavior, and limitations.
  - Status: Runtime reference documents the new advisory payload and constraints.
- [x] T005 Mirror bundles and validate.
  - Depends on: T004
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Full validation and parity checks pass.
  - Evidence: Full validation passed: unittest 133 tests OK; scan, archive-index, prompts, package-contract, sync-guard, and git diff --check returned zero errors.
  - Status: Source, bundled plugin, Claude plugin, and installed cache parity checks pass after package install.
