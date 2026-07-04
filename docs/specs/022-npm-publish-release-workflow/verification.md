---
title: npm publish and release workflow verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-07-02
---

# Verification

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`
- `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json`
- Workflow syntax validation where available.
- `git diff --check`

## Quality Gates

- CI and release workflows are deterministic and repository-scoped.
- Publish cannot run without explicit trusted release conditions.
- Package artifacts and metadata are captured as release evidence.

## Evidence Log

- 2026-07-02: Reconciliation found existing Spec 028/B026 package evidence:
  `.github/workflows/cross-platform.yml` runs PR/main/manual cross-platform
  tests, package-contract, cross-platform smoke, and `npm pack --dry-run`;
  package docs and manifests state `pack-ready-not-published`; local
  `package-contract` passed with source, bundled plugin, and Claude plugin
  parity in sync.
- 2026-07-02: Release workflow evidence remains pending: no
  `.github/workflows/release.yml` exists yet, no guarded npm publish path exists
  yet, and no automated release artifact upload/metadata capture has been
  recorded.

## Residual Risks

- Actual npm publish and remote `npx` install verification require configured
  npm organization access and GitHub Actions secrets or trusted publishing.
