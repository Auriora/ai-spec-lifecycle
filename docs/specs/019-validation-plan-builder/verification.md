---
title: Validation plan builder verification
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
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5`
- `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`
- `git diff --check`

## Quality Gates

- Planner is read-only and deterministic.
- MCP schema and output are documented and tested.
- Bundled plugin copies match source.

## Evidence Log

- Pending.

## Residual Risks

- Project-specific validation profiles remain future work.
