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

- [x] T001 Add evidence quality runtime helper.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Helper returns task evidence records, diagnostics, and summary counts for concrete, vague, missing, waived, deferred, not-applicable, and not-run evidence.
  - Evidence: Implemented CLI helper: PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py evidence-quality docs/specs/020-evidence-quality-check returned structured records, diagnostics, summary counts, advisory=true, mutates_files=false.
  - Status: Runtime helper and CLI command implemented; verification log cleanup continues in later tasks.
- [x] T002 Expose evidence quality through MCP.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: `evidence_quality_check` appears in `tools/list` and returns normalized structured output.
  - Evidence: MCP smoke check: PYTHONDONTWRITEBYTECODE=1 python3 -c import spec_mcp_server verified evidence_quality_check in tool_definitions and call_tool returned advisory=True, mutates_files=False, summary present.
  - Status: MCP tool schema and dispatch now delegate to runtime evidence_quality_check.
- [x] T003 Add runtime and MCP tests.
  - Depends on: T001, T002
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover concrete, vague, missing, waived, deferred, documentation-only not-applicable, and unsupported not-run evidence.
  - Evidence: Added focused tests in tests/runtime/test_spec_runtime.py and tests/runtime/test_spec_mcp_server.py; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server ran 106 tests OK.
  - Status: Runtime classifier, CLI JSON output, MCP tool listing, and MCP structured dispatch are covered.
- [x] T004 Document evidence quality checks.
  - Depends on: T003
  - Files: `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Docs describe read-only behavior, classifications, and limitations.
  - Evidence: Updated docs/reference/spec-lifecycle-runtime.md with the evidence-quality CLI command, MCP evidence_quality_check tool, payload shape, classification rules, read-only advisory behavior, and not-applicable limitation.
  - Status: Runtime reference documents evidence quality behavior and limitations.
- [x] T005 Mirror bundles and validate.
  - Depends on: T004
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Source/bundle/cache parity and full validation pass.
  - Evidence: Synced source skill to plugin and Claude bundles with rsync; refreshed local plugin cache via scripts/install-spec-lifecycle-manager-package.sh; validation passed: full unittest suite ran 128 tests OK, scan pass, archive-index pass, prompts pass, package-contract pass, sync-guard pass, git diff --check pass.
  - Status: Bundles and installed cache are in sync; full validation is clean.
