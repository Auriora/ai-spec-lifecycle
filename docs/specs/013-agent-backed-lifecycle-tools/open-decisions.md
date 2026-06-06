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
| D002 | accepted | Inline schema in runtime, JSON schema file, separate Python schema module, prompt-adjacent schema | Use a separate Python schema module so validation stays dependency-free while keeping schema contracts out of the main runtime file. | T002, T004 |
| D003 | accepted | Disabled stub first, Codex subagent adapter, local command adapter, provider API adapter | Implement disabled stub plus runner interface first; defer a local Codex CLI adapter as the first real runner candidate. | T004 |
| D004 | accepted | No persistence, review-result files, closure evidence only | Persist review results in predefined docs locations under `docs/reviews/spec-lifecycle-manager/` during early dogfooding so outputs can be inspected and refined. | T007 |
