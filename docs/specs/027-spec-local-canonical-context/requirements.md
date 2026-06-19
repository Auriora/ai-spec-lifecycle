---
title: Spec-local canonical context requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-19
---

# Requirements

## Introduction

Agents following an active spec can be led astray by older durable documents,
legacy reviews, or historical spec content that still exists in a repository.
The current lifecycle model says durable docs feed active specs and accepted
behavior is later promoted back to durable docs, but it does not give agents a
strict enough rule for which documents are canonical during an implementation
slice.

This spec introduces a spec-local canonical context model. During active
implementation, the active spec package declares the working sources an agent
may treat as canonical for that change. Durable governance, policy, security,
repository instructions, generated contracts, and live/system evidence remain
authoritative from their durable locations. Other durable docs remain useful
background only when the spec imports, references, or classifies them.

## Goals

- Define a spec-local canonical context artifact and workflow.
- Prevent stale or legacy durable docs from silently overriding an active spec.
- Preserve governance, policy, security, repository instructions, generated
  contracts, and live evidence as external authorities.
- Make copied or adapted durable content traceable to source path and source
  revision.
- Require accepted spec-local context to be promoted or routed before closure.
- Add template and runtime guidance so future specs can use the model
  consistently.

## Non-Goals

- Do not let active specs override `AGENTS.md`, governance, security, privacy,
  compliance, user instructions, system instructions, or generated/source-code
  contracts.
- Do not require every active spec to copy every durable document it touches.
- Do not move all durable docs into `docs/specs/` permanently.
- Do not implement a content ingestion or synchronization engine in the first
  slice.
- Do not change the repository's closure policy that completed spec packages
  are removed after durable promotion unless policy says otherwise.

## Glossary

| Term | Definition |
|------|------------|
| Spec-local canonical context | The active spec package's declared set of working sources that agents may treat as canonical for the implementation slice. |
| Always-canonical external source | A durable source that remains authoritative outside the spec package, such as `AGENTS.md`, governance, security policy, generated contracts, or live evidence. |
| Spec-canonical working source | A spec artifact, imported durable document, or adapted excerpt inside the active package that is canonical for the active implementation slice. |
| Imported source | A copied or adapted durable document or section placed under the active spec package with source path, source revision, and promotion target metadata. |
| Non-canonical background source | A durable or historical document that may explain context but must not drive implementation decisions for the active slice. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/spec-lifecycle-management.md` | Defines the lifecycle chain `durable docs -> active spec -> code/tests/config -> durable docs -> close spec`, durable source baselines, Agent Readiness Contract, context-budget discipline, and promotion rules. | high | Needs clarification that active specs can define canonical working context while preserving external authority exceptions. |
| `docs/design/coding-agent-operating-model.md` | Defines the quality spine, governance gates, evidence rules, and durable documentation boundary for coding-agent work. | high | Needs alignment with the spec-local context rule. |
| `docs/governance/constitution.md` | Contains governance constraints that outrank ordinary spec guidance. | high | Must remain an always-canonical external source. |
| `skills/spec-lifecycle-manager/SKILL.md` | Gives agents operational rules for reading specs, durable docs, reconciliation, implementation, promotion, and closure. | high | Main implementation target for behavior guidance. |
| `skills/spec-lifecycle-manager/references/spec-package/` | Provides fallback templates for new spec packages. | high | Needs a template or embedded sections for canonical context. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Provides scan, lint, readiness, reconciliation, promotion-plan, and closure checks. | high | May add warnings for missing canonical context when durable-doc impact is broad or stale-doc risk is declared. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| design | clarify | `docs/design/spec-lifecycle-management.md` | Add the spec-local canonical context model and external authority exceptions. |
| design | clarify | `docs/design/coding-agent-operating-model.md` | Add the agent operating rule for canonical working context. |
| governance | unchanged | `docs/governance/constitution.md` | Governance remains an always-canonical external authority. |
| skill guidance | modify | `skills/spec-lifecycle-manager/SKILL.md` | Add implementation, readiness, reconciliation, and closure guidance for canonical context. |
| templates | add | `skills/spec-lifecycle-manager/references/spec-package/` | Add a canonical-context template or embedded template sections. |
| runtime reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document any lint/readiness behavior added for canonical context. |
| tests | add | `tests/runtime/` or `tests/fixtures/` | Cover runtime diagnostics and template validation if runtime changes are implemented. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** authority hierarchy, canonical context artifact
  shape, imported-source metadata, lint/readiness behavior, and promotion rules
  are explicit.
- **Design-first exception:** no.
- **Optional artifacts recommended:** `change-impact.md`, `traceability.md`,
  `verification.md`
- **Downstream review needed:** design, templates, runtime behavior, closure
  behavior

## Requirements

### Requirement 1: Spec-Local Canonical Working Context

**User Story:** As a worker agent implementing an active spec, I want the spec
package to declare which documents are canonical for the slice, so that stale
legacy docs do not redirect the implementation.

#### Acceptance Criteria

1. GIVEN an active spec with canonical context declared, WHEN an agent prepares
   an implementation slice, THEN it SHALL treat the declared spec artifacts and
   imported sources as canonical working context for that slice.
2. GIVEN a durable document not listed as canonical, imported, or explicitly
   referenced by the spec, WHEN it conflicts with the active spec, THEN the
   agent SHALL treat that durable document as background or drift evidence
   rather than implementation authority.
3. WHEN an active spec has known stale or non-canonical documents, THEN it SHALL
   list them with a reason and the expected handling.
4. IF canonical context is missing for a broad durable-doc-impacting change,
   THEN readiness or lint output SHALL identify that gap.

### Requirement 2: Always-Canonical External Authority Exceptions

**User Story:** As a maintainer, I want governance and policy documents to
remain authoritative during spec work, so that a spec-local copy cannot bypass
repository rules.

#### Acceptance Criteria

1. GIVEN an active spec, WHEN it declares canonical working context, THEN it
   SHALL also preserve an always-canonical external source list or inherit the
   repository default list.
2. The default external authority list SHALL include applicable `AGENTS.md`
   files, system/developer/user instructions, governance docs, security policy,
   privacy/compliance policy, build/test/release instructions, generated
   contracts, source-code contracts, and live/system evidence where applicable.
3. IF spec-local context conflicts with an always-canonical external source,
   THEN the agent SHALL stop for reconciliation or a governance decision unless
   the user explicitly asks to change the higher-priority source.
4. The spec-local context model SHALL NOT weaken existing instruction priority
   rules.

### Requirement 3: Imported Durable Source Metadata

**User Story:** As a lead agent preparing a spec, I want copied or adapted
durable content to keep source metadata, so that future agents know where it
came from and how it should be promoted back.

#### Acceptance Criteria

1. WHEN durable content is copied or adapted into an active spec, THEN the
   imported source SHALL record source path, source revision or date,
   import/adaptation status, reason for import, and promotion target.
2. IF the imported content supersedes a durable document during the active
   slice, THEN the spec SHALL name the superseded source and the scope of
   supersession.
3. IF imported content is only background, THEN the spec SHALL label it as
   background and SHALL NOT treat it as canonical implementation authority.
4. Imported-source metadata SHALL use repo-relative paths in user-facing docs
   and diagnostics.

### Requirement 4: Agent Readiness And Context-Budget Integration

**User Story:** As a lead agent handing work to another agent, I want the
Agent Readiness Contract to name canonical and non-canonical sources, so that
the worker reads the right context first.

#### Acceptance Criteria

1. WHEN an Agent Readiness Contract is produced, THEN it SHALL identify
   spec-canonical working sources, always-canonical external sources, optional
   background sources, and known stale or non-canonical sources.
2. WHEN `task_context`, `traceability_lookup`, or equivalent runtime guidance
   lists must-read artifacts, THEN canonical context artifacts SHALL be visible
   for tasks that depend on them.
3. IF a task references a durable doc that has been superseded by spec-local
   context, THEN readiness output SHALL direct the agent to the spec-local
   source first.
4. Context-budget guidance SHALL prefer canonical context summaries and linked
   imported sections over broad scans of all durable docs.

### Requirement 5: Promotion And Closure Discipline

**User Story:** As a maintainer closing a spec, I want spec-local canonical
content promoted or routed, so that completed behavior does not remain trapped
inside temporary scaffolding.

#### Acceptance Criteria

1. BEFORE closure, accepted spec-local canonical content SHALL be promoted to
   durable docs, routed to backlog/roadmap/follow-up specs, or explicitly
   discarded with rationale.
2. Closure checks or closure guidance SHALL report residual spec-only canonical
   content as a blocker unless it is intentionally discarded or routed.
3. Promotion plans SHALL map imported or adapted sources back to durable
   destinations.
4. After closure, active indexes SHALL NOT present the removed spec package as
   the source of current behavior.

### Requirement 6: Template And Runtime Support

**User Story:** As a spec author, I want templates and runtime checks to guide
canonical context authoring, so that the rule is easy to apply consistently.

#### Acceptance Criteria

1. The fallback spec-package templates SHALL provide a canonical context
   artifact or canonical context sections.
2. Template guidance SHALL include examples for always-canonical external
   sources, spec-canonical working sources, imported sources, and non-canonical
   background sources.
3. Runtime lint or readiness checks SHALL warn when a spec declares broad
   durable-doc impact, stale-doc risk, or imported sources without enough
   canonical context metadata.
4. Existing specs SHALL NOT be forced to migrate unless they are resumed,
   modified for canonical context, or affected by a targeted migration decision.

## Correctness Properties

- **CP-001**: A spec-local canonical source cannot override an always-canonical
  external authority without an explicit governance or user decision.
- **CP-002**: Every imported durable source that is canonical for an active
  slice has source path and promotion target metadata.
- **CP-003**: Closure cannot claim durable completion while accepted canonical
  working content remains only in the active spec package.
- **CP-004**: Runtime guidance never instructs an agent to use stale or
  non-canonical background sources as implementation authority when a
  spec-local canonical source exists.

## Technical Context

- **Language/Version:** Python 3 standard library for runtime checks; Markdown
  for lifecycle docs and templates.
- **Primary Dependencies:** Existing `spec_runtime.py`, MCP adapter, fallback
  templates, and `unittest`.
- **Target Platform:** Local Codex skill and optional MCP server in repository
  checkouts.
- **Constraints:** Repo-relative user-facing paths; no new runtime dependency;
  advisory checks should avoid noisy false positives for small specs.
- **Performance Goals:** Canonical context diagnostics should run within
  existing scan/lint/readiness command expectations.

## Success Criteria

- **SC-001**: New spec-package guidance makes the active spec's canonical
  working context explicit without weakening governance or policy authority.
- **SC-002**: Future specs can copy/adapt durable docs into the active package
  with traceable source and promotion metadata.
- **SC-003**: Runtime or readiness guidance helps agents avoid stale durable
  docs for broad implementation slices.
- **SC-004**: Closure guidance blocks or flags accepted spec-local canonical
  content that has not been promoted, routed, or discarded.

## Related Artifacts

- Change Impact: `docs/specs/027-spec-local-canonical-context/change-impact.md`
- Design: `docs/specs/027-spec-local-canonical-context/design.md`
- Tasks: `docs/specs/027-spec-local-canonical-context/tasks.md`
- Traceability:
  `docs/specs/027-spec-local-canonical-context/traceability.md`
- Verification:
  `docs/specs/027-spec-local-canonical-context/verification.md`
