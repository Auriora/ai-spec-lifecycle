---
title: Compact lifecycle output and invocation provenance requirements
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: requirements
owner: platform
last_reviewed: 2026-07-12
backlog_item: B062
priority: P2
---

# Requirements

## Introduction

Session analysis shows frequent lifecycle calls, especially package linting,
and large nested results that consume agent context. The same histories are
difficult to interpret because responses do not consistently state runtime
version, resolved repository root, invocation surface, or why a direct-runtime
fallback was recommended. This spec defines a common compact response envelope
and privacy-safe invocation provenance for lifecycle tools. It does not own
OpenTelemetry spans, metrics, collection, or export; backlog B025 remains the
authority for operational observability.

## Goals

- Define a bounded, versioned response contract for new aggregate lifecycle
  surfaces without silently changing established tool defaults.
- Preserve complete evidence through deterministic follow-up arguments,
  evidence fingerprints, or explicit detail modes rather than embedding every
  nested payload.
- Report runtime version, invocation surface, resolved root, and fallback reason
  consistently enough for agents and local session analysis.
- Preserve deterministic behavior and avoid network observability export.
- Apply compact defaults first to new aggregate lifecycle surfaces; adopt
  provenance additively on selected established tools.

## Non-Goals

- Do not emit spans, metrics, or response provenance to a remote service.
- Do not record prompts, source content, secrets, or user identities.
- Do not remove evidence required to understand blockers.
- Do not make session-history availability a runtime dependency.
- Do not redefine lifecycle readiness, evidence, or closure semantics.

## Glossary

| Term | Definition |
|------|------------|
| compact envelope | Bounded response containing decision fields, counts, diagnostics summary, and references to detail. |
| expansion reference | Deterministic follow-up arguments plus an evidence fingerprint for retrieving bounded current detail or reporting stale evidence. |
| invocation surface | External entry point that returned the response: `mcp`, `cli`, `hook`, `prompt`, or `unknown`. |
| composition sources | Bounded list of internal lifecycle signals composed by an outer call; never a replacement for the external invocation surface. |
| fallback reason | Structured reason a direct runtime command is appropriate, such as CI, package validation, MCP debugging, or MCP unavailable. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/reference/spec-lifecycle-runtime.md` | Defines MCP-first use and allowed direct-runtime fallbacks. | high | Durable envelope/fallback target. |
| `skills/spec-lifecycle-manager/SKILL.md` | Defines runtime access order and context-budget rules. | high | Agent guidance target. |
| `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | Builds MCP results and exposes server version/root context. | high | Transport target. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Produces detailed lifecycle payloads shared by MCP and CLI. | high | Summary/detail seam. |
| `docs/specs/033-phase-gate-check/requirements.md` | Defines a bounded composite gate over existing signals. | high | First aggregate consumer. |
| `docs/specs/035-spec-id-allocation-and-creation-plan/requirements.md` | Defines inventory and creation-plan responses. | high | Second aggregate consumer. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| design | modify | `docs/design/spec-lifecycle-management.md` | Define compact/detail and local metadata boundaries. |
| reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document envelope fields and expansion behavior. |
| skill guidance | modify | `skills/spec-lifecycle-manager/SKILL.md` | Prefer compact results and targeted expansion. |
| backlog | modify | `docs/backlog/README.md` | Mark B062 complete at closure. |
| tests | add | `tests/runtime/` | Cover bounds, parity, redaction, and metadata. |
| package parity | modify | `plugins/spec-lifecycle-manager/`, `packaging/spec-lifecycle-manager/` | Sync bundled code, schemas, package/build identity, and install validation. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** satisfied on 2026-07-12 by the decisions below.
- **Design-first exception:** no
- **Optional artifacts recommended:** `research.md` for representative payload sizing only
- **Downstream review needed:** design, tasks, traceability, verification

## Requirements

### Requirement 1: Compact Default Results

**User Story:** As a coding agent, I want bounded lifecycle results, so that
routine checks do not consume context with low-value nested detail.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a lifecycle result contains repeated artifact, task, diagnostic, or
   evidence rows, WHEN default output is rendered, THEN THE SYSTEM SHALL return
   decision fields, counts, at most 20 summary findings, truncation state, and
   at most 10 next actions; serialized compact content SHALL target 32 KiB and
   SHALL report `limit_exceeded` if mandatory blockers alone exceed that target.
2. GIVEN omitted detail could affect a decision, WHEN the compact result is
   rendered, THEN THE SYSTEM SHALL provide deterministic follow-up arguments,
   an evidence fingerprint, and a schema version.
3. GIVEN a blocking diagnostic exists, WHEN output is compacted, THEN THE SYSTEM
   SHALL preserve its severity, code, source, and non-waivable status.
4. GIVEN a caller explicitly requests supported detail, WHEN the tool runs,
   THEN THE SYSTEM SHALL return bounded detail without changing semantics.
5. GIVEN repository evidence no longer matches an expansion fingerprint, WHEN
   expansion runs, THEN THE SYSTEM SHALL report `stale` and new follow-up
   arguments rather than claim to retrieve an unstored historical snapshot.

### Requirement 2: Invocation Metadata

**User Story:** As a maintainer, I want lifecycle responses to identify their
runtime context, so that stale installs and wrong-root behavior are diagnosable.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a v1 aggregate lifecycle call returns through an adapter, WHEN metadata
   is attached, THEN THE SYSTEM SHALL identify schema version, authoritative
   package/runtime version, build identity or `unknown`, and `repo_root: "."`.
2. GIVEN an adapter returns a response, WHEN metadata is attached, THEN THE
   SYSTEM SHALL report exactly one external `invocation_surface` from `mcp`,
   `cli`, `hook`, `prompt`, or `unknown`.
3. GIVEN an aggregate internally composes lifecycle signals, WHEN metadata is
   attached, THEN THE SYSTEM SHALL retain the external invocation surface and
   MAY include at most 20 normalized `composition_sources`.
4. GIVEN a response recommends a direct runtime command, WHEN provenance is
   rendered, THEN THE SYSTEM SHALL classify `fallback_reason` as `ci`,
   `package_validation`, `hook_execution`, `mcp_debugging`, `mcp_unavailable`,
   `explicit_recovery`, `other`, or `none`.
5. GIVEN source, bundle, and installed versions can differ, WHEN metadata is
   attached, THEN THE SYSTEM SHALL use authoritative package/build identities
   rather than a transport-local constant and SHALL represent missing identity
   as `unknown`.
6. GIVEN wrong-root diagnosis is needed, WHEN metadata is attached, THEN THE
   SYSTEM SHALL preserve `repo_root: "."` and add a privacy-reviewed non-path
   `repo_identity` plus `root_source` from `argument`, `environment`, `cwd`, or
   `unknown`.

### Requirement 3: Privacy And Determinism

**User Story:** As a repository owner, I want useful local provenance without
content disclosure, so that observability does not create a new privacy risk.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN invocation metadata is produced, WHEN it is rendered, THEN THE SYSTEM
   SHALL not include prompts, file contents, secrets, user identity, remote
   URLs, or remote transmission.
2. GIVEN the same input and runtime state, WHEN compact output is produced,
   THEN THE SYSTEM SHALL preserve deterministic decision content and expansion identity.
3. GIVEN absolute host paths are present internally, WHEN user-facing metadata
   is rendered, THEN THE SYSTEM SHALL use repo-relative paths unless the target
   is outside the repository and the path is necessary evidence.

### Requirement 4: Adoption And Compatibility

**User Story:** As a plugin maintainer, I want compact output introduced safely,
so that existing consumers are not silently broken.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a tool has an existing documented output schema, WHEN provenance is
   introduced, THEN THE SYSTEM SHALL add metadata compatibly without removing
   or renaming established decision fields.
2. GIVEN an established tool supports full payloads by default, WHEN v1 ships,
   THEN THE SYSTEM SHALL preserve that default or introduce a versioned new
   surface; a default flip requires a declared major schema/server version and
   migration window.
3. GIVEN phase gate and spec creation planning are new aggregate surfaces, WHEN
   their public schemas are frozen, THEN THE SYSTEM SHALL apply this compact
   envelope and default to compact output.
4. GIVEN MCP and CLI expose equivalent commands, WHEN compared, THEN THE SYSTEM
   SHALL preserve equivalent lifecycle decisions even if transport metadata differs.
5. GIVEN a tool adopts the envelope, WHEN it is published, THEN THE SYSTEM SHALL
   publish and validate a JSON Schema for its compact and supported detail modes.

## Correctness Properties

- **CP-001:** Compaction never changes readiness, severity, task state, or
  closure meaning.
- **CP-002:** Every omitted decision-relevant detail has a valid expansion route.
- **CP-003:** Invocation metadata contains no prompt, secret, or source-content fields.
- **CP-004:** Equivalent MCP and CLI calls produce equivalent lifecycle decisions.
- **CP-005:** Default payload bounds are deterministic and explicitly report truncation.
- **CP-006:** Internal composition never overwrites the external invocation surface.
- **CP-007:** Metadata is attached at transport boundaries; shared core
  lifecycle decisions do not infer their caller.

## Technical Context

- **Language/Version:** Python standard library, MCP JSON, retained CLI JSON.
- **Primary Dependencies:** shared lifecycle payloads, MCP result envelope, runtime adapter.
- **Target Platform:** Codex and Claude Code plugin clients plus local CI/recovery.
- **Constraints:** backward compatibility; schema versioning; repo-relative output; no remote service.
- **Performance Goals:** keep new aggregate defaults within the stated bounds
  while retaining one-step targeted expansion; measure established tools before
  proposing any later default migration.

## Accepted Requirements Decisions

| Decision | Rationale | Status |
|----------|-----------|--------|
| New aggregate tools use same-tool `detail=compact\|full\|section`; established tools retain their defaults. | Avoids stored cursors and preserves compatibility while enabling one-step expansion. | accepted |
| Fingerprints use domain-tagged, sorted, compact UTF-8 JSON and SHA-256 over repo-relative decision inputs. | Produces deterministic expansion identity without timestamps, content payloads, or host paths. | accepted |
| Repository identity uses a domain-separated hash of the Git root commit identity, otherwise `unknown`. | Distinguishes repositories without exposing host paths; the value is correlatable to a known public repository and must be documented as such. | accepted with privacy caveat |

## Success Criteria

- **SC-001:** New aggregate compact responses honor the 20-finding, 10-action,
  and 32-KiB target contract; established defaults remain compatible.
- **SC-002:** Agents can expand any decision-relevant omitted detail with one bounded follow-up.
- **SC-003:** Session evidence can distinguish MCP use from allowed CLI fallback classes.
- **SC-004:** Tests prove no readiness, severity, privacy, or parity regression.

## Related Artifacts

- Backlog: `docs/backlog/README.md` B062
- Related spec: `docs/specs/033-phase-gate-check/requirements.md`
- Related spec: `docs/specs/035-spec-id-allocation-and-creation-plan/requirements.md`
- Design: not created yet
- Tasks: not created yet
- Verification: not created yet
