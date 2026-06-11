---
title: Commit sync guard change impact
doc_type: change-impact
artifact_type: change-impact
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Commit Sync Guard Change Impact

## Durable Source Mapping

| Source | Impact |
| --- | --- |
| `docs/backlog/README.md` B016 | Update from candidate to delivered or done when implementation is validated. |
| `docs/roadmap/README.md` R005 | Update status once sync guard reporting exists. |
| `docs/reference/spec-lifecycle-runtime.md` | Add `sync-guard` command and payload behavior. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Add sync guard to validation checklist and reload troubleshooting. |

## Proposed Changes

| Target | Change |
| --- | --- |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Add read-only `sync-guard` command. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Keep bundled skill parity with source. |
| `tests/runtime/` | Add deterministic coverage for sync guard payloads. |

## Promotion Targets

| Destination | Promoted content |
| --- | --- |
| `docs/reference/spec-lifecycle-runtime.md` | Runtime command purpose, payload behavior, and validation command. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Install validation checklist entry and reload troubleshooting note. |
| `docs/backlog/README.md` | Mark B016 delivered/done after validation. |
| `docs/roadmap/README.md` | Mark R005 delivered/done after validation. |

## Deferred Work

- Automation that runs installer or reloads Codex remains out of scope.
- Blocking commit hooks remain out of scope.
