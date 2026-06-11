---
title: GHCR distribution packaging requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-11
---

# GHCR Distribution Packaging Requirements

## Introduction

The `spec-lifecycle-manager` plugin currently installs from a local marketplace
copy. The next packaging step is to define a GitHub Container Registry (GHCR)
distribution contract so the plugin can be installed or synchronized outside
this checkout without relying on ad hoc local paths.

This spec delivers the first deterministic packaging slice: package contract,
artifact layout, versioning, provenance metadata, and local validation. It does
not publish to GHCR.

## Goals

- Define the GHCR package shape for the self-contained Codex plugin.
- Keep the package contents aligned with `plugins/spec-lifecycle-manager/`.
- Define versioning and provenance metadata.
- Add deterministic validation that can run without network access.
- Update install/distribution documentation.

## Non-Goals

- Do not push to GHCR in this slice.
- Do not require Docker or network access for normal validation.
- Do not replace the existing local marketplace installer.
- Do not add installer behavior that mutates Codex config from a registry
  artifact.

## Glossary

| Term | Definition |
| --- | --- |
| GHCR package | OCI-compatible distribution artifact intended for `ghcr.io`. |
| Plugin bundle | The self-contained plugin tree under `plugins/spec-lifecycle-manager/`. |
| Package contract | Metadata, layout, labels, and validation rules for distribution. |
| Provenance | Repository, commit, version, source path, and validation metadata that identify the package source. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
| --- | --- | --- | --- |
| `plugins/spec-lifecycle-manager/` | Self-contained plugin bundle with skill, MCP config, hooks, prompts, templates, and scripts. | high | Package payload source. |
| `packaging/spec-lifecycle-manager/package-manifest.json` | Local package metadata and installer contract. | high | Extend for GHCR contract. |
| `scripts/install-spec-lifecycle-manager-package.sh` | Local marketplace install flow. | high | Keep as local install path. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Current install and validation model. | high | Promotion target. |
| `docs/backlog/README.md` B026 | Backlog item for GHCR distribution packaging. | high | Scope source. |

## Requirements

### Requirement 1: GHCR Package Contract

**User Story:** As a maintainer, I want a documented GHCR package contract, so
that the plugin can be distributed outside this checkout without ambiguity.

#### Acceptance Criteria

1. GIVEN the repository package metadata, WHEN a maintainer reads the contract,
   THEN it SHALL identify the package name, registry path, version source,
   payload root, entrypoint, labels, and compatibility requirements.
2. WHERE the contract references install or sync commands, THE SYSTEM SHALL
   distinguish local marketplace install from future GHCR install.
3. IF a field is not implemented yet, THEN the contract SHALL label it as
   planned rather than implying registry publishing already exists.

### Requirement 2: Package Layout Validation

**User Story:** As a maintainer, I want deterministic validation of package
inputs, so that a future GHCR artifact cannot omit required plugin files.

#### Acceptance Criteria

1. GIVEN the repository plugin bundle exists, WHEN validation runs, THEN it
   SHALL confirm required plugin files, MCP config, hook config, skill scripts,
   prompts, references, and manifest files exist.
2. GIVEN the source skill and bundled plugin skill exist, WHEN validation runs,
   THEN it SHALL confirm source/bundle parity using existing sync-guard logic or
   equivalent deterministic checks.
3. IF required package inputs are missing or drifted, THEN validation SHALL
   return structured diagnostics and a non-zero CLI exit through the existing
   runtime summary behavior.

### Requirement 3: Provenance And Versioning

**User Story:** As a maintainer, I want version and provenance metadata, so
that distributed packages can be traced back to source.

#### Acceptance Criteria

1. GIVEN package metadata exists, WHEN validation runs, THEN it SHALL report the
   declared package version, GHCR image reference, plugin manifest version, and
   repository source.
2. WHERE Git is available, THE SYSTEM SHALL report the current commit as
   provenance evidence.
3. IF Git is unavailable, THEN validation SHALL report structured unknown
   provenance rather than failing package-shape validation.

### Requirement 4: Documentation Promotion

**User Story:** As a maintainer, I want install docs updated for GHCR planning,
so that local install and future registry install boundaries remain clear.

#### Acceptance Criteria

1. GIVEN the package contract is implemented, WHEN docs are updated, THEN they
   SHALL explain local marketplace install remains the supported install path in
   this slice.
2. The docs SHALL list the validation command for package contract checks.
3. The docs SHALL link GHCR distribution packaging to B026 and identify publish
   as future work.

## Correctness Properties

- **CP-001**: Package validation is deterministic for the same repository tree.
- **CP-002**: Package validation does not mutate plugin files, Codex config, or
  registry state.
- **CP-003**: Required package files are reported by repo-relative path.

## Technical Context

- **Language/Version:** Python 3.9+ standard library for runtime validation.
- **Primary Dependencies:** None for validation; future publish may use Docker,
  `oras`, or GHCR-compatible tooling.
- **Target Platform:** Local repository validation and future GHCR artifact
  publishing.
- **Constraints:** Network-free validation; no registry push in this slice.
- **Performance Goals:** Complete within ordinary runtime validation latency.

## Success Criteria

- A GHCR package contract exists under `packaging/spec-lifecycle-manager/`.
- Runtime validation reports package contract status deterministically.
- Install docs distinguish local install from planned GHCR distribution.
- B026 is updated from candidate to delivered/done for the contract slice.

## Related Artifacts

- Design: `design.md`
- Tasks: `tasks.md`
- Change Impact: `change-impact.md`
- Verification: `verification.md`
