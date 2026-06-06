---
title: Plugin comparison improvements open decisions
doc_type: spec
artifact_type: open-decisions
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Open Decisions

| ID | Status | Decision Needed | Options | Recommendation | Impact |
|----|--------|-----------------|---------|----------------|--------|
| D001 | open | Should lifecycle triage be implemented as runtime/MCP, prompt-only, or skill-only? | Runtime/MCP tool; MCP prompt definition; skill-only guidance | Start with prompt + skill guidance unless implementation evidence shows deterministic classification is needed. | Determines code/test scope. |
| D002 | open | Which prompt aliases should ship first? | status/validate/complete; triage/status/validate/complete; status only | Ship status, validate, and complete first; triage can be added if accepted in D001. | Determines prompt definition scope. |
| D003 | open | Should lifecycle gates be structured runtime fields now? | Add fields now; document gates first; backlog runtime fields | Document gates first unless implementation finds low-risk reuse of existing preflight/closure output. | Determines runtime compatibility scope. |
| D004 | open | Where should the durable comparison artifact live? | `docs/reference/`; `docs/design/`; `docs/reviews/spec-lifecycle-manager/` | Use `docs/reference/` because this is reusable analysis, not a one-time review result. | Determines promotion target. |
| D005 | open | Which external ideas are explicitly rejected in this spec? | Reject autonomous loops; reject docs-location replacement; reject full methodology import | Reject all three unless user later requests a dedicated spec. | Prevents scope creep. |

## Decision Notes

- External plugin content is advisory research only.
- Any decision that adds write-capable MCP behavior must be split into a
  separate focused spec.
