---
title: npm publish and release workflow requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Requirements

## Durable Source Baseline

- B026 delivered a pack-ready npm package named `@auriora/ai-spec-lifecycle`.
- Install docs say npm publishing, registry authentication, and release
  automation remain future work.
- Package validation already includes `package-contract` and `npm pack
  --dry-run --json`.

## Goals

- Add GitHub Actions CI/CD for validation, packaging, release artifacts, and
  guarded npm publish.
- Support manual and tag-based release triggers.
- Keep publish credentials scoped to repository secrets or trusted publish
  configuration.
- Record release evidence and install verification.

## Non-Goals

- Do not publish automatically from arbitrary branches.
- Do not require Docker/GHCR.
- Do not store npm tokens in the repository.
- Do not implement semantic version policy beyond the package version source
  unless required by the workflow design.

## Requirements

### Requirement 1: CI Validation Workflow

**User Story:** As a maintainer, I want pull requests and main commits to run
the package validation suite, so that release candidates fail early.

#### Acceptance Criteria

1. GIVEN a PR or main commit, WHEN CI runs, THEN GitHub Actions SHALL run the
   full unit suite, scan, archive-index, prompts, package-contract, npm pack
   dry-run, and whitespace checks.
2. WHERE package or plugin files change, THE SYSTEM SHALL include sync guard or
   equivalent parity validation.
3. IF validation fails, THEN the workflow SHALL fail before publish or release.

### Requirement 2: Release Artifact Workflow

**User Story:** As a maintainer, I want release artifacts produced by CI, so
that package contents are reproducible and inspectable.

#### Acceptance Criteria

1. GIVEN a release dispatch or tag, WHEN the release workflow runs, THEN it
   SHALL build the npm tarball with `npm pack`.
2. The workflow SHALL upload the tarball and validation summary as artifacts or
   GitHub release assets.
3. The workflow SHALL record package name, version, tarball filename, shasum or
   integrity, and source commit.

### Requirement 3: Guarded npm Publish

**User Story:** As a maintainer, I want npm publish guarded by explicit release
conditions, so that accidental registry mutation is avoided.

#### Acceptance Criteria

1. GIVEN publish is requested, WHEN the workflow runs, THEN it SHALL require a
   trusted trigger such as a release tag or manual dispatch.
2. WHERE npm authentication is needed, THE SYSTEM SHALL use repository secrets
   or trusted publishing configuration, not committed credentials.
3. IF publish is disabled or credentials are absent, THEN the workflow SHALL
   stop after artifact generation with a clear status.

### Requirement 4: Post-Publish Verification

**User Story:** As a user, I want the published install path verified, so that
`npx @auriora/ai-spec-lifecycle install` is trustworthy.

#### Acceptance Criteria

1. AFTER publish, the workflow SHALL verify package metadata from npm or run a
   controlled install smoke test where credentials and network access permit.
2. The workflow SHALL document any verification skipped because publish was
   disabled or credentials were unavailable.
3. Release docs SHALL state install, rollback, and republish guidance.

## Correctness Properties

- CP-001: Release workflow SHALL not publish unless explicit publish gates are
  satisfied.
- CP-002: CI validation SHALL be reproducible from repository commands.
- CP-003: Published artifacts SHALL correspond to a recorded source commit and
  package version.

## Success Criteria

- `.github/workflows/` contains CI and release workflows.
- Runtime/install docs describe release and publish behavior.
- Tests or validation checks cover workflow files where feasible.
