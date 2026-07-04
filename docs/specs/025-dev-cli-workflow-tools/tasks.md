---
title: Developer CLI workflow tools tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-07-04
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

- [x] T001 Decide CLI identity and command contract.
  - Depends on: none
  - Files: `tools/devcli/pyproject.toml`, `tools/README.md`,
    `tools/devcli/README.md`
  - Acceptance: Primary command name, package metadata, alias policy, install
    command, and mutation-boundary language are documented.
  - Evidence: Complete. Primary command changed to `slc`, package metadata and
    README examples updated, no `proj` entry point remains, and
    `tools/README.md` plus `tools/devcli/README.md` document thin-wrapper and
    mutation-boundary policy.
  - [x] T001.1 Select primary command name.
    - Evidence: User selected `slc` on 2026-07-04.
  - [x] T001.2 Rename package metadata and script entry point.
    - Evidence: `tools/devcli/pyproject.toml` now uses package
      `slc-devcli` and script entry point `slc = "auriora_dev.cli:app"`.
  - [x] T001.3 Remove or explicitly deprecate template `proj` naming.
    - Evidence: `tools/devcli/README.md` documents `slc` examples and
      repository search no longer finds `proj` in `tools/`.

- [x] T002 Add shared runner and repository utilities.
  - Depends on: T001
  - Files: `tools/devcli/src/auriora_dev/runner.py`,
    `tools/devcli/src/auriora_dev/repo.py`,
    `tests/runtime/test_devcli_runner.py`
  - Acceptance: Wrapper commands can build deterministic command plans, render
    dry-runs, propagate failures, discover the repository root, and display
    repo-relative paths.
  - Evidence: Complete. `runner.py` defines `CommandSpec`, `CommandResult`,
    deterministic command-plan rendering, dry-run handling, subprocess
    execution, and stop-on-failure behavior. `repo.py` defines repo-root
    discovery, explicit repo-root resolution, and repo-relative path rendering.
    `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_devcli_runner`
    passed with 6 tests on 2026-07-04.
  - [x] T002.1 Implement command spec model.
    - Evidence: `CommandSpec` and `CommandResult` added in
      `tools/devcli/src/auriora_dev/runner.py`.
  - [x] T002.2 Implement subprocess runner and dry-run rendering.
    - Evidence: `run_plan` and `render_plan` added and covered by focused
      unittest cases.
  - [x] T002.3 Implement repo-root discovery and `--repo-root` override.
    - Evidence: `discover_repo_root`, `resolve_repo_root`, and `repo_relative`
      added in `tools/devcli/src/auriora_dev/repo.py`; explicit repo-root
      arguments are accepted by runner/repo helpers for later CLI options.
  - [x] T002.4 Test success, failure, dry-run, and path handling.
    - Evidence: `tests/runtime/test_devcli_runner.py` covers root discovery,
      repo-relative and out-of-repo paths, command-plan rendering, dry-run
      no-exec behavior, stop-on-failure behavior, and shell quoting.

- [x] T003 Replace placeholder CLI with `slc` command groups.
  - Depends on: T002
  - Files: `tools/devcli/src/auriora_dev/cli.py`,
    `tools/devcli/src/auriora_dev/commands/`, `tests/runtime/test_devcli_cli.py`
  - Acceptance: CLI help exposes real `agent-dev-lifecycle` command groups
    and no template commands remain.
  - Evidence: Complete. `tools/devcli/src/auriora_dev/cli.py` now exposes
    `check`, `doctor`, `sync`, `package`, `plugin`, `spec`, and `release`
    command groups. Old template commands such as `setup`, `dev`, `lint`,
    `test`, `spec show`, `spec scaffold-split`, and `spec new-task` were
    removed. `npm run test:devcli` passed 13 tests on 2026-07-04.

## Phase 2: Validation, Sync, Package, And Install

- [x] T004 Implement `slc check`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/check.py`,
    `tests/runtime/test_devcli_check.py`
  - Acceptance: Default plan runs full local validation; focused options and
    failure propagation are tested.
  - Evidence: Complete. `slc check --dry-run` renders the full validation plan:
    Python unit tests, lifecycle scan, archive-index, prompts,
    package-contract, npm pack dry-run, and `git diff --check`. The
    `--skip-package` option renders a visibly reduced plan. Covered by
    `tests/runtime/test_devcli_cli.py`; `npm run test:devcli` passed 13 tests
    on 2026-07-04.

- [x] T005 Implement `slc sync bundles` and `slc sync guard`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/sync.py`,
    `tests/runtime/test_devcli_sync.py`
  - Acceptance: Bundle sync copies source skill content into Codex and Claude
    bundled plugin copies or renders a dry-run plan; guard wraps `sync-guard`.
  - Evidence: Complete. `slc sync bundles` builds a mutating copy plan from
    `skills/spec-lifecycle-manager/.` into both bundled plugin skill locations
    and then runs package-contract. `slc sync guard` wraps
    `spec_runtime.py sync-guard .`. Covered by `tests/runtime/test_devcli_cli.py`.
    Direct `sync-guard` validation on 2026-07-04 reported source/bundle parity
    passing and only installed-cache drift warnings.

- [x] T006 Implement `slc package check`, `slc package pack`, and
  `slc package install-local`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/package.py`,
    `tests/runtime/test_devcli_package.py`
  - Acceptance: Package check wraps package-contract, npm dry-run, and
    sync-guard; install-local passes supported options to the installer and
    supports dry-run.
  - Evidence: Complete. `slc package check` wraps package-contract, npm pack
    dry-run, and sync-guard. `slc package pack` defaults to npm dry-run and
    requires `--write` for tarball creation. `slc package install-local`
    invokes `scripts/install-spec-lifecycle-manager-package.sh` with supported
    pass-through options and installer dry-run support. `npm run test:devcli`
    passed 13 tests; `SPEC_LIFECYCLE_PYTHON=python3 PYTHONPATH=tools/devcli/src
    python3 -m auriora_dev.cli package install-local --repo-root . --dry-run
    --skip-plugin-add` passed on 2026-07-04.

## Phase 3: Status, Spec, And Release Convenience

- [x] T007 Implement `slc plugin status` and `slc doctor`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/plugin.py`,
    `tools/devcli/src/auriora_dev/commands/doctor.py`,
    `tests/runtime/test_devcli_plugin.py`
  - Acceptance: Status is read-only and tolerant of missing Codex CLI; doctor
    reports local toolchain and metadata state without mutation.
  - Evidence: Complete. `slc plugin status` wraps read-only
    `codex plugin list` and the shared runner returns a degraded command result
    when the optional tool is unavailable. `slc doctor` reports Python, Node,
    npm, Codex CLI, package metadata, CLI metadata, and runtime script
    presence without mutation. Covered by `tests/runtime/test_devcli_cli.py`.

- [x] T008 Implement `slc spec` wrappers.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/spec.py`,
    `tests/runtime/test_devcli_spec.py`
  - Acceptance: Spec commands wrap `spec_runtime.py` scan, archive-index,
    prompts, summary, and lint without parsing spec packages directly.
  - Evidence: Complete. `slc spec scan`, `archive-index`, `prompts`,
    `summary`, and `lint` build plans around `spec_runtime.py` without parsing
    spec packages directly. Covered by `tests/runtime/test_devcli_cli.py`.

- [x] T009 Implement `slc release preflight`.
  - Depends on: T003
  - Files: `tools/devcli/src/auriora_dev/commands/release.py`,
    `tests/runtime/test_devcli_release.py`
  - Acceptance: Preflight checks working tree state, package validation,
    package metadata, npm dry-run, and active spec state without pushing,
    tagging, publishing, or creating releases.
  - Evidence: Complete. `slc release preflight` reports that push, tag, npm
    publish, and GitHub release commands are out of scope, checks working-tree
    state, and wraps package-contract, npm pack dry-run, and active spec scan.
    `--allow-dirty` supports explicit continuation for dirty local worktrees.
    Covered by `tests/runtime/test_devcli_cli.py` and verified with a dry-run
    command on 2026-07-04.

## Phase 4: Validation And Promotion

- [x] T010 Add CLI test command and repository validation integration.
  - Depends on: T004, T005, T006, T007, T008, T009
  - Files: `tools/devcli/pyproject.toml`, `package.json`,
    `tests/runtime/test_devcli_*.py`
  - Acceptance: There is a documented command to run CLI tests, and repository
    validation can include it without user-local Codex, npm publish, GitHub, or
    writable user-config dependencies.
  - Evidence: Complete. `package.json` now exposes `npm run test:devcli`,
    which runs `tests.runtime.test_devcli_runner` and
    `tests.runtime.test_devcli_cli` without Codex, npm publish, GitHub, or
    writable user-config dependencies. Full repository unittest discovery also
    includes these tests.

- [x] T011 Run validation and record evidence.
  - Depends on: T010
  - Files: `docs/specs/025-dev-cli-workflow-tools/verification.md`
  - Acceptance: CLI tests, full unit suite, lifecycle checks, package-contract,
    npm dry-run, sync guard, and `git diff --check` pass or have documented
    waivers.
  - Evidence: Complete. On 2026-07-04, full unittest discovery passed 165
    tests, package-contract returned no diagnostics, npm pack dry-run
    completed, `git diff --check` passed, `SPEC_LIFECYCLE_PYTHON=python3 npm
    run validate` passed, and `sync-guard` reported source/bundle parity
    passing with installed-cache drift warnings only. Verification details are
    recorded in `verification.md`.

- [x] T012 Promote CLI usage to durable docs and prepare closure.
  - Depends on: T011
  - Files: `tools/README.md`, `tools/devcli/README.md`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`,
    `docs/reference/spec-lifecycle-runtime.md`,
    `docs/specs/025-dev-cli-workflow-tools/verification.md`
  - Acceptance: Durable docs describe install, command groups, mutation
    boundaries, validation, and authoritative underlying commands; residual
    work is routed.
  - Evidence: Complete. `tools/README.md`, `tools/devcli/README.md`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`, and
    `docs/reference/spec-lifecycle-runtime.md` now document `slc` usage,
    command groups, mutation boundaries, validation, install wrappers, and
    authoritative underlying commands. Closure readiness still requires the
    normal final spec commit and closure/archive workflow.
