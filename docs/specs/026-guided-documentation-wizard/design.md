---
title: Guided documentation wizard design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-14
---

# Technical Design

## Overview

Add a guided documentation wizard as a thin orchestration layer over existing
spec lifecycle runtime and prompt surfaces. The wizard should not become a
second lifecycle engine. It should inspect current lifecycle state, identify the
next documentation stage, ask the next bounded question, and produce a
preview-first update plan for the relevant spec or durable-document artifact.

The first implementation should favor deterministic runtime output and prompt
guidance. Write-capable behavior remains out of scope unless a later task adds
it under the existing guarded write policy.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| R1 Stage-Aware Wizard Entry Point | AC1-AC4 | Wizard state model and existing lifecycle-guide/preflight composition | Runtime unit tests and manual prompt review |
| R2 Step-By-Step Documentation Flow | AC1-AC4 | Stage catalog and question sets | Unit tests for stage transitions |
| R3 Open-Question Guidance | AC1-AC4 | Question model with answer guidance and destinations | Unit tests for blocking/deferred questions |
| R4 Feedback Disposition Workflow | AC1-AC4 | Feedback disposition model | Unit tests for dispositions and routing |
| R5 Preview-First Edit Plan | AC1-AC4 | Edit-plan schema and write boundary | Unit tests for preview payload shape |
| R6 Existing Tool Composition | AC1-AC4 | Reuse scan/preflight/stage readiness/prompt validation | Runtime and MCP tests |
| R7 Durable Promotion And Closure Awareness | AC1-AC4 | Promotion and closure stage outputs | Closure/promotion scenario tests |

## Correctness Property Coverage

| Property | Design Behavior | Validation Direction | Notes |
|----------|-----------------|----------------------|-------|
| CP-001 | `ready_to_implement` remains false when blocking questions or downstream review needs exist. | Unit tests over wizard payloads and stage readiness inputs. | Applies before any implementation stage. |
| CP-002 | Stage transitions advance only when required answers are present or an explicit exception is recorded. | Unit tests for requirements/design/task transition decisions. | Exceptions must be visible. |
| CP-003 | Feedback payload requires one primary disposition before routing. | Unit tests for feedback classification. | Mirrors review-result disposition ideas. |
| CP-004 | Edit-plan item schema requires path, section, change type, and rationale. | Unit tests for preview plan validation. | No write behavior in first slice. |
| CP-005 | Closed specs are represented through closure/archive context only. | Unit tests or scenario fixture with removed package history. | Reuses no-active-spec context rules. |

## High-Level Design

### System Architecture

The wizard has three layers:

1. **Lifecycle context input:** existing runtime outputs such as scan,
   lifecycle guide, active spec preflight, stage readiness, task context, and
   no-active-spec context.
2. **Wizard decision model:** deterministic classification of current stage,
   missing answers, open questions, feedback items, preview edits, and next
   user prompt.
3. **Agent-facing surface:** CLI/MCP runtime output plus a prompt definition
   that tells Codex how to use the wizard without bypassing the skill.

### Components and Changes

- `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Add a read-only `documentation_wizard(...)` helper or equivalent command.
  - Compose existing helper functions instead of reparsing artifacts.
  - Return deterministic JSON with stage, questions, feedback guidance, edit
    preview, validation/recovery commands, and residual risk.
- `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Expose the wizard helper as a read-only MCP tool if the runtime helper is
    implemented.
- `skills/spec-lifecycle-manager/prompts/`
  - Add or refine a prompt such as `documentation-wizard` that instructs agents
    to call the read-only tool first, ask one stage of questions, and avoid
    file writes until approved.
- `skills/spec-lifecycle-manager/SKILL.md`
  - Add concise workflow guidance for user feedback and answering open
    questions.
- `docs/design/spec-lifecycle-management.md`
  - Promote accepted design behavior once implemented.
- `docs/reference/spec-lifecycle-runtime.md`
  - Document the runtime/MCP/prompt surface.

### Data Models

The wizard payload should use stable, JSON-friendly records:

```text
wizard_payload:
  repo_classification
  selected_spec
  current_stage
  next_question
  question_set[]
  open_questions[]
  feedback_items[]
  preview_edit_plan[]
  readiness
  validation_or_recovery_commands[]
  residual_risk[]
```

Question record:

```text
question:
  id
  stage
  prompt
  why_it_matters
  expected_answer_format
  artifact_destination
  blocking
  examples
```

Feedback record:

```text
feedback:
  id
  source
  summary
  disposition
  affected_artifacts
  validation_impact
  destination
  residual_risk
```

Preview edit item:

```text
preview_edit:
  path
  section
  change_type
  rationale
  source_question_or_feedback
  requires_approval
```

### Data Flow

1. Caller invokes the wizard with a repository root, optional spec path, optional
   user input, optional current stage, and optional feedback text.
2. Runtime gathers lifecycle context through existing helpers.
3. Runtime determines the stage and missing inputs.
4. Runtime emits the next question or feedback disposition guidance.
5. If enough information exists to propose edits, runtime emits a preview edit
   plan with target sections.
6. Agent asks the user the next bounded question or requests approval for the
   preview plan.
7. A later implementation step may apply approved edits with ordinary Codex file
   edits, not with an autonomous wizard write loop.

## Low-Level Design

### Algorithms and Logic

```text
function documentation_wizard(repo_root, spec_path, stage, user_input, feedback):
    scan = scan_specs(repo_root)
    guide = lifecycle_guide(repo_root)
    selected = resolve selected spec or selection need
    stage_context = stage_readiness(selected) when selected
    questions = build_question_set(stage, selected, stage_context)
    feedback_items = classify_feedback(feedback) when feedback provided
    preview = build_preview_plan(questions, feedback_items, selected)
    return payload
```

Stage selection should prefer:

1. Explicit caller stage when valid.
2. Active spec artifact state and `stage_readiness`.
3. No-active or blank-repo lifecycle-guide context.
4. Conservative fallback: ask for selection or requirements clarification.

### Function Signatures and Interfaces

Candidate runtime function:

```text
documentation_wizard(
    repo_root: Path,
    docs_root: str | None = None,
    spec_path: str | None = None,
    stage: str | None = None,
    user_input: str | None = None,
    feedback: str | None = None,
) -> dict[str, Any]
```

Candidate CLI:

```text
skills/spec-lifecycle-manager/scripts/spec_runtime.py documentation-wizard .
skills/spec-lifecycle-manager/scripts/spec_runtime.py documentation-wizard . --spec-path docs/specs/026-guided-documentation-wizard --stage requirements
```

Candidate MCP tool:

```text
documentation_wizard(repo_root?, docs_root?, spec_path?, stage?, user_input?, feedback?)
```

### Error Handling

- Invalid spec reference: return selection guidance and available active specs.
- Multiple active specs without selection: ask selection question; do not guess.
- Missing docs root: use blank/near-blank bootstrap guidance.
- Unsupported stage: return valid stage list and a conservative next question.
- Feedback without target spec: classify as advisory and ask for destination.
- Any unavailable MCP feature: report equivalent CLI recovery commands.

### Security, Trust, and Access

The first implementation is read-only and preview-first. It must not execute
external services, mutate user-level config, write repository files, or infer
secrets. If later write behavior is proposed, it must stay scoped to active
spec or durable documentation paths and require explicit write intent.

### Migration and Compatibility

Existing prompt names and runtime commands must continue to work. The wizard can
be introduced as a new prompt/tool without changing the behavior of
`developer-start`, `lifecycle-triage`, or `task-context`. Existing active specs
do not need migration unless they opt into wizard guidance.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| Focused runtime unit tests | Stage selection, questions, feedback, preview schema | `tests/runtime/` and task evidence | Semantic quality of prompts still needs human review. |
| MCP server tests | Tool exposure and payload normalization | `tests/runtime/test_spec_mcp_server.py` | Already-running MCP sessions may need reload. |
| Prompt validation | Prompt JSON contract | `prompts_validate` and CLI prompts command | Prompt usefulness needs dogfood. |
| Spec lint and scan | Package health | MCP `lint_spec_package`, `scan_specs` | Lint does not prove implementation quality. |
| Full unit suite | Regression coverage | `verification.md` | External plugin install parity needs sync/install checks if bundled files change. |

## Downstream Task Guidance

- Required checkpoints before implementation:
  - Confirm whether the first slice is prompt-only, runtime-only, or both.
  - Confirm whether a write-capable wizard is explicitly out of scope for v1.
- Properties or acceptance criteria that need explicit task coverage:
  - CP-001 through CP-005.
- Optional artifacts needed before implementation:
  - None beyond this package.
- Downstream review needed if this design changes after tasks are drafted:
  - Update `tasks.md`, `traceability.md`, and `verification.md`.

## Operational Considerations

The wizard should reduce conversational drift, not create mandatory ceremony for
small changes. It should be available when a user asks for guided documentation,
rough idea to spec, open-question handling, feedback routing, or phase
progression. Normal small direct patches can still bypass the wizard through
existing lifecycle triage.

## Open Questions

- **D001:** Should v1 be prompt-only plus durable guidance, or include a
  deterministic runtime/MCP `documentation_wizard` tool?
- **D002:** Should feedback disposition reuse the existing review-result
  template shape or have a smaller wizard-specific model?
- **D003:** Should the wizard ask questions one at a time by default, or return a
  compact stage checklist when the user wants speed?
- **D004:** Should approved preview plans be applied manually by Codex only, or
  should a later guarded write helper be considered?

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Change Impact: [change-impact.md](change-impact.md)
- Tasks: [tasks.md](tasks.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
