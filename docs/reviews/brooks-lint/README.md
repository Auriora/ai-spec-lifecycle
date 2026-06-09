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

Seed findings from the first Brooks architecture, debt, health, and test-quality
passes will be added by the active implementation spec after this schema is in
place.

## Maintenance Rules

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
