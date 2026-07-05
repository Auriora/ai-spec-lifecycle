---
title: Phase completion helper requirements
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: requirements
owner: platform
last_reviewed: 2026-07-05
backlog_item: B050
priority: P4
---

# Requirements

## Introduction

Closing implementation phases currently requires several repetitive edits:
updating task evidence, verification tables, evidence logs, readiness decisions,
and grouped task states. External agent feedback and recent dogfooding show
that this is expensive and error-prone, especially when agents confuse status
mutation with proof.

This spec defines a phase completion helper that can assemble reviewed
phase-completion updates from concrete validation evidence while preserving the
boundary between "recorded evidence" and "evidence exists."

## Goals

- Reduce manual phase-completion bookkeeping for implementation-heavy specs.
- Update task evidence, verification task tables, evidence logs, and readiness
  status from one reviewed input where safe.
- Preserve proof boundaries: the helper may record concrete evidence but must
  not treat planned or batch updates as proof.
- Compose with phase gate checks when available.

## Non-Goals

- Do not replace validation commands, code review, durable promotion, or human
  judgment.
- Do not mark tasks complete without concrete evidence.
- Do not create a broad write-capable agent-backed tool.
- Do not make phase completion automatic on every task edit.

## Glossary

| Term | Definition |
|------|------------|
| phase completion | Recorded checkpoint that a coherent phase, such as implementation or validation, has completed with evidence. |
| proof boundary | Rule that status updates only record evidence; they do not create proof by themselves. |
| reviewed input | Structured input that names commands, results, changed files, task IDs, residual risks, and reviewer/agent disposition. |
| grouped task state | A set of related tasks or phase rows updated together after evidence review. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/backlog/README.md` B050 | Captures phase completion helper candidate and proof-boundary constraint. | high | Source backlog item. |
| `docs/reviews/agent-feedback.md` | External feedback reported implementation-heavy phase overhead. | medium | Input should be treated as feedback, not accepted requirements beyond B050. |
| `skills/spec-lifecycle-manager/SKILL.md` | Defines task status and verification evidence rules. | high | Durable guidance target. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Contains task-state, evidence-quality, validation-plan, and closure-related helpers. | high | Likely shared implementation target. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime and MCP helper surfaces. | high | Durable reference target. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document helper behavior and write boundaries. |
| skill guidance | modify | `skills/spec-lifecycle-manager/SKILL.md` | Clarify phase-completion use and proof boundary. |
| design | modify | `docs/design/spec-lifecycle-management.md` | Describe where phase completion fits in lifecycle stages. |
| backlog | modify | `docs/backlog/README.md` | Mark B050 complete at closure. |
| tests | add | `tests/runtime/` | Cover preview/write behavior and evidence classification. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** write boundaries, proof requirements, and target
  artifacts are accepted.
- **Design-first exception:** no
- **Optional artifacts recommended:** none
- **Downstream review needed:** design, tasks, traceability, verification

## Requirements

### Requirement 1: Phase Completion Preview

**User Story:** As a maintainer, I want to preview phase-completion updates
before files change, so that I can verify evidence and scope.

#### Acceptance Criteria

1. GIVEN a phase-completion request, WHEN write intent is absent, THEN THE
   SYSTEM SHALL return a preview of intended task, verification, and evidence
   updates without mutating files.
2. GIVEN a preview is generated, WHEN output is returned, THEN THE SYSTEM SHALL
   list intended files, task IDs, evidence rows, readiness fields, and residual
   risk entries.
3. GIVEN input lacks concrete validation or review evidence, WHEN preview is
   generated, THEN THE SYSTEM SHALL classify the gap instead of marking the
   phase complete.

### Requirement 2: Guarded Writes

**User Story:** As a repository owner, I want phase-completion writes to be
explicit and bounded, so that lifecycle records cannot be mutated accidentally.

#### Acceptance Criteria

1. GIVEN a phase-completion write is requested, WHEN explicit write intent is
   missing, THEN THE SYSTEM SHALL reject mutation.
2. GIVEN explicit write intent is present, WHEN the helper writes files, THEN
   THE SYSTEM SHALL limit changes to declared active spec package targets.
3. GIVEN a requested update touches durable docs, closure records, or package
   cleanup targets, WHEN phase-completion helper runs, THEN THE SYSTEM SHALL
   reject or route that work to the appropriate promote/close workflow.

### Requirement 3: Evidence And Proof Boundary

**User Story:** As a coding agent, I want the helper to preserve the difference
between recording evidence and proving work, so that status updates do not hide
missing validation.

#### Acceptance Criteria

1. GIVEN evidence references concrete commands, results, files, reviews, or
   manual verification, WHEN the helper records completion, THEN THE SYSTEM
   SHALL preserve those references in task or verification evidence.
2. GIVEN evidence is planned, vague, not run, or blocked, WHEN the helper
   evaluates completion, THEN THE SYSTEM SHALL avoid marking the phase complete
   unless an explicit waiver or residual risk is recorded.
3. GIVEN multiple tasks are updated together, WHEN evidence differs per task,
   THEN THE SYSTEM SHALL keep task-level evidence specific enough for later
   audit.

### Requirement 4: Verification Artifact Updates

**User Story:** As a maintainer, I want phase-completion evidence reflected in
`verification.md` when present, so that phase evidence is not scattered across
only task rows.

#### Acceptance Criteria

1. GIVEN `verification.md` exists, WHEN phase-completion evidence is accepted,
   THEN THE SYSTEM SHALL update relevant task evidence tables, evidence logs,
   readiness status, or residual risk sections.
2. GIVEN `verification.md` is absent, WHEN phase completion needs a durable
   evidence artifact, THEN THE SYSTEM SHALL recommend creating it rather than
   silently dropping evidence.
3. GIVEN the verification artifact format differs from the fallback template,
   WHEN updates are planned, THEN THE SYSTEM SHALL preview exact changes or
   report that manual update is required.

### Requirement 5: Runtime And MCP Interfaces

**User Story:** As an agent, I want a consistent CLI/MCP helper surface, so that
phase completion can be scripted in Codex/Claude workflows and validated in CI.

#### Acceptance Criteria

1. GIVEN MCP is available, WHEN phase completion is requested, THEN THE SYSTEM
   SHALL expose a preview-first tool backed by shared lifecycle logic.
2. GIVEN MCP is unavailable or CI needs recovery, WHEN phase completion is
   requested, THEN THE SYSTEM SHALL provide an equivalent direct runtime
   command.
3. GIVEN MCP and CLI outputs are compared for the same input, THEN THE SYSTEM
   SHALL return equivalent structured data from shared internals.

## Correctness Properties

- **CP-001:** The helper never mutates files without explicit write intent.
- **CP-002:** The helper never marks phase completion from planned, vague, or
  blocked evidence unless an explicit waiver or residual risk is recorded.
- **CP-003:** Preview and write modes target the same bounded file set.
- **CP-004:** MCP and CLI surfaces call shared lifecycle logic and return
  equivalent structured results.
- **CP-005:** Durable promotion and closure records remain outside the helper's
  write scope.

## Technical Context

- **Language/Version:** Python 3 standard library runtime; MCP JSON tool
  output.
- **Primary Dependencies:** task-state, evidence-quality, validation-plan, and
  runtime adapter internals.
- **Target Platform:** Codex/Claude plugin users and direct CLI validation.
- **Constraints:** Write-capable behavior must be preview-first and bounded to
  active spec package files.
- **Performance Goals:** Suitable for phase-end use on one active package.

## Open Questions

| Question | Why it matters | Blocks design? |
|----------|----------------|----------------|
| Should the helper accept structured JSON input, infer from current package state, or both? | Determines CLI/MCP schema and tests. | yes |
| Which `verification.md` sections are safe to update mechanically? | Determines write scope and fallback behavior. | yes |
| Should phase completion depend on B031 phase gate output or merely compose with it when available? | Determines sequencing and coupling. | yes |

## Success Criteria

- **SC-001:** A phase-completion preview can show all intended task and
  verification updates without writing.
- **SC-002:** Write mode is explicit, bounded, and covered by regression tests.
- **SC-003:** Evidence quality remains visible; batch updates do not replace
  concrete proof.
- **SC-004:** Source and bundled plugin copies stay in sync after implementation.

## Related Artifacts

- Backlog: `docs/backlog/README.md` B050
- Design: not created yet
- Tasks: not created yet
- Verification: not created yet
