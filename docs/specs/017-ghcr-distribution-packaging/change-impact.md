---
title: GHCR distribution packaging change impact
doc_type: spec
artifact_type: change-impact
status: active
owner: platform
last_reviewed: 2026-06-11
---

# GHCR Distribution Packaging Change Impact

## Durable Source Mapping

| Source | Impact |
| --- | --- |
| `docs/backlog/README.md` B026 | Update from candidate to delivered/done for the package contract slice. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Add GHCR distribution contract and validation guidance. |
| `docs/reference/spec-lifecycle-runtime.md` | Add `package-contract` runtime command. |
| `packaging/spec-lifecycle-manager/package-manifest.json` | Add GHCR distribution metadata or link to the contract. |

## Proposed Changes

| Target | Change |
| --- | --- |
| `packaging/spec-lifecycle-manager/ghcr-package.json` | Add package distribution contract. |
| `packaging/spec-lifecycle-manager/Containerfile` | Add no-push OCI image layout template. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Add package-contract validation command. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Keep bundled runtime in sync. |
| `tests/runtime/test_spec_runtime.py` | Add package contract validation tests. |

## Promotion Targets

| Destination | Promoted content |
| --- | --- |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Distribution model, local-vs-GHCR boundary, validation checklist. |
| `docs/reference/spec-lifecycle-runtime.md` | Runtime command and payload behavior. |
| `docs/backlog/README.md` | Mark B026 delivered/done for contract and validation slice. |

## Deferred Work

- GHCR publish automation.
- Registry authentication and push validation.
- Pull/install directly from GHCR.
- Release tagging policy beyond the declared version source.
