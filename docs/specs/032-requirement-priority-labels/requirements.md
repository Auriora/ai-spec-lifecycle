---
title: Requirement priority labels requirements
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: requirements
owner: platform
last_reviewed: 2026-07-05
backlog_item: B057
priority: P2
---

# Requirements

## Introduction

Specs currently express requirements as a flat set. During planning,
implementation, and closure, agents can struggle to distinguish mandatory
closure gates from useful-but-negotiable enhancements. This spec introduces the
MoSCoW Method as the standard requirement priority notation so agents can
reason about must-have, should-have, could-have, and explicit won't-have or
out-of-scope behavior without weakening correctness or closure discipline.

## Goals

- Add a clear, low-noise MoSCoW priority model for requirements.
- Let agents distinguish mandatory implementation/closure requirements from
  lower-priority enhancements during design, task planning, validation, and
  scope negotiation.
- Preserve compatibility with existing specs that lack priority labels.
- Define where priority belongs in requirements text, templates, traceability,
  and lint/runtime output.

## Non-Goals

- Do not let priority labels bypass accepted acceptance criteria.
- Do not retrofit every closed spec.
- Do not require complex prioritization frameworks beyond MoSCoW and the needs
  of this lifecycle skill.
- Do not change task status semantics in this spec unless design proves it is
  necessary.

## Glossary

| Term | Definition |
|------|------------|
| must-have | MoSCoW requirement priority that blocks implementation or closure when accepted and unfulfilled. |
| should-have | MoSCoW requirement priority that is expected but may be routed with explicit rationale. |
| could-have | MoSCoW requirement priority that is optional enhancement scope and should not block closure when routed or rejected. |
| won't-have | MoSCoW priority for explicit exclusions. In spec packages, use non-goals, out-of-scope text, or rejected/routed decisions instead of treating excluded work as an accepted requirement. |
| priority label | A stable MoSCoW notation attached to a requirement that communicates scope importance. Requirement-level priority is canonical for this spec. Acceptance-criterion-level overrides are out of scope unless a later design decision explicitly introduces them. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/backlog/README.md` B057 | Captures need for must/should/could requirement priority labels. | high | Source backlog item for this spec. |
| `skills/spec-lifecycle-manager/references/spec-package/requirements.md` | Current fallback requirements template has no priority metadata. | high | Likely template target. |
| `skills/spec-lifecycle-manager/references/spec-package/traceability.md` | Traceability can carry coverage state but not requirement priority. | medium | Possible target after design decision. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Runtime lint/readiness logic may need to parse or report priority. | high | Implementation target if labels affect diagnostics. |
| `skills/spec-lifecycle-manager/SKILL.md` | Skill guidance defines staged authoring, wizard behavior, closure review, and lifecycle semantics. | high | Durable source and promotion target if priority changes workflow guidance. |
| `docs/design/spec-lifecycle-management.md` | Durable lifecycle design describes requirements and closure reconciliation. | high | Durable promotion target. |

## Canonical Context

| Source | Canonical role | Promotion route | Notes |
|--------|----------------|-----------------|-------|
| `docs/backlog/README.md` B057 | Spec-canonical intake source | Mark B057 done at closure. | Backlog text is authoritative for accepted scope. |
| `skills/spec-lifecycle-manager/references/spec-package/requirements.md` | Current template source | Update if labels are adopted. | Template behavior should stay backward compatible. |
| `skills/spec-lifecycle-manager/SKILL.md` | Workflow guidance source | Update if priority affects staged authoring, wizard guidance, or closure review. | Skill guidance must match prompt/runtime behavior. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Runtime behavior source | Update runtime docs and tests if parsing or lint behavior changes. | Code-derived behavior overrides stale prose. |
| `docs/history/spec-archive-index.md` | Historical lookup only | No active spec edits. | Closed specs may provide evidence but are not active targets. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| requirements | modify | `skills/spec-lifecycle-manager/references/spec-package/requirements.md` | Add priority notation guidance. |
| design | clarify | `docs/design/spec-lifecycle-management.md` | Explain priority role in lifecycle stages. |
| reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document any runtime/lint behavior. |
| skill guidance | modify | `skills/spec-lifecycle-manager/SKILL.md` | Explain MoSCoW usage where staged authoring or closure guidance depends on it. |
| backlog | modify | `docs/backlog/README.md` | Mark B057 complete at closure. |
| prompts/templates | modify | `skills/spec-lifecycle-manager/prompts/`, bundled plugin copies | Keep wizard guidance consistent. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** priority vocabulary, compatibility expectations,
  and affected surfaces are accepted.
- **Design-first exception:** no
- **Optional artifacts recommended:** none
- **Downstream review needed:** design, tasks, traceability, verification

## Requirements

### Requirement 1: Priority Vocabulary

**User Story:** As a maintainer, I want a simple MoSCoW priority vocabulary for
requirements, so that agents can tell mandatory gates from optional
enhancements.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a requirement is mandatory, WHEN it is authored, THEN THE SYSTEM SHALL
   support marking it with the canonical persisted label `must-have`.
2. GIVEN a requirement is expected but negotiable, WHEN it is authored, THEN THE
   SYSTEM SHALL support marking it with the canonical persisted label
   `should-have`.
3. GIVEN a requirement is optional enhancement scope, WHEN it is authored, THEN
   THE SYSTEM SHALL support marking it with the canonical persisted label
   `could-have`.
4. GIVEN a requirement is explicitly excluded, WHEN it is authored, THEN THE
   SYSTEM SHALL keep that exclusion in non-goals or out-of-scope text rather
   than treating `won't-have` as accepted implementation scope.
5. GIVEN user-facing guidance mentions shorthand values, WHEN the guidance is
   persisted in templates, traceability, runtime output, or tests, THEN THE
   SYSTEM SHALL normalize to `must-have`, `should-have`, `could-have`, or an
   explicit non-goal/out-of-scope disposition.
6. GIVEN a requirement has acceptance criteria, WHEN priority is recorded, THEN
   THE SYSTEM SHALL use requirement-level priority as the canonical scope signal
   without requiring duplicate priority labels on every acceptance criterion.

### Requirement 2: Backward Compatibility

**User Story:** As a lifecycle maintainer, I want existing specs without
priority labels to remain valid, so that the new model does not create noisy
retroactive work.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN an existing active spec lacks MoSCoW priority labels, WHEN lint or
   readiness checks run, THEN THE SYSTEM SHALL NOT fail solely because labels
   are absent.
2. GIVEN a new template includes priority guidance, WHEN a new spec is created,
   THEN THE SYSTEM SHALL show how to label requirements without requiring every
   acceptance criterion to carry duplicate metadata.
3. GIVEN a closed or removed spec lacks priority labels, WHEN archive or
   history checks run, THEN THE SYSTEM SHALL NOT ask agents to edit historical
   packages.

### Requirement 3: Lifecycle Semantics

**User Story:** As a coding agent, I want priority labels to affect planning and
closure guidance consistently, so that I do not treat optional work as blocking
or mandatory work as deferrable by accident.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a `must-have` requirement is accepted, WHEN design, task planning, or
   closure reconciliation runs, THEN THE SYSTEM SHALL treat missing coverage as
   blocking unless it is explicitly rejected or superseded by a human decision.
2. GIVEN a `should-have` requirement is not implemented, WHEN closure
   reconciliation runs, THEN THE SYSTEM SHALL require an explicit route,
   rationale, or accepted residual risk.
3. GIVEN a `could-have` requirement is not implemented, WHEN closure reconciliation
   runs, THEN THE SYSTEM SHALL allow closure when the item is explicitly routed,
   rejected, or marked out of current scope.
4. GIVEN MoSCoW priority labels are present, WHEN `stage_readiness`,
   `closure_check`, closure reconciliation, traceability lookup, or agent
   readiness output reports requirement coverage, THEN THE SYSTEM SHALL preserve
   the requirement priority in structured output or diagnostic context where
   that requirement is reported.
5. GIVEN closure reconciliation evaluates broad requirements, WHEN an accepted
   `must-have` requirement is missing coverage, THEN THE SYSTEM SHALL report the
   item as blocking rather than as a routable optional residual.

### Requirement 4: Tooling And Prompt Support

**User Story:** As a skill user, I want prompts and tooling to surface priority
without adding ceremony, so that requirement authoring remains ergonomic.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN the documentation wizard asks for requirements, WHEN priority is
   relevant, THEN THE SYSTEM SHALL ask for or infer priority only at the
   requirement level unless more detail is needed.
2. GIVEN runtime output reports requirement coverage, WHEN priority labels are
   present, THEN THE SYSTEM SHALL include priority in the relevant structured
   output or diagnostic context.
3. GIVEN package-contract or sync validation runs, WHEN template or prompt
   wording changes, THEN THE SYSTEM SHALL keep source and bundled plugin copies
   aligned.
4. GIVEN MoSCoW priority behavior is implemented, WHEN tests run, THEN THE
   SYSTEM SHALL include fixtures or unit tests for unlabeled legacy specs,
   labeled `must-have`/`should-have`/`could-have` specs, closed or removed specs
   without labels, and MCP/runtime structured output that includes priority when
   labels are present.

## Correctness Properties

- CP-001: Absence of MoSCoW priority labels in legacy specs does not create
  a blocking diagnostic by itself.
- CP-002: Accepted `must-have` requirements cannot be silently routed as
  optional closure leftovers.
- CP-003: `could-have` requirements do not block closure when explicitly
  routed or excluded from current scope.
- CP-004: Priority metadata remains visible to design, task, traceability,
  and closure workflows when present.
- CP-005: Requirement-level MoSCoW priority is canonical; acceptance
  criteria inherit their parent requirement priority unless a future design
  explicitly introduces a narrower override model.

## Technical Context

- **Language/Version:** Python 3 standard library runtime; Markdown templates;
  JSON prompts.
- **Primary Dependencies:** repo-local lifecycle runtime, MCP server, prompt
  validation.
- **Target Platform:** Source skill and bundled Codex/Claude plugins.
- **Constraints:** Keep labels simple and explainable; avoid breaking existing
  packages.
- **Priority Method:** MoSCoW, using canonical persisted labels `must-have`,
  `should-have`, and `could-have`; explicit exclusions belong in non-goals,
  out-of-scope text, rejected decisions, or routed residuals rather than
  accepted requirements.
- **Performance Goals:** No meaningful runtime scan or lint regression.

## Resolved Design Inputs

| Question | Decision | Rationale |
|----------|----------|-----------|
| Where should the canonical `must-have`/`should-have`/`could-have` value live? | Use a requirement body metadata line: `**Priority:** must-have`. | Keeps headings stable, keeps parsing simple, and keeps priority visible next to the user story and acceptance criteria. |
| Should missing labels in new specs be info-level guidance or no diagnostic at all? | Missing labels remain non-blocking. Templates and prompts should guide authors; lint/readiness may surface advisory context only when labels are already present or when a future mode explicitly asks for priority audit. | Preserves compatibility and avoids warning noise. |
| Should `won't-have` ever appear as a persisted priority value? | Do not persist `won't-have` as an accepted requirement priority in this spec. Excluded work belongs in non-goals, out-of-scope text, rejected decisions, or routed residuals. | Avoids treating excluded work as accepted implementation scope. |

## Success Criteria

- **SC-001:** New requirements templates show the accepted priority convention.
- **SC-002:** Runtime and prompts preserve compatibility for unlabeled specs.
- **SC-003:** Closure guidance can distinguish mandatory and optional residual
  requirement coverage when labels exist.
- **SC-004:** Tests demonstrate MoSCoW behavior for legacy unlabeled specs,
  labeled active specs, historical specs without labels, and MCP/runtime output.

## Related Artifacts

- Backlog: `docs/backlog/README.md` B057
- Design: `design.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
