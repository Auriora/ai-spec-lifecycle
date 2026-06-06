---
title: Spec closure log management requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-05
---

# Requirements

## Introduction

This spec defines requirements for adding closure log and changelog-management
support to the `spec-lifecycle-manager` skill. The goal is to let Git preserve
the full historical state of closed spec packages while durable docs keep only
current behavior plus a compact, auditable closure record.

The desired workflow is:

1. Complete implementation, verification, and durable-doc promotion.
2. Record final closure evidence in the spec.
3. Commit the final spec state.
4. Add or update a durable spec closure log entry that points to that final
   spec commit.
5. Remove, archive, or retain the spec package according to lifecycle policy.
6. Commit the closure cleanup separately.

This preserves auditability without leaving completed implementation
scaffolding in the active docs path.

## Durable Source Baseline

Current durable sources:

- [Spec lifecycle management](../../design/spec-lifecycle-management.md)
- [Agent development lifecycle constitution](../../governance/constitution.md)
- [Spec lifecycle manager skill](../../../skills/spec-lifecycle-manager/SKILL.md)
- [Document routing and expert review](../../../skills/spec-lifecycle-manager/references/document-routing-and-expert-review.md)
- [Document lifecycle template](../../../skills/spec-lifecycle-manager/references/durable-doc-templates/document-lifecycle.md)
- [Verification spec template](../../../skills/spec-lifecycle-manager/references/spec-package/verification.md)

Documentation gap:

- The lifecycle requires durable promotion and spec cleanup, but it does not
  yet define a durable closure log that records the final spec commit before
  removal.
- The workflow does not yet distinguish an active spec index, a spec closure
  log, and a broader product/release changelog.
- The skill does not yet require a two-commit close pattern when removing a
  closed spec from the active docs tree.

Promotion target after implementation:

- Update [Spec lifecycle management](../../design/spec-lifecycle-management.md)
  with the closure-log model.
- Update `skills/spec-lifecycle-manager/SKILL.md` close guidance.
- Add a durable documentation template for the spec closure log.
- Update validation fixtures and evidence to cover Git-backed spec cleanup.

## Goals

- Define a durable spec closure log that records compact closure entries.
- Use Git commits as the archive for final full spec package state whenever the
  spec is removed from active docs.
- Prevent closed specs from remaining the only source of implemented behavior.
- Keep active spec indexes focused on current work.
- Keep closure logs distinct from product changelogs and release notes.
- Define skill and template updates needed to make closure-log management
  repeatable.

## Non-Goals

- Replace Git history with copied archived spec packages.
- Require every repository to delete closed specs.
- Turn the closure log into a full release changelog.
- Force repositories with existing archival or compliance rules to abandon
  them.
- Build automation for rewriting Git history or recovering deleted specs.

## Glossary

| Term | Meaning |
| --- | --- |
| Active spec index | A current-work index that lists specs still being implemented or reconciled. |
| Closure log | Durable append-only or chronologically maintained record of closed specs, their final-spec commits, durable promotions, and cleanup actions. |
| Final spec commit | The commit that contains the complete final spec package before removal or cleanup. |
| Closure cleanup commit | The commit that removes, archives, or marks the spec package historical and updates indexes/logs. |
| Product changelog | User- or release-oriented change history. It may draw from closure logs but has a different audience. |
| Spec archive | Retained full spec package, either in Git history or a repository archive path when policy requires visible historical docs. |

## Requirements

### Requirement 1: Record A Durable Closure Log

**User Story:** As a maintainer, I want a durable closure log for completed
specs, so that removed spec packages remain discoverable through Git history
and closure evidence.

#### Acceptance Criteria

1. GIVEN a spec is closed, WHEN the closure action removes or archives the
   package, THEN a closure log entry SHALL record the spec ID, title, closed
   date, final spec commit, closure action, durable destinations, verification
   summary, residual risks, and follow-up work.
2. GIVEN a final spec commit is recorded, WHEN a reader inspects the closure
   log, THEN the commit SHALL be sufficient to recover the final spec package
   from Git history.
3. IF a final spec commit is not available, THEN the closure log SHALL record
   the blocker and the spec SHALL NOT be removed from active docs.

### Requirement 2: Separate Active Index, Closure Log, And Changelog Roles

**User Story:** As a future agent, I want active specs, closed-spec history,
and product changelogs to be separate, so that I do not mistake archived
implementation scaffolding for current work.

#### Acceptance Criteria

1. GIVEN active work exists, WHEN the active spec index is read, THEN it SHALL
   list only active or intentionally retained implementation specs.
2. GIVEN a spec closes, WHEN the closure log is updated, THEN the active spec
   index SHALL no longer present the spec as current work.
3. WHERE product or release changelogs exist, THE SYSTEM SHALL treat them as
   separate durable documents that may reference closure-log entries but do not
   replace closure records.

### Requirement 3: Support A Two-Commit Removal Workflow

**User Story:** As a developer operator, I want a clean two-commit close
workflow, so that Git stores the final spec state before deletion or cleanup.

#### Acceptance Criteria

1. GIVEN a spec is ready to close, WHEN the package still exists with final
   evidence, THEN the operator SHALL commit that final state before removal.
2. GIVEN the final spec commit exists, WHEN cleanup proceeds, THEN the closure
   cleanup commit SHALL add or update the closure log and remove, archive, or
   mark the package historical.
3. IF repository policy requires retaining full archived specs in the current
   tree, THEN the closure action SHALL record `archived` or
   `retained-as-history` instead of `removed`.

### Requirement 4: Extend Skill Close Guidance

**User Story:** As an agent using the skill, I want closure-log instructions in
the close workflow, so that spec removal is auditable and current docs remain
clean.

#### Acceptance Criteria

1. GIVEN a close request, WHEN the skill evaluates closure readiness, THEN it
   SHALL check whether a closure log is required by the repository lifecycle.
2. GIVEN a spec package will be removed, WHEN closing, THEN the skill SHALL
   require a final spec commit hash before removal.
3. GIVEN a closure log entry is written, WHEN closure is complete, THEN the
   skill SHALL report the final spec commit, closure cleanup commit if known,
   durable docs, and residual risks.

### Requirement 5: Provide Closure Log Templates

**User Story:** As a repository maintainer, I want a closure-log template, so
that closure records are consistent across specs and easy for agents to parse.

#### Acceptance Criteria

1. GIVEN a repository has no closure-log template, WHEN the fallback durable
   templates are used, THEN a `spec-closure-log.md` template SHALL be
   available.
2. GIVEN a closure entry is added, WHEN the log is linted or reviewed, THEN
   required fields SHALL be visible and structured.
3. IF a repository already has an authoritative changelog or archival template,
   THEN the skill SHALL prefer that template and record the template authority
   decision.

### Requirement 6: Preserve Verification And Promotion Traceability

**User Story:** As a reviewer, I want closure entries to link verification and
promotion evidence, so that I can understand what changed without reopening the
full spec immediately.

#### Acceptance Criteria

1. GIVEN durable docs were updated, WHEN the closure entry is written, THEN it
   SHALL list each durable destination or documented deferral.
2. GIVEN validation was run or waived, WHEN the closure entry is written, THEN
   it SHALL summarize evidence and residual risk.
3. GIVEN follow-up work exists, WHEN the closure entry is written, THEN it
   SHALL link the issue, backlog item, roadmap item, or follow-up spec.

### Requirement 7: Avoid Stale Active Documentation

**User Story:** As a future agent, I want closed spec scaffolding removed from
the active knowledge path, so that implementation history does not override
durable current-state docs.

#### Acceptance Criteria

1. GIVEN a spec is closed and removed, WHEN docs indexes are read, THEN current
   behavior SHALL be discoverable from durable docs rather than the deleted
   spec path.
2. GIVEN a spec is retained as history, WHEN a reader opens it, THEN metadata
   and headings SHALL clearly mark it as historical, archived, or superseded.
3. IF durable promotion is blocked, THEN the spec SHALL remain active or be
   routed to an explicit blocker record rather than removed.

## Correctness Properties

- A removed spec has a recorded final spec commit before its removal commit.
- A closure log entry never replaces durable current-state documentation.
- Active spec indexes do not list removed specs as active work.
- Git-backed archival is used only when the final state exists in committed
  history.
- A closure log entry distinguishes removed, archived, and retained historical
  specs.

## Success Criteria

- A closure-log implementation plan exists.
- The skill close workflow includes final spec commit and closure cleanup
  guidance.
- Durable templates include a spec closure log template.
- Verification templates and document lifecycle guidance reference closure-log
  records.
- The active spec index, closure log, and product changelog roles are clearly
  separated.

## Open Questions

- Should the default closure log path be `docs/history/spec-closure-log.md`,
  `docs/changelog/spec-lifecycle.md`, or `docs/specs/closure-log.md`?
- Should the closure log be append-only, reverse-chronological, or generated
  from structured entries?
- Should closure cleanup commits be recorded after the fact by amending the
  closure log, or should the closure entry initially record only the final spec
  commit?
- Should a future MCP tool automate final-spec commit detection and closure-log
  validation?
