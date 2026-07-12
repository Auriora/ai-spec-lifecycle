---
title: Closure Response Contract Design
doc_type: spec
artifact_type: design
status: active
owner: maintainers
last_reviewed: 2026-07-12
---

# Design

## Overview

Separate the internal executable plan from the agent-facing manifest, then
derive every apply action from explicit inputs and current repository state.

## High-Level Design

The shared closure core continues to build a full internal plan for deterministic
execution and retained CLI recovery. The MCP adapter projects it into a small
manifest that never includes replacement bodies. Apply calls regenerate the
internal plan from `spec_path`, final commit, closure action, and current files;
the supplied `plan_id` authenticates the spec-package snapshot and intent.

Actions are repository-derived rather than process-state-derived. Record writes
upsert by spec ID. Cleanup selects only the package edit and requires matching
durable records. This makes sequential calls independent and restart-safe.

## Low-Level Design

- `closure_plan_manifest(plan, detail, section)` maps full edits to summaries
  containing path, action, precondition hash, output hash/size, and bounded
  preview.
- The plan fingerprint hashes normalized closure metadata plus a deterministic
  spec-package tree hash. Record writes do not invalidate it; spec edits do.
- MCP `closure_apply` regenerates with reference scanning disabled, compares
  fingerprints, then invokes shared `closure_apply` for one action.
- `_insert_closure_log` replaces an existing matching heading section;
  `_insert_archive_row` replaces a matching first-column spec ID.
- Reference scanning combines root ignore rules with narrow safety exclusions
  for cache, VCS, database/WAL/SHM, Python cache, and detected binary files.

## Error Handling

- Fingerprint mismatch: `CLOSURE_PLAN_STALE`.
- Cleanup without matching records: `CLOSURE_RECORDS_NOT_APPLIED`.
- Missing write intent and file precondition failures retain existing guarded
  rejection behavior.

## Operational Considerations

The 32 KiB ceiling is asserted in regression tests. It is a safety invariant,
not a truncation strategy. Full generated content remains local to one call and
is reconstructed after a restart.

## Open Questions

None. The retained full-plan CLI recovery format is explicitly outside this
agent-facing response contract.
