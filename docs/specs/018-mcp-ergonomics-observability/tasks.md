---
title: MCP ergonomics and observability hardening tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003 -> T004

## Implementation

- [x] T001 Add structured spec reference resolution.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `tests/runtime/test_spec_mcp_server.py`, `tests/runtime/test_spec_runtime.py`
  - Acceptance: Active, archived, missing, and ambiguous references return structured status payloads.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server tests.runtime.test_spec_plugin_package` passed; full unittest discovery passed.

- [x] T002 Publish selector contracts and resource root metadata.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: `review_packet`, `agent_backed_tool`, and resource payload tests confirm published metadata and repo scoping.
  - Evidence: `tests.runtime.test_spec_mcp_server` passed; full unittest discovery passed.

- [x] T003 Add deterministic MCP audit summary.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: CLI/runtime and MCP tests summarize session file mentions and explicit errors without mutation.
  - Evidence: `tests.runtime.test_spec_runtime` and `tests.runtime.test_spec_mcp_server` passed; full unittest discovery passed.

- [x] T004 Extend package parity evidence.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/test_spec_plugin_package.py`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: `sync-guard` and `package-contract` report Claude parity alongside Codex bundle parity.
  - Evidence: `package-contract .` passed with `source_bundle_parity` and `source_claude_parity` both `in_sync`; `sync-guard . --commits 5` reported those source parity checks `in_sync` and correctly warned that the installed Codex cache is stale until install.

- [x] T005 Validate and mirror bundled plugin copies.
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Full runtime tests, scan, archive index, prompts validation, package contract, and whitespace checks pass.
  - Evidence: Full unittest discovery, `scan .`, `archive-index .`, `prompts .`, `package-contract .`, `npm pack --dry-run --json`, and `git diff --check` passed. `sync-guard . --commits 5` completed with an expected installed-cache drift warning because the package has not been installed after this implementation.
