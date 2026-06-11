---
title: npm distribution packaging change impact
doc_type: spec
artifact_type: change-impact
status: active
owner: platform
last_reviewed: 2026-06-11
---

# npm Distribution Packaging Change Impact

## Durable Source Mapping

| Source | Impact |
| --- | --- |
| `docs/backlog/README.md` B026 | Update from GHCR wording to npm package distribution. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Add npm package install path and validation guidance. |
| `docs/reference/spec-lifecycle-runtime.md` | Clarify `package-contract` validates npm distribution metadata. |
| `packaging/spec-lifecycle-manager/package-manifest.json` | Add npm distribution metadata and remove GHCR as active package target. |

## Proposed Changes

| Target | Change |
| --- | --- |
| `package.json` | Add npm package manifest, files list, bin, and validation scripts. |
| `packaging/spec-lifecycle-manager/npm-package.json` | Add npm distribution contract. |
| `packaging/spec-lifecycle-manager/npm-install.js` | Add `npx` installer wrapper. |
| `packaging/spec-lifecycle-manager/Containerfile` | Remove superseded Docker image packaging artifact. |
| `packaging/spec-lifecycle-manager/ghcr-package.json` | Remove superseded GHCR image packaging artifact. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Validate npm package contract. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Keep bundled runtime in sync. |
| `tests/runtime/test_spec_runtime.py` | Add package contract validation tests. |
| `tests/runtime/test_spec_plugin_package.py` | Add npm package metadata and `npm pack --dry-run` tests. |

## Promotion Targets

| Destination | Promoted content |
| --- | --- |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Local install, npm package install, and validation checklist. |
| `docs/reference/spec-lifecycle-runtime.md` | Runtime command and npm payload behavior. |
| `docs/backlog/README.md` | Mark B026 delivered/done for npm package contract and validation slice. |

## Deferred Work

- npm publish automation.
- npm registry authentication and publish validation.
- Release tagging policy beyond the declared version source.
- Optional OCI/ORAS packaging only if a future use case proves it is useful.
