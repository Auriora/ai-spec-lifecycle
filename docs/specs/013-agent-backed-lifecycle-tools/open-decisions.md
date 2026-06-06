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
| D001 | accepted | `active_spec_preflight`, `agent_readiness_packet`, `no_active_spec_context`, `closure_risk_review`, `draft_traceability_matrix`, `promotion_draft` | Start with deterministic `active_spec_preflight`, `agent_readiness_packet`, and `no_active_spec_context`; defer cheap-agent execution until the context foundation is stable. | T001 |
| D002 | open | Inline schema in runtime, JSON schema file, prompt-adjacent schema | Prefer runtime-owned schema first to keep validation dependency-free. | T002 |
| D003 | open | Disabled stub first, Codex subagent adapter, local command adapter, provider API adapter | Prefer disabled stub plus interface first, then add a runner adapter after contract tests pass. | T004 |
| D004 | open | No persistence, review-result files, closure evidence only | Prefer no persistence for initial implementation unless user asks for audit history. | T007 |
