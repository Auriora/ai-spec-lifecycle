---
title: npm publish and release workflow design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Design

## Overview

Add GitHub Actions workflows that validate the repository, build the npm
package, publish only under explicit release conditions, and preserve release
evidence.

The package and cross-platform installer are already implemented. This design
starts from the existing `cross-platform.yml`, package manifests, package
contract, and install/runtime docs rather than recreating packaging.

## High-Level Design

- CI coverage: extend `.github/workflows/cross-platform.yml` or add a focused
  `ci.yml` that runs on pull requests and pushes to `main`.
- `release.yml`: runs on version tags and manual dispatch.
- CI runs the same validation commands used locally.
- Release builds the tarball, captures metadata, optionally publishes to npm,
  and uploads evidence.
- Decision: keep CI validation in `.github/workflows/cross-platform.yml` so the
  existing OS/Python matrix proves the complete validation family instead of
  splitting a second PR workflow.

## Low-Level Design

- Use Node 18 or newer for npm packaging.
- Use Python 3.10 or newer for runtime validation, matching the current package
  baseline.
- Use `npm ci` only if dependencies are introduced; current package has no
  dependency lock requirement.
- Publish gate inputs:
  - manual workflow dispatch;
  - `publish: true` input for manual dispatch;
  - repository secret `NPM_TOKEN`;
  - existing-version check with `npm view` before registry mutation.
- Artifact evidence:
  - package filename;
  - package version;
  - source commit;
  - npm pack JSON;
  - validation command summary.

## Operational Considerations

- GitHub Actions should not push Docker images for this package.
- Publish should be idempotent-safe: if the version already exists, the
  workflow should stop with a clear message rather than attempting overwrite.
- Rollback for npm is a new patch release or deprecation guidance; unpublish is
  not the normal rollback path.

## Open Questions

- OD-001: Resolved 2026-07-04. Use `NPM_TOKEN` first because it is compatible
  with the current repository setup and keeps publishing explicitly gated.
  Trusted publishing can be evaluated later without changing artifact
  generation.
- OD-002: Resolved 2026-07-04. Keep CI coverage in `cross-platform.yml` so
  PR/main validation and cross-platform installer smoke coverage stay together.
