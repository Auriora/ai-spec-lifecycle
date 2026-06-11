---
title: Spec archive index
doc_type: history
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Spec Archive Index

This index is the compact lookup surface for closed implementation spec package
archive state. The closure log remains the narrative history with verification
summaries and residual risks; this index records the fields runtime tools need
to verify removed or explicitly retained package evidence.

## Entries

| Spec ID | Title | Package path | Status | Final spec commit | Cleanup commit | Closure action | Durable destinations | Verification |
|---------|-------|--------------|--------|-------------------|----------------|----------------|----------------------|--------------|
| 018-mcp-ergonomics-observability | MCP ergonomics and observability hardening | `docs/specs/018-mcp-ergonomics-observability/` | removed | `e4703ff` | `613f9bf` | removed | `docs/reference/spec-lifecycle-runtime.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; `tests/runtime/test_spec_runtime.py`; `tests/runtime/test_spec_mcp_server.py`; `tests/runtime/test_spec_plugin_package.py` | `docs/history/spec-closure-log.md` |
| 017-npm-distribution-packaging | npm distribution packaging | `docs/specs/017-npm-distribution-packaging/` | removed | `e4703ff` | `613f9bf` | removed | `package.json`; `packaging/spec-lifecycle-manager/npm-package.json`; `packaging/spec-lifecycle-manager/npm-install.js`; `packaging/spec-lifecycle-manager/package-manifest.json`; `plugins/spec-lifecycle-manager/claude-plugin/`; `docs/reference/spec-lifecycle-manager-mcp-install.md`; `docs/reference/spec-lifecycle-runtime.md`; `docs/backlog/README.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; `tests/runtime/test_spec_runtime.py`; `tests/runtime/test_spec_mcp_server.py`; `tests/runtime/test_spec_plugin_package.py` | `docs/history/spec-closure-log.md` |
| 016-commit-sync-guard | Commit sync guard | `docs/specs/016-commit-sync-guard/` | removed | `0522ea9` | `43dd031` | removed | `docs/reference/spec-lifecycle-runtime.md`; `docs/reference/spec-lifecycle-manager-mcp-install.md`; `docs/backlog/README.md`; `docs/roadmap/README.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `tests/runtime/test_spec_runtime.py` | `docs/history/spec-closure-log.md` |
| 015-brooks-lint-findings-tracking | Brooks-Lint findings tracking | `docs/specs/015-brooks-lint-findings-tracking/` | removed | `4b73823` | `160b582` | removed | `docs/reviews/brooks-lint/README.md`; `docs/backlog/README.md` | `docs/history/spec-closure-log.md` |
| 014-plugin-comparison-improvements | Plugin comparison improvements | `docs/specs/014-plugin-comparison-improvements/` | removed | `356c335` | `d7edc98` | removed | `docs/reference/plugin-comparison-improvements.md`; `docs/reference/spec-lifecycle-runtime.md`; `docs/README.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/prompts/`; `skills/spec-lifecycle-manager/references/spec-package/`; `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md`; `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/prompts/`; `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/references/spec-package/`; `docs/backlog/README.md`; `tests/runtime/test_spec_runtime.py` | `docs/history/spec-closure-log.md` |
| 013-agent-backed-lifecycle-tools | Agent-backed lifecycle tools | `docs/specs/013-agent-backed-lifecycle-tools/` | removed | `bb6c436` | `6d23a40` | removed | `docs/reference/spec-lifecycle-runtime.md`; `docs/design/spec-lifecycle-management.md`; `docs/reviews/spec-lifecycle-manager/README.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; `tests/runtime/test_spec_runtime.py`; `tests/runtime/test_spec_mcp_server.py` | `docs/history/spec-closure-log.md` |
| 012-operating-model-governance-adoption | Operating model governance adoption | `docs/specs/012-operating-model-governance-adoption/` | removed | `2d17440` | `af3c344` | removed | `docs/governance/constitution.md`; `docs/design/coding-agent-operating-model.md`; `docs/backlog/README.md`; `docs/roadmap/README.md` | `docs/history/spec-closure-log.md` |
| 011-spec-archive-index-runtime | Spec archive index runtime | `docs/specs/011-spec-archive-index-runtime/` | removed | `4712010` | `af3c344` | removed | `docs/history/spec-archive-index.md`; `docs/design/spec-lifecycle-management.md`; `docs/reference/spec-lifecycle-runtime.md`; `docs/backlog/README.md`; `docs/roadmap/README.md`; `docs/README.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | `docs/history/spec-closure-log.md` |
| 003-coding-agent-operating-model | Coding agent operating model | `docs/specs/003-coding-agent-operating-model/` | removed | `7ee157b` | `af3c344` | removed | `docs/design/coding-agent-operating-model.md`; `docs/reference/coding-agent-workflow-research.md`; `docs/README.md` | `docs/history/spec-closure-log.md` |
| 010-codex-hook-dogfood | Codex hook dogfood | `docs/specs/010-codex-hook-dogfood/` | removed | `d1eb6b3` | `af3c344` | removed | `docs/reference/spec-lifecycle-runtime.md`; `docs/reference/spec-lifecycle-manager-mcp-install.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py` | `docs/history/spec-closure-log.md` |
| 002-spec-lifecycle-validation | Spec lifecycle validation | `docs/specs/002-spec-lifecycle-validation/` | removed | `d1eb6b3` | `af3c344` | removed | `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/references/spec-package/`; `skills/spec-lifecycle-manager/references/durable-doc-templates/` | `docs/history/spec-closure-log.md` |
| 009-archived-spec-scan-hygiene | Archived spec scan hygiene | `docs/specs/009-archived-spec-scan-hygiene/` | removed | `1095b7f` | `af3c344` | removed | `docs/reference/spec-lifecycle-runtime.md`; `docs/design/spec-lifecycle-management.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | `docs/history/spec-closure-log.md` |
| 006-backlog-roadmap-templates | Backlog and roadmap templates | `docs/specs/006-backlog-roadmap-templates/` | removed | `1095b7f` | `af3c344` | removed | `skills/spec-lifecycle-manager/references/durable-doc-templates/backlog.md`; `skills/spec-lifecycle-manager/references/durable-doc-templates/roadmap.md`; `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md`; `skills/spec-lifecycle-manager/SKILL.md`; `docs/design/spec-lifecycle-management.md`; `docs/backlog/README.md` | `docs/history/spec-closure-log.md` |
| 005-spec-closure-log-management | Spec closure log management | `docs/specs/005-spec-closure-log-management/` | removed | `1095b7f` | `af3c344` | removed | `docs/design/spec-lifecycle-management.md`; `docs/README.md`; `docs/history/spec-closure-log.md`; `skills/spec-lifecycle-manager/SKILL.md`; `skills/spec-lifecycle-manager/references/durable-doc-templates/spec-closure-log.md` | `docs/history/spec-closure-log.md` |
| 008-agent-workbench-spec-lifecycle-install | Agent Workbench spec lifecycle install | `docs/specs/008-agent-workbench-spec-lifecycle-install/` | removed | `59359bb` | `af3c344` | removed | `docs/backlog/README.md`; `docs/reference/spec-lifecycle-manager-mcp-install.md` | `docs/history/spec-closure-log.md` |
| 007-spec-lifecycle-mcp-server | Spec lifecycle MCP server | `docs/specs/007-spec-lifecycle-mcp-server/` | removed | `e7485bd` | `af3c344` | removed | `docs/reference/spec-lifecycle-runtime.md`; `docs/README.md`; `skills/spec-lifecycle-manager/SKILL.md`; `docs/backlog/README.md`; `docs/history/spec-closure-log.md` | `docs/history/spec-closure-log.md` |
| 004-spec-management-mcp | Spec management MCP | `docs/specs/004-spec-management-mcp/` | removed | `86687b6` | `af3c344` | removed | `docs/reference/spec-lifecycle-runtime.md`; `docs/design/spec-lifecycle-management.md`; `docs/README.md` | `docs/history/spec-closure-log.md` |
| 001-spec-lifecycle-manager-skill | Spec lifecycle manager skill | `docs/specs/001-spec-lifecycle-manager-skill/` | removed | `3f0ab61` | `af3c344` | removed | `skills/spec-lifecycle-manager/SKILL.md`; `docs/design/spec-lifecycle-management.md`; `docs/README.md` | `docs/history/spec-closure-log.md` |

## Status Values

| Status | Meaning |
|--------|---------|
| retained | Package remains in the repository by explicit exception as an archived historical record. |
| removed | Package was removed after the final spec commit preserved its completed state. |
| superseded | Package was replaced by another durable record or later spec. |

## Legacy Gaps

None. Spec 001 was added to the archive index before package removal using a
final spec commit that still contains the historical package.

## Related Artifacts

- Closure log: [spec-closure-log.md](spec-closure-log.md)
- Lifecycle design: [../design/spec-lifecycle-management.md](../design/spec-lifecycle-management.md)
- Active spec convention: `docs/specs/[###-slug]/`
