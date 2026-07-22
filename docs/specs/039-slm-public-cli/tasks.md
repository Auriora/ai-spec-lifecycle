---
title: Public slm CLI tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-07-22
---

# Tasks

**Input**: `requirements.md`, `design.md`, `change-impact.md`,
`canonical-context.md`, `traceability.md`, and `verification.md`

**Prerequisites**: The user-approved decisions recorded in `requirements.md`
and the public/package boundary in `design.md`.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T002 -> T004
T003 + T004 -> T005
T005 -> T006
T006 -> T007
T007 -> T008
T008 -> T009
T009 -> T010
T010 -> T011
```

## Phase 1: Contract Foundation

**Purpose**: Freeze public behavior and shared record semantics before changing
the package executable.

- [x] T001 Add public CLI contract fixtures and focused failing tests.
  - Depends on: none
  - Requirement: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005, CP-006, CP-007
  - Files: `tests/runtime/`, `tests/fixtures/`
  - Acceptance: Tests define the sole `slm` bin, help and install behavior,
    active inventory, selection ambiguity, task filter unions and exclusions,
    next-task equivalence,
    requirement priorities, durable history, JSON parity, repository discovery,
    exit codes, and read-only behavior.
  - Evidence mode: validation
  - Evidence: Added tests/fixtures/public-cli-contract.json and tests/runtime/test_public_views.py covering executable/help/install contract metadata, normalized envelopes, inventory and selection, task-state unions/exclusions and next equivalence, requirement priority semantics, durable history validation, repo-relative output, and read-only projection. Contract-first red run: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_views failed at import because lifecycle.public_views was intentionally not yet implemented.

  - Status: Contract fixture and focused red tests complete; T002 may implement the shared view layer.
- [x] T002 Implement normalized shared lifecycle view records.
  - Depends on: T001
  - Requirement: Requirement 2, Requirement 3, Requirement 4, Requirement 5,
    Requirement 6
  - Properties: CP-001, CP-002, CP-005, CP-006, CP-007
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/requirements.py`, new
    public-view module as accepted by implementation
  - Acceptance: Active specs, tasks, requirements, and historic entries are
    projected from shared core semantics; requirement inventory exposes
    canonical priorities and linked tasks; no Markdown parser is duplicated in
    the presentation layer.
  - Evidence mode: validation
  - Evidence: Implemented lifecycle/public_views.py and extended the shared resolver for active and historic numeric-prefix/slug references. Shared records compose scan_specs, spec_summary, task_list, next_task, archive_index, requirement_blocks, and traceability parsers. Focused plus shared-core regression run passed 21 tests.

  - Status: Normalized active-spec, task, requirement, and history records are complete.
- [x] T003 Checkpoint - Shared record and filter validation.
  - Depends on: T002
  - Requirement: Requirement 2, Requirement 3, Requirement 4, Requirement 5,
    Requirement 6
  - Files: `tests/runtime/`, `docs/specs/039-slm-public-cli/verification.md`
  - Acceptance: Focused tests prove exact marker/state partitions, next-task
    equivalence, ambiguity handling, priority semantics, and history sourcing
    before renderers or package bins are implemented.
  - Validation: Run the focused Python public-view/core test module.
  - Evidence mode: validation
  - Evidence: Phase 1 checkpoint passed: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_views plus focused resolver/archive/priority/next/task-list regressions ran 22 tests successfully; git diff --check passed; MCP lint reported 0 errors, 0 warnings, and 0 info findings. Tests cover successful empty inventory, all normalized marker partitions, filter unions and exclusivity, exact next_task equivalence, absent/ambiguous/historic selection, numeric-prefix and slug resolution, canonical/missing/diagnostic priority semantics, compact linked-task ranges, durable history ordering/filtering/fail-closed diagnostics, repo-relative paths, and read-only projection.

  - Status: Phase 1 contract foundation and shared-record checkpoint complete; T004 is the next implementation task.
## Phase 2: Public CLI

**Purpose**: Deliver the read-only Python command surface and consistent human
and machine output.

- [x] T004 Implement the standard-library `slm` Python CLI and renderers.
  - Depends on: T002
  - Requirement: Requirement 2, Requirement 3, Requirement 4, Requirement 5,
    Requirement 6, Requirement 7, Requirement 8, Requirement 9
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005, CP-006, CP-007
  - Files: `skills/spec-lifecycle-manager/scripts/slm_cli.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/public_cli.py`,
    `tests/runtime/`
  - Acceptance: `specs`, `tasks`, `next`, `requirements`, and `history` support
    the agreed selectors and filters, plain output, `--json`, root discovery,
    deterministic ordering, and documented error exits without mutation.
  - Evidence mode: validation
  - Evidence: Implemented scripts/slm_cli.py and lifecycle/public_cli.py with standard-library parsing, bare-specs defaulting, all five read-only query commands, compatible filters, deterministic selection, nested/-C repository resolution, shared normalized table/JSON rendering, control-sequence sanitization, and exit 0/1/2 mapping. Focused public CLI/view suite passed 31 tests. Live checkout smokes passed for specs, tasks/next, requirements, history, specs --all, table and JSON output; history limit was reconciled to the archive index's newest-first durable order. The specs view reuses scan health and does not call spec_summary, avoiding a repeated full lint per active spec.

  - Status: Public Python CLI and renderers complete; T005 checkpoint is ready.
- [x] T005 Checkpoint - Public command validation.
  - Depends on: T003, T004
  - Requirement: Requirement 2, Requirement 3, Requirement 4, Requirement 5,
    Requirement 6, Requirement 7, Requirement 8, Requirement 9
  - Files: `tests/runtime/`, `docs/specs/039-slm-public-cli/verification.md`
  - Acceptance: Focused CLI tests pass for table and JSON output, nested
    working directories, explicit roots, valid empty repositories, ambiguity,
    invalid filters, malformed history, and worktree preservation.
  - Validation: Run focused public CLI tests and `git diff --check`.
  - Evidence mode: validation
  - Evidence: Phase 2 checkpoint passed: 36 public CLI, shared-view, resolver, archive, priority, next-task, and grouped-task tests passed. Direct slm_cli.py --help succeeded; an invalid --next/--pending invocation exited 2, wrote no stdout, and reported the exclusive-filter error on stderr. Python module compilation and git diff --check passed. MCP lint reported 0 errors, 0 warnings, and 0 info findings. Focused fixtures verify table/JSON parity, nested discovery, explicit roots, valid empty repositories, ambiguity, invalid filters, malformed history, deterministic output, control-sequence sanitization, and complete worktree preservation.

  - Status: Phase 2 public CLI and checkpoint complete; T006 package dispatcher is next.
## Phase 3: Packaging and Distribution

**Purpose**: Make `slm` the sole release-package executable while preserving
the package installer subcommand and repository-local `slc` separation.

- [x] T006 Implement the Node dispatcher and sole-bin package contract.
  - Depends on: T005
  - Requirement: Requirement 1, Requirement 8, Requirement 9
  - Files: `package.json`, `packaging/spec-lifecycle-manager/slm-cli.js`,
    `packaging/spec-lifecycle-manager/npm-install.js`,
    `packaging/spec-lifecycle-manager/package-manifest.json`,
    `packaging/spec-lifecycle-manager/npm-package.json`, package-contract code,
    `tests/runtime/*.test.mjs`
  - Acceptance: `slm` is the only npm bin; bare `slm` routes to `specs`;
    `slm install` retains installer behavior; read commands launch the bundled
    Python CLI through `resolve-python.mjs` without a shell; obsolete executable
    aliases are removed from package contracts and tests.
  - Evidence mode: validation
  - Evidence: Implemented packaging/spec-lifecycle-manager/slm-cli.js, sole package.json bin {slm: slm-cli.js}, in-process install routing, shell-free bundled Python query dispatch through resolve-python.mjs, child exit/signal forwarding, and strict package-contract bin_name/bin validation. Removed obsolete npm-install.js and long executable aliases. Updated package manifests, installer requirements/usage, package tests, and CI packaged-smoke step. Node syntax plus 16 dispatcher/resolver tests and 3 package-contract tests passed; git diff --check passed.

  - Status: Node dispatcher and sole-bin contract complete; T007 bundle and packaged execution validation is ready.
- [x] T007 Synchronize plugin bundles and validate packaged execution.
  - Depends on: T006
  - Requirement: Requirement 1, Requirement 7, Requirement 8, Requirement 9
  - Files: `plugins/spec-lifecycle-manager/`,
    `plugins/spec-lifecycle-manager/claude-plugin/`, package tests and fixtures
  - Acceptance: Source and Codex/Claude bundles are equivalent; npm dry-run
    includes every dispatcher/runtime file; an isolated built-tarball smoke
    proves `slm --help`, `slm specs --json`, and `slm install --help`; Windows,
    macOS, and Linux CI paths are represented.
  - Validation: Run source/bundle sync guard, package contract, npm pack
    dry-run, focused Node tests, and isolated tarball smoke.
  - Evidence mode: validation
  - Evidence: Synchronized the 65-file source skill to byte-equivalent Codex and Claude bundle trees with repo-local slc. Package contract passed with zero findings and sole slm bin. All 31 Node tests and 48 focused Python package/CLI/workflow tests passed. npm pack dry-run contained 158 files with every dispatcher and both bundled public runtimes. tests/runtime/slm_package_smoke.mjs built and installed the tarball in isolated roots, confirmed the npm slm shim and absence of legacy shims, and passed slm --help, slm specs --json, and slm install --help. Windows/macOS/Linux matrix workflow now runs the packaged smoke. git diff --check and MCP lint passed. Broader sync guard confirmed source bundle and Claude parity; its only cache finding is the intentionally unchanged user-wide 0.4.0 install, which checkout testing must not overwrite.

  - Status: Phase 3 package dispatcher, bundles, and isolated packaged execution are complete; T008 durable documentation is next.
## Phase 4: Durable Documentation and Closure Readiness

**Purpose**: Promote the accepted command contract and complete release-quality
validation.

- [x] T008 Update durable public CLI, runtime, design, and install docs.
  - Depends on: T007
  - Requirement: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9
  - Files: `README.md`, `docs/design/spec-lifecycle-management.md`,
    `docs/reference/spec-lifecycle-runtime.md`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`, release notes if a
    release is prepared
  - Acceptance: Durable docs use `slm`, distinguish public CLI from `slc` and
    MCP, explain filters and state semantics, document the executable breaking
    change, and contain a validated user path from package installation to each
    read-only view.
  - Evidence mode: implementation
  - Evidence: Promoted the accepted public CLI contract to README.md, docs/design/spec-lifecycle-management.md, docs/reference/spec-lifecycle-runtime.md, docs/reference/spec-lifecycle-manager-mcp-install.md, and docs/release-notes/v0.5.0.md. The docs distinguish public slm, checkout-only slc, and agent MCP; define selection, filter/state, JSON, failure, read-only, and history semantics; document the sole-bin breaking rename and isolated tarball path. Every documented query example passed against the checkout dispatcher.

- [x] T009 Run full validation, package review, and semantic closure review.
  - Depends on: T008
  - Requirement: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005, CP-006, CP-007
  - Files: `docs/specs/039-slm-public-cli/verification.md`, durable follow-up
    destinations if needed
  - Acceptance: Full tests, lifecycle scan/lint, prompt validation, package
    contract, sync guard, npm pack dry-run, whitespace checks, isolated
    packaged smoke, and package/release review pass or have explicit bounded
    dispositions; every Must requirement and public-interface design target is
    complete or routed with one owner before closure.
  - Evidence mode: validation
  - Evidence: Phase 4 full validation passed after correcting two archive/closure destinations made stale by the intentional npm-install.js replacement. npm run validate passed 353 Python tests, 32 Node tests, lifecycle scan, archive index, prompt validation, package contract, sync guard, a 158-file npm pack dry-run, and git diff --check. The isolated installed-tarball smoke repassed, and MCP scan/lint/prompts/archive checks reported healthy output with zero package lint or archive findings. Package/public-interface review passed the sole-bin migration, installer/query separation, shell-free dispatch, shared semantic, read-only, durable-doc, bundle, and package boundaries. The breaking rename is documented in docs/release-notes/v0.5.0.md. GitHub Actions run 29683557635 then passed all six Linux/macOS/Windows jobs on Python 3.10 and 3.12, including the installed-package smoke; no implementation backlog remains.

  - Status: Phase 4 implementation, promotion, full validation, and semantic review complete; actual spec closure remains separate.
  - Destination: none
  - Decision owner: none

## Phase 5: Unified Spec Navigation

**Purpose**: Add the user-requested singular `spec` command as a routing layer
over the already accepted public view contracts.

- [x] T010 Implement and document unified singular spec navigation.
  - Depends on: T009
  - Requirement: Requirement 10
  - Properties: CP-003, CP-004, CP-005, CP-008
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/public_cli.py`,
    `tests/runtime/test_public_cli.py`, `tests/runtime/slm-cli.test.mjs`,
    `README.md`, `docs/reference/spec-lifecycle-runtime.md`,
    `docs/design/spec-lifecycle-management.md`, bundle copies, and this spec's
    traceability, quickstart, and verification artifacts
  - Acceptance: `slm spec` defaults to open inventory; `all` and `closed`
    select combined and historic inventory; a spec reference defaults to tasks;
    explicit `tasks`, `next`, and `requirements` delegate to the existing
    builders and filters; plural commands remain compatible; invalid mixed
    forms fail with exit 2; source/bundle and packaged validation pass.
  - Validation: Run focused Python and Node CLI tests, direct source command
    equivalence smokes, package contract, source/bundle sync guard, full
    validation, and `git diff --check`.
  - Evidence mode: validation
  - Evidence: Implemented unified `slm spec` inventory and per-spec routing with the requested defaults; retained plural compatibility; synchronized Codex and Claude bundles; promoted README, design, runtime, and install guidance. Validation passed: 34 focused Python tests, 7 dispatcher tests, seven live singular/plural JSON equivalence pairs, isolated installed-tarball smoke, and full `npm run validate` with 356 Python tests, 33 Node tests, lifecycle/package/sync checks, npm dry-run, and `git diff --check`.
  - Status: Singular spec routing, compatibility coverage, durable documentation, bundle synchronization, and package validation complete.

## Phase 6: Phase Progress Projection

**Purpose**: Expose task-derived phase progress and state in active spec
inventory without creating a second phase or task-state interpretation.

- [x] T011 Implement and document task-derived phase progress in spec inventory.
  - Depends on: T010
  - Requirement: Requirement 11
  - Properties: CP-003, CP-004, CP-009
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/public_views.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/public_cli.py`,
    `tests/runtime/test_public_views.py`, `tests/runtime/test_public_cli.py`,
    `README.md`, `docs/reference/spec-lifecycle-runtime.md`,
    `docs/design/spec-lifecycle-management.md`, bundle copies, and this spec's
    traceability, quickstart, change-impact, and verification artifacts
  - Acceptance: Phased specs expose completed/total phase progress, current
    phase name, and a normalized task-derived phase state; no-phase specs expose
    null/`-` fields; task-free headings do not count; singular/plural routes
    remain equivalent; source/bundle and packaged validation pass.
  - Validation: Run focused public-view and CLI tests, live table/JSON smokes,
    package smoke, source/bundle sync guard, full validation, lifecycle lint,
    and `git diff --check`.
  - Evidence mode: validation
  - Evidence: Implemented task-derived phase progress and normalized current-phase state in active spec records; added PHASES and PHASE STATE table columns plus JSON fields, explicit no-phase nulls, deterministic precedence coverage, durable documentation, and synchronized Codex/Claude bundles. Validation passed: 38 focused Python tests, live table/JSON output, isolated installed-tarball smoke, and full `npm run validate` with 360 Python tests, 33 Node tests, lifecycle/package/source-bundle checks, npm dry-run, and `git diff --check`.
  - Status: Phase grouping, progress/state projection, absent-phase behavior, presentation, durable documentation, bundle synchronization, and package validation complete.
## Execution Rules

- Do not implement from this file alone. Read all linked artifacts and current
  package/runtime source before starting a task.
- Mark one selected task `[~]` before implementation and use the guarded task
  state tool when available.
- Keep `slm` read-only except for its explicitly selected `install` subcommand.
- Do not introduce compatibility aliases that contradict Requirement 1.
- Do not copy the Typer-based `slc` implementation into the release package.
- Do not add a CLI-only interpretation of task state, next-task selection,
  requirement priority, spec resolution, or history validity.
- Run focused tests at each checkpoint; do not wait until T009 to discover a
  public-contract or packaging mismatch.
- Verify the built tarball in isolated roots. A checkout invocation alone is
  not distribution evidence.
- Preserve unrelated worktree changes and keep generated package artifacts out
  of commits unless repository policy explicitly requires them.
- Before closure, promote all accepted CLI behavior and migration guidance to
  the durable targets in `change-impact.md`.

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: `change-impact.md`
- Design: `design.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
- Quickstart: `quickstart.md`
