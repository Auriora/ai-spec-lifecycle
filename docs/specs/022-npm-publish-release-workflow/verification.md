---
title: npm publish and release workflow verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Verification

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_github_workflows`
- `SPEC_LIFECYCLE_PYTHON=python3 npm run validate`
- `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`
- Workflow syntax validation where available.
- `git diff --check`

## Quality Gates

- CI and release workflows are deterministic and repository-scoped.
- Publish cannot run without explicit trusted release conditions.
- Package artifacts and metadata are captured as release evidence.

## Evidence Log

- 2026-07-02 `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`
  passed with source, bundled plugin, and Claude plugin parity in sync before
  release workflow edits.
- 2026-07-04 `.github/workflows/cross-platform.yml` includes Python tests,
  Node tests, lifecycle scan, archive-index, prompts, package-contract,
  sync-guard, cross-platform smoke, `npm pack --dry-run --json`, and
  `git diff --check` on PR/main/manual matrix runs.
- 2026-07-04 `.github/workflows/release.yml` includes `v*` tag and manual
  dispatch triggers, `npm pack --json`, `npm-pack.json`,
  `release-summary.md`, `actions/upload-artifact@v4`, `workflow_dispatch`
  `publish=true`, `NPM_TOKEN`, existing-version `npm view`, `npm publish
  --access public`, and post-publish `npm view`.
- 2026-07-04 `docs/reference/spec-lifecycle-manager-mcp-install.md` and
  `docs/reference/spec-lifecycle-runtime.md` describe release triggers,
  artifact evidence, publish-disabled behavior, publish gates, rollback,
  republish, and post-publish verification guidance.
- 2026-07-04 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_github_workflows`
  ran 2 tests successfully.
- 2026-07-04 `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` ran 167 Python
  tests, 2 Node tests, lifecycle scan, archive-index validation, prompt
  validation, package-contract validation, sync-guard,
  `npm pack --dry-run --json`, and `git diff --check`.
- 2026-07-04 `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/022-npm-publish-release-workflow`
  reported zero diagnostics.
- 2026-07-04 local-checker waiver recorded because `actionlint` was
  unavailable. `tests/runtime/test_github_workflows.py` covers required
  workflow commands, artifact generation, publish-disabled behavior, publish
  gate, and post-publish metadata verification; GitHub Actions will provide
  authoritative workflow syntax validation on push.

## Residual Risks

- Actual npm publish and remote `npx` install verification require configured
  npm organization access and GitHub Actions secrets or trusted publishing.
- Current registry status remains `pack-ready-not-published` until a maintainer
  runs the manual publish gate with `NPM_TOKEN`.
