---
title: Developer CLI workflow tools change impact
doc_type: spec
artifact_type: change-impact
status: active
owner: platform
last_reviewed: 2026-06-14
---

# Change Impact

## Durable Source Mapping

| Source | Current behavior | Impact |
|--------|------------------|--------|
| `tools/README.md` | Generic tools directory guidance. | Modify to document `adl` once implemented. |
| `tools/devcli/README.md` | Template `proj` commands and placeholder behavior. | Replace with project-specific install and command docs. |
| `tools/devcli/pyproject.toml` | Generic `proj-devcli` metadata and `proj` entry point. | Modify to repository-specific metadata and `adl` entry point. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Documents authoritative install and validation commands. | Clarify CLI wrappers after implementation while preserving underlying commands. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime commands and path policy. | Add CLI convenience wrapper references after implementation. |
| `package.json` | Owns npm validation and pack dry-run scripts. | Optional test-script update if CLI tests join repository validation. |
| `docs/specs/022-npm-publish-release-workflow/` | Owns release automation and guarded npm publish design. | No change unless release-preflight scope requires cross-linking. |

## Proposed Changes

| Change | Type | Target | Notes |
|--------|------|--------|-------|
| Rename CLI package metadata and command entry point. | modify | `tools/devcli/pyproject.toml` | Use `adl` as proposed primary command unless decision changes. |
| Add shared runner and repo utilities. | add | `tools/devcli/src/auriora_dev/` | Must keep command execution testable. |
| Add command modules. | add | `tools/devcli/src/auriora_dev/commands/` | Check, sync, package, plugin, spec, release, doctor. |
| Add CLI tests. | add | `tools/devcli/tests/` | Mock external commands and avoid user-local mutation. |
| Update tools docs. | modify | `tools/README.md`, `tools/devcli/README.md` | Document commands and mutation boundaries. |
| Add optional repository validation hook. | modify | `package.json` | Only if safe and agreed. |

## Promotion Targets

| Content | Durable destination | Promotion condition |
|---------|---------------------|---------------------|
| CLI install and command usage | `tools/README.md`, `tools/devcli/README.md` | Commands implemented and tested. |
| Install/package wrapper guidance | `docs/reference/spec-lifecycle-manager-mcp-install.md` | Install-local and package check implemented. |
| Runtime wrapper guidance | `docs/reference/spec-lifecycle-runtime.md` | Spec and validation wrappers implemented. |
| Release-preflight boundary | `docs/reference/spec-lifecycle-manager-mcp-install.md` or active release docs | Release preflight implemented without external mutation. |
| Deferred publish/push commands | `docs/backlog/README.md` or spec `022` | If future release mutation remains out of scope. |

## Out Of Scope

- npm publish implementation.
- GitHub release creation.
- Tag pushing.
- Replacing `spec_runtime.py` with CLI logic.
- User-level Codex config edits outside the authoritative installer.
