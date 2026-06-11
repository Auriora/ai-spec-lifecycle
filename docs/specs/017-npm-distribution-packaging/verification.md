---
title: npm distribution packaging verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-11
---

# npm Distribution Packaging Verification

## Validation Plan

- Run focused package contract and plugin package tests.
- Run `spec_runtime.py package-contract .`.
- Run `npm pack --dry-run --json`.
- Run `spec_runtime.py sync-guard .`.
- Run the full unittest suite.
- Run spec lint and closure readiness before closing.
- Run `git diff --check`.

## Quality Gates

| Gate | Requirement | Evidence |
| --- | --- | --- |
| npm contract present | `package.json`, `npm-package.json`, and npm installer bin exist and validate. | Package-contract command and tests. |
| Package shape | Required plugin, manifest, MCP, hook, prompt, script, reference, npm, and installer paths exist. | Package-contract command and npm pack dry-run. |
| Source parity | Source skill and bundled plugin skill are in sync. | Package-contract and sync-guard commands. |
| Documentation promotion | Runtime and install docs explain local/npm boundary and Docker/GHCR deferral. | Task T005 evidence. |

## Evidence Log

| Check | Result | Evidence |
| --- | --- | --- |
| Focused runtime/package tests | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_plugin_package` passed 52 tests. |
| Package contract command | Pass | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` returned status `pass`, npm package `@auriora/spec-lifecycle-manager`, 0 errors, and 0 warnings. |
| npm pack dry-run | Pass | `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` returned `auriora-spec-lifecycle-manager-0.1.0-codex.20260606221001.tgz`, 59 entries, package size about 88 KB, and included package metadata, installer bin, existing installer script, and plugin bundle without bytecode artifacts. |
| Sync guard command | Pass with install advisory | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5` returned source/bundle `in_sync` and installed cache drift pending reinstall. |
| Full unittest suite | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed 78 tests. |
| Spec lint | Pass | MCP `lint_spec_package` returned 0 errors and 0 warnings. |
| Traceability preflight | Pass | MCP `active_spec_preflight` for T006 returned status `ready` with no traceability gaps. |
| Closure check | Pass | MCP `closure_check` returned ready with no blockers and 0 lint diagnostics after T006 evidence was recorded. |
| Archive index | Pass | MCP `archive_index` returned 0 diagnostics. |
| Prompt validation | Pass | MCP `prompts_validate` returned 0 diagnostics. |
| Whitespace check | Pass | `git diff --check` returned no whitespace findings. |

## Residual Risks

- npm publishing remains future work.
- Contract validation and `npm pack --dry-run` cannot prove registry
  authentication, publish, or remote `npx` install behavior until a
  publish/install slice exists.
