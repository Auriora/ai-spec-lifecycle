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

- [x] T001 Add runtime validation plan helper.
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Helper returns deterministic plan items from changed files and optional task context, including `not_applicable` versus `not_run` classification, planned/executed/blocked/inspection-only validation state, and a validation contract when task evidence can support one.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed; `spec_runtime.py validation-plan` returned required planned checks and contract for T001; `package-contract`, `npm pack --dry-run --json`, `scan`, `archive-index`, `prompts`, and `git diff --check` passed. `sync-guard` source/bundle parity passed with installed cache drift left for the bundle/install validation slice.

- [x] T002 Expose validation planning through MCP.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: `tools/list` exposes `validation_plan`; `tools/call` returns normalized structured content.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server` passed with `validation_plan` listed in MCP schema and `tools/call` output matching the normalized runtime payload.

- [x] T003 Add tests for planner behavior.
  - Depends on: T001, T002
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover file classification, package changes, spec changes, documentation-only changes, skipped-noise prevention, validation-contract gaps, planned-versus-executed validation state, and MCP schema/call output.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime` and `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server` passed with runtime coverage for file groups, package/spec/history/prompt/doc-only/baseline planning, `not_run`, contract gaps, executed evidence, and MCP schema/call parity.

- [x] T004 Document the validation planner.
  - Depends on: T003
  - Files: `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Runtime docs describe command/tool inputs, output fields, validation contract fields, validation state semantics, and read-only behavior.
  - Evidence: `lint_doc docs/reference/spec-lifecycle-runtime.md`, `spec_runtime.py lint docs/specs/019-validation-plan-builder`, and `git diff --check` passed after documenting the CLI/MCP inputs, output fields, validation contract, state semantics, docs-only behavior, and read-only boundary.

- [x] T005 Mirror bundles and validate.
  - Depends on: T004
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Source, Codex bundle, Claude bundle, package contract, sync guard, full tests, scan, archive index, prompts, and whitespace checks pass.
  - Evidence: Source changes were mirrored into Codex and Claude plugin bundles; `scripts/install-spec-lifecycle-manager-package.sh` refreshed the installed cache; `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`, `scan .`, `archive-index .`, `prompts .`, `package-contract .`, `sync-guard . --commits 5`, `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`, and `git diff --check` passed.
