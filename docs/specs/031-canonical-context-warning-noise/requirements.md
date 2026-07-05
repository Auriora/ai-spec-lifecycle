---
title: Canonical context warning noise requirements
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
backlog_item: B058
priority: P1
---

# Requirements

## Introduction

`CANONICAL_CONTEXT_MISSING` and related canonical-context risk signals are
intended to help agents notice real stale-doc, imported-source, or
authority-conflict risks. Recent dogfooding showed that agents can treat these
advisory signals as instructions to retroactively create `canonical-context.md`
or reopen historical packages, even when the package is small or the matched
wording only describes ordinary durable promotion or closure work.

This spec clarifies the diagnostic wording, readiness guidance, and heuristic
signals so agents understand when canonical context is useful and when no
artifact should be added.

## Goals

- Keep canonical-context diagnostics advisory unless a future spec deliberately
  promotes a gate with false-positive handling.
- Prevent agents from adding `canonical-context.md` by default for small specs,
  ordinary promotion wording, or historical/closed package references.
- Tighten `imported-source-risk` and related detection so ordinary closure or
  durable-promotion language does not look like imported-source authority.
- Update runtime, prompt, template, and durable documentation wording so agents
  route the signal correctly.

## Non-Goals

- Do not remove canonical-context support.
- Do not make canonical-context diagnostics blocking.
- Do not recreate, edit, or modernize closed spec packages.
- Do not change the active spec package model beyond diagnostic and guidance
  clarity.

## Glossary

| Term | Definition |
|------|------------|
| canonical context | Spec-local map of authoritative sources, imported sources, stale-doc risks, and promotion routes. |
| advisory diagnostic | A finding that should inform agent judgment but does not block progress by itself. |
| imported-source risk | Signal that a spec depends on external or durable source text that may need explicit authority and promotion handling. |
| ordinary promotion wording | Text that discusses durable-doc promotion without importing source authority or creating stale-doc risk. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/backlog/README.md` B058 | Captures the canonical-context warning noise candidate and desired outcome. | high | Source backlog item for this spec. |
| `skills/spec-lifecycle-manager/SKILL.md` | Defines when `canonical-context.md` is optional and when wizard mode should create it. | high | Likely durable promotion target. |
| `skills/spec-lifecycle-manager/references/spec-package/requirements.md` | Describes durable-source baseline and canonical-context intent in fallback requirements template. | high | Template wording may need clarification. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Contains lint, readiness, and risk-signal logic for canonical context diagnostics. | high | Implementation target if heuristic changes are accepted. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime diagnostics and lifecycle helper behavior. | high | Durable reference target. |

## Canonical Context

| Source | Canonical role | Promotion route | Notes |
|--------|----------------|-----------------|-------|
| `docs/backlog/README.md` B058 | Spec-canonical intake source | Mark B058 done at closure. | Backlog text is authoritative for this spec's problem statement. |
| `skills/spec-lifecycle-manager/SKILL.md` | Current agent guidance | Update if accepted behavior changes. | Do not treat older closed specs as active guidance. |
| `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | Runtime behavior source | Update tests and runtime reference with accepted heuristic changes. | Code-derived behavior overrides stale prose. |
| `docs/history/spec-archive-index.md` | Historical lookup only | No active spec edits. | Removed package paths are evidence pointers, not edit targets. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| requirements | clarify | `docs/backlog/README.md` | Mark B058 complete at closure. |
| design | clarify | `docs/design/spec-lifecycle-management.md` | Clarify canonical context as optional, risk-triggered context. |
| reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document advisory signal behavior and expected agent response. |
| skill guidance | modify | `skills/spec-lifecycle-manager/SKILL.md` | Tighten instructions for when to add `canonical-context.md`. |
| templates/prompts | modify | `skills/spec-lifecycle-manager/references/spec-package/`, `skills/spec-lifecycle-manager/prompts/` | Clarify wording where diagnostics or wizard guidance are surfaced. |
| runtime surfaces | modify | `lint_spec_package`, `agent_readiness_packet`, `closure_check` | Review and align all surfaces that can return canonical-context diagnostics or readiness guidance. |
| bundled plugin copies | modify | `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/` | Keep distributed skill, prompts, templates, and runtime copies aligned with source. |

## Staged Readiness

- **Current stage:** tasks
- **Next stage:** agent_ready
- **Ready to design when:** diagnostic classes, affected runtime surfaces, and
  expected non-blocking behavior are accepted. Complete.
- **Design-first exception:** no
- **Optional artifacts recommended:** `traceability.md` with `tasks.md`
- **Downstream review needed:** implementation readiness and verification

## Requirements

### Requirement 1: Advisory Diagnostic Wording

**User Story:** As a coding agent, I want canonical-context diagnostics to
state that they are advisory, so that I do not create unnecessary artifacts or
treat them as closure blockers.

#### Acceptance Criteria

1. GIVEN `CANONICAL_CONTEXT_MISSING` is emitted, WHEN the agent reads the
   diagnostic, THEN THE SYSTEM SHALL state that the finding is advisory unless a
   separate repository policy makes it blocking.
2. GIVEN a diagnostic is advisory, WHEN guidance is returned, THEN THE SYSTEM
   SHALL recommend inspecting the context risk before creating
   `canonical-context.md`.
3. GIVEN a closed, archived, removed, or historical spec package is referenced,
   WHEN canonical-context guidance is returned, THEN THE SYSTEM SHALL NOT tell
   the agent to add artifacts to that historical package.

### Requirement 2: Canonical Context Creation Conditions

**User Story:** As a spec author, I want clear conditions for creating
`canonical-context.md`, so that optional artifacts are added only when they
carry useful authority information.

#### Acceptance Criteria

1. GIVEN a spec has real stale durable docs, imported sources, confusing
   history, multiple authorities, or broad durable-doc impact, WHEN the wizard
   or runtime recommends canonical context, THEN THE SYSTEM SHALL explain the
   concrete trigger.
2. GIVEN a spec is small and embeds durable-source baseline information in
   `requirements.md`, WHEN no concrete authority conflict exists, THEN THE
   SYSTEM SHALL allow the spec to proceed without a separate
   `canonical-context.md`.
3. GIVEN canonical context is not required, WHEN the agent asks what to do next,
   THEN THE SYSTEM SHALL route work to the current lifecycle stage rather than
   artifact backfill.

### Requirement 3: Risk Signal Precision

**User Story:** As a maintainer, I want canonical-context risk signals to avoid
false positives from closure and promotion wording, so that diagnostics stay
useful.

#### Acceptance Criteria

1. GIVEN text only mentions durable promotion, closure records, archive indexes,
   or promotion targets, WHEN risk signals are computed, THEN THE SYSTEM SHALL
   NOT classify that text as imported-source authority by itself.
2. GIVEN text identifies imported source material, stale durable-doc authority,
   or conflicting source-of-truth claims, WHEN risk signals are computed, THEN
   THE SYSTEM SHALL identify the relevant risk class.
3. GIVEN a heuristic match is uncertain, WHEN diagnostics are returned, THEN THE
   SYSTEM SHALL present the uncertainty as review guidance rather than a hard
   requirement.

### Requirement 4: Prompt And Template Alignment

**User Story:** As a skill maintainer, I want prompts and templates to match the
runtime diagnostic semantics, so that different agents respond consistently.

#### Acceptance Criteria

1. GIVEN prompt guidance discusses canonical context, WHEN the prompt is
   validated, THEN THE SYSTEM SHALL preserve advisory wording and stage order.
2. GIVEN fallback templates mention canonical context, WHEN a new spec is
   created, THEN THE SYSTEM SHALL distinguish embedded durable-source baseline
   from separate canonical-context artifacts.
3. GIVEN source and bundled plugin copies are validated, WHEN package-contract
   or sync checks run, THEN THE SYSTEM SHALL show updated guidance in source
   and bundled copies.

### Requirement 5: Runtime Surface Alignment

**User Story:** As a coding agent, I want every lifecycle surface that reports
canonical-context guidance to use the same advisory semantics, so that tool
choice does not change whether I create artifacts or block progress.

#### Acceptance Criteria

1. GIVEN `lint_spec_package` reports canonical-context diagnostics, WHEN the
   output is inspected, THEN THE SYSTEM SHALL preserve advisory wording and the
   concrete risk trigger.
2. GIVEN `agent_readiness_packet` includes canonical-context guidance, WHEN the
   output is inspected, THEN THE SYSTEM SHALL distinguish readiness guidance
   from mandatory artifact creation.
3. GIVEN `closure_check` encounters canonical-context-related evidence or
   missing artifacts, WHEN the output is inspected, THEN THE SYSTEM SHALL NOT
   block closure solely because `canonical-context.md` is absent unless a
   separate accepted rule makes it blocking.
4. GIVEN direct CLI and MCP outputs expose the same surface, WHEN they are
   compared, THEN THE SYSTEM SHALL return equivalent diagnostic semantics from
   shared lifecycle internals.

## Correctness Properties

- **CP-001:** Advisory canonical-context diagnostics never require artifact
  creation by themselves.
- **CP-002:** Historical package references are not treated as active artifact
  edit targets.
- **CP-003:** Ordinary durable-promotion or closure wording does not trigger
  imported-source risk by itself.
- **CP-004:** Real stale-doc, imported-source, or authority-conflict evidence
  remains detectable after false-positive reduction.
- **CP-005:** `lint_spec_package`, `agent_readiness_packet`, and
  `closure_check` do not disagree about whether canonical-context findings are
  advisory or blocking.

## Technical Context

- **Language/Version:** Python 3 standard library runtime; JSON prompt
  definitions; Markdown docs/templates.
- **Primary Dependencies:** `unittest`, repo-local lifecycle runtime and MCP
  server.
- **Target Platform:** Codex and Claude plugin users through source and bundled
  plugin copies.
- **Constraints:** Keep diagnostics advisory and waiver-friendly; avoid
  dogfood-breaking behavior changes.
- **Performance Goals:** No material scan or lint performance regression.

## Resolved Design Questions

| Question | Resolution | Design destination |
|----------|------------|--------------------|
| Which concrete wording changes belong in prompts/templates/docs, and which heuristic changes belong in runtime signal detection? | Runtime signal detection handles concrete risk classification and false-positive reduction. Prompts, templates, skill guidance, and durable docs handle wording and agent-response expectations. | `design.md#overview`, `design.md#components-and-changes` |
| Should prompt changes include `documentation-wizard` only or all lifecycle prompts that mention canonical context? | All prompt surfaces that mention canonical context are in scope. | `design.md#overview`, `design.md#components-and-changes` |
| Should `agent_readiness_packet` and `closure_check` directly compute canonical-context guidance or consume normalized diagnostics from shared internals? | They should consume normalized shared runtime diagnostics and closure blockers rather than computing separate meanings. | `design.md#system-architecture`, `design.md#data-flow` |

## Success Criteria

- **SC-001:** Agents receive clear advisory wording for canonical-context
  diagnostics.
- **SC-002:** Regression tests cover ordinary promotion wording and real
  imported-source risk.
- **SC-003:** Prompt, template, runtime reference, and bundled plugin copies
  remain in sync after the change.
- **SC-004:** `lint_spec_package`, `agent_readiness_packet`, and
  `closure_check` expose consistent advisory semantics for canonical-context
  findings.

## Related Artifacts

- Backlog: `docs/backlog/README.md` B058
- Design: `docs/specs/031-canonical-context-warning-noise/design.md`
- Tasks: `docs/specs/031-canonical-context-warning-noise/tasks.md`
- Verification: not created yet
