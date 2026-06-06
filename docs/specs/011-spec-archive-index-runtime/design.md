---
title: Spec archive index runtime design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Technical Design

## Overview

Add a durable archive index beside the closure log and teach the runtime to
validate it. The index is a compact, machine-checkable table for closed spec
packages. The closure log remains the narrative history; the archive index is
the lookup and consistency surface.

## High-Level Design

### Components

| Component | Responsibility |
|-----------|----------------|
| `docs/history/spec-archive-index.md` | Durable index of closed spec package archive state. |
| `spec_runtime.py archive-index` | CLI command that validates index shape and closure-log consistency. |
| `spec_mcp_server.py` | Read-only MCP tool/resource exposing archive index validation. |
| Durable docs | Explain when retained specs can be removed and how Git evidence is preserved. |

### Data Model

Archive index rows use stable text fields:

| Field | Meaning |
|-------|---------|
| Spec ID | Directory slug, such as `011-spec-archive-index-runtime`. |
| Title | Human-readable title. |
| Package path | Former or current spec package path. |
| Status | `retained`, `removed`, or `superseded`. |
| Final spec commit | Commit that contains the completed package before cleanup. |
| Cleanup commit | Commit that archived, removed, or otherwise cleaned the package. |
| Closure action | `retained-as-history`, `removed-after-index`, or another documented action. |
| Durable destinations | Comma-separated durable docs or `none`. |
| Verification | Verification artifact or closure-log entry. |

### Data Flow

```text
closed spec package -> closure log -> archive index -> runtime validation -> MCP/hook advisory payloads
```

## Low-Level Design

### Archive Index Parser

Reuse markdown table parsing patterns already present in `spec_runtime.py`
instead of adding dependencies. The parser should:

1. locate `docs/history/spec-archive-index.md`;
2. parse the primary table under `## Entries`;
3. normalize spec IDs, paths, commit values, and status values;
4. return entries plus diagnostics.

### Validation Rules

Runtime validation should report:

- missing archive index file;
- malformed or duplicate spec IDs;
- missing final spec commit;
- missing cleanup commit unless explicitly pending during the active cleanup
  commit;
- closure-log entry missing for indexed spec;
- field drift between closure log and archive index;
- referenced package path missing when status is `retained`;
- referenced durable destination missing unless explicitly external.

### CLI Shape

Add:

```bash
skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .
```

Expected JSON:

```json
{
  "entries": [],
  "diagnostics": [],
  "summary": {
    "total": 0,
    "retained": 0,
    "removed": 0,
    "superseded": 0,
    "error": 0,
    "warn": 0,
    "info": 0
  }
}
```

### MCP Shape

Expose one read-only tool:

- `archive_index`: validate and return archive index state.

Optionally expose one resource:

- `history://spec-archive-index`

## Operational Considerations

- This slice should not remove existing archived spec packages.
- The runtime should remain dependency-free.
- Commit existence checks can start as syntactic hash checks plus package path
  presence; deeper Git object validation can be added later if needed.
- Hooks should use this as advisory until dogfooding shows low noise.

## Open Questions

- Should Git object validation be part of the first runtime command or a later
  stricter mode?
- Should the closure log be generated from the archive index in future, or
  remain manually curated narrative history?
- Should removed spec packages be deleted immediately after this support lands,
  or only during a later cleanup spec?

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Tasks: [tasks.md](tasks.md)
- Backlog: [../../backlog/README.md](../../backlog/README.md)
- Roadmap: [../../roadmap/README.md](../../roadmap/README.md)
