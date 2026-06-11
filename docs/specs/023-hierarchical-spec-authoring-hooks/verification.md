---
title: Hierarchical spec authoring hooks verification
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
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract --repo-root .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard --repo-root .`
- `npm pack --dry-run --json`
- `git diff --check`

## Quality Gates

- Runtime hook tests prove ordinary spec-file writes do not dump unrelated
  package-wide task evidence diagnostics.
- Wrapper tests prove `PostToolUse` output includes concise next-action
  guidance and relevant helper surfaces.
- Explicit validation, resume, and closure paths still expose full package
  health when requested.
- Bundle parity checks pass before closure.

## Evidence Log

- T001: `docs/backlog/README.md` marks B046 active and
  `docs/specs/023-hierarchical-spec-authoring-hooks/` defines this package.
- T002: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime`
  passed with 52 tests after adding `spec_authoring_context`.
- T003: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime`
  passed with 54 tests after routing `spec-file-changed` through authoring
  context.
- T004: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_codex_spec_lifecycle_hook`
  passed with 6 tests after adding concise authoring guidance formatting.
- T005: Runtime and wrapper coverage is present in
  `tests/runtime/test_spec_runtime.py` and
  `tests/runtime/test_codex_spec_lifecycle_hook.py`; the focused suites above
  passed.
- T006: `docs/reference/spec-lifecycle-runtime.md` documents the
  hierarchy-aware `spec-file-changed` behavior and Codex wrapper next-action
  guidance; `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
  'test_*.py'` passed with 94 tests.
- T007: `scripts/install-spec-lifecycle-manager-package.sh` installed the
  bundled plugin, then `PYTHONDONTWRITEBYTECODE=1
  skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` passed
  with source, bundled plugin, Claude plugin, and installed cache in sync.

## Residual Risks

- Hook payloads may not include enough diff detail to isolate changed task IDs.
  If so, implementation must make fallback scope explicit and avoid noisy
  package-wide output during ordinary authoring.
