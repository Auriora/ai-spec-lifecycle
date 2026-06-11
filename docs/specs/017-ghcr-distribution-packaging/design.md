---
title: GHCR distribution packaging design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Technical Design

## Overview

Add a repo-owned GHCR distribution contract for the Spec Lifecycle Manager
plugin and validate it with a read-only runtime command. The package payload
remains the existing self-contained plugin tree under
`plugins/spec-lifecycle-manager/`.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
| --- | --- | --- | --- |
| Requirement 1 | AC1-AC3 | Package contract JSON and durable docs. | Runtime package validation and docs review. |
| Requirement 2 | AC1-AC3 | Required path validation and source/bundle parity. | Focused runtime tests and package validation command. |
| Requirement 3 | AC1-AC3 | Metadata fields and Git provenance lookup. | Runtime command output. |
| Requirement 4 | AC1-AC3 | Install docs and backlog update. | Spec closure validation and docs diff. |

## High-Level Design

### System Architecture

The first GHCR slice adds:

- `packaging/spec-lifecycle-manager/ghcr-package.json`
- `packaging/spec-lifecycle-manager/Containerfile`
- a `package-contract` command in `spec_runtime.py`
- focused runtime tests
- install/distribution documentation

The contract is authoritative for package shape. The Containerfile is a
publishable artifact template, but validation does not build or push it.

### Components and Changes

- **Package contract:** JSON metadata for image reference, version source,
  payload root, required paths, labels, annotations, compatibility, and publish
  status.
- **Containerfile:** Minimal OCI image layout that copies the plugin bundle and
  package manifest into `/opt/spec-lifecycle-manager/`.
- **Runtime validation:** Read-only command validates package contract,
  required paths, source/bundle parity, package metadata, and optional Git
  provenance.
- **Docs:** Install reference describes local marketplace install as supported
  and GHCR as contract-ready but not published by this slice.

### Data Models

Runtime payload:

```text
{
  repo_root,
  contract_path,
  manifest_path,
  status,
  package,
  required_paths,
  source_bundle_parity,
  provenance,
  diagnostics,
  summary
}
```

### Data Flow

```text
repo root
  -> load package-manifest.json
  -> load ghcr-package.json
  -> validate required files and directories
  -> compare source skill and bundled skill parity
  -> collect Git commit provenance if available
  -> emit diagnostics and summary
```

## Low-Level Design

### Package Contract

`ghcr-package.json` contains:

- package name and registry
- image reference template
- version source
- payload root
- package manifest path
- Containerfile path
- required files
- OCI labels and annotations
- compatibility and dependency notes
- publish status

### Runtime Command

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .
```

Function signatures:

```text
package_contract(repo_root: Path) -> dict[str, Any]
load_json_file(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]
git_head_commit(repo_root: Path) -> dict[str, Any]
```

The command exits non-zero when diagnostics include errors through existing
summary behavior.

### Error Handling

Missing or malformed JSON returns structured diagnostics. Missing required
paths are errors. Git provenance failures are warnings or unknown metadata, not
package-shape failures.

### Security, Trust, and Access

Validation is read-only and network-free. It does not invoke Docker, `oras`,
`gh`, or GHCR. Future publish tooling must be a separate explicit slice.

### Migration and Compatibility

The existing local marketplace installer remains the supported install path.
GHCR metadata does not change Codex config or plugin runtime behavior.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
| --- | --- | --- | --- |
| Focused package-contract tests | Requirements 1-3 | `verification.md` | Does not prove registry push. |
| Full unit suite | Runtime regression | `verification.md` | None expected. |
| Manual package-contract command | Local package state | `verification.md` | Git provenance depends on local Git availability. |
| Sync guard | Source/bundle/cache parity | `verification.md` | Installed cache may need reinstall after runtime changes. |

## Operational Considerations

Publishing remains future work. A future publish spec should choose whether to
push an OCI image, an OCI artifact, or both, and should define authentication,
tagging, rollback, and provenance verification.

## Open Questions

- Should the first published GHCR artifact be a runnable image, an OCI artifact
  containing the plugin tree, or both?
- Should publish use Docker, `oras`, GitHub Actions, or another explicit tool?

## Related Artifacts

- Requirements: `requirements.md`
- Tasks: `tasks.md`
- Change Impact: `change-impact.md`
- Verification: `verification.md`
