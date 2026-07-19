---
title: Lifecycle adoption workflow tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Lifecycle Adoption Workflow Tasks

**Input:** `requirements.md`, `research.md`, `design.md`, `change-impact.md`,
`traceability.md`, and `verification.md`

## Task Dependency Graph

```text
T001 -> T002 -> T003
T001 -> T004 -> T005
T001 -> T006 -> T007
T001 -> T008
T003 + T005 + T007 + T008 -> T009
T009 -> T010
T009 + T010 -> T011 -> T012
```

## Phase 1: Contract Reconciliation

- [x] T001 Reconcile the implementation contract and review findings.
  - Depends on: none
  - Requirements: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6
  - Files: `docs/specs/038-lifecycle-adoption-workflow/`
  - Acceptance: DR-001 through DR-003 are resolved; every requirement,
    acceptance criterion, correctness property, and success criterion has an
    explicit delivery mapping; package lint and task-context lookup report no
    blocking contract gap.
  - Evidence mode: validation
  - Evidence: 2026-07-18 full package lint returned zero diagnostics; T002 and
    T006 task-context lookups resolved every linked requirement with no gaps;
    DR-001 through DR-003, explicit AC/CP/SC mappings, measurable skill
    acceptance, post-validation promotion, and bounded task families were
    reviewed across the package.

## Phase 2: Implementation-Start Composition

- [x] T002 Add contract tests for the declarative implementation-start prompt.
  - Depends on: T001
  - Requirements: Requirement 2, Requirement 4
  - Properties: CP-001, CP-002, CP-006
  - Files: `tests/runtime/test_spec_runtime.py`, prompt fixtures
  - Acceptance: Pre-implementation fixtures cover R2, R4, CP-001, CP-002, and
    CP-006 as specified in `verification.md`.
  - Evidence: 2026-07-18 runtime task context resolved Requirement 2,
    Requirement 4, CP-001, CP-002, and CP-006 with no gaps before editing;
    focused pre-implementation tests failed only because
    `implementation-start` was absent and the prompt count remained 10.

- [x] T003 Implement the declarative implementation-start prompt.
  - Depends on: T002
  - Requirements: Requirement 2, Requirement 4
  - Files: `skills/spec-lifecycle-manager/prompts/implementation-start.json`,
    prompt registry documentation, Codex and Claude prompt mirrors
  - Acceptance: The prompt passes T002 without adding a shared-core aggregate or
    mutation path.
  - Evidence: 2026-07-18 added the declarative prompt and Codex/Claude mirrors;
    five focused runtime and MCP prompt tests passed, prompt validation returned
    zero diagnostics with 11 definitions, package contract reported both source
    mirrors in sync, and no shared-core runtime or mutation path was added.

## Phase 3: Next-Action And Interface Routing

- [x] T004 Add contract tests for evidence, promotion, and MCP/CLI action
  routing.
  - Depends on: T001
  - Requirements: Requirement 3, Requirement 4
  - Properties: CP-001, CP-002
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Pre-implementation fixtures cover R3, R4, CP-001, and CP-002 as
    specified in `verification.md`.
  - Evidence: 2026-07-18 runtime task context resolved R3, R4, CP-001, and
    CP-002 with no gaps; three focused pre-implementation tests failed only
    because shared presentation, MCP-primary action identity, and separated CLI
    recovery did not yet exist.

- [x] T005 Implement shared next-action and interface presentation routing.
  - Depends on: T004
  - Requirements: Requirement 3, Requirement 4
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/actions.py`,
    affected shared-core and adapter modules
  - Acceptance: T004 passes with existing authorities, adapter provenance, and
    bounded response contracts preserved.
  - Evidence: 2026-07-18 added shared MCP-primary action presentation with
    repo-relative labelled CLI recovery; validation, evidence quality,
    promotion, and closure are ordered through existing authorities; blockers
    are preserved in a bounded 20-item view with source expansion. Four focused
    contract tests and four supporting runtime/MCP/module checks passed, and
    package parity reported both 62-file mirrors in sync.

## Phase 4: Advisory Hook Boundary

- [x] T006 Add focused tests for ordinary-write and lifecycle-boundary hooks.
  - Depends on: T001
  - Requirement: Requirement 6
  - Property: CP-003
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_codex_spec_lifecycle_hook.py`
  - Acceptance: Pre-implementation fixtures cover every R6 boundary and CP-003
    invariant specified in `verification.md`.
  - Evidence: 2026-07-19 runtime task context resolved Requirement 6 and
    CP-003 with no gaps; five focused checks preserved resume/closure lint,
    debounce, and advisory failure handling while failing only because ordinary
    verification guidance named full lint and the wrapper omitted the narrow
    verification hook.

- [x] T007 Implement the explicit hook recommendation boundary.
  - Depends on: T006
  - Requirement: Requirement 6
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`,
    `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py` only if
    wrapper behavior must change
  - Acceptance: T006 passes without new persistent state, mutation, or blocking
    behavior.
  - Evidence: 2026-07-19 replaced ordinary verification full-lint guidance
    with validation-plan and evidence-quality actions and routed verification
    writes through the narrow `verification-updated` hook. Eighteen focused
    runtime/wrapper checks passed without new persistence, mutation, or blocking
    behavior; source, Codex, and Claude copies were synchronized.

## Phase 5: Concise Skill And Capability Context

- [x] T008 Reduce the skill entrypoint against the mandatory-rule inventory.
  - Depends on: T001
  - Requirement: Requirement 5
  - Property: CP-005
  - Files: source and package skill trees
  - Acceptance: The inventory, 37,399-byte ceiling, linked expansions, and
    source/package parity checks pass.
  - Evidence: 2026-07-19 reduced the source entrypoint from 53,427 to
    16,452 bytes (69.2%), retained all eight mandatory-rule categories with
    direct named expansions, and added a focused regression contract. Eleven
    package tests passed; package-contract validation reported exact 62-file
    source/Codex/Claude parity with zero diagnostics.

## Phase 6: Integrated Validation And Dogfood

- [x] T009 Validate prompts, runtime routing, hooks, skill, bundles, and the
  installed package.
  - Depends on: T003, T005, T007, T008
  - Requirements: Requirement 2, Requirement 3, Requirement 4, Requirement 5,
    Requirement 6
  - Properties: CP-001, CP-002, CP-003, CP-005, CP-006
  - Files: validation evidence and affected test/package surfaces
  - Acceptance: All focused, full, prompt, byte, inventory, package, and sync
    checks pass with residual risks recorded.
  - Evidence mode: validation
  - Evidence: 2026-07-19 all 230 focused tests and all 317 repository tests
    passed; source and installed prompt validation returned 11 definitions with
    zero diagnostics; package contract, sync guard, archive validation,
    mandatory inventory, byte ceiling, exact-copy, and whitespace checks
    passed. The repository installer installed and enabled version 0.3.0; all
    138 installed files match the bundle. This already-running session retained
    its former 0.2.1 advisory-hook path until reload, recorded as a non-blocking
    session-lifetime residual.

- [x] T010 Review the qualified external adoption report.
  - Depends on: T009
  - Requirement: Requirement 1
  - Property: CP-004
  - Files: external report receipt and dogfood validation evidence
  - Acceptance: The qualified receipt satisfies R1 and CP-004 without analyser
    implementation or causal claims.
  - Evidence mode: validation
  - Evidence: 2026-07-19 reviewed the Chat Analyser 2026-07-18 report evidence
    at producer revision `9db3f5f7cbdbfd01ecd1a6d23d50cb8714339ea5`.
    The metadata-only receipt preserves its bounded 22-history/174 MB completed
    cohort, non-contributing larger attempts, confirmed structured Codex/Claude
    use, the producer's fail-closed exact-distribution qualification after an
    attribution defect, and the prohibition on correctness, preference,
    usefulness, or causal claims.

- [x] T009.1 Clarify capability status and retain bounded MCP client metadata.
  - Depends on: T009
  - Requirements: Requirement 4, Requirement 5
  - Properties: CP-002, CP-005
  - Files: capability core, MCP session adapter, schemas, bundle mirrors, and
    focused runtime/MCP tests
  - Acceptance: Missing client metadata is informational rather than a partial
    lifecycle result; standard initialization identity is retained in memory
    when supplied; lifecycle decisions remain repository-state-based; CLI
    recovery is labelled as a hypothetical condition rather than current MCP
    failure.
  - Evidence mode: validation
  - Evidence: 2026-07-19 changed the capability result to `ready` regardless
    of optional client observation, added explicit `observed`/`not_observed`
    metadata status and a zero-impact informational limitation, retained
    allowlisted standard initialization metadata in process memory, and
    labelled CLI recovery with `applies_when: mcp_unavailable`. Six
    pre-implementation contracts failed on the former behavior and passed after
    implementation; 222 affected tests and all 318 repository tests passed;
    prompt, package, installed-cache, and source/Codex/Claude parity checks
    passed with zero findings. After reload, the live MCP result reported
    `status=ready`, `client_metadata_status=observed`, Codex client version
    `0.144.6`, no limitations, and recovery commands labelled
    `applies_when=mcp_unavailable`.

## Phase 7: Promotion And Closure

- [ ] T011 Promote validated behavior and record residual destinations.
  - Depends on: T009, T009.1, T010
  - Requirements: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6
  - Files: durable promotion targets listed in `change-impact.md`
  - Acceptance: Validated behavior is promoted and every residual has one
    owning destination.
  - Evidence mode: validation
  - Evidence: Pending.

- [ ] T012 Run final reconciliation and closure gates.
  - Depends on: T011
  - Requirements: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6
  - Files: `docs/specs/038-lifecycle-adoption-workflow/`, closure log and archive
    index planning evidence
  - Acceptance: Reconciliation and closure gates pass with final spec and
    cleanup commits recorded before removal.
  - Evidence mode: validation
  - Evidence: Pending.

## Execution Rules

- Do not implement from this file alone; use requirements, design,
  traceability, verification, and governance context.
- Treat external Chat Analyser reports as qualified evidence. Methodology or
  product defects belong in the owning backlog and do not become source
  requirements here.
- Keep incomplete external findings incomplete; do not reconstruct exact
  operation counts inside the lifecycle manager.
- Keep ordinary hooks advisory, narrow, quiet when no guidance is needed,
  debounced, and free of lifecycle mutation or full-package lint advice.
- Preserve MCP as the primary agent interface while retaining CLI behavior for
  hooks, CI, validation, debugging, and explicit recovery.
- Do not update current-state durable docs until T009 and T010 have produced
  accepted validation evidence.

## Review Reconciliation

Reviewed against the current requirements and design on 2026-07-18. The former
combined implementation task is split across T002-T008, integrated validation
is isolated in T009, and durable promotion cannot begin before T009 and T010.

## Related Artifacts

- Requirements: `requirements.md`
- Research: `research.md`
- Design: `design.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
