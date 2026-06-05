---
title: Backlog and roadmap templates design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Technical Design

## Overview

Add backlog and roadmap as fallback durable document classes. The skill will
route deferred work based on readiness and sequencing: vague or exploratory
work goes to backlog, scheduled or multi-stage work goes to roadmap, ready
implementation work becomes a focused spec or issue.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1, AC2, AC3 | Backlog template shape and README entry | Template inspection and spec lint |
| Requirement 2 | AC1, AC2, AC3 | Roadmap template shape and README entry | Template inspection and spec lint |
| Requirement 3 | AC1, AC2, AC3 | Skill routing guidance and durable lifecycle docs | Review `SKILL.md` and lifecycle docs |
| Requirement 4 | AC1, AC2, AC3 | Closure/promotion guidance and B001 backlog update | Verification evidence and backlog update |

## High-Level Design

### System Architecture

No runtime architecture changes are required. This is a documentation and skill
guidance change:

```text
active spec -> promotion/closure decision -> backlog | roadmap | issue | follow-up spec
```

The durable templates live in
`skills/spec-lifecycle-manager/references/durable-doc-templates/` and are
copied or adapted only when the target repository lacks authoritative planning
templates.

### Components and Changes

- Durable template README:
  Add backlog and roadmap document classes, storage guidance, and split rules.
- Backlog template:
  Provide item fields, status vocabulary, promotion links, and maintenance
  rules.
- Roadmap template:
  Provide horizons, milestones, dependencies, exit criteria, review cadence,
  and decision notes.
- Skill guidance:
  Clarify deferred-work routing during promotion and closure.
- Durable lifecycle docs:
  Explain backlog/roadmap roles and the boundary with active specs and closure
  logs.

### Data Models

Backlog item fields:

| Field | Purpose |
|-------|---------|
| ID | Stable backlog item identifier. |
| Status | proposed, accepted, in-progress, promoted, done, deferred, dropped. |
| Topic | Short item title. |
| Source | Spec, review, closure log, user request, or issue that created it. |
| Owner | Role or team accountable for next action. |
| Priority | Relative urgency or sequencing hint. |
| Target | Follow-up spec, issue, roadmap item, or durable doc destination. |
| Notes | Concise context and next action. |

Roadmap item fields:

| Field | Purpose |
|-------|---------|
| Horizon | now, next, later, or date/milestone. |
| Status | proposed, planned, active, complete, deferred, dropped. |
| Outcome | Planned outcome or capability. |
| Dependencies | Backlog items, specs, issues, decisions, or external prerequisites. |
| Exit Criteria | Observable condition for completion. |
| Owner | Role or team accountable for delivery. |
| Evidence | Linked spec, closure log, review, or release evidence. |

### Data Flow

1. During promotion or closure, identify deferred work.
2. Classify the deferred work by readiness and sequencing:
   - not ready or exploratory -> backlog;
   - sequencing/milestone/adoption concern -> roadmap;
   - ready and scoped -> follow-up spec or issue;
   - external tracker owned -> issue tracker, with a link from backlog or
     roadmap when useful.
3. Record the destination in task evidence, verification, closure log, or
   durable docs.

## Low-Level Design

### Algorithms and Logic

```text
function route_deferred_work(item):
    if item.has_clear_scope and item.has_acceptance_criteria:
        return "follow-up spec or issue"
    if item.has_schedule_or_stage_dependency:
        return "roadmap"
    if item.is_external_tracker_owned:
        return "issue tracker"
    return "backlog"
```

### Function Signatures and Interfaces

No code interfaces change. Markdown templates are the interface.

### Error Handling

Ambiguous deferred work should be recorded in backlog with a next-action note
rather than being dropped or treated as a ready implementation task.

### Security, Trust, and Access

No new command execution, credentials, network access, or untrusted-input
handling is introduced.

### Migration and Compatibility

Repository-specific backlog, roadmap, product-planning, and issue-tracking
systems remain authoritative. The fallback templates are opt-in references.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| `spec_runtime.py lint docs/specs/006-backlog-roadmap-templates` | Spec package shape | `verification.md` | none expected |
| `spec_runtime.py closure-check docs/specs/006-backlog-roadmap-templates` | Promotion and closure readiness | `verification.md` | none expected |
| `python3 -m unittest discover -s tests -p 'test_*.py'` | Runtime regression | `verification.md` | none expected |
| Manual template review | Requirements 1-4 | `verification.md` | Templates are guidance, not enforcement |

## Operational Considerations

After commit, sync the skill into `~/.codex/skills/spec-lifecycle-manager/` so
new sessions see the templates and routing guidance.

## Open Questions

- None for the MVP.

## Related Artifacts

- Requirements: requirements.md
- Tasks: tasks.md
- Traceability: traceability.md
- Verification: verification.md
