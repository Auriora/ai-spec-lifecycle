---
title: npm publish and release workflow tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-07-02
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003 -> T004 -> T005 -> T006

## Tasks

- [x] T001 Add backlog and roadmap release workflow framing.
  - Files: `docs/backlog/README.md`, `docs/roadmap/README.md`
  - Acceptance: B044 and R009 identify npm publish/release workflow scope and dependency on B026.
  - Evidence: `docs/backlog/README.md` adds B044 and `docs/roadmap/README.md` adds R009.

- [/] T002 Add or extend CI validation workflow.
  - Depends on: T001
  - Files: `.github/workflows/cross-platform.yml`, optional `.github/workflows/ci.yml`
  - Acceptance: PR/main CI runs unit tests, scan, archive-index, prompts, package-contract, npm pack dry-run, and whitespace checks.
  - Evidence: Partial. Existing `.github/workflows/cross-platform.yml` runs on
    PR, `main`, and manual dispatch, and covers Python tests, Node tests,
    package-contract, cross-platform smoke, and `npm pack --dry-run`.
    Remaining: add scan, archive-index, prompts, whitespace checks, and decide
    whether this belongs in `cross-platform.yml` or a separate `ci.yml`.

- [/] T003 Add release artifact workflow.
  - Depends on: T002
  - Files: `.github/workflows/release.yml`
  - Acceptance: Release workflow builds npm tarball, captures pack metadata, and uploads artifacts/release assets.
  - Evidence: Partial. `npm pack --dry-run` and GitHub release tarball
    distribution are documented from Spec 028, but no `release.yml` currently
    builds the tarball, captures metadata, or uploads workflow artifacts/release
    assets.

- [ ] T004 Add guarded npm publish step.
  - Depends on: T003
  - Files: `.github/workflows/release.yml`, `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - Acceptance: Publish runs only on trusted release trigger with configured credentials or trusted publishing; otherwise it exits after artifact generation with clear status.
  - Evidence: Pending.

- [/] T005 Add release documentation and verification.
  - Depends on: T004
  - Files: `docs/reference/spec-lifecycle-manager-mcp-install.md`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Docs describe release triggers, install verification, rollback, and residual risks.
  - Evidence: Partial. Durable docs describe the package contract, unpacked or
    release-tarball install paths, and current `pack-ready-not-published`
    status. Remaining: document release triggers, guarded publish behavior,
    skipped-publish evidence, rollback, republish guidance, and post-publish
    verification.

- [/] T006 Validate workflow and package behavior.
  - Depends on: T005
  - Files: `.github/workflows/`, `tests/runtime/`
  - Acceptance: T006.1-T006.4 are complete with evidence.
  - Evidence: Partial. `package-contract` passes locally as of 2026-07-02 and
    reports package status `pack-ready-not-published` with source, bundled
    plugin, and Claude plugin parity in sync. Remaining: run the full validation
    plan after release workflow changes and record workflow syntax validation
    or a local-checker waiver.
  - [x] T006.1 Validate current package contract baseline.
    - Acceptance: Current package contract passes before release workflow edits.
    - Evidence: 2026-07-02 `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` passed.
  - [ ] T006.2 Run full local lifecycle validation after workflow changes.
    - Acceptance: Full validation plan in `verification.md` passes or records explicit waivers.
    - Evidence: Pending.
  - [ ] T006.3 Validate workflow syntax or record local-checker waiver.
    - Acceptance: Workflow syntax is checked with an available local tool or a documented waiver explains why no local checker was available.
    - Evidence: Pending.
  - [ ] T006.4 Record release artifact and publish-gate evidence.
    - Acceptance: Release artifact metadata and publish-gate behavior are captured in `verification.md`.
    - Evidence: Pending.
