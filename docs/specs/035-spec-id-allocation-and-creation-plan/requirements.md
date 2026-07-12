---
title: Spec ID allocation and creation plan requirements
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: requirements
owner: platform
last_reviewed: 2026-07-12
backlog_item: B061
priority: P2
---

# Requirements

## Introduction

Agents currently choose a new `docs/specs/[###-slug]/` identifier by scanning
active packages and historical records themselves. The runtime has no
authoritative next-number surface, while blank-repository `bootstrap_plan`
hard-codes `000`. This creates avoidable tool calls, inconsistent treatment of
closed IDs, and collision risk when more than one agent creates a package.

This spec defines deterministic, archive-aware spec ID inventory and a
preview-only creation plan. The runtime selects a provisional monotonic number,
reports its evidence and confidence, and prepares the package path and template
authority without claiming an atomic reservation or writing files.

## Goals

- Return the next provisional numeric spec ID without agent-side arithmetic.
- Keep allocation monotonic across active, archived, removed, and explicitly
  retained spec evidence; do not reuse gaps by default.
- Detect duplicate numeric prefixes, malformed package IDs, and incomplete
  historical coverage.
- Integrate the same allocation logic into bootstrap and normal creation plans.
- Expose the next provisional ID through normal scan and no-active-spec
  orientation so an agent does not need a separate discovery round trip.
- Preview the proposed ID, slug, path, template authority, artifact set,
  preconditions, and validation commands through MCP and CLI surfaces.

## Non-Goals

- Do not reserve an ID atomically in the read-only v1 surface.
- Do not create or populate a spec package automatically.
- Do not infer a feature slug when the caller has not supplied one.
- Do not renumber existing specs or reuse historical gaps automatically.
- Do not merge spec numbering with durable-document numbering.

## Glossary

| Term | Definition |
|------|------------|
| numeric prefix | Zero-padded leading number in a package ID such as `035` in `035-example`. |
| provisional allocation | A read-only next-ID result that must be revalidated immediately before package creation. |
| numbering evidence | Active packages, archive index, closure log, retained archive paths, and explicit legacy-gap records used to calculate the next ID. |
| creation plan | Preview-only result containing the proposed ID/path, template authority, planned artifacts, preconditions, and validation. |
| numbering scope | One explicitly selected docs root together with its active-spec and matching history locations. |
| evidence fingerprint | Deterministic digest of the allocation inputs used to detect a stale creation plan; it is not a reservation. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Discovers active packages and parses closure/archive history, but exposes no allocation contract. | high | Shared runtime target. |
| `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | Exposes scan and bootstrap planning; bootstrap accepts a slug and previews `000-<slug>`. | high | MCP target. |
| `docs/reference/spec-lifecycle-runtime.md` | Defines MCP-first runtime and preview-only bootstrap behavior. | high | Durable reference target. |
| `docs/design/spec-lifecycle-management.md` | Defines temporary spec packages and numbering conventions. | high | Durable design target. |
| `docs/history/spec-archive-index.md` | Records closed spec IDs where current archive metadata exists. | high | Allocation evidence. |
| `docs/history/spec-closure-log.md` | Preserves older closed IDs and legacy history. | medium | May contain incomplete or non-tabular history. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| design | modify | `docs/design/spec-lifecycle-management.md` | Define monotonic provisional allocation and creation planning. |
| reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document MCP/CLI contracts and staleness behavior. |
| skill guidance | modify | `skills/spec-lifecycle-manager/SKILL.md` | Require runtime allocation rather than agent-side numbering. |
| backlog | modify | `docs/backlog/README.md` | Mark B061 complete at closure. |
| tests | add | `tests/runtime/` | Cover inventory, history, collisions, roots, and parity. |
| package parity | modify | `plugins/spec-lifecycle-manager/`, `packaging/spec-lifecycle-manager/` | Sync bundled copies, schemas, manifests, and install validation. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** numbering evidence precedence, legacy-gap handling,
  provisional allocation semantics, and creation-plan/write boundaries are accepted.
- **Design-first exception:** no
- **Optional artifacts recommended:** `research.md` only if historical ID parsing needs empirical classification
- **Downstream review needed:** design, tasks, traceability, verification

## Requirements

### Requirement 1: Numbering Inventory

**User Story:** As a coding agent, I want the runtime to inventory used spec
numbers, so that I do not reconstruct allocation state manually.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN active packages exist under the explicitly selected docs root, WHEN numbering
   inventory runs, THEN THE SYSTEM SHALL report their numeric prefixes and paths.
2. GIVEN archive-index, closure-log, or retained archive evidence contains
   closed spec IDs, WHEN inventory runs, THEN THE SYSTEM SHALL include those IDs.
3. GIVEN duplicate numeric prefixes or malformed IDs exist, WHEN inventory
   runs, THEN THE SYSTEM SHALL return deterministic diagnostics and evidence.
4. GIVEN historical coverage is incomplete or represented by a legacy range,
   WHEN inventory runs, THEN THE SYSTEM SHALL report reduced confidence rather
   than silently treating the missing history as unused.
5. GIVEN a selected docs root has no matching history source or has ambiguous
   history ownership, WHEN inventory runs, THEN THE SYSTEM SHALL return an
   ambiguity diagnostic rather than consulting another docs root silently.

### Requirement 2: Next Spec ID

**User Story:** As a coding agent, I want one call to return the next provisional
spec ID, so that numbering is consistent across repositories and clients.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN valid numbering evidence exists, WHEN next-ID allocation runs, THEN
   THE SYSTEM SHALL return one more than the greatest parsed prefix or explicit
   legacy-range upper bound in the selected numbering scope.
2. GIVEN lower-numbered gaps exist, WHEN allocation runs, THEN THE SYSTEM SHALL
   not reuse them by default.
3. GIVEN the caller supplies a valid ASCII lower-kebab slug containing only
   lowercase letters, digits, and single hyphens, WHEN allocation runs, THEN THE SYSTEM
   SHALL return the padded number, proposed spec ID, and repo-relative path.
4. GIVEN a slug contains a separator, dot segment, control character, empty
   segment, leading/trailing hyphen, or non-ASCII character, WHEN allocation
   runs, THEN THE SYSTEM SHALL reject it and SHALL NOT construct a path.
5. GIVEN no numbering evidence exists, WHEN allocation runs, THEN THE SYSTEM
   SHALL use `000` as the first numeric prefix for bootstrap compatibility.
6. GIVEN the result is read-only, WHEN it is returned, THEN THE SYSTEM SHALL
   label it provisional and require revalidation before creation.

### Requirement 3: Preview-Only Creation Plan

**User Story:** As a maintainer, I want allocation and package planning in one
call, so that an agent does not separately discover numbers, templates, paths,
and validation steps.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a slug and explicitly selected docs root, WHEN creation planning runs, THEN THE
   SYSTEM SHALL return the proposed ID/path, template authority, planned core
   artifacts, required user values, preconditions, validation commands, selected
   numbering scope, and evidence fingerprint.
2. GIVEN repository spec-package templates exist, WHEN planning runs, THEN THE
   SYSTEM SHALL prefer them over fallback templates and report the decision.
3. GIVEN the proposed path or numeric prefix has been claimed, WHEN planning or
   pre-creation revalidation runs, THEN THE SYSTEM SHALL report a collision and
   propose a freshly calculated ID.
4. GIVEN write intent is absent, WHEN the plan runs, THEN THE SYSTEM SHALL not
   mutate files.
5. GIVEN a docs root or proposed path is normalized, WHEN the plan is returned,
   THEN THE SYSTEM SHALL prove the path remains beneath the selected specs root.
6. GIVEN a docs-root-specific spec-package template exists, WHEN planning runs,
   THEN THE SYSTEM SHALL prefer that template; otherwise it SHALL report the
   repository-root and skill-fallback chain deterministically.

### Requirement 4: Bootstrap And Existing Repo Consistency

**User Story:** As a plugin maintainer, I want bootstrap and normal creation to
share allocation semantics, so that `000` is not an accidental special case.

**Priority:** should-have

#### Acceptance Criteria

1. GIVEN bootstrap previews an optional first spec, WHEN it selects a path,
   THEN THE SYSTEM SHALL use the shared numbering policy.
2. GIVEN an established repository requests a new spec, WHEN creation planning
   runs, THEN THE SYSTEM SHALL work without misclassifying the repo as blank.
3. GIVEN MCP and CLI expose inventory, next-ID, and creation-plan behavior,
   WHEN their results are compared, THEN THE SYSTEM SHALL return equivalent data
   from shared internals.
4. GIVEN `scan_specs` or no-active-spec orientation returns for a selected docs
   root, WHEN allocation evidence is valid, THEN THE SYSTEM SHALL include
   `next_available_spec_number` and a creation-plan action without requiring
   agent-side arithmetic.

### Requirement 5: Stale Plan Validation And Future Write Boundary

**User Story:** As a future package writer, I want a creation plan to carry
verifiable evidence, so that stale advisory allocation is never mistaken for a
safe reservation.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a creation plan is revalidated against unchanged evidence, WHEN
   validation runs, THEN THE SYSTEM SHALL confirm the fingerprint and proposed
   path without claiming a reservation.
2. GIVEN numbering evidence, template authority, scope, or the proposed path
   changed, WHEN validation runs, THEN THE SYSTEM SHALL fail the plan as stale
   and return a freshly calculated proposal.
3. GIVEN a future writer consumes a valid plan, WHEN it creates the package,
   THEN ITS CONTRACT SHALL require an atomic directory claim and fail or
   reallocate on collision; validation followed by ordinary writes SHALL NOT be
   described as race-safe.

## Correctness Properties

- **CP-001:** A returned next number is greater than every parsed active or
  historical prefix and every explicit legacy-range upper bound in the selected
  numbering scope.
- **CP-002:** Identical repository evidence and inputs produce identical plans.
- **CP-003:** Read-only allocation and creation planning never mutate files.
- **CP-004:** A stale provisional allocation cannot be presented as reserved or
  safe to write without revalidation.
- **CP-005:** MCP and CLI results are equivalent for the same repository state.
- **CP-006:** A proposed path cannot escape the selected specs root.
- **CP-007:** A changed allocation input invalidates the evidence fingerprint.

## Technical Context

- **Language/Version:** Python standard library runtime and JSON MCP transport.
- **Primary Dependencies:** active spec discovery, archive-index and closure-log parsers, template authority.
- **Target Platform:** Codex, Claude Code, and retained CLI validation/recovery.
- **Constraints:** repo-relative output; multiple docs roots; removal-by-default history; no v1 write mutation.
- **Performance Goals:** one bounded repository inventory suitable for spec creation preflight.

## Accepted Design Decisions

- Reuse the shared Spec 036 canonical JSON and evidence-fingerprint helper with
  a `spec-creation-plan-v1` domain. Fingerprint only selected scope, normalized
  numbering evidence, template authority, requested slug, proposed path, and
  artifact/precondition contract.
- Expose two public read-only surfaces: `spec_id_inventory` owns numbering
  evidence and `next_available_spec_number`; `spec_creation_plan` requires a
  caller-supplied slug and composes inventory with template and path planning.
  Add the next number and a creation-plan action to scan/no-active orientation
  instead of creating a third next-ID tool.

## Success Criteria

- **SC-001:** Agents can obtain a proposed spec ID and package path in one call.
- **SC-002:** Active, closed, retained, malformed, duplicate, and legacy-range fixtures are covered.
- **SC-003:** Bootstrap and established-repo creation use one documented numbering contract.
- **SC-004:** Collision and staleness behavior is explicit enough for a future guarded creation writer.
- **SC-005:** Multi-root, traversal, Unicode-confusable, legacy-range, and
  concurrent-state-change fixtures exercise fail-closed behavior.

## Related Artifacts

- Backlog: `docs/backlog/README.md` B061
- Contract dependency: `docs/specs/036-compact-output-and-invocation-telemetry/requirements.md`
- Design: `docs/specs/035-spec-id-allocation-and-creation-plan/design.md`
- Tasks: not created yet
- Verification: not created yet
