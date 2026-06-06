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
| B001 | done | Backlog and roadmap templates | MCP implementation discussion; `docs/specs/006-backlog-roadmap-templates/` | Durable templates and skill guidance added for backlog and roadmap docs, including routing deferred spec work to `docs/backlog/`, `docs/roadmap/`, issue trackers, or follow-up specs. |
| B002 | done | Agent Workbench MCP packaging and hook install | `docs/specs/007-spec-lifecycle-mcp-server/`; `docs/specs/008-agent-workbench-spec-lifecycle-install/` | Host-level companion MCP install policy, Agent Workbench reference guidance, advisory-only hook policy, and validation checklist completed. |
| B003 | done | Spec archive index and closure-log runtime support | User request for Git-backed spec archives; `docs/specs/005-spec-closure-log-management/` residual risk | Completed in `docs/specs/011-spec-archive-index-runtime/`; runtime now validates archive index and closure-log consistency and exposes read-only MCP access. |
| B004 | done | Blocking lifecycle hooks | `docs/specs/010-codex-hook-dogfood/`; external verification feedback; R002 | Decision: keep lifecycle hooks advisory-only. Any future blocking hook proposal must be opened as a new focused spec with false-positive handling, rollback path, and explicit approval. |
| B005 | done | Coding agent operating model governance adoption | `docs/design/coding-agent-operating-model.md`; `docs/specs/012-operating-model-governance-adoption/` | Selected hard operating-model rules adopted into `docs/governance/constitution.md`; flexible workflow mechanics remain durable design guidance. |
| B006 | proposed | Archived spec audit report | Archived scan hygiene work; default scan now excludes archived authoring lint | Add an explicit audit/report flow if historical package modernization becomes useful; do not migrate old records by default. |

## Maintenance

- Promote an item into a focused spec when scope, owner, and acceptance
  criteria are clear.
- Promote or link an item to roadmap when sequencing, milestone, adoption, or
  multi-spec dependency tracking matters.
- Link closed specs to backlog items when follow-up work is intentionally
  deferred.
- Keep backlog items concise; detailed requirements belong in a spec package.
