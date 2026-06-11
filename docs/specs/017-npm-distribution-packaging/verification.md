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
| Claude plugin shape | Claude plugin manifest, MCP config, hooks, skill, and runtime scripts exist and validate. | Package tests and npm pack dry-run. |
| Source parity | Source skill and bundled plugin skill are in sync. | Package-contract and sync-guard commands. |
| Documentation promotion | Runtime and install docs explain local/npm boundary and Docker/GHCR deferral. | Task T005 evidence. |

## Evidence Log

| Check | Result | Evidence |
| --- | --- | --- |
| Focused runtime/package tests | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_plugin_package` passed 53 tests. |
| Package contract command | Pass | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` returned status `pass`, npm package `@auriora/ai-spec-lifecycle`, 0 errors, and 0 warnings. |
| npm pack dry-run | Pass | `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` returned `auriora-ai-spec-lifecycle-0.1.0-codex.20260606221001.tgz`, 110 entries, package size about 118 KB, and included package metadata, installer bin, existing installer script, Codex plugin bundle, and Claude plugin wrapper without bytecode artifacts. |
| Sync guard command | Pass with install advisory | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5` returned source/bundle `in_sync` and installed cache drift pending reinstall. |
| Full unittest suite | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed 78 tests. |
| Spec lint | Pass | MCP `lint_spec_package` returned 0 errors and 0 warnings after the Claude plugin packaging update. |
| Traceability preflight | Pass | MCP `active_spec_preflight` for T006 returned status `ready` with no traceability gaps. |
| Closure check | Pass | MCP `closure_check` returned ready with no blockers and 0 lint diagnostics after T008 evidence was recorded. |
| Archive index | Pass | MCP `archive_index` returned 0 diagnostics. |
| Prompt validation | Pass | MCP `prompts_validate` returned 0 diagnostics. |
| Whitespace check | Pass | `git diff --check` returned no whitespace findings. |
| Claude plugin focused tests | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_plugin_package` passed 8 tests, including Claude manifest, MCP config, hook config, skill parity, and npm payload assertions. |
| Claude plugin package contract | Pass | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` returned status `pass`, 0 errors, 0 warnings, and confirmed required Claude plugin paths. |
| Claude plugin package payload | Pass | `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` returned `auriora-ai-spec-lifecycle-0.1.0-codex.20260606221001.tgz`, 110 entries, package size about 116 KB, and included the Claude plugin manifest, `.mcp.json`, hooks, README, skill, and runtime scripts. |
| Full unittest suite after Claude plugin | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed 79 tests. |
| Sync guard after Claude plugin | Pass with install advisory | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5` reported source/bundle `in_sync` and installed cache drift pending reinstall. |
| Review packet mapping focused tests | Pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server` passed 64 tests, including implementation aliases, generic fallback, and MCP schema publication. |
| Review packet implementation alias CLI | Pass | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py review-packet docs/specs/017-npm-distribution-packaging --review-type implementation-readiness --model-class coding` returned `review_type` `implementation_review` and preserved `requested_review_type` `implementation-readiness`. |
| Review packet generic fallback CLI | Pass | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py review-packet docs/specs/017-npm-distribution-packaging --review-type release-polish --model-class coding` returned `review_type` `generic_review` and preserved `requested_review_type` `release-polish`. |
| Full unittest suite after review mapping | Pass | `find . -type d -name __pycache__ -prune -exec rm -rf {} + && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed 83 tests. |
| Package contract after review mapping | Pass | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` returned status `pass`, source/bundle parity `in_sync`, 0 errors, and 0 warnings. |
| Spec closure after review mapping | Pass | MCP `lint_spec_package` returned 0 diagnostics and MCP `closure_check` returned ready with no blockers after T009 evidence was recorded. |
| Installed cache after review mapping | Pass | `scripts/install-spec-lifecycle-manager-package.sh` installed the plugin to `~/.codex/plugins/cache/auriora-local/spec-lifecycle-manager/0.1.0+codex.20260606221001`; `sync-guard . --commits 5` returned source/bundle/cache `in_sync` with 0 warnings and 0 errors. |

## Residual Risks

- npm publishing remains future work.
- Contract validation and `npm pack --dry-run` cannot prove registry
  authentication, publish, or remote `npx` install behavior until a
  publish/install slice exists.
