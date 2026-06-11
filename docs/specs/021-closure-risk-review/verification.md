---
title: Closure risk review verification
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
- `git diff --check`

## Quality Gates

- Risk classifier is deterministic and advisory.
- Findings cite source artifacts or blind spots.
- Closure risk complements, not replaces, closure-check.

## Evidence Log

- Pending.

## Residual Risks

- Human judgment remains required for semantic closure decisions.
