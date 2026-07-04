---
title: npm publish and release workflow tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003 -> T004 -> T005 -> T006

## Tasks

- [x] T001 Add backlog and roadmap release workflow framing.
  - Files: `docs/backlog/README.md`, `docs/roadmap/README.md`
  - Acceptance: B044 and R009 identify npm publish/release workflow scope and dependency on B026.
  - Evidence: `docs/backlog/README.md` adds B044 and `docs/roadmap/README.md` adds R009.

- [x] T002 Add or extend CI validation workflow.
  - Depends on: T001
  - Files: `.github/workflows/cross-platform.yml`, optional `.github/workflows/ci.yml`
  - Acceptance: PR/main CI runs unit tests, scan, archive-index, prompts, package-contract, npm pack dry-run, and whitespace checks.
  - Evidence: Complete 2026-07-04. Extended
    `.github/workflows/cross-platform.yml` instead of adding `ci.yml` (OD-002)
    so the existing PR/main/manual matrix now runs Python tests, Node tests,
    lifecycle scan, archive-index validation, prompt validation,
    package-contract, sync-guard, cross-platform smoke,
    `npm pack --dry-run --json`, and `git diff --check`.

- [x] T003 Add release artifact workflow.
  - Depends on: T002
  - Files: `.github/workflows/release.yml`
  - Acceptance: Release workflow builds npm tarball, captures pack metadata, and uploads artifacts/release assets.
  - Evidence: Complete 2026-07-04. Added `.github/workflows/release.yml` with
    `v*` tag and manual dispatch triggers. The workflow validates the package
    candidate, runs `npm pack --json`, writes `npm-pack.json` and
    `release-summary.md`, and uploads the tarball plus metadata with
    `actions/upload-artifact@v4`.

- [x] T004 Add guarded npm publish step.
  - Depends on: T003
  - Files: `.github/workflows/release.yml`, `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - Acceptance: Publish runs only on trusted release trigger with configured credentials or trusted publishing; otherwise it exits after artifact generation with clear status.
  - Evidence: Complete 2026-07-04. Release workflow uses explicit
    `workflow_dispatch` `publish=true` plus repository secret `NPM_TOKEN`
    before running `npm publish --access public`. When the publish gate is
    closed, the workflow intentionally stops after artifact generation with a
    publish-disabled status. The workflow checks `npm view` before publish and
    refuses to overwrite an existing version. OD-001 resolved to `NPM_TOKEN`.

- [x] T005 Add release documentation and verification.
  - Depends on: T004
  - Files: `docs/reference/spec-lifecycle-manager-mcp-install.md`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Docs describe release triggers, install verification, rollback, and residual risks.
  - Evidence: Complete 2026-07-04. Updated
    `docs/reference/spec-lifecycle-manager-mcp-install.md` and
    `docs/reference/spec-lifecycle-runtime.md` with CI coverage, release
    triggers, artifact metadata, guarded publish behavior, publish-disabled
    status, npm metadata verification, rollback, and republish guidance.

- [x] T006 Validate workflow and package behavior.
  - Depends on: T005
  - Files: `.github/workflows/`, `tests/runtime/`
  - Acceptance: T006.1-T006.4 are complete with evidence.
  - Evidence: Complete 2026-07-04. Focused workflow regression tests,
    Spec 022 lint, and `SPEC_LIFECYCLE_PYTHON=python3 npm run validate`
    passed after workflow and docs changes. `actionlint` was not installed
    locally, so workflow syntax validation is covered by text-level regression
    tests plus an explicit local-checker waiver in `verification.md`.
  - [x] T006.1 Validate current package contract baseline.
    - Acceptance: Current package contract passes before release workflow edits.
    - Evidence: 2026-07-02 `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` passed.
  - [x] T006.2 Run full local lifecycle validation after workflow changes.
    - Acceptance: Full validation plan in `verification.md` passes or records explicit waivers.
    - Evidence: 2026-07-04 `SPEC_LIFECYCLE_PYTHON=python3 npm run validate`
      passed, including Python tests, Node tests, lifecycle scan,
      archive-index validation, prompt validation, package-contract,
      sync-guard, `npm pack --dry-run --json`, and `git diff --check`.
  - [x] T006.3 Validate workflow syntax or record local-checker waiver.
    - Acceptance: Workflow syntax is checked with an available local tool or a documented waiver explains why no local checker was available.
    - Evidence: 2026-07-04 local-checker waiver recorded because `actionlint`
      was unavailable. Added `tests/runtime/test_github_workflows.py` to assert
      required CI commands, release artifact generation, publish-disabled path,
      `NPM_TOKEN` gate, existing-version guard, `npm publish`, and post-publish
      `npm view` verification are present.
  - [x] T006.4 Record release artifact and publish-gate evidence.
    - Acceptance: Release artifact metadata and publish-gate behavior are captured in `verification.md`.
    - Evidence: 2026-07-04 `.github/workflows/release.yml` captures
      `npm-pack.json`, `release-summary.md`, tarball filename, integrity,
      shasum, source commit, publish-requested state, npm-token state, and the
      publish-disabled status when the publish gate is closed.
