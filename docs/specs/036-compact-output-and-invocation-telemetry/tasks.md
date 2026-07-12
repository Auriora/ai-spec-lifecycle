---
title: Compact lifecycle output and invocation provenance tasks
doc_type: spec
artifact_type: tasks
status: active
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-12
---

# Tasks

## Phase 1: Contract Foundation

- [x] T001 Add deterministic identity and fingerprint primitives
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/provenance.py`,
    `tests/runtime/test_lifecycle_provenance.py`
  - Implement canonical JSON, SHA-256 fingerprints, owning-package identity
    resolution, repository identity, closed enums, and metadata assembly.
  - Acceptance: deterministic tests cover source, bundled, missing, malformed,
    Git, non-Git, and privacy-sensitive inputs.
  - Evidence: 2026-07-12, 8 tests passed with
    `python3 -m unittest tests.runtime.test_lifecycle_provenance`;
    `git diff --check` passed.

- [x] T002 Replace hard-coded MCP runtime identity
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/capabilities.py`, relevant tests
  - Use owning-package identity for MCP initialize and lifecycle capabilities;
    preserve every established response field and default.
  - Acceptance: both responses report the authoritative package version and
    missing build data as `unknown`.
  - Evidence: 2026-07-12, MCP initialize and lifecycle capabilities report
    source package `0.3.0`; explicit override and target-repo isolation tests
    passed in the 51-test focused runtime/MCP run.

- [x] T003 Add capabilities provenance canary and schemas
  - Depends on: T001, T002
  - Files: MCP/CLI adapters, `spec_agent_schemas.py`, relevant tests
  - Preserve root-selection source and attach additive lifecycle metadata only
    to capabilities in this compatibility slice.
  - Acceptance: MCP/CLI decisions remain equivalent after ignoring metadata;
    surfaces and root-source precedence are correct.
  - Evidence: 2026-07-12, 200 focused tests and 248 full tests passed;
    lifecycle capabilities retains decision parity while MCP/CLI provenance,
    root-source precedence, privacy, and schema assertions pass. Bundle sync and
    package contract passed.

## Phase 2: Packaging And Aggregate Contract

- [x] T004 Materialize and validate packaged build identity
  - Depends on: T001
  - Files: packaging/release helpers, package contract tests, bundled build info
  - Generate immutable build identity and validate manifest/version agreement.
  - Acceptance: packed source, Codex manifest, Claude manifest, and build info
    report one package version and an immutable or explicitly unknown build ID.
  - Evidence: 2026-07-12, six-source version agreement and two-build identity
    validation pass; an actual npm artifact contained `git:<full SHA>` and
    postpack restored deterministic `unknown` baselines. Full `npm run validate`
    passed with 250 Python and 25 Node tests.

- [x] T005 Publish reusable compact-envelope schemas
  - Depends on: T001
  - Files: `spec_agent_schemas.py`, schema tests
  - Encode bounds, detail modes, expansion arguments, fingerprint, stale state,
    and metadata enums without tightening existing tool schemas.
  - Acceptance: schema fixtures accept all supported modes and reject invalid
    enums, missing section selectors, and malformed fingerprints.
  - Evidence: 2026-07-12, valid compact/full/section selectors, compact and
    stale envelopes pass; invalid modes, conditional sections, fingerprints,
    bounds, and provenance fail schema validation. Full `npm run validate`
    passed with 256 Python and 25 Node tests.

- [x] T006 Apply the accepted contract to Specs 033 and 035
  - Depends on: T003, T005 and accepted designs for Specs 033/035
  - New aggregate tools default compact; established tools remain unchanged.
  - Acceptance: both aggregates honor bounds, preserve blockers, expose stale
    expansion behavior, and return equivalent MCP/CLI decisions.
  - Evidence: 2026-07-12, Spec 033 `phase_gate_check` was confirmed compliant;
    Spec 035 `spec_creation_plan` now defaults compact with bounded
    full/numbering/template/validation expansion, blocker preservation, stale
    refresh, strict schemas, and MCP/CLI parity. V022-V025 passed in 88 focused
    tests; direct CLI compact/section smokes and `git diff --check` passed.
    Bundle sync remains T007.

## Phase 3: Promotion And Closure

- [x] T007 Synchronize bundles and validate package parity
  - Depends on: each source implementation slice
  - Run `slc sync bundles`, package contract, and sync guard.
  - Acceptance: source, Codex, and Claude copies match and all package checks pass.
  - Evidence: 2026-07-12, source synchronized into Codex and Claude bundles.
    V026-V028 passed: bundle sync and package contract passed; both
    source/bundle parity checks are `in_sync`. `npm run validate` passed with
    303 Python and 25 Node tests plus lifecycle, package, dry-run pack, and
    whitespace checks. Sync guard only reports expected older installed-cache,
    reload, and pre-commit sync-evidence advisories.

- [ ] T008 Promote durable documentation and close B062
  - Depends on: T001-T007
  - Update design/reference/skill guidance, record verification evidence,
    reconcile residual risks, and complete lifecycle closure.
  - Acceptance: durable docs describe shipped behavior, B062 is reconciled,
    closure checks pass, and temporary scaffolding is removed per policy.

## Dependency Summary

`T001 -> T002 -> T003`; `T001 -> T004`; `T001 -> T005`; then
`T003 + T005 + Specs 033/035 design -> T006`; all implementation slices feed
`T007`, followed by `T008`.

## Agent Readiness Contract

T001 is ready for implementation. Read `requirements.md`, `design.md`, this
task, `traceability.md`, and `verification.md`. Edit only the files named by
T001 plus synchronized bundle copies after source validation. Do not add global
response metadata or compact existing tools in T001.
