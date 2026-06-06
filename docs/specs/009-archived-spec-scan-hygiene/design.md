---
title: Archived spec scan hygiene design
doc_type: spec
artifact_type: design
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Design

## Overview

Default scan becomes an active-health view over all discovered packages. The
inventory still includes archived packages, but their health is marked as a
skipped historical record unless the caller explicitly opts into archived lint.

## High-Level Design

### System Architecture

The runtime keeps one discovery path and adds lifecycle classification after
frontmatter status is read. Scan consumers receive both per-spec lifecycle
metadata and a summary bucket that separates active and archived packages.

### Components And Changes

| Component | Change |
|-----------|--------|
| `spec_runtime.py` | Add archived status classification, scan summary counts, skipped archived health, and CLI audit flag. |
| `spec_mcp_server.py` | Add `include_archived_lint` scan argument and forward it to runtime scan. |
| `tests/runtime/` | Cover default skipped archived health, opt-in archived audit, and MCP option exposure. |
| Durable docs | Document default active-health semantics and explicit audit behavior. |

### Data Models

Scan spec entries add:

| Field | Meaning |
|-------|---------|
| `lifecycle` | `active` or `archived`, derived from frontmatter status. |
| `health.skipped` | Whether scan skipped authoring lint for this package. |
| `health.reason` | Human-readable reason when lint is skipped. |

Scan payloads add:

| Field | Meaning |
|-------|---------|
| `summary.total` | Number of discovered packages. |
| `summary.active` | Number of active packages. |
| `summary.archived` | Number of archived packages. |
| `summary.active_pass` | Active packages with pass health. |
| `summary.active_warn` | Active packages with warning health. |
| `summary.active_error` | Active packages with error health. |

### Data Flow

1. `scan_specs` discovers package directories.
2. Each package status is read from current or old-format frontmatter.
3. Status values `archived`, `closed`, and `superseded` classify as archived.
4. Default scan returns skipped archived health without running package lint.
5. Audit scan runs package lint for every package.
6. Summary counts are computed from the resulting spec entries.

## Low-Level Design

### Algorithms

`health_summary(spec_path, include_archived_lint=False)` checks lifecycle before
lint. If the package is archived and audit mode is false, it returns archived
skipped health. Otherwise it runs the existing `lint_spec_package` path.

`scan_specs(repo_root, docs_root=None, include_archived_lint=False)` forwards
the audit flag to each health calculation and appends summary counts.

### Function Signatures And Interfaces

```python
def scan_specs(repo_root: Path, docs_root: str | None = None, include_archived_lint: bool = False) -> dict[str, Any]: ...
def health_summary(spec_path: Path, include_archived_lint: bool = False) -> dict[str, Any]: ...
```

CLI:

```bash
skills/spec-lifecycle-manager/scripts/spec_runtime.py scan . --include-archived-lint
```

MCP:

```json
{"name": "scan_specs", "arguments": {"repo_root": "/path/to/repo", "include_archived_lint": "true"}}
```

### Error Handling

Archived scan skipping is not an error. Direct lint and closure checks keep
their existing strict behavior so explicit audits remain useful.

## Operational Considerations

Archived packages that fail current lint are not automatically migrated.
Modernization requires a separate resumption or migration decision because
historical delivery records may intentionally preserve old evidence.

## Validation Strategy

- Unit-test default scan archived skip behavior.
- Unit-test CLI audit flag behavior.
- MCP-test scan schema and audit argument behavior.
- Run the full test suite, spec lint, closure check, and diff whitespace check.

## Open Questions

None.
