---
title: Developer CLI workflow tools tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-14
---

# Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003
T003 -> T004,T005,T006,T007,T008,T009
T004,T005,T006,T007,T008,T009 -> T010
T010 -> T011
T011 -> T012
```

## Phase 1: CLI Foundation

- [ ] T001 Decide CLI identity and command contract.
  - Depends on: none
  - Files: `tools/devcli/pyproject.toml`, `tools/README.md`,
    `tools/devcli/README.md`
  - Acceptance: Primary command name, package metadata, alias policy, install
    command, and mutation-boundary language are documented.
  - Evidence: Pending.
  - [ ] T001.1 Select primary command name.
  - [ ] T001.2 Rename package metadata and script entry point.
  - [ ] T001.3 Remove or explicitly deprecate template `proj` naming.

- [ ] T002 Add shared runner and repository utilities.
  - Depends on: T001
  - Files: `tools/devcli/src/auriora_dev/runner.py`,
    `tools/devcli/src/auriora_dev/repo.py`, `tools/devcli/tests/`
  - Acceptance: Wrapper commands can build deterministic command plans, render
    dry-runs, propagate failures, discover the repository root, and display
    repo-relative paths.
  - Evidence: Pending.
  - [ ] T002.1 Implement command spec model.
  - [ ] T002.2 Implement subprocess runner and dry-run rendering.
  - [ ] T002.3 Implement repo-root discovery and `--repo-root` override.
  - [ ] T002.4 Test success, failure, dry-run, and path handling.

- [ ] T003 Replace placeholder CLI with `adl` command groups.
  - Depends on: T002
  - Files: `tools/devcli/src/auriora_dev/cli.py`,
    `tools/devcli/src/auriora_dev/commands/`, `tools/devcli/tests/`
  - Acceptance: CLI help exposes real `agent-dev-lifecycle` command groups
    and no template commands remain.
  - Evidence: Pending.

## Phase 2: Validation, Sync, Package, And Install

- [ ] T004 Implement `adl check`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/check.py`,
    `tools/devcli/tests/`
  - Acceptance: Default plan runs full local validation; focused options and
    failure propagation are tested.
  - Evidence: Pending.

- [ ] T005 Implement `adl sync bundles` and `adl sync guard`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/sync.py`,
    `tools/devcli/tests/`
  - Acceptance: Bundle sync copies source skill content into Codex and Claude
    bundled plugin copies or renders a dry-run plan; guard wraps `sync-guard`.
  - Evidence: Pending.

- [ ] T006 Implement `adl package check`, `adl package pack`, and
  `adl package install-local`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/package.py`,
    `tools/devcli/tests/`
  - Acceptance: Package check wraps package-contract, npm dry-run, and
    sync-guard; install-local passes supported options to the installer and
    supports dry-run.
  - Evidence: Pending.

## Phase 3: Status, Spec, And Release Convenience

- [ ] T007 Implement `adl plugin status` and `adl doctor`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/plugin.py`,
    `tools/devcli/src/auriora_dev/commands/doctor.py`,
    `tools/devcli/tests/`
  - Acceptance: Status is read-only and tolerant of missing Codex CLI; doctor
    reports local toolchain and metadata state without mutation.
  - Evidence: Pending.

- [ ] T008 Implement `adl spec` wrappers.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/spec.py`,
    `tools/devcli/tests/`
  - Acceptance: Spec commands wrap `spec_runtime.py` scan, archive-index,
    prompts, summary, and lint without parsing spec packages directly.
  - Evidence: Pending.

- [ ] T009 Implement `adl release preflight`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/release.py`,
    `tools/devcli/tests/`
  - Acceptance: Preflight checks working tree state, package validation,
    package metadata, npm dry-run, and active spec state without pushing,
    tagging, publishing, or creating releases.
  - Evidence: Pending.

## Phase 4: Validation And Promotion

- [ ] T010 Add CLI test command and repository validation integration.
  - Depends on: T004, T005, T006, T007, T008, T009
  - Files: `tools/devcli/pyproject.toml`, `package.json`,
    `tools/devcli/tests/`
  - Acceptance: There is a documented command to run CLI tests, and repository
    validation can include it without user-local Codex, npm publish, GitHub, or
    writable user-config dependencies.
  - Evidence: Pending.

- [ ] T011 Run validation and record evidence.
  - Depends on: T010
  - Files: `docs/specs/025-dev-cli-workflow-tools/verification.md`
  - Acceptance: CLI tests, full unit suite, lifecycle checks, package-contract,
    npm dry-run, sync guard, and `git diff --check` pass or have documented
    waivers.
  - Evidence: Pending.

- [ ] T012 Promote CLI usage to durable docs and prepare closure.
  - Depends on: T011
  - Files: `tools/README.md`, `tools/devcli/README.md`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`,
    `docs/reference/spec-lifecycle-runtime.md`,
    `docs/specs/025-dev-cli-workflow-tools/verification.md`
  - Acceptance: Durable docs describe install, command groups, mutation
    boundaries, validation, and authoritative underlying commands; residual
    work is routed.
  - Evidence: Pending.
