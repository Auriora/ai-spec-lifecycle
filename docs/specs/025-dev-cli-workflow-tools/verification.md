---
title: Developer CLI workflow tools verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-14
---

# Verification

## Quality Gates

| Gate | Command or method | Required before | Status | Evidence |
|------|-------------------|-----------------|--------|----------|
| Spec package lint | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/025-dev-cli-workflow-tools` | implementation | pending | |
| CLI unit tests | chosen CLI test command | task completion | pending | |
| Full unit suite | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | validation | pending | |
| Lifecycle scan | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | validation | pending | |
| Archive index | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | validation | pending | |
| Prompt validation | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts` | validation | pending | |
| Package contract | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | validation | pending | |
| Sync guard | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` | validation | pending | |
| npm package dry-run | `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` | validation | pending | |
| Whitespace | `git diff --check` | validation | pending | |

## Evidence Log

| Date | Task(s) | Evidence | Result | Notes |
|------|---------|----------|--------|-------|
| 2026-06-14 | spec creation | Spec package created from user request and Agent Workbench spec 028 pattern. | pending validation | Implementation not started. |

## Coverage Map

| Requirement | Validation signal |
|-------------|-------------------|
| R1 | CLI metadata/help tests |
| R2 | Runner dry-run/failure tests |
| R3 | `adl check` command plan tests and full validation run |
| R4 | Bundle sync tests and package-contract/sync-guard evidence |
| R5 | Package command tests and installer dry-run evidence |
| R6 | Mocked Codex unavailable/available tests |
| R7 | Spec wrapper tests invoking `spec_runtime.py` commands |
| R8 | Release preflight tests proving no push/tag/publish command is run |
| R9 | Documentation review and durable-doc promotion map |
| R10 | CLI test command and CI-safe validation evidence |

## Residual Risks

- CLI implementation may expose too many convenience commands if scope is not
  kept to high-friction workflows.
- Real local install verification depends on the user's Codex environment and
  should be recorded separately from dry-run tests.
- Release-preflight behavior overlaps active spec `022`; this spec must avoid
  owning actual publish automation.
- Test framework choice may add a new development dependency under
  `tools/devcli`.

## Release Or Closure Readiness

- **Ready for implementation:** no, until open decisions in `traceability.md`
  are resolved or explicitly scoped.
- **Ready for release:** no.
- **Ready for closure:** no.
