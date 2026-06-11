---
title: npm publish and release workflow tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003 -> T004 -> T005 -> T006

## Tasks

- [x] T001 Add backlog and roadmap release workflow framing.
  - Files: `docs/backlog/README.md`, `docs/roadmap/README.md`
  - Acceptance: B044 and R009 identify npm publish/release workflow scope and dependency on B026.
  - Evidence: `docs/backlog/README.md` adds B044 and `docs/roadmap/README.md` adds R009.

- [ ] T002 Add CI validation workflow.
  - Depends on: T001
  - Files: `.github/workflows/ci.yml`
  - Acceptance: PR/main CI runs unit tests, scan, archive-index, prompts, package-contract, npm pack dry-run, and whitespace checks.
  - Evidence: Pending.

- [ ] T003 Add release artifact workflow.
  - Depends on: T002
  - Files: `.github/workflows/release.yml`
  - Acceptance: Release workflow builds npm tarball, captures pack metadata, and uploads artifacts/release assets.
  - Evidence: Pending.

- [ ] T004 Add guarded npm publish step.
  - Depends on: T003
  - Files: `.github/workflows/release.yml`, `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - Acceptance: Publish runs only on trusted release trigger with configured credentials or trusted publishing; otherwise it exits after artifact generation with clear status.
  - Evidence: Pending.

- [ ] T005 Add release documentation and verification.
  - Depends on: T004
  - Files: `docs/reference/spec-lifecycle-manager-mcp-install.md`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Docs describe release triggers, install verification, rollback, and residual risks.
  - Evidence: Pending.

- [ ] T006 Validate workflow and package behavior.
  - Depends on: T005
  - Files: `.github/workflows/`, `tests/runtime/`
  - Acceptance: Local validation passes; workflow syntax is checked where a local checker is available; package contract and npm pack dry-run pass.
  - Evidence: Pending.
