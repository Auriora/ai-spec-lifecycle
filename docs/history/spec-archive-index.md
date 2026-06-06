---
title: Spec archive index
doc_type: history
status: active
owner: platform
last_reviewed: 2026-06-06
---

# Spec Archive Index

This index is the compact lookup surface for closed implementation spec package
archive state. The closure log remains the narrative history with verification
summaries and residual risks; this index records the fields runtime tools need
to verify retained or removed package evidence.

## Entries

| Spec ID | Title | Package path | Status | Final spec commit | Cleanup commit | Closure action | Durable destinations | Verification |
|---------|-------|--------------|--------|-------------------|----------------|----------------|----------------------|--------------|
| 012-operating-model-governance-adoption | Operating model governance adoption | `docs/specs/012-operating-model-governance-adoption/` | retained | `2d17440` | pending | retained-as-history | `docs/governance/constitution.md`; `docs/design/coding-agent-operating-model.md`; `docs/backlog/README.md`; `docs/roadmap/README.md` | `docs/specs/012-operating-model-governance-adoption/verification.md`; `docs/history/spec-closure-log.md` |
| 011-spec-archive-index-runtime | Spec archive index runtime | `docs/specs/011-spec-archive-index-runtime/` | retained | `4712010` | `25dc62e` | retained-as-history | `docs/history/spec-archive-index.md`; `docs/design/spec-lifecycle-management.md`; `docs/reference/spec-lifecycle-runtime.md`; `docs/backlog/README.md`; `docs/roadmap/README.md`; `docs/README.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | `docs/specs/011-spec-archive-index-runtime/verification.md`; `docs/history/spec-closure-log.md` |
| 003-coding-agent-operating-model | Coding agent operating model | `docs/specs/003-coding-agent-operating-model/` | retained | `7ee157b` | `a86eaec` | retained-as-history | `docs/design/coding-agent-operating-model.md`; `docs/reference/coding-agent-workflow-research.md`; `docs/README.md` | `docs/specs/003-coding-agent-operating-model/verification.md`; `docs/history/spec-closure-log.md` |
| 010-codex-hook-dogfood | Codex hook dogfood | `docs/specs/010-codex-hook-dogfood/` | retained | `d1eb6b3` | `59b7120` | retained-as-history | `docs/reference/spec-lifecycle-runtime.md`; `docs/reference/spec-lifecycle-manager-mcp-install.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py` | `docs/specs/010-codex-hook-dogfood/verification.md`; `docs/history/spec-closure-log.md` |
| 002-spec-lifecycle-validation | Spec lifecycle validation | `docs/specs/002-spec-lifecycle-validation/` | retained | `d1eb6b3` | `59b7120` | retained-as-history | `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/references/spec-package/`; `skills/spec-lifecycle-manager/references/durable-doc-templates/` | `docs/specs/002-spec-lifecycle-validation/verification.md`; `docs/history/spec-closure-log.md` |
| 009-archived-spec-scan-hygiene | Archived spec scan hygiene | `docs/specs/009-archived-spec-scan-hygiene/` | retained | `1095b7f` | `ccba3e9` | retained-as-history | `docs/reference/spec-lifecycle-runtime.md`; `docs/design/spec-lifecycle-management.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | `docs/specs/009-archived-spec-scan-hygiene/verification.md`; `docs/history/spec-closure-log.md` |
| 006-backlog-roadmap-templates | Backlog and roadmap templates | `docs/specs/006-backlog-roadmap-templates/` | retained | `1095b7f` | `ccba3e9` | retained-as-history | `skills/spec-lifecycle-manager/references/durable-doc-templates/backlog.md`; `skills/spec-lifecycle-manager/references/durable-doc-templates/roadmap.md`; `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md`; `skills/spec-lifecycle-manager/SKILL.md`; `docs/design/spec-lifecycle-management.md`; `docs/backlog/README.md` | `docs/specs/006-backlog-roadmap-templates/verification.md`; `docs/history/spec-closure-log.md` |
| 005-spec-closure-log-management | Spec closure log management | `docs/specs/005-spec-closure-log-management/` | retained | `1095b7f` | `ccba3e9` | retained-as-history | `docs/design/spec-lifecycle-management.md`; `docs/README.md`; `docs/history/spec-closure-log.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/references/durable-doc-templates/spec-closure-log.md` | `docs/specs/005-spec-closure-log-management/verification.md`; `docs/history/spec-closure-log.md` |
| 008-agent-workbench-spec-lifecycle-install | Agent Workbench spec lifecycle install | `docs/specs/008-agent-workbench-spec-lifecycle-install/` | retained | `59359bb` | `29a2d54` | retained-as-history | `docs/backlog/README.md`; `docs/reference/spec-lifecycle-manager-mcp-install.md` | `docs/specs/008-agent-workbench-spec-lifecycle-install/verification.md`; `docs/history/spec-closure-log.md` |
| 007-spec-lifecycle-mcp-server | Spec lifecycle MCP server | `docs/specs/007-spec-lifecycle-mcp-server/` | retained | `e7485bd` | `ea0c6a0` | retained-as-history | `docs/reference/spec-lifecycle-runtime.md`; `docs/README.md`; `skills/spec-lifecycle-manager/SKILL.md`; `docs/backlog/README.md`; `docs/history/spec-closure-log.md` | `docs/specs/007-spec-lifecycle-mcp-server/verification.md`; `docs/history/spec-closure-log.md` |
| 004-spec-management-mcp | Spec management MCP | `docs/specs/004-spec-management-mcp/` | retained | `86687b6` | `1a72d07` | retained-as-history | `docs/reference/spec-lifecycle-runtime.md`; `docs/design/spec-lifecycle-management.md`; `docs/README.md` | `docs/specs/004-spec-management-mcp/verification.md`; `docs/history/spec-closure-log.md` |

## Status Values

| Status | Meaning |
|--------|---------|
| retained | Package remains in the repository as an archived historical record. |
| removed | Package was removed after the final spec commit preserved its completed state. |
| superseded | Package was replaced by another durable record or later spec. |

## Legacy Gaps

| Spec ID | Gap | Current handling |
|---------|-----|------------------|
| 001-spec-lifecycle-manager-skill | Archived package predates the closure-log and archive-index workflow. | Retained in `docs/specs/001-spec-lifecycle-manager-skill/`; do not reconstruct commit evidence without a separate audit decision. |

## Related Artifacts

- Closure log: [spec-closure-log.md](spec-closure-log.md)
- Lifecycle design: [../design/spec-lifecycle-management.md](../design/spec-lifecycle-management.md)
- Active specs: [../specs/](../specs/)
