---
title: Spec lifecycle manager skill
doc_type: spec
status: archived
owner: platform
last_reviewed: 2026-06-01
---

# Feature Specification

## Summary

Create a reusable Codex skill that helps agents manage implementation specs from intake through reconciliation, implementation, durable documentation promotion, expert review, and spec closure.

The skill must be generic across repositories while assuming active spec packages use `docs/specs/[###-slug]/` unless a repository documents an equivalent location.

## Problem

AI agents often treat implementation specs as permanent truth. This creates drift: completed behavior stays in temporary specs, durable docs become stale, task checkboxes do not reflect verification, and reviewers cannot tell which expert roles should inspect each document or whole spec package.

The process needs a reusable skill that makes specs useful while work is active, then rolls accepted content into durable repository docs and closes the spec.

## Goals

- Provide a generic spec lifecycle workflow for AI coding agents.
- Keep specs, durable docs, code, tests, and config consistent.
- Use `docs/specs/[###-slug]/` as the default active spec package convention.
- Require reconciliation when it adds clear implementation or documentation value.
- Route accepted spec content into durable docs before spec closure.
- Define role-based expert review guidance for document classes and whole-package review.
- Support task completion states where automated tests pass, alternate verification is recorded, or work remains explicitly unverified.

## Non-Goals

- Creating a subject-matter-specific workflow for one product domain.
- Replacing repository-specific AGENTS.md, coding standards, test commands, or documentation templates.
- Forcing every small task through a heavyweight planning ceremony.
- Requiring automated tests for tasks that are inherently documentation-only, decision-only, exploratory, or externally verified.

## Requirements

### Functional Requirements

- **FR-001**: The skill MUST identify active spec packages using `docs/specs/[###-slug]/` by default.
- **FR-002**: The skill MUST inspect repository-specific instructions and document structure before assuming durable doc locations.
- **FR-003**: The skill MUST treat specs as temporary implementation control documents, not final durable truth.
- **FR-004**: The skill MUST reconcile specs against durable docs, code, tests, and config when resuming a spec, when evidence is stale or partial, or when the change affects cross-cutting contracts.
- **FR-005**: The reconciliation output MUST classify drift as spec stale, code incomplete, durable docs stale, decision unresolved, implemented but unverified, or intentionally deferred.
- **FR-006**: The skill MUST select coherent implementation slices from task phases, checkpoints, user stories, or requirement groups.
- **FR-007**: The skill MUST map validation back to task IDs, requirements, acceptance criteria, success criteria, or documented review criteria where practical.
- **FR-008**: The skill MUST update task checkboxes only when completion criteria are met.
- **FR-009**: The skill MUST allow non-automated verification when appropriate, but MUST record the method and residual risk.
- **FR-010**: The skill MUST route lasting spec content into the correct durable document class before closure.
- **FR-011**: The skill MUST include role-based expert review guidance for individual document classes and whole spec packages.
- **FR-012**: The skill MUST require closure checks so completed behavior does not remain documented only in `docs/specs/`.
- **FR-013**: The skill MUST remain concise enough to load as a Codex skill without consuming excessive context.
- **FR-014**: The canonical skill package MUST be tracked in the repository under `skills/spec-lifecycle-manager/`; any copy under `~/.codex/skills/` is an installed artifact.
- **FR-015**: The skill MUST include fallback spec-package templates and MUST prefer repository-provided templates or documentation direction when present.
- **FR-016**: The skill MUST assume only the active spec package path `docs/specs/[###-slug]/` and MUST discover durable documentation locations from each target repository.

### Key Entities

- **Spec package**: A temporary active implementation package under `docs/specs/[###-slug]/`.
- **Durable docs**: Current-state documentation such as requirements, architecture, design, API, data-flow, runbook, ADR, reference, backlog, and review docs.
- **Reconciliation summary**: A concise comparison of spec claims, durable docs, code, tests, and config.
- **Promotion target**: The durable doc location where accepted spec content should live after implementation.
- **Expert role**: A process or system review perspective such as systems architect, software architect, developer process expert, senior developer, QA/test strategy expert, operations/SRE expert, security/compliance expert, documentation architect, API/contract expert, data/integration architecture expert, or product/requirements analyst.

## Acceptance Criteria

1. **Given** a repository with `docs/specs/001-example/`, **When** the skill is invoked to continue work, **Then** it finds the active spec package and reads the relevant spec artifacts before editing code.
2. **Given** an existing partially completed spec, **When** implementation resumes, **Then** the skill produces a useful reconciliation summary before selecting work.
3. **Given** a small new implementation task with a fresh spec and no conflicting docs, **When** reconciliation would add no value, **Then** the skill may keep reconciliation brief and proceed.
4. **Given** a completed implementation task with passing tests, **When** updating `tasks.md`, **Then** the task can be checked complete and validation evidence recorded.
5. **Given** a documentation-only or externally verified task, **When** no automated test applies, **Then** the task can be marked complete only with the alternate verification method and residual risk.
6. **Given** accepted spec content affects durable docs, **When** the implementation is complete, **Then** the skill routes updates into requirements, design, architecture, API, data-flow, runbook, ADR, reference, backlog, or review docs as appropriate.
7. **Given** a spec is ready to close, **When** closure is reviewed, **Then** no accepted current behavior remains documented only in the active spec package.
8. **Given** a document is created or updated, **When** review guidance is needed, **Then** the skill identifies the relevant role-based expert reviews.
9. **Given** a repository has spec-package templates, **When** a new spec package is created, **Then** the skill uses those repository templates before falling back to bundled templates.

## User Scenarios And Testing

### User Story 1 - Continue An Active Spec (Priority: P1)

An agent needs to continue implementation from an existing spec package without losing track of code/doc drift.

**Why this priority**: This is the primary use case for avoiding stale specs and unsafe task checkbox updates.

**Independent Test**: Apply the skill to a fixture spec with mismatched tasks, docs, and code evidence; verify the skill instructs the agent to reconcile and classify drift before implementation.

### User Story 2 - Promote Completed Spec Content (Priority: P1)

An agent needs to move accepted behavior from a completed spec into durable docs before closing the spec.

**Why this priority**: It ensures the repository's current-state documentation remains the long-term source of truth.

**Independent Test**: Apply the skill to a completed fixture spec and verify it produces routing guidance for requirements, design, runbook, ADR, API, data-flow, reference, backlog, and review content.

### User Story 3 - Expert Review Routing (Priority: P2)

An agent needs to identify role-based reviewers for changed documents and the whole spec package.

**Why this priority**: It helps review the process and system shape without relying on feature-specific subject-matter expertise.

**Independent Test**: Apply the skill to a spec that touches API, runbook, design, and data-flow docs; verify it recommends the correct expert role set.

### User Story 4 - Create Or Start A New Spec (Priority: P2)

An agent needs to start a new generic spec package using the `[###-slug]` format.

**Why this priority**: The lifecycle begins at intake, and the skill should help create well-formed specs rather than only recover stale ones.

**Independent Test**: Ask the skill to start a new spec and verify it uses the default package shape and records durable doc inputs, review roles, validation criteria, and promotion targets.

## Edge Cases

- Repository uses equivalent doc classes but different folder names.
- No `docs/` folder exists yet.
- Spec package exists but lacks `tasks.md` or `design.md`.
- Durable docs conflict with code and neither is obviously authoritative.
- Tests cannot be run locally due to missing services, network restrictions, or credentials.
- A task is completed by documentation review, ADR acceptance, or external validation rather than automated tests.
- A spec contains subject-matter decisions that need user or stakeholder input outside the generic expert roles.
- Closure would remove useful decision history that belongs in an ADR or history note.

## Success Criteria

- **SC-001**: The skill body is concise and references supporting docs only when needed.
- **SC-002**: The skill can guide implementation in repositories using `docs/specs/[###-slug]/` without product-specific assumptions.
- **SC-003**: The skill distinguishes active implementation specs from durable docs.
- **SC-004**: The skill includes clear reconciliation, promotion, expert review, and closure rules.
- **SC-005**: The first implementation includes validation passes against one mature documentation repository and one smaller agent-runtime repository.

## Validation Targets

Use representative repositories to validate that the skill handles both a
mature product documentation system and a smaller agent-runtime repository:

| Repository class | Validation focus |
| --- | --- |
| Mature documentation repository | Mature docs/spec lifecycle, broad durable documentation classes, active and completed spec packages, data-flow/API/runbook/ADR promotion pressure. |
| Smaller agent-runtime repository | Portability across a different repository, active `docs/specs/[###-slug]/` package, runtime docs, and local agent-development workflow. |

Expected validation evidence:

- active spec package detected;
- repository-specific instructions and durable docs identified;
- concise reconciliation summary produced when useful;
- next coherent task slice selected;
- durable documentation promotion targets listed;
- relevant expert review roles recommended;
- closure blockers or follow-up actions identified.

## Related Artifacts

- Design: [../../design/spec-lifecycle-management.md](../../design/spec-lifecycle-management.md)
- Review matrix: [../../reference/document-routing-and-expert-review-matrix.md](../../reference/document-routing-and-expert-review-matrix.md)
- Plan: [plan.md](plan.md)
- Tasks: [tasks.md](tasks.md)
