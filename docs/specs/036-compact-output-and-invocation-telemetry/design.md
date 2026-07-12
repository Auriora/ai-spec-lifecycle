---
title: Compact lifecycle output and invocation provenance design
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

Spec 036 introduces a caller-agnostic provenance library and attaches metadata
only at transport boundaries. New aggregate tools use a versioned compact
envelope; established tools keep their current fields and defaults. The first
implementation slice replaces stale hard-coded runtime identity and establishes
fingerprint/provenance primitives without globally changing tool results.

## High-Level Design

```text
lifecycle core decision payload
             |
             v
MCP / CLI / hook adapter ---- root source + invocation surface
             |
             v
provenance helper ----------- package/build/repository identity
             |
             v
compatible result or new compact aggregate envelope
```

### Component Boundaries

- `lifecycle/provenance.py` owns canonical JSON, evidence fingerprints,
  package/build identity resolution, repository identity, and metadata assembly.
- `lifecycle/core.py` remains caller-agnostic and does not infer invocation
  surface or transport metadata.
- `spec_mcp_server.py` and `lifecycle/runtime_adapter.py` retain root-source
  information and attach metadata at their response boundaries.
- `spec_agent_schemas.py` exposes reusable metadata and compact-envelope schema
  fragments. Existing schemas remain additive and compatible.
- packaging produces or carries immutable build identity. Missing build data is
  represented as `unknown`, never guessed from the target repository.

## Low-Level Design

### Public Contract

#### Metadata Object

The additive object is named `lifecycle_metadata`:

```json
{
  "schema_version": "1",
  "package_version": "0.3.0",
  "build_identity": "unknown",
  "invocation_surface": "mcp",
  "composition_sources": [],
  "repo_root": ".",
  "repo_identity": "sha256:<hex-or-unknown>",
  "root_source": "argument",
  "fallback_reason": "none"
}
```

Allowed invocation surfaces are `mcp`, `cli`, `hook`, `prompt`, and `unknown`.
Allowed root sources are `argument`, `environment`, `cwd`, and `unknown`.
Fallback reasons follow the closed enum in requirements, with `other` for a
future unrecognized class.

#### Compact Envelope

New aggregate tools default to `detail=compact`; `detail=full` returns the
bounded complete current result and `detail=section` requires a section name.
Compact results preserve decision fields and blockers, cap summaries at 20 and
next actions at 10, target 32 KiB, and expose:

- truncation and limit state;
- schema version;
- deterministic follow-up `{tool, arguments}`;
- an evidence fingerprint.

Established tools retain existing defaults. They may receive additive metadata
only after their schema and compatibility tests cover it.

### Deterministic Identity Algorithms

#### Evidence Fingerprint

1. Select only decision-relevant fields defined by the calling tool.
2. Normalize in-repository paths to POSIX repo-relative form.
3. Add an explicit fingerprint schema/domain tag.
4. Serialize UTF-8 JSON with sorted keys and compact separators.
5. Return `sha256:<hex digest>`.

Timestamps, absolute paths, prompts, file contents, secrets, and user identity
are excluded. Expansion recomputes the fingerprint; mismatch returns `stale`
with refreshed arguments because v1 stores no historical snapshots.

#### Runtime And Build Identity

The resolver searches the owning distribution, not the target repository:

1. adjacent generated `build-info.json`;
2. owning `.codex-plugin/plugin.json` or `.claude-plugin/plugin.json`;
3. source-checkout `package.json` whose package name matches this project;
4. `unknown`.

Package version is sourced from the same owning manifest. Build identity is an
immutable packaged commit/build identifier or `unknown`. The MCP initialize and
capabilities responses use this resolver instead of constants.

#### Repository Identity

When Git evidence exists, compute SHA-256 over the domain
`spec-lifecycle-repo-v1`, a NUL separator, and the repository root commit ID.
Non-Git or unborn repositories return `unknown`. The hash exposes no host path,
but it can be correlated with a known public repository; durable reference docs
must disclose that limitation.

### Root And Invocation Provenance

Adapters preserve how the root was selected rather than trying to reconstruct
it after resolution. Explicit arguments outrank environment binding, which
outranks current working directory. Hook execution reports `hook`, even when it
uses the retained CLI adapter internally. Internal composition is recorded in a
bounded `composition_sources` list and never replaces the external surface.

## Operational Considerations

### Compatibility And Rollout

1. Land pure provenance and fingerprint helpers with tests.
2. Replace hard-coded MCP package version in initialize and capabilities.
3. Add metadata to capabilities as the compatibility canary.
4. Add reusable schemas and build-info packaging validation.
5. Apply the contract to new Spec 033 and Spec 035 aggregate surfaces.
6. Measure established high-volume tools before proposing later migration.

No existing full/default payload is compacted in this spec's first slice.

### Error Handling

- Missing or malformed identity files yield `unknown` plus a deterministic
  local diagnostic in validation surfaces; normal calls remain available.
- Unsupported detail values fail schema validation.
- Fingerprint mismatch returns `stale`, not historical evidence.
- Mandatory blockers exceeding the size target remain present and set
  `limit_exceeded`; correctness outranks the byte target.

## Verification Strategy

- Unit-test canonical serialization, fingerprint stability, identity fallback,
  repository identity, privacy exclusions, and enum validation.
- Assert MCP initialize and lifecycle capabilities use the authoritative
  package version while preserving established fields.
- Assert MCP, CLI, and hook surfaces and root-source precedence at adapters.
- Validate JSON schemas, package contract, source/bundle parity, and full tests.

## Durable Promotion Targets

- `docs/design/spec-lifecycle-management.md`
- `docs/reference/spec-lifecycle-runtime.md`
- `skills/spec-lifecycle-manager/SKILL.md`
- package/build contract documentation where generated identity is introduced

## Residual Risks

- Repository identity is intentionally correlatable to known Git history.
- The 32 KiB target requires real payload measurements before established-tool
  migration.
- Installed legacy bundles without build information remain diagnosable only by
  package version and `unknown` build identity.

## Open Questions

None blocking the first implementation slice. Exact build-info generation is a
later task whose contract is fixed here but whose release integration remains
subject to packaging validation.
