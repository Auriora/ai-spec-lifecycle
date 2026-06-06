---
title: Agent-backed lifecycle tools open decisions
doc_type: spec
artifact_type: open-decisions
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Open Decisions

| Decision | Status | Options | Recommendation | Needed By |
|----------|--------|---------|----------------|-----------|
| D001 | open | `closure_risk_review`, `draft_traceability_matrix`, `promotion_draft`, `agent_readiness_packet` | Start with `closure_risk_review` if closure quality is the priority, or `draft_traceability_matrix` if implementation context quality is the priority. | T001 |
| D002 | open | Inline schema in runtime, JSON schema file, prompt-adjacent schema | Prefer runtime-owned schema first to keep validation dependency-free. | T002 |
| D003 | open | Disabled stub first, Codex subagent adapter, local command adapter, provider API adapter | Prefer disabled stub plus interface first, then add a runner adapter after contract tests pass. | T004 |
| D004 | open | No persistence, review-result files, closure evidence only | Prefer no persistence for initial implementation unless user asks for audit history. | T007 |
