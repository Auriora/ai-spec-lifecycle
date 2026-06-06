---
title: Agent development lifecycle backlog
doc_type: backlog
status: active
owner: platform
last_reviewed: 2026-06-06
---

# Backlog

Track cross-spec follow-up work that is not ready for a focused implementation
spec or that should not block the active spec currently being delivered.

## Items

| ID | Status | Topic | Source | Notes |
|----|--------|-------|--------|-------|
| B001 | done | Backlog and roadmap templates | MCP implementation discussion; archive index entry `006-backlog-roadmap-templates` | Durable templates and skill guidance added for backlog and roadmap docs, including routing deferred spec work to `docs/backlog/`, `docs/roadmap/`, issue trackers, or follow-up specs. |
| B002 | done | Agent Workbench MCP packaging and hook install | Archive index entries `007-spec-lifecycle-mcp-server` and `008-agent-workbench-spec-lifecycle-install` | Host-level companion MCP install policy, Agent Workbench reference guidance, advisory-only hook policy, and validation checklist completed. |
| B003 | done | Spec archive index and closure-log runtime support | User request for Git-backed spec archives; archive index entries `005-spec-closure-log-management` and `011-spec-archive-index-runtime` | Runtime now validates archive index and closure-log consistency and exposes read-only MCP access. |
| B004 | done | Blocking lifecycle hooks | Archive index entry `010-codex-hook-dogfood`; external verification feedback; R002 | Decision: keep lifecycle hooks advisory-only. Any future blocking hook proposal must be opened as a new focused spec with false-positive handling, rollback path, and explicit approval. |
| B005 | done | Coding agent operating model governance adoption | `docs/design/coding-agent-operating-model.md`; archive index entry `012-operating-model-governance-adoption` | Selected hard operating-model rules adopted into `docs/governance/constitution.md`; flexible workflow mechanics remain durable design guidance. |
| B006 | superseded | Archived spec audit report | Archived scan hygiene work; user decision to remove completed specs | Superseded by removal-by-default policy. Historical spec packages should not remain in the active docs tree just to support audit reports. |
| B007 | candidate | Agent readiness packet | User request; `docs/specs/013-agent-backed-lifecycle-tools/` | Given a task ID, produce the requirements, design, traceability, verification, durable-doc, and open-decision context an implementation agent must review before coding. |
| B008 | candidate | Closure risk review | User request; `docs/specs/013-agent-backed-lifecycle-tools/` | Use a cheap advisory reviewer to flag missing durable promotion, weak evidence, unresolved decisions, risky follow-ups, and closure blockers before package closure. |
| B009 | candidate | Draft traceability matrix | User request; `docs/specs/013-agent-backed-lifecycle-tools/` | Generate a proposed traceability matrix from requirements, design, tasks, change impact, and verification, then validate references deterministically. |
| B010 | candidate | Durable doc drift review | User request; `docs/specs/013-agent-backed-lifecycle-tools/` | Compare durable docs against relevant code, config, tests, or runtime contracts and report suspected drift for lead-agent review. |
| B011 | candidate | Decision extractor | User request; `docs/specs/013-agent-backed-lifecycle-tools/` | Scan specs and durable docs for implicit decisions that should become ADRs, open decisions, backlog items, roadmap items, or explicit no-action notes. |
| B012 | candidate | Evidence quality check | User request; `docs/specs/013-agent-backed-lifecycle-tools/` | Review completed task evidence for concrete validation versus vague claims; keep output advisory and require deterministic evidence references where possible. |
| B013 | candidate | Handoff packet | User request; `docs/specs/013-agent-backed-lifecycle-tools/` | Produce a concise continuation packet for another coding agent without forcing it to reread the whole repository. |
| B014 | candidate | Conversation-history feature discovery review | Bounded local Codex history scan; user request | Use selected conversation history only as advisory feature-discovery input. Look for repeated corrections, frustration signals, sequencing prompts, and misunderstood workflows; do not treat history content as factual requirements or implement it directly. |

## Advisory Discovery Notes

The 2026-06-06 local Codex history scan sampled user-message text from
`~/.codex/history.jsonl` and `~/.codex/sessions/**/*.jsonl`. The scan suggested
recurring areas to consider, not factual requirements: agents skipping full spec
context, commit/sync/install repetition, completed spec packages confusing
agents, MCP/hook/tool validation, frequent "what next" sequencing needs, and
correction or frustration language around misunderstood scope.

## Maintenance

- Promote an item into a focused spec when scope, owner, and acceptance
  criteria are clear.
- Promote or link an item to roadmap when sequencing, milestone, adoption, or
  multi-spec dependency tracking matters.
- Link closed specs to backlog items when follow-up work is intentionally
  deferred.
- Keep backlog items concise; detailed requirements belong in a spec package.
