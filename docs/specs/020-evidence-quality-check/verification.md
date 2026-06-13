---
title: Evidence quality check verification
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
- `git diff --check`

## Quality Gates

- Classifier is deterministic and advisory.
- Not-applicable validation is accepted only when validation-plan or task
  context supports the scope.
- Unsupported documentation-only skip claims are reported as not-run or weak
  evidence with residual risk.
- Diagnostics point to task IDs or verification sections.
- MCP output matches runtime output after normalization.

## Evidence Log

- Pending.

## Residual Risks

- Implementation-file inspection is intentionally deferred to B037.
