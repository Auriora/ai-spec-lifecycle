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
| B003 | promoted | Spec archive index and closure-log runtime support | User request for Git-backed spec archives; `docs/specs/005-spec-closure-log-management/` residual risk | Promoted to `docs/specs/011-spec-archive-index-runtime/` to add a durable archive index/check surface before removing any retained spec packages. |
| B004 | deferred | Blocking lifecycle hooks | `docs/specs/010-codex-hook-dogfood/`; closure log residual risks | Revisit only after advisory hook noise is low across repeated real edits. Target: roadmap item R002. |
| B005 | accepted | Coding agent operating model governance adoption | `docs/design/coding-agent-operating-model.md` | Consider a governance update only if the operating model becomes mandatory policy rather than durable guidance. Target: roadmap item R003. |
| B006 | proposed | Archived spec audit report | Archived scan hygiene work; default scan now excludes archived authoring lint | Add an explicit audit/report flow if historical package modernization becomes useful; do not migrate old records by default. |

## Maintenance

- Promote an item into a focused spec when scope, owner, and acceptance
  criteria are clear.
- Promote or link an item to roadmap when sequencing, milestone, adoption, or
  multi-spec dependency tracking matters.
- Link closed specs to backlog items when follow-up work is intentionally
  deferred.
- Keep backlog items concise; detailed requirements belong in a spec package.
