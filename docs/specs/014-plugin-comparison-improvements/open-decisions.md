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
| D001 | accepted | Should lifecycle triage be implemented as runtime/MCP, prompt-only, or skill-only? | Runtime/MCP tool; MCP prompt definition; skill-only guidance | Implement as MCP prompt plus skill guidance; defer deterministic runtime classification to backlog. | Keeps this slice additive and avoids runtime schema churn. |
| D002 | accepted | Which prompt aliases should ship first? | status/validate/complete; triage/status/validate/complete; status only | Ship `lifecycle-status`, `lifecycle-validate`, `lifecycle-complete`, and `lifecycle-triage`. | Prompt surface is explicit while remaining MCP-first and read-only. |
| D003 | accepted | Should lifecycle gates be structured runtime fields now? | Add fields now; document gates first; backlog runtime fields | Document gates first; route runtime phase-gate checks to backlog. | Avoids compatibility changes while preserving shared gate vocabulary. |
| D004 | accepted | Where should the durable comparison artifact live? | `docs/reference/`; `docs/design/`; `docs/reviews/spec-lifecycle-manager/` | Use `docs/reference/plugin-comparison-improvements.md`. | Makes comparison reusable durable reference material, not one-off review output. |
| D005 | accepted | Which external ideas are explicitly rejected in this spec? | Reject autonomous loops; reject docs-location replacement; reject full methodology import | Reject autonomous loops, docs-location replacement, and full methodology import; preserve bounded ideas in backlog. | Prevents scope creep and protects repository lifecycle conventions. |

## Decision Notes

- External plugin content is advisory research only.
- Any decision that adds write-capable MCP behavior must be split into a
  separate focused spec.
- Runtime lifecycle gate fields, workflow mode contracts, approval policies,
  Kiro import support, and hook-derived task audits are deferred to backlog
  items rather than implemented in this spec.
