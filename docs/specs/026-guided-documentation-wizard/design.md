---
title: Guided documentation wizard design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-17
---

# Technical Design

## Overview

Add a guided documentation wizard as a prompt-based workflow over existing
spec lifecycle runtime and prompt surfaces. The wizard does not add a new
runtime helper, MCP tool, or JSON payload schema. It is a prompt definition
that instructs Codex/Claude how to gather lifecycle context with existing
read-only tools (`scan_specs`, `lifecycle_guide`, `active_spec_preflight`,
`stage_readiness`, `task_context`, `traceability_lookup`,
`no_active_spec_context`), ask one bounded question at a time, classify
feedback, and produce a preview-first edit plan before any file write.

**Resolved 2026-06-17 (D001):** v1 is prompt-only plus durable guidance. No
deterministic runtime/MCP `documentation_wizard` tool is implemented. See
[Open Questions](#open-questions) for the full decision record.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|------------------|---------------------|
| R1 Stage-Aware Wizard Entry Point | AC1-AC4 | Prompt instructs the agent to call `scan_specs`/`lifecycle_guide`/`active_spec_preflight` and report stage, selection, and next action | Prompt content review and manual dogfood review |
| R2 Step-By-Step Documentation Flow | AC1-AC4 | Stage catalog and per-stage question sets documented in the prompt | Prompt content review against stage catalog |
| R3 Open-Question Guidance | AC1-AC4 | Prompt fields for why-it-matters, answer format, blocking status, destination | Prompt content review against question fields |
| R4 Feedback Disposition Workflow | AC1-AC4 | Prompt instructs the agent to classify feedback using the existing review-result disposition shape (accept/revise/defer/reject/human-decision) | Prompt content review against disposition list |
| R5 Preview-First Edit Plan | AC1-AC4 | Prompt requires a preview plan (file, section, change type, rationale) before any write | Prompt content review; no write-capable tool exists to test |
| R6 Existing Tool Composition | AC1-AC4 | Prompt names the existing tools it composes and forbids independent parsing | `prompts_validate` and manual cross-check against tool list |
| R7 Durable Promotion And Closure Awareness | AC1-AC4 | Prompt instructs the agent to report durable destinations and closure blockers at promotion/closure stages | Prompt content review against closure checklist |

## Correctness Property Coverage

| Property | Design Behavior | Validation Direction | Notes |
|----------|-----------------|----------------------|-------|
| CP-001 | Prompt instructs the agent never to report implementation readiness while blocking questions or downstream review needs remain | Prompt content review against `stage_readiness`/`closure_risk_review` output | Enforcement depends on the agent following prompt instructions, not code. |
| CP-002 | Prompt instructs the agent to advance stages only when required answers are present or an explicit, recorded exception exists | Prompt content review | Same caveat as CP-001. |
| CP-003 | Prompt instructs the agent to assign exactly one disposition before treating feedback as accepted, deferred, or rejected | Prompt content review | |
| CP-004 | Prompt requires path, section, change type, and rationale in every preview edit item | Prompt content review | No write-capable flow exists in v1. |
| CP-005 | Prompt instructs the agent to treat removed/closed spec packages as historical evidence only, using `no_active_spec_context`/archive index | Prompt content review | Depends on archive/closure history quality. |

Because v1 is prompt-only, these properties are validated by reading the
prompt content and by manual dogfood review, not by automated unit tests
against runtime code.

## High-Level Design

### System Architecture

The wizard has two layers:

1. **Lifecycle context input:** existing read-only runtime/MCP outputs such
   as `scan_specs`, `lifecycle_guide`, `active_spec_preflight`,
   `stage_readiness`, `task_context`, `traceability_lookup`, and
   `no_active_spec_context`.
2. **Agent-facing prompt surface:** a prompt definition that tells
   Codex/Claude which of the above tools to call, how to classify the
   current stage, how to ask the next bounded question, how to classify
   feedback, and how to produce a preview-first edit plan — without
   bypassing the skill or inventing a second lifecycle engine.

There is no separate "wizard decision model" code layer. The decision logic
(stage selection, question selection, feedback classification, preview-plan
construction) lives in the prompt's instructions to the agent, not in
`spec_runtime.py` or a new MCP tool.

### Components and Changes

- `skills/spec-lifecycle-manager/prompts/`
  - Add or refine a prompt such as `documentation-wizard` that instructs
    agents to call the existing read-only tools above, ask one stage of
    questions at a time by default (with an explicit checklist mode on
    request, per D003), classify feedback (per D002, reusing the existing
    review-result disposition shape), and stay preview-first.
- `skills/spec-lifecycle-manager/SKILL.md`
  - Add concise workflow guidance for user feedback and answering open
    questions.
- `docs/design/spec-lifecycle-management.md`
  - Promote accepted wizard behavior once implemented.
- `docs/reference/spec-lifecycle-runtime.md`
  - Document the prompt surface and the existing tools it composes.

### Conversation Output Shape

The prompt should instruct the agent to structure its replies around the
following information, reported in conversation rather than returned as a
JSON payload from a new tool:

```text
- current stage, selected spec or selection need
- next bounded question (or compact checklist, if requested)
- open questions: why it matters, expected answer format, blocking status,
  artifact destination
- feedback items: source, summary, disposition (per the review-result
  shape), affected artifacts, destination, residual risk
- preview edit plan: path, section, change type, rationale
- readiness signal (never "ready to implement" while blocking items remain)
- equivalent CLI/MCP recovery commands
- residual risk
```

### Data Flow

1. The agent receives a guided-documentation request.
2. The prompt instructs the agent to gather lifecycle context by calling
   `scan_specs`, `lifecycle_guide`, `active_spec_preflight`, and
   `stage_readiness` (when a spec is selected).
3. The agent determines the current stage and missing inputs using the
   prompt's stage catalog.
4. The agent asks the next bounded question or reports feedback-disposition
   guidance.
5. If enough information exists, the agent proposes a preview edit plan with
   target file, section, change type, and rationale.
6. The user approves or revises the plan.
7. The agent applies approved edits with ordinary file edits — there is no
   wizard write tool in v1.

## Low-Level Design

### Prompt Behavior

Stage selection should prefer, in order:

1. Explicit caller stage when valid.
2. Active spec artifact state and `stage_readiness`.
3. No-active or blank-repo `lifecycle_guide` context.
4. Conservative fallback: ask for selection or requirements clarification.

### Error Handling

The prompt should instruct the agent to handle these cases:

- Invalid spec reference: report selection guidance and available active
  specs.
- Multiple active specs without selection: ask a selection question; do not
  guess.
- Missing docs root: use blank/near-blank bootstrap guidance.
- Unsupported stage: report the valid stage list and a conservative next
  question.
- Feedback without a target spec: classify as advisory and ask for a
  destination.
- Any tool that is unavailable: report the equivalent CLI recovery command.

### Security, Trust, and Access

The wizard is read-only and preview-first by construction: it has no
write-capable tool to misuse. The prompt must not instruct the agent to write
repository files outside ordinary, user-approved edits, infer secrets, or
execute external services. A later write-capable wizard helper is a separate
decision (see D004) and is out of scope for this prompt.

### Migration and Compatibility

Existing prompt names and runtime commands must continue to work. The wizard
is introduced as a new prompt without changing the behavior of
`developer-start`, `lifecycle-triage`, or `task-context`. Existing active
specs do not need migration unless they opt into wizard guidance.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|----------------|
| Prompt content review | Stage selection, questions, feedback, preview-plan guidance | `tests/runtime/test_spec_runtime.py` prompt fixtures and task evidence | Enforcement depends on agent compliance, not code; no unit test proves runtime behavior. |
| Prompt validation | Prompt JSON contract | `prompts_validate` and CLI `prompts` command | Validates structure, not semantic quality. |
| Spec lint and scan | Package health | MCP `lint_spec_package`, `scan_specs` | Lint does not prove guidance quality. |
| Full unit suite | Regression coverage | `verification.md` | External plugin install parity needs sync/install checks if bundled files change. |

## Downstream Task Guidance

- D001-D004 are resolved; see [Open Questions](#open-questions).
- Properties or acceptance criteria that need explicit task coverage:
  - CP-001 through CP-005, validated by prompt content review since v1 has
    no runtime code to unit test.
- Optional artifacts needed before implementation:
  - None beyond this package.
- Downstream review needed if this design changes after tasks are drafted:
  - Update `tasks.md`, `traceability.md`, and `verification.md`.

## Operational Considerations

The wizard should reduce conversational drift, not create mandatory ceremony
for small changes. It should be available when a user asks for guided
documentation, rough idea to spec, open-question handling, feedback routing,
or phase progression. Normal small direct patches can still bypass the wizard
through existing lifecycle triage.

## Open Questions

All four decisions below were resolved on 2026-06-17 during T001.

- **D001 (resolved):** v1 is prompt-only plus durable guidance. No
  deterministic runtime/MCP `documentation_wizard` tool is implemented.
  Rationale: lower implementation cost; the prompt can compose existing
  read-only tools directly. Residual risk: enforcement depends on the agent
  following prompt instructions rather than code, so correctness properties
  are validated by prompt content review, not unit tests. A future spec may
  revisit a deterministic tool if prompt-only guidance proves insufficient.
- **D002 (resolved):** Feedback disposition reuses the existing review-result
  template shape rather than a smaller wizard-specific model, for
  consistency with other review workflows.
- **D003 (resolved):** The wizard asks one stage-specific question at a time
  by default, with an explicit user-requested checklist/fast mode as a
  documented exception (consistent with CP-002).
- **D004 (resolved):** Preview plans are applied manually by Codex/the user
  in v1; no write-capable wizard helper is built. A future guarded-write
  helper, if pursued, is to be routed to `docs/backlog/README.md` under T004
  rather than designed here.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Change Impact: [change-impact.md](change-impact.md)
- Tasks: [tasks.md](tasks.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
