---
title: Public slm CLI canonical context
doc_type: spec
artifact_type: canonical-context
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Canonical Context

## Purpose

This spec crosses three easily confused command surfaces: the packaged public
CLI being introduced, the existing repository-local maintainer CLI, and the
JSON/MCP lifecycle runtime. This map prevents implementation from treating an
old executable name, a development-only command, or a temporary package path as
the authority for the public design.

## Authority Hierarchy

The spec-local context is canonical only for the active Spec 039 implementation
slice. It does not override user/system instructions, `AGENTS.md`, governance,
source and package contracts, tests, live package evidence, or release policy.
Conflicts with current implementation are reconciliation inputs; conflicts with
the user-approved requirements require a recorded decision before changing the
contract.

## Always-Canonical External Sources

| Source | Authority reason | Handling |
|--------|------------------|----------|
| `AGENTS.md` | Repository instructions and MCP-first lifecycle rules | Read before modifying source, package, tests, or docs. |
| `docs/governance/constitution.md` | Durable governance | Stop for a decision if implementation conflicts with policy. |
| `package.json` and packed tarball metadata | Actual distributed executable/file contract | Reconcile with this spec; validate the final artifact, not only the checkout. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/` | Shared lifecycle interpretation | Reuse existing semantics; do not fork parsing in the CLI. |
| `tools/devcli/` | Current maintainer CLI implementation | Preserve `slc` as repo-local tooling. |
| tests and CI evidence | Executable truth | Use as verification, not as authority to weaken requirements silently. |

## Spec-Canonical Working Sources

| Source | Role | Scope | Notes |
|--------|------|-------|-------|
| `requirements.md` | accepted public behavior | Spec 039 | Includes the user-approved naming, commands, filters, read-only boundary, and no-alias decision. |
| `design.md` | implementation and packaging approach | Spec 039 | May refine internal module names without changing observable acceptance criteria. |
| `tasks.md` | execution index | Spec 039 | Do not implement from tasks alone. |
| `traceability.md` | requirement/design/task/evidence navigation | Spec 039 | Update when task or interface scope changes. |
| `verification.md` | validation and closure evidence | Spec 039 | Tarball evidence is mandatory for distribution claims. |
| `change-impact.md` | durable rename and promotion map | Spec 039 | Every pending target must be promoted or explicitly routed before closure. |

## Imported Sources

| Spec path | Source path | Source revision or date | Status | Canonical scope | Promotion target |
|-----------|-------------|-------------------------|--------|-----------------|------------------|
| `requirements.md`, `design.md` | User decisions in the 2026-07-19 discussion | 2026-07-19 | adapted | Public name, commands, filters, read-only boundary, and no compatibility alias | README and runtime/install references |
| all artifacts | `README.md` | commit `225e2f2` baseline | background | Current packaged installation language | `README.md` |
| all artifacts | `docs/reference/spec-lifecycle-runtime.md` | 2026-07-19 working tree | summarized | Existing runtime/state/history semantics | same file |
| all artifacts | `docs/reference/spec-lifecycle-manager-mcp-install.md` | 2026-07-19 working tree | summarized | Current package and interpreter contract | same file |
| `design.md`, `tasks.md` | current `tools/devcli/` and package dispatcher source | 2026-07-19 working tree | summarized | Current `slc` and long-bin implementation boundaries | design/install docs |

## Non-Canonical Background Sources

| Source | Reason non-canonical | Handling |
|--------|----------------------|----------|
| Existing `spec-lifecycle-manager` and `ai-spec-lifecycle` bin names | Superseded by the accepted `slm` sole-bin requirement for this slice | Use only for migration tests and documentation updates. |
| Repo-local `.venv/bin/slc` | Development/maintainer surface, not the proposed public package | Preserve; do not copy or rename into `slm`. |
| Removed spec package paths in history | Historical evidence, not active implementation authority | Read closure/index records instead of recreating packages. |
| Plugin cache paths | Host-local installation detail and possibly stale | Use only in explicit install diagnostics. |

## Promotion Map

| Spec-local content | Durable destination or route | Required before closure |
|--------------------|------------------------------|-------------------------|
| Public `slm` command and examples | `README.md` | yes |
| Shared-core and CLI/MCP/`slc` boundary | `docs/design/spec-lifecycle-management.md` | yes |
| Command/filter/output/state contract | `docs/reference/spec-lifecycle-runtime.md` | yes |
| Bin migration and package verification | `docs/reference/spec-lifecycle-manager-mcp-install.md` | yes |
| Release-visible breaking rename | next release notes | yes before release; closure may route to the owned release process if implementation is not released immediately |

## Related Artifacts

- Requirements: `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Change impact: `change-impact.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
