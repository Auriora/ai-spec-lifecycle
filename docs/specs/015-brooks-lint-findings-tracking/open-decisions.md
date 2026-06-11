---
title: Brooks-Lint findings tracking open decisions
doc_type: spec
artifact_type: open-decisions
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Open Decisions

| ID | Decision | Options | Needed By | Status | Rationale |
|----|----------|---------|-----------|--------|-----------|
| D001 | Register validation mode | Markdown-only first; add runtime validation now; JSON register | Before T004 | accepted | Use Markdown-only first. The register is still stabilizing, the seeded findings can be maintained through documented rules, and runtime validation should wait until repeated Brooks runs show real drift. |
| D002 | Brooks history file treatment | Commit `.brooks-lint-history.json`; ignore it; document as optional local telemetry | Before T002 | accepted | Treat `.brooks-lint-history.json` as optional supporting score-history evidence. It may remain tracked when present, but `docs/reviews/brooks-lint/README.md` is the durable source of finding truth and must remain useful if score history is unavailable. |
| D003 | Deferred finding routing | Backlog immediately; backlog only at spec closure; roadmap for multi-step work only | Before T005 | accepted | Route accepted and deferred findings before spec closure. Use existing backlog and roadmap items where they already cover the work; add new candidate backlog items only for uncovered durable follow-up. |
| D004 | Finding ID namespace | Mode-specific prefixes; one global sequence | Before T001 | accepted | Use mode-specific prefixes such as `BL-ARCH-001`, `BL-DEBT-001`, `BL-HEALTH-001`, and `BL-TEST-001` to avoid collisions across Brooks modes while preserving mode context. |
