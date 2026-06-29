---
title: Cross-platform packaging change impact
doc_type: spec
artifact_type: change-impact
status: active
owner: platform
last_reviewed: 2026-06-29
---

# Change Impact

## Durable Source Mapping

- `packaging/spec-lifecycle-manager/README.md` and `package-manifest.json` —
  describe the install model and `hook_config_fallback`.
- Durable install/operations docs under `docs/`.
- Plugin/hook configuration docs describing `.mcp.json` and `hooks.json`.

## Proposed Changes

| Change | Class | Durable doc to update before closure |
| --- | --- | --- |
| `.sh` installer → Node `installer.mjs`; `npm-install.js` no longer spawns a shell | modify | `packaging/.../README.md`, install docs |
| `.mcp.json` `python3` → resolved interpreter, exec form (both copies) | modify | plugin/MCP config docs |
| `hooks.json` shell-form `python3 "..."` → exec form + resolved interpreter | modify | hook config docs |
| New Python interpreter resolver + `SPEC_LIFECYCLE_PYTHON` override | add | install/operations docs |
| Supported platform/interpreter matrix (Windows/macOS/Linux) | add | install docs |
| Marketplace static-config decision | add/clarify | install docs (Open Question 1) |

## Promotion Targets

- The platform/interpreter matrix, resolution order, and override variable
  promote into durable install/operations docs at closure (task T010).
- The marketplace static-config decision (Open Question 1) promotes into install
  docs; if marketplace is deferred to npm-only, record it in the backlog.

## Bug-Fix Corrections

- The plugin currently advertises installability but cannot install on Windows,
  and `python3` will not resolve there at launch. Closure must correct any
  durable doc that implies Windows support today.
