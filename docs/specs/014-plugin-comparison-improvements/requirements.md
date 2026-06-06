---
title: Plugin comparison improvements requirements
doc_type: spec
artifact_type: requirements
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Requirements

## Introduction

This spec defines a focused improvement pass for the Spec Lifecycle Manager
plugin based on comparison with adjacent AI-agent workflow plugins. The work
must preserve links to external reference plugins for deeper analysis while
turning the comparison into concrete, scoped enhancements for this repository.

## Goals

- Preserve durable references to relevant external plugin examples.
- Identify comparison-backed improvements that fit this repository's lifecycle
  model.
- Convert the highest-value ideas into bounded implementation tasks.
- Avoid importing another plugin's full workflow or changing this repository's
  durable docs structure without explicit decision.

## Non-Goals

- Do not clone or vendor external plugin code.
- Do not replace the `docs/specs/` lifecycle model with `.claude/specs/`,
  Praxis staging docs, or Superpowers' full methodology.
- Do not implement autonomous long-running spec loops in this spec.
- Do not add write-capable MCP tools without a separate explicit spec.

## Glossary

| Term | Definition |
|------|------------|
| Comparative reference | External plugin repository used as an analysis input, not as authoritative requirements. |
| Lifecycle triage | A lightweight decision step that classifies work before loading heavier spec workflows. |
| Gate marker | A compact, explicit lifecycle readiness condition such as ready to implement, ready to close, or ready to archive. |
| Prompt alias | A Codex-facing prompt or skill entry phrase that maps user intent to an existing MCP/runtime workflow. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `plugins/spec-lifecycle-manager/.codex-plugin/plugin.json` | Plugin manifest now bundles skills and MCP server metadata. | high | Current plugin surface to improve. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md` | Skill defines lifecycle workflow and MCP-first guidance. | high | Primary agent guidance surface. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Runtime provides deterministic scan, preflight, readiness, review packet, and closure surfaces. | high | Implementation source for MCP tools. |
| `docs/backlog/README.md` | Tracks deferred lifecycle work and priorities. | high | Candidate improvements may update backlog. |
| `docs/roadmap/README.md` | Tracks sequencing for lifecycle hardening. | high | May need new horizon after comparison. |
| `docs/reference/spec-lifecycle-runtime.md` | Durable reference for runtime and MCP behavior. | high | Promotion target for accepted runtime changes. |

## Comparative References

| Reference | URL | Analysis Use |
|-----------|-----|--------------|
| Praxis | `https://github.com/ouonet/praxis` | Lightweight scope triage, compact skills, staging-to-living-docs discipline, cross-harness packaging ideas. |
| Spec Driven | `https://github.com/Habib0x0/spec-driven-plugin` | Command/prompt surface, EARS workflow, cross-spec dependency handling, validation/status/loop concepts. |
| Superpowers | `https://github.com/obra/superpowers` | Gated workflow discipline, TDD/review/finish gates, skill trigger conventions, verification-before-completion behavior. |
| Codex plugin build docs | `https://developers.openai.com/codex/plugins/build` | Canonical Codex plugin packaging and bundled component rules. |
| Codex plugin overview docs | `https://developers.openai.com/codex/plugins` | Installation, use, permissions, and plugin behavior model. |

## Requirements

### Requirement 1: Durable Comparative Analysis

**User Story:** As a maintainer, I want a durable comparison of relevant
workflow plugins, so that future improvements can cite concrete external
patterns without relying on conversation memory.

#### Acceptance Criteria

1. GIVEN this spec is implemented, WHEN a maintainer reviews the comparison,
   THEN THE SYSTEM SHALL preserve links to Praxis, Spec Driven, Superpowers,
   and Codex plugin documentation.
2. GIVEN an external pattern is recommended, WHEN it is recorded, THEN THE
   SYSTEM SHALL describe why it fits or does not fit this repository's
   lifecycle model.
3. GIVEN an external pattern is not adopted, WHEN it is recorded, THEN THE
   SYSTEM SHALL include a concise rejection or deferral rationale.

### Requirement 2: Lifecycle Triage Candidate

**User Story:** As a coding agent, I want lightweight lifecycle triage before
heavy spec workflow, so that trivial or small changes are not over-processed.

#### Acceptance Criteria

1. GIVEN a user asks for lifecycle work, WHEN triage guidance or tooling is
   available, THEN THE SYSTEM SHALL classify the request into at least
   `trivial`, `small`, `spec-needed`, `review`, or `closure`.
2. GIVEN a request is classified as `trivial` or `small`, THEN THE SYSTEM SHALL
   route to proportionate guidance and avoid creating a spec by default.
3. GIVEN a request is classified as `spec-needed`, THEN THE SYSTEM SHALL route
   to the existing spec package workflow.

### Requirement 3: Clear Status and Validation Entry Points

**User Story:** As a maintainer, I want obvious status and validation entry
points, so that agents do not need to infer tool names from implementation
details.

#### Acceptance Criteria

1. GIVEN the plugin is installed, WHEN a user asks "what next" or "status",
   THEN THE SYSTEM SHALL have a clear prompt alias, MCP prompt, or skill
   guidance route to `active_spec_preflight` or `no_active_spec_context`.
2. GIVEN a user asks to validate lifecycle state, THEN THE SYSTEM SHALL route
   to deterministic validation surfaces such as scan, archive index, prompt
   validation, package lint, or closure check.
3. GIVEN a user asks to complete lifecycle work, THEN THE SYSTEM SHALL route to
   closure readiness and durable-promotion guidance before cleanup.

### Requirement 4: Explicit Lifecycle Gates

**User Story:** As a maintainer, I want explicit lifecycle gate markers, so
that agents know when implementation, closure, and archival are actually ready.

#### Acceptance Criteria

1. GIVEN an active spec exists, WHEN readiness is requested, THEN THE SYSTEM
   SHALL expose whether the package is ready to implement, ready to validate,
   ready to close, or blocked.
2. GIVEN a gate is not ready, THEN THE SYSTEM SHALL include concrete blockers
   and evidence targets.
3. GIVEN a gate is ready, THEN THE SYSTEM SHALL include the validation evidence
   expected before proceeding.

### Requirement 5: Bounded Improvement Routing

**User Story:** As a maintainer, I want comparison findings routed to backlog,
roadmap, spec tasks, or no-action decisions, so that external inspiration does
not become unbounded scope.

#### Acceptance Criteria

1. GIVEN a comparison finding is accepted, THEN THE SYSTEM SHALL route it to
   this spec's tasks, backlog, roadmap, or durable docs.
2. GIVEN a finding is deferred, THEN THE SYSTEM SHALL preserve it as a backlog
   or roadmap candidate with a reason.
3. GIVEN a finding is rejected, THEN THE SYSTEM SHALL record the rationale in
   the comparison artifact or open decisions.

## Correctness Properties

- **CP-001**: Every adopted idea must trace to at least one requirement and one
  validation method.
- **CP-002**: Every external reference must remain advisory and must not
  override repository governance, user instructions, or Codex plugin docs.
- **CP-003**: Any new agent-facing workflow must preserve MCP-first behavior
  when MCP tools are visible.
- **CP-004**: No implementation task may require network access at runtime.

## Technical Context

- **Language/Version:** Python 3.9+ standard library for runtime changes.
- **Primary Dependencies:** Codex plugin manifest, bundled skill, MCP server,
  prompt definitions, Markdown docs.
- **Target Platform:** Codex CLI/app plugin installation.
- **Constraints:** Keep plugin self-contained; avoid third-party runtime
  dependencies; keep hooks advisory-only.
- **Performance Goals:** Any new deterministic runtime command or MCP tool
  should return promptly on this repository without network access.

## Success Criteria

- **SC-001**: A durable comparison artifact exists with references to Praxis,
  Spec Driven, Superpowers, and Codex plugin docs.
- **SC-002**: At least one accepted improvement is represented as either a
  runtime/prompt/skill change or a concrete backlog/roadmap item.
- **SC-003**: Validation commands pass: plugin validation, unit tests,
  lifecycle scan, archive index, prompt validation, and whitespace check.
- **SC-004**: No new plugin packaging drift is introduced.

## Related Artifacts

- Change Impact: [change-impact.md](change-impact.md)
- Research: [research.md](research.md)
- Design: [design.md](design.md)
- Tasks: [tasks.md](tasks.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
- Open Decisions: [open-decisions.md](open-decisions.md)
