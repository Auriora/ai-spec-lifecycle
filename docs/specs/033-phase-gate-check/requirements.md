---
title: Phase gate check requirements
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: requirements
owner: platform
last_reviewed: 2026-07-12
backlog_item: B031
priority: P2
---

# Requirements

## Introduction

Lifecycle phase transitions are currently guided by prose, artifact presence,
and separate tools such as lint, task context, validation planning, promotion
planning, and closure checks. Agents can still advance too early: design may
not cover accepted requirements, tasks may be stale against design, or
implementation evidence may be treated as proof before verification and durable
promotion are complete.

This spec defines a deterministic phase gate check that reports the current
phase, whether the package is ready to advance, and which missing evidence or
decisions block the next lifecycle stage.

## Goals

- Make requirements, design, tasks, implementation, promotion, and closure
  gates inspectable through runtime and MCP surfaces.
- Report missing review, stale downstream artifacts, blocking decisions,
  validation gaps, and next required action.
- Compose existing lifecycle checks where possible instead of adding a second
  lifecycle engine.
- Keep gate output advisory unless an existing closure or lint rule is already
  blocking.

## Non-Goals

- Do not replace `lint_spec_package`, `task_context`, `validation_plan`,
  `promotion_plan`, or `closure_check`.
- Do not mutate files.
- Do not create specs or downstream artifacts automatically.
- Do not make every phase gate blocking without separate governance approval.

## Glossary

| Term | Definition |
|------|------------|
| phase gate | Deterministic check that reports whether a lifecycle stage has enough evidence to advance. |
| current phase | The stage inferred from artifact frontmatter, existing artifacts, and task state. |
| ready to advance | Boolean or structured status showing whether the next stage can start without known blockers. |
| stale downstream artifact | Design, tasks, traceability, or verification content that no longer matches upstream requirements or decisions. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/backlog/README.md` B031 | Captures phase gate check candidate details. | high | Source backlog item. |
| `skills/spec-lifecycle-manager/SKILL.md` | Defines staged artifact progression and wizard mode. | high | Durable guidance target. |
| `docs/design/spec-lifecycle-management.md` | Describes lifecycle stages and promotion/closure model. | high | Durable design target. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime/MCP tool surfaces. | high | Runtime reference target. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Hosts existing lifecycle checks that phase gate output should compose. | high | Likely implementation target. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| design | modify | `docs/design/spec-lifecycle-management.md` | Describe phase gate semantics. |
| reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document CLI/MCP output. |
| skill guidance | modify | `skills/spec-lifecycle-manager/SKILL.md` | Update staged workflow guidance. |
| backlog | modify | `docs/backlog/README.md` | Mark B031 complete at closure. |
| tests | add | `tests/runtime/` | Add runtime and MCP coverage. |
| package parity | modify | `plugins/spec-lifecycle-manager/`, `packaging/spec-lifecycle-manager/` | Sync bundled runtime, schemas, and package validation. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** satisfied on 2026-07-12 by the accepted decisions below.
- **Design-first exception:** no
- **Optional artifacts recommended:** none
- **Downstream review needed:** design, tasks, traceability, verification

## Requirements

### Requirement 1: Phase Detection

**User Story:** As a coding agent, I want the lifecycle runtime to identify the
current phase of a spec, so that I know which kind of work is appropriate next.

#### Acceptance Criteria

1. GIVEN a spec package has only accepted requirements, WHEN phase gate check
   runs, THEN THE SYSTEM SHALL identify the current phase as requirements and
   report design as the next stage.
2. GIVEN a package has design but no task plan, WHEN phase gate check runs,
   THEN THE SYSTEM SHALL identify design-to-tasks readiness.
3. GIVEN tasks are complete and verification/promotion evidence exists, WHEN
   phase gate check runs, THEN THE SYSTEM SHALL identify promotion or closure
   readiness as appropriate.
4. GIVEN phase cannot be inferred safely, WHEN phase gate check runs, THEN THE
   SYSTEM SHALL report unknown phase with concrete missing evidence.

### Requirement 2: Advancement Readiness

**User Story:** As a maintainer, I want phase gate output to say whether the
next phase can start, so that agents do not advance on stale or incomplete
artifacts.

#### Acceptance Criteria

1. GIVEN required upstream artifacts are missing, WHEN phase gate check runs,
   THEN THE SYSTEM SHALL report `ready_to_advance` as false and list missing
   artifacts or sections.
2. GIVEN open decisions block the next phase, WHEN phase gate check runs, THEN
   THE SYSTEM SHALL list those decisions and their source artifact.
3. GIVEN downstream artifacts are stale relative to changed upstream artifacts,
   WHEN phase gate check runs, THEN THE SYSTEM SHALL identify the stale
   artifacts and recommend reconciliation.
4. GIVEN the phase is ready, WHEN phase gate check runs, THEN THE SYSTEM SHALL
   return the next required action and relevant validation commands.

### Requirement 3: Composition With Existing Checks

**User Story:** As a skill maintainer, I want phase gate checks to reuse
existing lifecycle tools, so that the runtime does not duplicate logic or drift
from established checks.

#### Acceptance Criteria

1. GIVEN package lint has diagnostics, WHEN phase gate check runs, THEN THE
   SYSTEM SHALL include relevant lint findings in gate output.
2. GIVEN task, validation, promotion, or closure checks already provide a
   signal, WHEN phase gate check runs, THEN THE SYSTEM SHALL include or link the
   source signal rather than recomputing incompatible semantics.
3. GIVEN MCP and CLI surfaces expose phase gate output, WHEN they are compared,
   THEN THE SYSTEM SHALL return equivalent structured data from shared internals.
4. GIVEN an agent would otherwise call preflight, lint, task selection,
   traceability, validation, promotion, and closure tools separately, WHEN the
   phase gate check runs, THEN THE SYSTEM SHALL return one bounded aggregate
   result with the applicable source signals and omit inapplicable detail.
5. GIVEN a source signal has evidence too large for the aggregate response,
   WHEN the phase gate check renders it, THEN THE SYSTEM SHALL return a compact
   summary plus deterministic follow-up arguments and an evidence fingerprint
   instead of embedding the complete nested payload.
6. GIVEN the common compact-response contract is not yet accepted, WHEN the
   phase-gate response is designed, THEN THE SYSTEM SHALL treat its public
   envelope as provisional and SHALL NOT freeze or implement a competing
   expansion schema.

### Requirement 4: Advisory Boundary

**User Story:** As a repository owner, I want phase gates to guide agents
without silently changing governance, so that adoption can be dogfooded safely.

#### Acceptance Criteria

1. GIVEN a phase gate finding is advisory, WHEN output is rendered, THEN THE
   SYSTEM SHALL make the advisory status clear.
2. GIVEN an existing lint or closure rule is blocking, WHEN phase gate check
   includes it, THEN THE SYSTEM SHALL preserve that blocking severity.
3. GIVEN a future repository wants stricter gating, WHEN this v1 runs, THEN THE
   SYSTEM SHALL require a separate governance or spec change before making new
   blockers mandatory.

## Correctness Properties

- **CP-001:** Phase gate output does not report readiness when required
  upstream artifacts or blocking decisions are missing.
- **CP-002:** Existing blocking lint or closure diagnostics remain blocking when
  surfaced through phase gate output.
- **CP-003:** MCP and CLI phase gate outputs are equivalent for the same input
  package.
- **CP-004:** The tool is read-only and does not create, update, or remove spec
  artifacts.
- **CP-005:** The aggregate gate result does not change the severity, authority,
  or proof meaning of a composed source signal.
- **CP-006:** Expansion arguments identify the source tool and selected evidence;
  when the evidence fingerprint no longer matches, expansion reports `stale`
  rather than presenting current evidence as the referenced result.

## Technical Context

- **Language/Version:** Python 3 standard library runtime; MCP JSON tool
  output.
- **Primary Dependencies:** existing lifecycle core functions, runtime adapter,
  MCP server.
- **Target Platform:** Codex/Claude plugin users and direct CLI validation.
- **Constraints:** Compose existing checks; avoid broad refactors unless shared
  internals require a small extraction.
- **Performance Goals:** Suitable for preflight use on one active spec.

## Accepted Requirements Decisions

| Decision | Rationale | Status |
|----------|-----------|--------|
| V1 phases are `requirements`, `design`, `tasks`, `implementation`, `verification`, `promotion`, `closure`, and `unknown`. | Separates artifact authoring, delivery, evidence, durable promotion, and final closure without exposing the current coarse internal labels. | accepted |
| Add standalone `phase_gate_check`; do not change `active_spec_preflight` defaults or payload. | Preserves compatibility and avoids composing a selection facade that already repeats scan/lint/task work. | accepted |
| Recorded upstream fingerprints prove `current` or `stale`; missing fingerprints produce `review_required`. Modification times remain advisory and cannot prove semantic staleness. | Avoids false blockers after checkout, copy, restore, or timestamp-only changes. | accepted |
| Promotion remains the inferred phase until durable-promotion evidence and authoritative closure checks support closure. | Current promotion planning identifies targets but does not prove completion. | accepted |

## Cross-Spec Contract Dependency

The phase-gate operation is the preferred decision facade, not a replacement
for the authoritative source tools. Its source summaries and expansion behavior
depend on the minimum compact-response contract in Spec 036. Spec 036's envelope,
detail selection, evidence-fingerprint, and compatibility decisions must be
accepted before this spec freezes or implements a public response schema.

## Success Criteria

- **SC-001:** Agents can call one read-only check to understand current phase,
  next required action, relevant task context, and applicable validation or
  closure state without manually chaining lifecycle tools.
- **SC-002:** Tests cover requirements-to-design, design-to-tasks,
  implementation-to-promotion, and closure readiness cases.
- **SC-003:** Durable docs and skill guidance describe how phase gate output
  should be used without replacing lifecycle judgment.

## Related Artifacts

- Backlog: `docs/backlog/README.md` B031
- Contract dependency: `docs/specs/036-compact-output-and-invocation-telemetry/requirements.md`
- Design: not created yet
- Tasks: not created yet
- Verification: not created yet
