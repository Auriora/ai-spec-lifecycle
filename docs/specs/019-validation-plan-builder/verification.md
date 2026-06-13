---
title: Validation plan builder verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Verification

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5`
- `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`
- `git diff --check`

## Quality Gates

- Planner is read-only and deterministic.
- Documentation-only changes classify unrelated code/runtime checks as
  `not_applicable`, not missing validation.
- Applicable checks that did not run are classified as `not_run` with blocker
  and residual-risk context.
- MCP schema and output are documented and tested.
- Bundled plugin copies match source.

## Evidence Log

- T001: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed; `spec_runtime.py validation-plan` returned required planned checks and a validation contract for T001; `package-contract`, `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`, `scan`, `archive-index`, `prompts`, and `git diff --check` passed. `sync-guard` source/bundle parity passed and reported installed cache drift for the later bundle/install validation slice.
- T002: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server` passed with `validation_plan` exposed in `tools/list` and `tools/call` returning the normalized runtime payload.
- T003: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime` and `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server` passed with coverage for file classification, package/spec/history/prompt/doc-only/baseline planning, skipped-noise prevention, `not_run`, validation-contract gaps, planned-versus-executed state, and MCP schema/call output.
- T004: `lint_doc docs/reference/spec-lifecycle-runtime.md`, `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/019-validation-plan-builder`, and `git diff --check` passed after documenting command/tool inputs, output fields, contract fields, validation state semantics, and read-only behavior.
- T005: Source changes were mirrored into Codex and Claude plugin bundles. `scripts/install-spec-lifecycle-manager-package.sh` refreshed the installed cache, then `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`, `scan .`, `archive-index .`, `prompts .`, `package-contract .`, `sync-guard . --commits 5`, `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`, and `git diff --check` passed.

## Residual Risks

- Project-specific validation profiles remain future work.
