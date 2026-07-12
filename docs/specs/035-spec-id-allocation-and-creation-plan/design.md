---
title: Spec ID allocation and creation plan design
doc_type: spec
artifact_type: design
status: accepted
authoring_mode: wizard
lifecycle_stage: design
owner: platform
last_reviewed: 2026-07-12
---

# Design

## Overview

Add caller-agnostic numbering inventory and creation planning to the shared
lifecycle core. Inventory selects one explicit docs root, combines active and
historical evidence within that scope, diagnoses ambiguity, and returns a
provisional monotonic next number. Creation planning requires a validated slug
and composes inventory, template authority, safe path construction, artifact
selection, preconditions, validation, and a stale-plan fingerprint without
writing or reserving anything.

## High-Level Design

```text
selected docs root
      |
      +-- active package directories
      +-- matching archive index / closure log / retained archive paths
      +-- explicit legacy range evidence
      |
      v
spec_id_inventory -> next_available_spec_number + confidence + diagnostics
      |
      +-- caller slug
      +-- template authority
      +-- safe specs-root path
      v
spec_creation_plan -> provisional path + artifacts + preconditions + fingerprint
```

`scan_specs` and no-active-spec orientation consume the same inventory result
and expose its next number plus a `spec_creation_plan` action. They do not
reimplement allocation arithmetic.

## Component Boundaries

- `lifecycle/core.py` owns scope selection, evidence parsing, diagnostics,
  monotonic allocation, slug/path validation, and creation-plan composition.
- `lifecycle/provenance.py` provides canonical JSON and evidence fingerprinting
  with a creation-plan-specific domain.
- `lifecycle/runtime_adapter.py` exposes retained CLI commands for validation,
  CI, MCP debugging, and no-MCP recovery.
- `spec_mcp_server.py` exposes the normal agent-facing tools and attaches MCP
  provenance without changing core decisions.
- `spec_agent_schemas.py` defines closed input/output schemas using the shared
  Spec 036 metadata and bounded-response fragments.
- Existing template helpers remain authoritative; allocation consumes their
  reported decision rather than duplicating template selection.

## Low-Level Design

## Public Contracts

### `spec_id_inventory`

Inputs:

- `repo_root` at the adapter boundary;
- optional `docs_root`, resolved to exactly one repo-relative docs root.

The core result includes:

```json
{
  "schema_version": "1",
  "numbering_scope": {
    "docs_root": "docs",
    "specs_root": "docs/specs",
    "history_sources": [
      "docs/history/spec-archive-index.md",
      "docs/history/spec-closure-log.md"
    ]
  },
  "used_numbers": [0, 1, 2],
  "highest_used_number": 2,
  "next_available_spec_number": "003",
  "provisional": true,
  "confidence": "high",
  "evidence": [],
  "diagnostics": []
}
```

Evidence entries carry source kind, repo-relative source/path, parsed spec ID,
numeric prefix, and status. Normal results are deterministically ordered by
numeric prefix, spec ID, source priority, and path. Duplicate prefixes,
malformed IDs, ambiguous history ownership, missing selected-root history, and
legacy coverage gaps are diagnostics rather than silently discarded inputs.

### `spec_creation_plan`

Inputs add required `slug` and optional `expected_fingerprint`. A valid plan
returns:

- the embedded numbering scope and provisional next number;
- `proposed_spec_id` and repo-relative `proposed_path`;
- template authority and deterministic fallback chain;
- planned core artifacts and required user values;
- collision/revalidation preconditions;
- MCP-first and retained CLI validation commands;
- `evidence_fingerprint`, `provisional: true`, and `reservation: false`.

If `expected_fingerprint` differs, return `status: stale` with a freshly
calculated proposal and refreshed arguments. A path or prefix collision is a
stale/collision result, never an instruction to reuse the previous number.

## Numbering Scope And Evidence

One invocation owns one explicit docs root. Default `docs` remains compatible,
but a caller selecting `docs/platform` consults only:

- `docs/platform/specs/`;
- `docs/platform/history/spec-archive-index.md` and closure log when present;
- retained archive paths beneath that partition;
- explicitly recognized legacy-range records belonging to that partition.

The tool never borrows another root's history. More than one plausible history
owner yields `SPEC_ID_HISTORY_AMBIGUOUS`; no matching historical source in an
established root yields reduced confidence and `SPEC_ID_HISTORY_MISSING`.

Parse numeric prefixes only from canonical ASCII IDs matching
`^[0-9]{3,}-[a-z0-9]+(?:-[a-z0-9]+)*$`. Preserve malformed evidence in
diagnostics. Duplicate numeric prefixes are allowed as evidence but produce
`SPEC_ID_PREFIX_DUPLICATE` and reduce confidence. Explicit legacy upper bounds
participate in the maximum even when individual entries are unavailable.

Allocation is:

```text
if no parsed prefix or legacy upper bound exists: 000
else: zero-pad(max(all parsed prefixes and upper bounds) + 1, at least 3)
```

Lower gaps are never reused by v1.

## Slug And Path Safety

Accept only ASCII lower-kebab slugs matching
`^[a-z0-9]+(?:-[a-z0-9]+)*$`. Reject empty values, separators, dot segments,
control characters, non-ASCII text, repeated hyphens, and leading/trailing
hyphens before path construction.

Construct `<selected-specs-root>/<number>-<slug>`, normalize it, and prove with
path ancestry that it remains below the selected specs root. Return only
repo-relative POSIX paths. Existing paths or prefixes cause collision output.

## Template And Artifact Planning

Template authority is resolved in this order:

1. `<selected-docs-root>/templates/spec-package/`;
2. repository-root `docs/templates/spec-package/` when the selected root differs;
3. the skill fallback `references/spec-package/`.

The plan lists the files present in the selected authority, but always
identifies `requirements.md`, `design.md`, and `tasks.md` as core lifecycle
artifacts. It reports optional artifacts separately and never copies them.
Required user values include project intent and slug plus any unresolved
template placeholders that cannot be derived safely.

## Evidence Fingerprint

Use shared canonical JSON with domain `spec-creation-plan-v1` over:

- normalized numbering scope;
- sorted evidence identities, parsed prefixes, explicit upper bounds, and
  decision-relevant diagnostics;
- selected template authority and relative template file inventory;
- validated slug, proposed ID/path, artifact set, and preconditions.

Exclude timestamps, absolute paths, diagnostic prose, invocation metadata,
file contents, and user identity. Any changed allocation input, template
authority, scope, or claimed path changes the fingerprint.

## Bootstrap And Orientation Integration

`bootstrap_plan` calls the shared allocator. An empty scope still yields `000`,
but the value is no longer hard-coded. Established repositories may call
`spec_creation_plan` directly without blank-repository classification.

`scan_specs` and no-active-spec context add:

- `next_available_spec_number` when allocation is usable;
- allocation confidence and diagnostics summary;
- a `plan_spec_creation` next action targeting `spec_creation_plan`.

These are additive fields. Existing scan inventories and bootstrap defaults
remain compatible.

## Future Writer Boundary

V1 is read-only. Revalidation proves only that the evidence fingerprint still
matches at the instant of the check. A future writer must atomically claim the
directory, fail closed on collision, and then either return a fresh proposal or
require an explicit retry. Validation followed by ordinary file writes is not
race-safe and must never be described as reservation.

## Operational Considerations

## Error Handling

- Invalid docs roots, ambiguous ownership, or path escape attempts fail closed.
- Malformed evidence and duplicates remain visible with reduced confidence.
- Invalid slugs return diagnostics and no proposed path.
- Unsupported schema/detail values fail adapter validation.
- Source read failures become bounded diagnostics; they are not treated as an
  empty high-confidence inventory.

## Verification Strategy

Cover empty/bootstrap, active, removed, retained, legacy-range, duplicate,
malformed, multi-root, missing/ambiguous history, slug rejection, path escape,
collision, template precedence, fingerprint stability/staleness, read-only
behavior, scan/no-active integration, bootstrap reuse, MCP/CLI parity, schema
validation, privacy, and source/bundle parity.

## Durable Promotion Targets

- `docs/design/spec-lifecycle-management.md`
- `docs/reference/spec-lifecycle-runtime.md`
- `skills/spec-lifecycle-manager/SKILL.md`
- backlog B061 and roadmap status

## Residual Risks

- Repositories with incomplete historical records can only receive reduced
  confidence; v1 does not reconstruct missing Git history automatically.
- Provisional allocation remains vulnerable to concurrent claims until a
  separately specified atomic writer exists.
- Repository-specific nonstandard history formats require explicit adapters or
  diagnostics rather than heuristic silent acceptance.

## Open Questions

None blocking task planning.
