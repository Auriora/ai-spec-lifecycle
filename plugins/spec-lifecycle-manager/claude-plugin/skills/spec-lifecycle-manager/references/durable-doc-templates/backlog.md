---
title: Backlog template
doc_type: backlog
status: draft
owner: team-or-person
last_reviewed: YYYY-MM-DD
---

# Backlog

Use this template for proposed or deferred work that is not yet ready to become
a focused implementation spec. Keep entries concise; detailed requirements,
design, and validation plans belong in a spec package once the work is ready.

## Scope

- **Backlog owner:**
- **Decision cadence:**
- **Planning system authority:** this document | issue tracker | product tool |
  other
- **Related roadmap:** `docs/roadmap/README.md` | none

## Items

| ID | Status | Topic | Source | Owner | Priority | Target | Notes |
|----|--------|-------|--------|-------|----------|--------|-------|
| B001 | proposed | Short title | Spec, closure log, review, user request, or issue | Role | low/medium/high | follow-up spec, issue, roadmap item, durable doc, or TBD | Concise context and next action. |

## Status Values

| Status | Meaning |
|--------|---------|
| proposed | Captured but not accepted for planning. |
| accepted | Worth doing, but not yet scheduled or scoped as an implementation spec. |
| in-progress | Being clarified, routed, or actively planned. |
| promoted | Converted into a focused spec, issue, or roadmap item. |
| done | Completed without needing an active backlog entry. |
| deferred | Intentionally postponed; keep reason and review trigger in notes. |
| dropped | No longer planned; keep reason in notes. |

## Routing Rules

- Use backlog when work is useful but lacks enough scope, acceptance criteria,
  or timing to become an active spec.
- Promote to a follow-up spec when the item has clear requirements, design
  direction, acceptance criteria, and validation expectations.
- Promote or link to roadmap when the item affects sequencing, milestones,
  adoption stages, or multi-spec dependencies.
- Use an issue tracker when the repository treats issues as the authoritative
  planning system; keep the issue link in `Target`.
- Link closure-log entries to backlog items when closed specs defer work that
  should remain visible.

## Maintenance

- Review open items on the documented cadence.
- Keep one primary destination in `Target`; use notes for cross-links.
- Remove or mark stale items instead of letting them become hidden active work.
- Do not use the backlog as the source of truth for implemented behavior.

## Related Artifacts

- Roadmap:
- Spec closure log:
- Active specs:
