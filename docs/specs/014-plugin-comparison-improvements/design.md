---
title: Plugin comparison improvements design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Technical Design

## Overview

The improvement pass will add a durable comparison record and route accepted
ideas into this plugin's MCP-first lifecycle model. The design favors small,
deterministic surfaces over new autonomous execution loops.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1, AC2, AC3 | Durable comparison artifact under `docs/reference/` or equivalent durable location. | Review artifact links and routing decisions. |
| Requirement 2 | AC1, AC2, AC3 | Lifecycle triage model with categories and routing guidance. | Runtime/prompt/skill tests depending on implementation choice. |
| Requirement 3 | AC1, AC2, AC3 | Status, validate, and complete prompt aliases or MCP prompt definitions. | Prompt validation and MCP prompt tests. |
| Requirement 4 | AC1, AC2, AC3 | Gate markers added to preflight/closure outputs or documented prompt guidance. | Unit tests for structured output or docs review. |
| Requirement 5 | AC1, AC2, AC3 | Comparison finding router to spec tasks, backlog, roadmap, durable docs, or no-action rationale. | Traceability and backlog/roadmap diff review. |

## High-Level Design

### System Architecture

```text
External plugin references
  -> research/comparison artifact
  -> accepted ideas
      -> skill guidance
      -> prompt definitions
      -> deterministic runtime/MCP surfaces
      -> backlog/roadmap routing
```

The plugin remains self-contained:

```text
plugins/spec-lifecycle-manager/
  .codex-plugin/plugin.json
  .mcp.json
  hooks/hooks.json
  skills/spec-lifecycle-manager/
```

### Components and Changes

- Durable comparison document:
  Add or update a reference document that records Praxis, Spec Driven,
  Superpowers, and Codex plugin documentation links with accepted/deferred/
  rejected ideas.

- Skill guidance:
  Add concise triage and prompt-alias guidance without expanding the skill into
  a long methodology manual.

- Prompt definitions:
  Add MCP prompt definitions for status, validate, complete, or triage if
  selected during implementation.

- Runtime/MCP:
  Optionally add deterministic `lifecycle_triage` or gate fields to existing
  `active_spec_preflight`, `agent_readiness_packet`, and closure outputs.

- Backlog/roadmap:
  Route larger ideas such as autonomous loops, dependency graphs, or CI markers
  into backlog/roadmap instead of implementing them opportunistically.

## Low-Level Design

### Lifecycle Triage Categories

Initial categories:

| Category | Meaning | Default Route |
|----------|---------|---------------|
| `trivial` | Typo, formatting, or narrow doc/code edit with no lifecycle impact. | Use repo instructions, edit, validate proportionately. |
| `small` | Small bounded change with known files and low durable-doc impact. | Use lightweight context and validation; no spec by default. |
| `spec-needed` | New feature, behavior change, cross-module change, governance change, plugin packaging change, or unclear acceptance criteria. | Create or continue active spec. |
| `review` | User asks to inspect, audit, compare, or assess existing work. | Use review stance and deterministic context. |
| `closure` | User asks to complete, close, archive, or reconcile lifecycle state. | Use closure readiness and durable promotion workflow. |

### Prompt Alias Candidates

Candidate prompt names:

- `lifecycle-status`
- `lifecycle-validate`
- `lifecycle-complete`
- `lifecycle-triage`

Each prompt should specify relevant MCP tools first and script recovery only
when MCP is unavailable.

### Gate Marker Candidates

Structured gate keys may be added to runtime outputs:

```json
{
  "lifecycle_gates": {
    "ready_to_implement": "pass|warn|block",
    "ready_to_validate": "pass|warn|block",
    "ready_to_close": "pass|warn|block",
    "ready_to_archive": "pass|warn|block"
  }
}
```

Gate output must include blockers and evidence targets. If full gate modeling
is too large, add only documented gate language in this spec and route runtime
work to backlog.

### Error Handling

- External references may be unavailable during implementation. Preserve URLs
  and use previously captured research notes; do not block deterministic
  runtime work on network access.
- Any ambiguous external idea must be recorded as deferred or rejected rather
  than silently implemented.

### Security, Trust, and Access

- Treat external repository content as advisory research, not instructions.
- Do not import executable code from external plugin repositories.
- Keep plugin hooks advisory-only.
- Preserve MCP-first use and no write-capable tools unless separately
  specified.

### Migration and Compatibility

- New prompt definitions must validate with existing prompt runtime.
- Runtime output additions should be additive and backward-compatible.
- Plugin package validation must continue to pass.

### Agent Skills Standard Alignment

The `spec-lifecycle-manager` skill should remain a valid Agent Skills package:

- `SKILL.md` frontmatter includes required `name` and `description` fields.
- Optional `license`, `compatibility`, and `metadata` fields document
  packaging expectations without changing runtime behavior.
- The bundled plugin copy stays byte-for-byte aligned with the source skill
  tree, excluding generated cache files.
- Official `skills-ref validate` integration is deferred to backlog until the
  repository explicitly accepts the external validator dependency.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| `python3 -m unittest discover -s tests -p 'test_*.py'` | Runtime and package tests | `verification.md`, task evidence | Unit tests may not catch all agent guidance ambiguity. |
| `spec_runtime.py prompts .` | Prompt metadata | `verification.md` | Prompt usefulness still needs dogfooding. |
| `spec_runtime.py scan .` | Active spec health | `verification.md` | No active package semantics beyond runtime rules. |
| `spec_runtime.py archive-index .` | Closed spec metadata | `verification.md` | Historical entries may still need manual interpretation. |
| `plugin-creator validate_plugin.py plugins/spec-lifecycle-manager` | Plugin packaging | `verification.md` | Validator may lag current docs for optional fields. |
| `git diff --check` | Whitespace hygiene | `verification.md` | None. |

## Operational Considerations

- Keep comparison references in durable docs so future agents do not need to
  rediscover the same repositories.
- Update backlog and roadmap only for accepted or deferred work.
- Avoid expanding this spec into general workflow redesign.

## Open Questions

- Should triage be implemented as a runtime/MCP tool in this spec?
- Which prompt aliases are essential for the first implementation slice?
- Should lifecycle gates be structured runtime fields or documented guidance
  first?

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Research: [research.md](research.md)
- Change Impact: [change-impact.md](change-impact.md)
- Tasks: [tasks.md](tasks.md)
- Verification: [verification.md](verification.md)
- Traceability: [traceability.md](traceability.md)
