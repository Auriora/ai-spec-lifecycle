---
title: npm publish and release workflow design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Design

## Overview

Add GitHub Actions workflows that validate the repository, build the npm
package, publish only under explicit release conditions, and preserve release
evidence.

## High-Level Design

- `ci.yml`: runs on pull requests and pushes to `main`.
- `release.yml`: runs on version tags and manual dispatch.
- CI runs the same validation commands used locally.
- Release builds the tarball, captures metadata, optionally publishes to npm,
  and uploads evidence.

## Low-Level Design

- Use Node 18 or newer for npm packaging.
- Use Python 3.9 or newer for runtime validation.
- Use `npm ci` only if dependencies are introduced; current package has no
  dependency lock requirement.
- Publish gate inputs:
  - tag pattern or manual workflow dispatch;
  - `NPM_TOKEN` or trusted publishing configuration;
  - optional `publish: true` input for manual dispatch.
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

- Decide whether to use npm trusted publishing or `NPM_TOKEN` first based on
  repository and npm organization readiness during implementation.
