---
title: npm distribution packaging requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-11
---

# npm Distribution Packaging Requirements

## Introduction

The `spec-lifecycle-manager` plugin needs a useful distribution artifact that
can be installed outside this checkout. A Docker/GHCR image containing plugin
files is not directly consumable by Codex users, so this spec pivots B026 to an
npm package with an `npx` installer command.

## Goals

- Define an npm package for the self-contained Codex plugin.
- Support `npx @auriora/ai-spec-lifecycle install`.
- Include a Claude Code plugin wrapper for users who want to load the package
  through Claude Code plugin support.
- Publish and tolerate review packet type mappings so MCP callers do not need
  to guess hidden internal IDs.
- Keep package contents aligned with `plugins/spec-lifecycle-manager/`.
- Validate npm package metadata and tarball contents without publishing.
- Update durable docs and backlog language away from Docker/GHCR as the primary
  distribution path.

## Non-Goals

- Do not publish to npm in this slice.
- Do not push Docker/GHCR images.
- Do not require Docker for validation.
- Do not remove the existing local marketplace installer.

## Glossary

| Term | Definition |
| --- | --- |
| npm package | Distributable package named `@auriora/ai-spec-lifecycle`. |
| Plugin bundle | The self-contained plugin tree under `plugins/spec-lifecycle-manager/`. |
| Package contract | Metadata, layout, install command, and validation rules for distribution. |
| Provenance | Repository, commit, version, source path, and validation metadata that identify the package source. |
| Review packet type | Canonical review packet template ID used by the runtime and MCP `review_packet` tool. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
| --- | --- | --- | --- |
| `plugins/spec-lifecycle-manager/` | Self-contained plugin bundle with skill, MCP config, hooks, prompts, templates, and scripts. | high | Package payload source. |
| `scripts/install-spec-lifecycle-manager-package.sh` | Local marketplace install flow. | high | Reused by npm bin with `--source` set to the unpacked package root. |
| `packaging/spec-lifecycle-manager/package-manifest.json` | Local package metadata and installer contract. | high | Extended with npm distribution metadata. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Current install and validation model. | high | Promotion target. |
| `docs/backlog/README.md` B026 | Backlog item for distribution packaging. | high | Scope source; GHCR wording is superseded by this pivot. |

## Requirements

### Requirement 1: npm Package Contract

**User Story:** As a maintainer, I want an npm package contract, so that the
plugin can be distributed without requiring a repository checkout.

#### Acceptance Criteria

1. GIVEN the repository package metadata, WHEN a maintainer reads the contract,
   THEN it SHALL identify the npm package name, version source, payload root,
   installer bin, install command, publish status, and required files.
2. WHERE the package references install commands, THE SYSTEM SHALL use
   `npx @auriora/ai-spec-lifecycle install` as the package install path.
3. IF publishing is not implemented yet, THEN the contract SHALL label npm
   publish status as pack-ready but not published.

### Requirement 2: npm Package Layout Validation

**User Story:** As a maintainer, I want deterministic validation of package
inputs, so that the npm tarball cannot omit required plugin files.

#### Acceptance Criteria

1. GIVEN the repository plugin bundle exists, WHEN validation runs, THEN it
   SHALL confirm required plugin files, MCP config, hook config, skill scripts,
   prompts, references, installer script, npm package manifest, and package
   contract exist.
2. GIVEN source and bundled plugin skills exist, WHEN validation runs, THEN it
   SHALL confirm source/bundle parity using deterministic checks.
3. IF required package inputs are missing or drifted, THEN validation SHALL
   return structured diagnostics and a non-zero CLI exit through the existing
   runtime summary behavior.

### Requirement 3: npx Installer

**User Story:** As a user, I want a package bin that installs the plugin from
the unpacked npm package, so that I can use the package without knowing its
internal paths.

#### Acceptance Criteria

1. GIVEN the npm package is unpacked, WHEN `spec-lifecycle-manager install`
   runs, THEN it SHALL invoke the existing installer with `--source` pointing at
   the npm package root.
2. WHERE installer options are passed after `install`, THE SYSTEM SHALL forward
   them to the existing installer.
3. IF an unknown command is provided, THEN the bin SHALL print usage and exit
   non-zero.

### Requirement 4: Documentation Promotion

**User Story:** As a maintainer, I want install docs updated for npm
distribution, so that users do not confuse Docker images with the supported
package path.

#### Acceptance Criteria

1. GIVEN the npm package contract is implemented, WHEN docs are updated, THEN
   they SHALL describe local install and npm package install separately.
2. The docs SHALL list validation commands for package contract and npm pack
   checks.
3. The docs SHALL record Docker/GHCR as superseded or deferred, not the primary
   distribution artifact.

### Requirement 5: Claude Code Plugin Wrapper

**User Story:** As a Claude Code user, I want a bundled Claude plugin wrapper,
so that I can load the Spec Lifecycle Manager MCP server and skill without
manually wiring the MCP command.

#### Acceptance Criteria

1. GIVEN the npm package payload, WHEN the Claude plugin is inspected, THEN it
   SHALL include `.claude-plugin/plugin.json`, `.mcp.json`, a skill, and hook
   configuration under `plugins/spec-lifecycle-manager/claude-plugin/`.
2. GIVEN the Claude plugin is loaded with `claude --plugin-dir`, WHEN Claude
   starts the MCP server, THEN the MCP config SHALL launch the bundled
   `spec_mcp_server.py` from the Claude plugin root.
3. WHERE hooks are packaged, THE SYSTEM SHALL keep them advisory-only and
   rooted at `${CLAUDE_PLUGIN_ROOT}`.

### Requirement 6: Review Packet Type Mapping

**User Story:** As an MCP caller, I want review packet types and aliases to be
published and forgiving, so that natural implementation review requests do not
fail with hidden internal enum errors.

#### Acceptance Criteria

1. GIVEN `review_packet` receives `review_type` values such as
   `implementation` or `implementation-readiness`, WHEN the packet is
   generated, THEN the runtime SHALL resolve them to `implementation_review`
   and preserve the requested value in the payload.
2. GIVEN `review_packet` receives any other unknown non-empty review type, WHEN
   the packet is generated, THEN the runtime SHALL resolve it to
   `generic_review` and preserve the requested value in the payload.
3. WHERE the MCP tool schema exposes review packet inputs, THE SYSTEM SHALL
   publish the default, canonical review packet types, alias mapping, and
   unknown-value fallback behavior.

## Correctness Properties

- **CP-001**: Package validation is deterministic for the same repository tree.
- **CP-002**: Package validation does not mutate plugin files, Codex config, or
  registry state.
- **CP-003**: Required package files are reported by repo-relative path.
- **CP-004**: `npm pack --dry-run --json` includes the installer bin, package
  contract, existing installer script, and plugin bundle.
- **CP-005**: Review packet type resolution is deterministic for the same input
  string.

## Technical Context

- **Language/Version:** Python 3.9+ standard library for runtime validation;
  Node.js 18+ for the npm bin wrapper.
- **Primary Dependencies:** None beyond npm/Node for package creation.
- **Target Platform:** Local package validation and future npm publishing.
- **Constraints:** Network-free validation; no npm publish in this slice.
- **Performance Goals:** Complete within ordinary runtime validation latency.

## Success Criteria

- `package.json` defines `@auriora/ai-spec-lifecycle` with a bin entry.
- `packaging/spec-lifecycle-manager/npm-package.json` defines the package
  contract.
- `plugins/spec-lifecycle-manager/claude-plugin/` defines a Claude Code plugin
  wrapper.
- `npm pack --dry-run --json` includes the required distribution payload.
- `spec_runtime.py package-contract .` validates npm package shape.
- Install docs distinguish local install from npm package install.
- `review_packet` maps implementation-style and unknown review type values
  without throwing runtime enum errors.

## Related Artifacts

- Design: `design.md`
- Tasks: `tasks.md`
- Change Impact: `change-impact.md`
- Verification: `verification.md`
