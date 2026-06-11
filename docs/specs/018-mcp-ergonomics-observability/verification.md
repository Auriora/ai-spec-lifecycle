---
title: MCP ergonomics and observability hardening verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Verification

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .`
- `git diff --check`

## Quality Gates

- Resolver statuses are structured and deterministic.
- MCP resource payloads remain repo-relative.
- Audit command is read-only.
- Codex and Claude bundled skill copies match source.

## Evidence Log

- 2026-06-11: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server tests.runtime.test_spec_plugin_package` passed, 77 tests.
- 2026-06-11: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed, 88 tests.
- 2026-06-11: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` passed with 2 active specs, both `health: pass`.
- 2026-06-11: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` passed with 0 diagnostics.
- 2026-06-11: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` passed with 0 diagnostics.
- 2026-06-11: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` passed with 0 diagnostics; source-to-Codex and source-to-Claude parity were `in_sync`.
- 2026-06-11: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5` completed and reported source-to-Codex and source-to-Claude parity `in_sync`; installed cache drift remains until install/reload.
- 2026-06-11: `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` passed and included both Codex and Claude plugin payloads.
- 2026-06-11: `git diff --check` passed.

## Residual Risks

- Existing running MCP sessions can still hold stale installed cache code until
  the client reloads.
- The local installed Codex plugin cache still differs from the bundled plugin
  until the package installer is run and the client reloads.
