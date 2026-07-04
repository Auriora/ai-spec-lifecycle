---
title: Developer CLI workflow tools verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Verification

## Quality Gates

| Gate | Command or method | Required before | Status | Evidence |
|------|-------------------|-----------------|--------|----------|
| Spec package lint | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/025-dev-cli-workflow-tools` | implementation | pass | 2026-07-04: MCP `lint_spec_package` returned 0 diagnostics. |
| CLI unit tests | `npm run test:devcli` | task completion | pass | 2026-07-04: 13 tests passed for runner, repo utilities, command groups, and command plan builders. |
| Full unit suite | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | validation | pass | 2026-07-04: 165 tests passed. |
| Lifecycle scan | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | validation | pass | 2026-07-04: 3 active specs, all pass. |
| Archive index | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | validation | pass | 2026-07-04: 0 diagnostics. |
| Prompt validation | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts` | validation | pass | 2026-07-04: 0 diagnostics. |
| Package contract | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | validation | pass | 2026-07-04: status pass; 0 diagnostics. |
| Sync guard | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` | validation | warn accepted | 2026-07-04: source/bundle and source/Claude parity passed; installed plugin cache drift warning remains until local install/reload. |
| npm package dry-run | `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` | validation | pass | 2026-07-04: tarball dry-run completed and listed 123 payload entries. |
| Whitespace | `git diff --check` | validation | pass | 2026-07-04: no whitespace errors. |
| Repository validation bundle | `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` | validation | pass | 2026-07-04: Python suite, Node runtime tests, package-contract, and npm dry-run passed. |

## Evidence Log

| Date | Task(s) | Evidence | Result | Notes |
|------|---------|----------|--------|-------|
| 2026-07-04 | T001, T002 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_devcli_runner` | pass | 6 tests covered command-plan rendering, dry-run no-exec behavior, stop-on-failure, root discovery, repo-relative paths, out-of-repo paths, and shell quoting. |
| 2026-07-04 | T001, T002 | MCP `lint_spec_package`; `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts`; `git diff --check` | pass | Spec lint returned 0 diagnostics; full unittest suite passed 158 tests; scan reported 3 active specs all pass; archive-index and prompts returned 0 diagnostics; whitespace check passed. |
| 2026-07-04 | T003-T010 | `npm run test:devcli`; `PYTHONPATH=tools/devcli/src python3 -m auriora_dev.cli check --repo-root . --dry-run`; `PYTHONPATH=tools/devcli/src python3 -m auriora_dev.cli release preflight --repo-root . --dry-run --allow-dirty`; `SPEC_LIFECYCLE_PYTHON=python3 PYTHONPATH=tools/devcli/src python3 -m auriora_dev.cli package install-local --repo-root . --dry-run --skip-plugin-add` | pass | CLI tests passed 13 tests; validation and release-preflight dry-runs rendered expected plans; installer dry-run passed when Python interpreter was supplied explicitly. |
| 2026-07-04 | T011 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .`; `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`; `git diff --check` | pass with accepted warning | Full unittest suite passed 165 tests; package-contract passed; npm dry-run completed; whitespace passed; sync-guard source/bundle parity passed with installed-cache drift warning only. |
| 2026-07-04 | T011 | `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` | pass | Repository validation bundle passed. Plain `npm run validate` in this sandbox hit Node `spawnSync python3 EPERM` during interpreter probing, so the documented interpreter override was used. |

## Coverage Map

| Requirement | Validation signal |
|-------------|-------------------|
| Requirement 1 | CLI metadata/help tests |
| Requirement 2 | Runner dry-run/failure tests |
| Requirement 3 | `slc check` command plan tests and full validation run |
| Requirement 4 | Bundle sync tests and package-contract/sync-guard evidence |
| Requirement 5 | Package command tests and installer dry-run evidence |
| Requirement 6 | Mocked Codex unavailable/available tests |
| Requirement 7 | Spec wrapper tests invoking `spec_runtime.py` commands |
| Requirement 8 | Release preflight tests proving no push/tag/publish command is run |
| Requirement 9 | Documentation review and durable-doc promotion map |
| Requirement 10 | CLI test command and CI-safe validation evidence |

## Residual Risks

- CLI implementation may expose too many convenience commands if scope is not
  kept to high-friction workflows.
- Real local install verification depends on the user's Codex environment. A
  dry-run install passes with `SPEC_LIFECYCLE_PYTHON=python3`; `sync-guard`
  still warns that the currently installed plugin cache differs from the
  bundled plugin until a real local install and Codex reload are performed.
- Release-preflight behavior overlaps active spec `022`; this spec must avoid
  owning actual publish automation.
- Test framework choice may add a new development dependency under
  `tools/devcli`.

## Release Or Closure Readiness

- **Ready for implementation:** complete for Spec 025.
- **Ready for release:** no.
- **Ready for closure:** yes. `closure_check` reports ready with no blockers
  and closure-risk review reports low risk with no findings. Final package
  removal still requires the normal final spec commit, closure-log entry,
  archive-index entry, and cleanup commit workflow.
