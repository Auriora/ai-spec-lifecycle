---
title: Brooks-Lint findings register
doc_type: review
status: active
owner: platform
last_reviewed: 2026-06-09
---

# Brooks-Lint Findings Register

## Purpose

Track accepted Brooks-Lint findings as durable project memory. This register
preserves finding identity, source context, triage, and verification evidence
across Brooks skill runs without relying on conversation history or transient
score output.

Brooks-Lint findings remain advisory until a maintainer or lead agent records a
triage state. Accepted or deferred findings must eventually route to a task,
backlog item, roadmap item, follow-up spec, commit, or explicit no-action
decision.

## ID Namespace

Use mode-specific IDs:

| Prefix | Mode |
|--------|------|
| `BL-ARCH-###` | Architecture audit |
| `BL-REVIEW-###` | Code review |
| `BL-DEBT-###` | Technical debt assessment |
| `BL-HEALTH-###` | Health dashboard |
| `BL-TEST-###` | Test quality review |

Allocate IDs sequentially within each mode. Repeated findings from later runs
should update `Last seen`, `Evidence`, and `Verification` on the existing
finding instead of creating a duplicate.

## Finding States

| State | Meaning | Required follow-up |
|-------|---------|--------------------|
| `needs-decision` | Finding is recorded but not yet triaged. | Decide accepted, deferred, dismissed, or resolved. |
| `accepted` | Finding should be fixed or tracked through planned work. | Link task, backlog item, roadmap item, follow-up spec, or owner. |
| `deferred` | Finding is valid but not planned now. | Record reason and durable destination. |
| `dismissed` | Finding is not actionable for this repository. | Record rationale. |
| `resolved` | Finding has been fixed or otherwise closed. | Record verification evidence and commit or doc reference. |

## Score History Relationship

`.brooks-lint-history.json` records score snapshots from Brooks runs when that
file is present. Treat it as optional supporting score-history evidence, not as
the durable finding register.

Use score history to answer trend questions such as "did the health score move
after this remediation?" or "which Brooks mode changed between runs?" Use this
Markdown register to answer finding questions such as "what is the issue?",
"where is it?", "what state is it in?", "why was it deferred?", and "what
evidence resolved it?"

Rules:

- The register must remain usable when `.brooks-lint-history.json` is absent,
  stale, local-only, or generated differently by a future Brooks run.
- Score changes should be explained by updates to finding state, evidence, or
  scope when possible.
- A score snapshot without a corresponding finding detail is not enough to
  accept, defer, dismiss, or resolve a finding.
- If the history file is tracked in this repository, keep it as supporting
  evidence only; do not make it the source of truth for finding fields.

## Register Schema

Each finding entry should include these fields:

| Field | Required | Notes |
|-------|----------|-------|
| ID | yes | Stable `BL-<MODE>-<NNN>` ID. |
| Mode | yes | Brooks skill mode that produced the finding. |
| Date first seen | yes | Date the finding was first recorded. |
| Last seen | yes | Latest Brooks run or review date that observed the finding. |
| Scope | yes | Repository area, subsystem, file family, or module. |
| Severity | yes | Preserve Brooks severity or local severity label. |
| State | yes | One of the states above. |
| Symptom | yes | Observable problem. |
| Source | yes | Code, design, test, doc, or process source. |
| Consequence | yes | Why the finding matters. |
| Remedy | yes | Suggested remediation or next action. |
| Repository references | when available | Repository-relative paths, symbols, tests, docs, or commits. |
| Brooks attribution | when available | Risk code, book/principle attribution, score dimension, or mode-specific evidence. |
| Triage rationale | yes after triage | Why the state was chosen. |
| Destination | required for accepted/deferred | Task, backlog item, roadmap item, follow-up spec, owner, or no-action record. |
| Verification | required for resolved | Command, review, commit, or manual evidence. |

## Mode-Specific Fields

### Technical Debt

Preserve these fields when Brooks-Debt provides them:

- Pain score
- Spread score
- Priority score
- Debt classification
- Debt intent

### Health Dashboard

Preserve these fields when Brooks-Health provides them:

- Dimension
- Dimension score
- Composite score
- Code-quality skipped or included
- Score weighting notes

### Test Quality

Preserve these fields when Brooks-Test provides them:

- Test risk code
- Suite map
- Test layer
- Coverage area or gap
- Relevant test files

## Findings

All seed findings below were recorded from the first Brooks runs on
2026-06-06 and triaged on 2026-06-11. Findings that describe the same
underlying issue are linked to the same durable backlog or no-action route
instead of creating duplicate remediation work.

### Architecture Audit Findings

#### BL-ARCH-001 - `spec_runtime.py` lifecycle god module

- Mode: Architecture Audit
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: lifecycle runtime CLI and helper commands
- Severity: warning
- State: deferred
- Symptom: `spec_runtime.py` concentrates scan, lint, task, closure, archive,
  prompt, review, and hook support behavior in one module.
- Source: Broad command dispatch and lifecycle helper functions share the same
  runtime file.
- Consequence: Changes to one lifecycle concern have a wide blast radius, and
  future additions can make the runtime harder to test or reason about.
- Remedy: Split stable lifecycle concerns into focused modules or facades when
  adjacent runtime changes justify the move.
- Repository references:
  `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
  `tests/runtime/test_spec_runtime.py`.
- Brooks attribution: Architecture Audit score 84/100; first run reported 3
  warnings and 1 suggestion.
- Triage rationale: Valid structural risk, but not urgent enough to refactor inside this tracking spec.
- Destination: B042 runtime modularization candidate.
- Verification: Deferred; validate when B042 is promoted.

#### BL-ARCH-002 - Bundled plugin copy can drift from development skill

- Mode: Architecture Audit
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: source skill and bundled plugin package
- Severity: warning
- State: accepted
- Symptom: The development skill tree and bundled plugin copy can diverge.
- Source: The repository keeps source files under
  `skills/spec-lifecycle-manager/` and bundled plugin files under
  `plugins/spec-lifecycle-manager/`.
- Consequence: Users can install a plugin that does not match the maintained
  source skill, especially after manual sync or packaging changes.
- Remedy: Keep sync validation visible and route any remaining package-drift
  risk to installer or packaging work.
- Repository references:
  `skills/spec-lifecycle-manager/`,
  `plugins/spec-lifecycle-manager/`,
  `tests/runtime/test_spec_plugin_package.py`.
- Brooks attribution: Architecture Audit score 84/100; duplication and
  package-boundary risk.
- Triage rationale: Valid packaging risk. Existing parity tests reduce drift,
  but commit-time install/cache drift remains a planned lifecycle hardening
  item.
- Destination: B016 commit sync guard; roadmap R005.
- Verification: Existing parity coverage in
  `tests/runtime/test_spec_plugin_package.py`; B016/R005 remains open.

#### BL-ARCH-003 - Installer concentrates deployment concerns

- Mode: Architecture Audit
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: local plugin installer
- Severity: warning
- State: deferred
- Symptom: The installer handles package copy, Codex cleanup, marketplace
  edits, and plugin registration in one script.
- Source: `scripts/install-spec-lifecycle-manager-package.sh` orchestrates
  several deployment concerns directly.
- Consequence: A small installer change can affect unrelated installation
  behavior and make validation or rollback less obvious.
- Remedy: Split installer phases or add stronger phase-level validation before
  making further installer behavior changes.
- Repository references:
  `scripts/install-spec-lifecycle-manager-package.sh`,
  `docs/reference/spec-lifecycle-manager-package.md`.
- Brooks attribution: Architecture Audit score 84/100; dependency-disorder
  signal.
- Triage rationale: Valid installer coupling risk, but decomposition should be
  handled with packaging/distribution work instead of this findings register
  spec.
- Destination: B026 distribution packaging for GHCR.
- Verification: Deferred; validate when B026 is promoted.

#### BL-ARCH-004 - Hook runtime execution is hardwired to subprocess

- Mode: Architecture Audit
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: Codex hook adapter
- Severity: suggestion
- State: dismissed
- Symptom: Hook checks shell out to the lifecycle runtime through a hardwired
  subprocess boundary.
- Source: `codex_spec_lifecycle_hook.py` executes runtime behavior through
  subprocess calls instead of a direct testable adapter contract.
- Consequence: Hook behavior is harder to exercise without command-output
  fixtures, and runtime contract changes may only surface through integration
  tests.
- Remedy: Introduce a narrow hook runner abstraction if hook behavior expands
  beyond the current command adapter.
- Repository references:
  `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`,
  `tests/runtime/test_codex_spec_lifecycle_hook.py`.
- Brooks attribution: Architecture Audit score 84/100; subprocess-boundary
  suggestion.
- Triage rationale: Current subprocess boundary is acceptable while the hook
  remains a thin command adapter. Introducing an abstraction now would add more
  ceremony than value.
- Destination: Explicit no-action decision in this register; revisit only if
  hook behavior expands.
- Verification: Existing hook tests remain the validation surface.

### Technical Debt Findings

#### BL-DEBT-001 - Lifecycle runtime responsibility concentration

- Mode: Tech Debt Assessment
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: lifecycle runtime CLI and helpers
- Severity: warning
- State: deferred
- Symptom: `spec_runtime.py` concentrates many lifecycle responsibilities.
- Source: Multiple lifecycle commands and helper domains are implemented in
  one runtime module.
- Consequence: Maintainers must load many unrelated concepts to make local
  changes, increasing review cost and regression risk.
- Remedy: Extract focused runtime modules when adding or materially changing
  lifecycle behavior.
- Repository references:
  `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
  `tests/runtime/`.
- Brooks attribution: Tech Debt Assessment score 84/100; risk code Cognitive
  Overload; pain 2; spread 3; priority 6; classification Scheduled debt;
  intent accidental.
- Triage rationale: Same underlying runtime concentration as BL-ARCH-001,
  independently confirmed by Brooks-Debt.
- Destination: B042 runtime modularization candidate.
- Verification: Deferred; validate when B042 is promoted.

#### BL-DEBT-002 - Development and bundled skill duplication

- Mode: Tech Debt Assessment
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: source skill, bundled plugin, and package sync
- Severity: warning
- State: accepted
- Symptom: Development skill and bundled plugin trees can drift.
- Source: Maintained source and packaged plugin content live in separate
  directory trees.
- Consequence: Packaging fixes can be missed, duplicated manually, or shipped
  inconsistently between development and installed surfaces.
- Remedy: Preserve package-sync validation and consider a single authoritative
  package assembly path.
- Repository references:
  `skills/spec-lifecycle-manager/`,
  `plugins/spec-lifecycle-manager/`,
  `tests/runtime/test_spec_plugin_package.py`.
- Brooks attribution: Tech Debt Assessment score 84/100; risk code Knowledge
  Duplication; pain 2; spread 3; priority 6; classification Scheduled debt;
  intent accidental.
- Triage rationale: Same packaging drift risk as BL-ARCH-002, independently
  confirmed by Brooks-Debt.
- Destination: B016 commit sync guard; roadmap R005.
- Verification: Existing parity coverage in
  `tests/runtime/test_spec_plugin_package.py`; B016/R005 remains open.

#### BL-DEBT-003 - Installer change propagation risk

- Mode: Tech Debt Assessment
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: local installer orchestration
- Severity: warning
- State: deferred
- Symptom: Installer changes mix package copy, Codex cleanup, marketplace
  edits, and plugin registration.
- Source: The install script owns several separate deployment responsibilities.
- Consequence: Installer changes can propagate through unrelated local state,
  making regressions harder to isolate.
- Remedy: Separate installer responsibilities or add phase-specific tests and
  rollback notes before expanding installer behavior.
- Repository references:
  `scripts/install-spec-lifecycle-manager-package.sh`,
  `tests/runtime/test_spec_plugin_package.py`.
- Brooks attribution: Tech Debt Assessment score 84/100; risk code Change
  Propagation; pain 2; spread 2; priority 4; classification Scheduled debt;
  intent accidental.
- Triage rationale: Same installer coupling risk as BL-ARCH-003, independently
  confirmed by Brooks-Debt.
- Destination: B026 distribution packaging for GHCR.
- Verification: Deferred; validate when B026 is promoted.

#### BL-DEBT-004 - Hook subprocess boundary debt

- Mode: Tech Debt Assessment
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: Codex hook runtime checks
- Severity: suggestion
- State: dismissed
- Symptom: Hook checks shell out through a hardwired subprocess boundary.
- Source: Hook code delegates to the lifecycle runtime through command
  execution.
- Consequence: Tests couple to process behavior and exact output contracts,
  which can make future hook changes more brittle.
- Remedy: Monitor the boundary and introduce an adapter only when hook behavior
  grows beyond current command execution.
- Repository references:
  `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`,
  `tests/runtime/test_codex_spec_lifecycle_hook.py`.
- Brooks attribution: Tech Debt Assessment score 84/100; risk code Dependency
  Disorder; pain 1; spread 2; priority 2; classification Monitored debt;
  intent accidental.
- Triage rationale: Same subprocess-boundary concern as BL-ARCH-004. The debt
  is low-priority monitored debt and does not justify a backlog item now.
- Destination: Explicit no-action decision in this register; revisit only if
  hook behavior expands.
- Verification: Existing hook tests remain the validation surface.

### Health Dashboard Findings

#### BL-HEALTH-001 - Installer fan-out dependency signal

- Mode: Health Dashboard
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: installer dependencies and local Codex state changes
- Severity: warning
- State: deferred
- Symptom: Installer fan-out is the main dependency-disorder signal.
- Source: The install script touches package content, installed plugin state,
  marketplace state, and cleanup behavior.
- Consequence: Health can degrade if installer responsibilities keep expanding
  without clearer validation boundaries.
- Remedy: Route installer hardening or decomposition if the triage pass accepts
  this finding.
- Repository references:
  `scripts/install-spec-lifecycle-manager-package.sh`,
  `docs/reference/spec-lifecycle-manager-package.md`.
- Brooks attribution: Health Dashboard composite score 93/100; dimension
  Architecture; dimension score 95/100; code-quality skipped; weighting moved
  package and installer risk into Architecture.
- Triage rationale: Same installer coupling risk as BL-ARCH-003 and
  BL-DEBT-003, seen through the health dashboard.
- Destination: B026 distribution packaging for GHCR.
- Verification: Deferred; validate when B026 is promoted.

#### BL-HEALTH-002 - `spec_runtime.py` maintainability hotspot

- Mode: Health Dashboard
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: lifecycle runtime maintainability
- Severity: warning
- State: deferred
- Symptom: `spec_runtime.py` remains the top maintainability hotspot.
- Source: Runtime responsibilities and command support are concentrated in one
  module.
- Consequence: The runtime can become harder to evolve safely as additional
  lifecycle features land.
- Remedy: Keep runtime changes small and extract focused modules when a
  cohesive boundary becomes clear.
- Repository references:
  `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
  `tests/runtime/test_spec_runtime.py`.
- Brooks attribution: Health Dashboard composite score 93/100; dimension Tech
  Debt; dimension score 85/100; code-quality skipped.
- Triage rationale: Same runtime concentration risk as BL-ARCH-001 and
  BL-DEBT-001, seen through the health dashboard.
- Destination: B042 runtime modularization candidate.
- Verification: Deferred; validate when B042 is promoted.

#### BL-HEALTH-003 - Skill and plugin duplication drift risk

- Mode: Health Dashboard
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: skill source, bundled plugin package, and install path
- Severity: warning
- State: accepted
- Symptom: Skill/plugin duplication remains a drift risk.
- Source: Development and packaged copies are maintained separately.
- Consequence: Health can regress if packaged plugin behavior differs from the
  source skill or documented install workflow.
- Remedy: Keep package-sync evidence current and route any remaining drift risk
  after triage.
- Repository references:
  `skills/spec-lifecycle-manager/`,
  `plugins/spec-lifecycle-manager/`,
  `tests/runtime/test_spec_plugin_package.py`.
- Brooks attribution: Health Dashboard composite score 93/100; dimension Tech
  Debt; dimension score 85/100; code-quality skipped.
- Triage rationale: Same packaging drift risk as BL-ARCH-002 and BL-DEBT-002,
  seen through the health dashboard.
- Destination: B016 commit sync guard; roadmap R005.
- Verification: Existing parity coverage in
  `tests/runtime/test_spec_plugin_package.py`; B016/R005 remains open.

#### BL-HEALTH-004 - Installer orchestration scheduled debt

- Mode: Health Dashboard
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: installer orchestration
- Severity: warning
- State: deferred
- Symptom: Installer orchestration remains scheduled debt.
- Source: The installer still combines multiple local deployment operations.
- Consequence: Future installer changes may require broader validation than the
  apparent edit size suggests.
- Remedy: Defer or route installer decomposition based on T005 triage and T006
  planning.
- Repository references:
  `scripts/install-spec-lifecycle-manager-package.sh`.
- Brooks attribution: Health Dashboard composite score 93/100; dimension Tech
  Debt; dimension score 85/100; code-quality skipped.
- Triage rationale: Same installer orchestration risk as BL-ARCH-003,
  BL-DEBT-003, and BL-HEALTH-001.
- Destination: B026 distribution packaging for GHCR.
- Verification: Deferred; validate when B026 is promoted.

#### BL-HEALTH-005 - Subprocess-heavy CLI and hook tests

- Mode: Health Dashboard
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: runtime CLI and hook tests
- Severity: suggestion
- State: dismissed
- Symptom: CLI and hook tests rely on subprocess fixtures in several places.
- Source: Runtime and hook behavior are validated through process-level command
  execution and captured output.
- Consequence: Minor output or process-boundary changes can create test churn
  even when lifecycle behavior remains correct.
- Remedy: Preserve current integration coverage, and add narrower unit
  contracts only if subprocess coupling starts slowing changes.
- Repository references:
  `tests/runtime/`,
  `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
  `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`.
- Brooks attribution: Health Dashboard composite score 93/100; dimension Test
  Quality; dimension score 99/100; code-quality skipped.
- Triage rationale: Current subprocess-heavy checks provide useful integration
  confidence. Add narrower tests only if output churn becomes a real
  maintenance cost.
- Destination: Explicit no-action decision in this register.
- Verification: Existing runtime and hook tests remain the validation surface.

### Test Quality Findings

#### BL-TEST-001 - Duplicated spec-package fixture builders

- Mode: Test Quality Review
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: runtime, MCP, hook, and traceability tests
- Severity: warning
- State: deferred
- Symptom: Spec-package fixture builders are duplicated across runtime, MCP,
  hook, and traceability tests.
- Source: Several test files construct similar spec package directories and
  artifacts locally.
- Consequence: Schema or lifecycle fixture changes must be repeated in multiple
  places, increasing the chance of stale tests.
- Remedy: Introduce a shared fixture builder when the next fixture-heavy change
  touches multiple suites.
- Repository references:
  `tests/runtime/`,
  `tests/traceability/`.
- Brooks attribution: Test Quality Review score 89/100; risk code Test
  Duplication; suite map covers runtime, MCP adapter, traceability lookup,
  Codex hook, and plugin package; test layer integration/unit mix; coverage gap
  reusable fixture layer.
- Triage rationale: Valid test-maintenance risk, but best handled when the
  next fixture-heavy change touches multiple suites.
- Destination: B043 shared lifecycle test fixtures.
- Verification: Deferred; validate when B043 is promoted.

#### BL-TEST-002 - Plugin package coverage gap

- Mode: Test Quality Review
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: plugin package tests and installer behavior
- Severity: warning
- State: accepted
- Symptom: Plugin package tests verify component presence but not full
  development-skill to bundled-plugin sync or installer behavior.
- Source: Package tests focus on required files and manifest wiring.
- Consequence: A package can appear structurally valid while still drifting
  from the source skill or missing installer cleanup behavior.
- Remedy: Confirm whether later package-sync work resolved this gap; if not,
  add sync or installer behavior coverage.
- Repository references:
  `tests/runtime/test_spec_plugin_package.py`,
  `skills/spec-lifecycle-manager/`,
  `plugins/spec-lifecycle-manager/`,
  `scripts/install-spec-lifecycle-manager-package.sh`.
- Brooks attribution: Test Quality Review score 89/100; risk code Coverage
  Illusion; coverage areas plugin package and installer behavior; coverage gap
  full plugin/source sync and installer behavior.
- Triage rationale: Source-to-bundled skill parity is now covered, while
  broader installer/distribution behavior remains planned work.
- Destination: B016 commit sync guard and B026 distribution packaging.
- Verification: Existing parity coverage in
  `tests/runtime/test_spec_plugin_package.py`; installer behavior remains
  routed to B026.

#### BL-TEST-003 - Subprocess and output-coupled tests

- Mode: Test Quality Review
- Date first seen: 2026-06-06
- Last seen: 2026-06-06
- Scope: CLI and hook test boundaries
- Severity: suggestion
- State: dismissed
- Symptom: CLI and hook tests rely on subprocess boundaries and exact
  stdout/stderr behavior.
- Source: Tests exercise commands through subprocesses and assert output
  details.
- Consequence: Tests can become brittle when command presentation changes but
  lifecycle semantics do not.
- Remedy: Keep process-level tests for integration confidence and add narrower
  semantic tests if output churn becomes a maintenance problem.
- Repository references:
  `tests/runtime/test_codex_spec_lifecycle_hook.py`,
  `tests/runtime/test_spec_runtime.py`.
- Brooks attribution: Test Quality Review score 89/100; risk code Test
  Brittleness; suite map covers runtime CLI and hook behavior; coverage area
  command execution.
- Triage rationale: Same subprocess-boundary concern as BL-ARCH-004,
  BL-DEBT-004, and BL-HEALTH-005. Current integration tests are acceptable.
- Destination: Explicit no-action decision in this register.
- Verification: Existing runtime and hook tests remain the validation surface.

## Maintenance Rules

- Validation mode is Markdown-only first. Maintainers should review the fields
  below during Brooks triage and closure checks; runtime validation should be
  added only if repeated Brooks runs show real register drift.
- Keep findings stable even when the wording is refined.
- Update an existing finding when a later run reports the same structural issue.
- Do not treat score changes alone as durable findings; record the concrete
  maintainability, architecture, debt, or test-quality issue.
- Keep dismissed findings visible with rationale so they are not repeatedly
  rediscovered.
- Link accepted and deferred findings to tasks, backlog, roadmap, or follow-up
  specs before closing the implementation spec that introduced them.
- Record verification before moving a finding to `resolved`.

## Related Artifacts

- Active spec: `docs/specs/015-brooks-lint-findings-tracking/`
- Backlog: `docs/backlog/README.md`
- Roadmap: `docs/roadmap/README.md`
