---
title: npm distribution packaging design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Technical Design

## Overview

Add a repo-owned npm distribution contract for the Spec Lifecycle Manager
plugin and validate it with the existing `package-contract` runtime command.
The package payload remains the self-contained plugin tree under
`plugins/spec-lifecycle-manager/`.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
| --- | --- | --- | --- |
| Requirement 1 | AC1-AC3 | npm contract JSON, root `package.json`, durable docs. | Runtime package validation and docs review. |
| Requirement 2 | AC1-AC3 | Required path validation and source/bundle parity. | Focused runtime tests and package validation command. |
| Requirement 3 | AC1-AC3 | Node bin wrapper around existing installer. | Unit/package tests and `npm pack --dry-run --json`. |
| Requirement 4 | AC1-AC3 | Install docs and backlog update. | Spec closure validation and docs diff. |

## High-Level Design

### System Architecture

The npm distribution slice adds:

- root `package.json`
- `packaging/spec-lifecycle-manager/npm-package.json`
- `packaging/spec-lifecycle-manager/npm-install.js`
- npm-aware `package-contract` validation in `spec_runtime.py`
- focused package tests
- install/distribution documentation

The npm package is the useful distribution artifact. The previous Docker/GHCR
image experiment is superseded by this design and should not be pushed.

### Components and Changes

- **Root package manifest:** Defines `@auriora/spec-lifecycle-manager`, files
  included in the tarball, Node engine, validation scripts, and bin entry.
- **npm package contract:** JSON metadata for package name, version source,
  payload root, install command, required paths, and provenance.
- **npm installer bin:** Node wrapper that resolves the unpacked package root
  and invokes `scripts/install-spec-lifecycle-manager-package.sh --source`.
- **Runtime validation:** Read-only command validates npm contract, `package.json`,
  required paths, source/bundle parity, package metadata, and optional Git
  provenance.
- **Docs:** Install reference describes local checkout install and npm package
  install as distinct paths.

### Data Models

Runtime payload:

```text
{
  repo_root,
  contract_path,
  manifest_path,
  npm_package_path,
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
repo or unpacked package root
  -> load package.json
  -> load package-manifest.json
  -> load npm-package.json
  -> validate required files and directories
  -> compare source skill and bundled skill parity
  -> collect Git commit provenance if available
  -> emit diagnostics and summary
```

## Low-Level Design

### npm Package Contract

`npm-package.json` contains:

- npm package name and registry
- version source
- payload root
- installer bin path
- install and pack commands
- required files
- publish status
- provenance metadata

### npm Installer Bin

```bash
npx @auriora/spec-lifecycle-manager install
```

The bin:

1. Resolves package root from `__dirname`.
2. Accepts `install`, `help`, and `--help`.
3. Invokes `scripts/install-spec-lifecycle-manager-package.sh --source <root>`.
4. Forwards additional installer options.
5. Exits with the underlying installer status.

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
paths are errors. Git provenance failures are unknown metadata, not
package-shape failures.

### Security, Trust, and Access

Validation is read-only and network-free. It does not invoke `npm publish`,
Docker, GHCR, or any registry mutation.

### Migration and Compatibility

The existing local marketplace installer remains supported. The npm bin reuses
that installer instead of duplicating Codex plugin installation logic.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
| --- | --- | --- | --- |
| Focused package-contract tests | Requirements 1-3 | `verification.md` | Does not prove npm publish. |
| `npm pack --dry-run --json` | Tarball contents | `verification.md` | Does not prove registry install. |
| Full unit suite | Runtime regression | `verification.md` | None expected. |
| Manual package-contract command | Local package state | `verification.md` | Git provenance depends on local Git availability. |
| Sync guard | Source/bundle/cache parity | `verification.md` | Installed cache may need reinstall after runtime changes. |

## Operational Considerations

Publishing remains future work. A future publish slice should define npm
registry access, package provenance, release tags, and whether the package name
belongs under `@auriora` or another scope.

## Open Questions

- Which npm scope should be authoritative for public publishing?
- Should publish be manual, GitHub Actions based, or another release workflow?

## Related Artifacts

- Requirements: `requirements.md`
- Tasks: `tasks.md`
- Change Impact: `change-impact.md`
- Verification: `verification.md`
