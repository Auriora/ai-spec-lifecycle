---
title: Public slm CLI change impact
doc_type: spec
artifact_type: change-impact
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Change Impact

## Purpose

Record the public executable rename, new read-only inspection behavior,
packaging changes, and durable documentation that must be promoted before this
spec can close.

## Durable Source Mapping

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `README.md` | Uses `spec-lifecycle-manager install` and does not expose public inspection commands. | high | Must be updated atomically with the bin change. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Defines package entrypoints, install flow, Python resolution, and supported platforms. | high | Owns migration and packaged verification guidance. |
| `docs/reference/spec-lifecycle-runtime.md` | Defines current JSON recovery CLI, runtime states, filters, and archive semantics. | high | Must distinguish `slm` from `spec_runtime.py`. |
| `docs/design/spec-lifecycle-management.md` | Defines MCP-first lifecycle architecture. | high | Must place `slm` as a read-only presentation adapter over shared core. |
| `package.json` and package manifests | Expose `ai-spec-lifecycle` and `spec-lifecycle-manager` installer bins. | high | Replaced by sole `slm` bin. |
| `tools/devcli/` | Exposes repo-local `slc`. | high | Reviewed and intentionally unchanged. |

## Change Type

- **Primary type:** feature and rename
- **Breaking change:** yes - executable names change without aliases
- **Durable docs required:** yes
- **External behavior affected:** yes

## Proposed Changes

| Change | Type | Source of truth | New durable destination | Promotion required |
|--------|------|-----------------|-------------------------|-------------------|
| Replace long package bins with sole `slm` executable | rename/remove | `package.json` | `README.md`, install reference, release notes | yes |
| Retain installer as `slm install` | modify | package dispatcher and installer | `README.md`, install reference | yes |
| Add active spec inventory | add | shared scan/task/next contracts | runtime reference and design | yes |
| Add task filters and next alias | add | shared task marker and `next_task` contracts | runtime reference | yes |
| Add requirement-priority inventory | add | shared requirements parser and traceability | runtime reference | yes |
| Add durable closed/history inventory | add | archive index and closure log | runtime reference | yes |
| Add human table and stable JSON presentation | add | public CLI output schema | runtime reference and design | yes |
| Preserve `slc` as maintainer-only tooling | clarify | `tools/devcli/` | README and design | yes |

## Promotion Targets

| Spec content | Durable destination | Promotion status | Notes |
|--------------|---------------------|------------------|-------|
| User command/install path | `README.md` | pending | Include examples for all four plural commands and `next`. |
| Public CLI architecture and ownership | `docs/design/spec-lifecycle-management.md` | pending | Keep MCP primary for agents and shared core authoritative. |
| Commands, filters, output, state semantics, exit behavior | `docs/reference/spec-lifecycle-runtime.md` | pending | Include `pending` versus `open` and no synthetic spec state. |
| Bin rename, Python resolution, tarball verification | `docs/reference/spec-lifecycle-manager-mcp-install.md` | pending | State that compatibility aliases are intentionally absent. |
| Breaking executable rename and feature summary | next release notes | pending | Required when implementation is released. |

## Unchanged Durable Areas

| Durable area | Reviewed source | Reason unchanged |
|--------------|-----------------|------------------|
| MCP tool names and schemas | `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | The public CLI composes shared core; no new MCP surface is required. |
| Spec document format and markers | skill/templates/runtime docs | The CLI reads existing contracts and does not modify them. |
| Repository-maintainer workflow | `tools/devcli/` | `slc` remains separate and repo-local. |
| Codex and Claude plugin registration | plugin manifests and installer | The global public executable does not change plugin identity. |
| Hook mutation boundary | packaged hook definitions | Inspection commands do not invoke advisory hooks. |

## Bug Fix Details

Not applicable. This is an additive public interface plus an intentional
executable rename.

## Open Questions

None. Compatibility aliases were explicitly rejected because the prior long
executables are not in use.

## Related Artifacts

- Requirements: `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
