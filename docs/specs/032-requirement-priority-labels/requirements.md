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
closure gates from useful-but-negotiable enhancements. This spec introduces a
standard requirement priority notation so agents can reason about must, should,
could, and explicit out-of-scope behavior without weakening correctness or
closure discipline.

## Goals

- Add a clear, low-noise priority model for requirements.
- Let agents distinguish mandatory implementation/closure requirements from
  lower-priority enhancements during design, task planning, validation, and
  scope negotiation.
- Preserve compatibility with existing specs that lack priority labels.
- Define where priority belongs in requirements text, templates, traceability,
  and lint/runtime output.

## Non-Goals

- Do not let priority labels bypass accepted acceptance criteria.
- Do not retrofit every closed spec.
- Do not require complex prioritization frameworks beyond the needs of this
  lifecycle skill.
- Do not change task status semantics in this spec unless design proves it is
  necessary.

## Glossary

| Term | Definition |
|------|------------|
| must | Requirement priority that blocks implementation or closure when accepted and unfulfilled. |
| should | Requirement priority that is expected but may be routed with explicit rationale. |
| could | Requirement priority that is optional enhancement scope and should not block closure when routed or rejected. |
| priority label | A stable notation attached to a requirement or acceptance criterion that communicates scope importance. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/backlog/README.md` B057 | Captures need for must/should/could requirement priority labels. | high | Source backlog item for this spec. |
| `skills/spec-lifecycle-manager/references/spec-package/requirements.md` | Current fallback requirements template has no priority metadata. | high | Likely template target. |
| `skills/spec-lifecycle-manager/references/spec-package/traceability.md` | Traceability can carry coverage state but not requirement priority. | medium | Possible target after design decision. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Runtime lint/readiness logic may need to parse or report priority. | high | Implementation target if labels affect diagnostics. |
| `docs/design/spec-lifecycle-management.md` | Durable lifecycle design describes requirements and closure reconciliation. | high | Durable promotion target. |

## Canonical Context

| Source | Canonical role | Promotion route | Notes |
|--------|----------------|-----------------|-------|
| `docs/backlog/README.md` B057 | Spec-canonical intake source | Mark B057 done at closure. | Backlog text is authoritative for accepted scope. |
| `skills/spec-lifecycle-manager/references/spec-package/requirements.md` | Current template source | Update if labels are adopted. | Template behavior should stay backward compatible. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Runtime behavior source | Update runtime docs and tests if parsing or lint behavior changes. | Code-derived behavior overrides stale prose. |
| `docs/history/spec-archive-index.md` | Historical lookup only | No active spec edits. | Closed specs may provide evidence but are not active targets. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| requirements | modify | `skills/spec-lifecycle-manager/references/spec-package/requirements.md` | Add priority notation guidance. |
| design | clarify | `docs/design/spec-lifecycle-management.md` | Explain priority role in lifecycle stages. |
| reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document any runtime/lint behavior. |
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

**User Story:** As a maintainer, I want a simple priority vocabulary for
requirements, so that agents can tell mandatory gates from optional
enhancements.

#### Acceptance Criteria

1. GIVEN a requirement is mandatory, WHEN it is authored, THEN THE SYSTEM SHALL
   support marking it as `must` or equivalent.
2. GIVEN a requirement is expected but negotiable, WHEN it is authored, THEN THE
   SYSTEM SHALL support marking it as `should` or equivalent.
3. GIVEN a requirement is optional enhancement scope, WHEN it is authored, THEN
   THE SYSTEM SHALL support marking it as `could` or equivalent.
4. GIVEN a requirement is explicitly excluded, WHEN it is authored, THEN THE
   SYSTEM SHALL keep that exclusion in non-goals or out-of-scope text rather
   than overloading priority labels.

### Requirement 2: Backward Compatibility

**User Story:** As a lifecycle maintainer, I want existing specs without
priority labels to remain valid, so that the new model does not create noisy
retroactive work.

#### Acceptance Criteria

1. GIVEN an existing active spec lacks priority labels, WHEN lint or readiness
   checks run, THEN THE SYSTEM SHALL NOT fail solely because labels are absent.
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

#### Acceptance Criteria

1. GIVEN a `must` requirement is accepted, WHEN design, task planning, or
   closure reconciliation runs, THEN THE SYSTEM SHALL treat missing coverage as
   blocking unless it is explicitly rejected or superseded by a human decision.
2. GIVEN a `should` requirement is not implemented, WHEN closure reconciliation
   runs, THEN THE SYSTEM SHALL require an explicit route, rationale, or accepted
   residual risk.
3. GIVEN a `could` requirement is not implemented, WHEN closure reconciliation
   runs, THEN THE SYSTEM SHALL allow closure when the item is explicitly routed,
   rejected, or marked out of current scope.

### Requirement 4: Tooling And Prompt Support

**User Story:** As a skill user, I want prompts and tooling to surface priority
without adding ceremony, so that requirement authoring remains ergonomic.

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

## Correctness Properties

- **CP-001:** Absence of priority labels in legacy specs does not create a
  blocking diagnostic by itself.
- **CP-002:** Accepted `must` requirements cannot be silently routed as
  optional closure leftovers.
- **CP-003:** `could` requirements do not block closure when explicitly routed
  or excluded from current scope.
- **CP-004:** Priority metadata remains visible to design, task, traceability,
  and closure workflows when present.

## Technical Context

- **Language/Version:** Python 3 standard library runtime; Markdown templates;
  JSON prompts.
- **Primary Dependencies:** repo-local lifecycle runtime, MCP server, prompt
  validation.
- **Target Platform:** Source skill and bundled Codex/Claude plugins.
- **Constraints:** Keep labels simple and explainable; avoid breaking existing
  packages.
- **Performance Goals:** No meaningful runtime scan or lint regression.

## Open Questions

| Question | Why it matters | Blocks design? |
|----------|----------------|----------------|
| Should labels live in headings, a table, frontmatter-like metadata, or requirement body text? | Determines parser and template shape. | yes |
| Should priority apply only to requirements or also to individual acceptance criteria? | Affects complexity and traceability. | yes |
| Should missing labels in new specs be info-level guidance or no diagnostic at all? | Affects noise level. | yes |

## Success Criteria

- **SC-001:** New requirements templates show the accepted priority convention.
- **SC-002:** Runtime and prompts preserve compatibility for unlabeled specs.
- **SC-003:** Closure guidance can distinguish mandatory and optional residual
  requirement coverage when labels exist.

## Related Artifacts

- Backlog: `docs/backlog/README.md` B057
- Design: not created yet
- Tasks: not created yet
- Verification: not created yet
