---
title: GHCR distribution packaging verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-11
---

# GHCR Distribution Packaging Verification

## Validation Plan

- Run focused package contract tests.
- Run `spec_runtime.py package-contract .`.
- Run `spec_runtime.py sync-guard .`.
- Run the full unittest suite.
- Run spec lint and closure readiness before closing.
- Run `git diff --check`.

## Quality Gates

| Gate | Requirement | Evidence |
| --- | --- | --- |
| Contract present | `ghcr-package.json` and Containerfile exist and validate. | Package-contract command and tests. |
| Package shape | Required plugin, manifest, MCP, hook, prompt, script, and reference paths exist. | Package-contract command. |
| Source parity | Source skill and bundled plugin skill are in sync. | Package-contract and sync-guard commands. |
| Documentation promotion | Runtime and install docs explain local/GHCR boundary. | Task T004 evidence. |

## Evidence Log

| Check | Result | Evidence |
| --- | --- | --- |
| Focused runtime tests | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_plugin_package` passed 50 tests. |
| Package contract command | Pass | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` returned status `pass`, 0 errors, 0 warnings, and all required paths present. |
| Sync guard command | Pass with install advisory | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5` returned source/bundle `in_sync`, commit evidence `ok`, and installed cache drift pending reinstall. |
| Full unittest suite | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed 76 tests. |
| Spec lint | Pass | MCP `lint_spec_package` returned 0 errors and 0 warnings. |
| Traceability preflight | Pass | MCP `active_spec_preflight` for T005 returned status `ready` with no gaps after explicit requirement references were recorded. |
| Closure check | Pass | MCP `closure_check` and CLI `spec_runtime.py closure-check docs/specs/017-ghcr-distribution-packaging` returned ready with no blockers and 0 lint diagnostics. |
| Archive index | Pass | MCP `archive_index` and CLI `spec_runtime.py archive-index .` returned 0 diagnostics. |
| Prompt validation | Pass | MCP `prompts_validate` and CLI `spec_runtime.py prompts .` returned 0 diagnostics. |
| Whitespace check | Pass | `git diff --check` returned no whitespace findings. |

## Residual Risks

- GHCR publishing remains future work.
- Contract validation cannot prove registry authentication, pull, or install
  behavior until a publish/install slice exists.
