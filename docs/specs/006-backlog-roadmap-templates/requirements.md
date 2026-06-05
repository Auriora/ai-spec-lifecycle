---
title: Backlog and roadmap templates requirements
doc_type: spec
artifact_type: requirements
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Requirements

## Introduction

This spec implements backlog item B001 by adding durable backlog and roadmap
templates plus skill guidance for routing deferred work. The goal is to make
follow-up work visible without turning every idea into an active
implementation spec.

## Goals

- Add fallback durable templates for backlog and roadmap documents.
- Clarify when deferred work belongs in a backlog, roadmap, issue tracker, or
  follow-up spec.
- Promote the guidance into the skill and durable lifecycle docs.
- Keep backlog and roadmap documents distinct from temporary spec packages.

## Non-Goals

- Implement an issue tracker integration.
- Create project-planning automation beyond template and guidance updates.
- Replace repository-specific backlog, roadmap, or product planning systems.

## Glossary

| Term | Definition |
|------|------------|
| Backlog | Durable list of proposed or deferred work that is not yet a focused implementation spec. |
| Roadmap | Durable sequencing view for planned work, milestones, dependencies, or adoption stages. |
| Follow-up spec | A new active implementation package created when deferred work has enough scope and acceptance criteria to implement. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/backlog/README.md` | Contains B001 and basic backlog maintenance guidance. | high | Needs template backing and routing guidance. |
| `docs/design/spec-lifecycle-management.md` | Routes deferred implementation work to backlog or follow-up specs. | high | Does not yet describe roadmap or issue tracker boundaries. |
| `skills/spec-lifecycle-manager/SKILL.md` | Promotion and closure guidance routes deferred work to backlog, roadmap, issue tracker, or follow-up specs. | high | Needs clearer selection rules. |
| `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md` | Lists supported durable document classes. | high | Does not yet include backlog or roadmap templates. |

## Requirements

### Requirement 1: Durable Backlog Template

**User Story:** As a maintainer, I want a durable backlog template, so that
deferred work can be recorded consistently without creating premature specs.

#### Acceptance Criteria

1. GIVEN a repository has no authoritative backlog template, WHEN the skill
   fallback templates are used, THEN a backlog template SHALL provide item
   fields for ID, status, topic, source, owner, priority, target, and notes.
2. GIVEN a backlog item is promoted, WHEN it becomes implementable, THEN the
   template SHALL show how to link it to a follow-up spec, issue, or roadmap
   entry.
3. IF a backlog item is too vague to implement, THEN the template SHALL keep it
   concise and avoid pretending it is an active spec.

### Requirement 2: Durable Roadmap Template

**User Story:** As a process owner, I want a durable roadmap template, so that
sequenced lifecycle work can be planned without overloading the backlog.

#### Acceptance Criteria

1. GIVEN staged lifecycle work, WHEN a roadmap is created, THEN it SHALL include
   horizons, status, dependencies, target specs or issues, and exit criteria.
2. WHERE a roadmap item depends on backlog items or specs, THE SYSTEM SHALL
   provide fields to link those dependencies.
3. IF roadmap plans change, THEN the template SHALL support review notes and
   decision history without becoming a product changelog.

### Requirement 3: Routing Guidance

**User Story:** As an implementation agent, I want explicit routing rules for
deferred work, so that I choose backlog, roadmap, issue, or follow-up spec
appropriately during promotion and closure.

#### Acceptance Criteria

1. GIVEN deferred work lacks clear acceptance criteria, WHEN it is recorded,
   THEN it SHALL be routed to backlog.
2. GIVEN deferred work has scheduling, sequencing, or milestone implications,
   WHEN it is recorded, THEN it SHALL be routed to roadmap or linked from the
   roadmap.
3. GIVEN deferred work is ready to implement, WHEN it is recorded, THEN it
   SHALL be promoted into a focused follow-up spec or repository issue.

### Requirement 4: Lifecycle Integration

**User Story:** As a documentation maintainer, I want backlog and roadmap docs
integrated into lifecycle guidance, so that closure and promotion remain
consistent.

#### Acceptance Criteria

1. GIVEN a spec closes with deferred work, WHEN closure evidence is recorded,
   THEN it SHALL identify the backlog, roadmap, issue, or follow-up spec
   destination.
2. GIVEN durable template guidance is consulted, WHEN backlog or roadmap docs
   are needed, THEN the templates SHALL be discoverable from the durable
   templates README.
3. GIVEN this repository's backlog B001 is implemented, WHEN the backlog is
   updated, THEN B001 SHALL no longer appear as unpromoted work.

## Correctness Properties

- **CP-001**: Backlog and roadmap templates are durable document templates, not
  spec-package templates.
- **CP-002**: Deferred work has exactly one primary destination: backlog,
  roadmap, issue tracker, or follow-up spec, with cross-links where useful.
- **CP-003**: Closing a spec does not silently discard deferred work.

## Technical Context

- **Language/Version:** Markdown documentation and Python runtime validation.
- **Primary Dependencies:** `spec_runtime.py` linter and closure-check.
- **Target Platform:** Local repository and installed Codex skill.
- **Constraints:** Repository-specific planning systems remain authoritative.
- **Performance Goals:** Not applicable.

## Success Criteria

- **SC-001**: Backlog and roadmap templates exist and are listed in the durable
  templates README.
- **SC-002**: Skill guidance tells agents how to choose backlog, roadmap,
  issue tracker, or follow-up spec destinations.
- **SC-003**: Spec 006 lints clean and closure-check reports ready.

## Related Artifacts

- Design: design.md
- Tasks: tasks.md
- Traceability: traceability.md
- Verification: verification.md
