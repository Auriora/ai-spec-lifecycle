---
title: Guided documentation wizard requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-14
---

# Requirements

## Introduction

The `spec-lifecycle-manager` skill now has useful staged lifecycle surfaces:
`lifecycle_guide`, `bootstrap_plan`, `stage_readiness`, prompt definitions, and
task-context tools. Those surfaces help an agent orient itself, but they do not
yet provide a user-facing step-through documentation workflow.

The missing behavior is a guided wizard that helps a maintainer or coding agent
move one stage at a time through requirements, design, tasks, feedback, open
questions, approval gates, and durable-document promotion. The wizard should
make the next question explicit, preserve answers in the right artifact, and
avoid jumping from a rough idea directly into implementation.

## Goals

- Add a guided documentation workflow for spec authoring and resumed spec work.
- Make open questions actionable by recommending answer formats, decision
  owners, blocking status, and the artifact that should receive the answer.
- Capture user feedback as explicit accept, revise, defer, reject, or decision
  states rather than treating feedback as ordinary prose.
- Connect wizard stages to existing lifecycle runtime surfaces instead of
  creating a separate lifecycle engine.
- Keep the first implementation read-only or preview-first until explicit file
  writes are approved.
- Preserve the current temporary-spec and durable-doc promotion model.

## Non-Goals

- Do not implement an autonomous agent loop that repeatedly asks and edits
  without user approval.
- Do not replace `requirements.md`, `design.md`, `tasks.md`, `traceability.md`,
  or `verification.md` with a new canonical artifact.
- Do not adopt CLU, Kiro, or any external tool's folder layout as the source of
  truth for this repository.
- Do not create write-capable MCP tools outside the existing guarded write
  policy without an explicit approval and permission design.
- Do not solve npm publishing, developer CLI tooling, or plugin install drift in
  this spec.

## Glossary

| Term | Definition |
|------|------------|
| Wizard | A guided, stage-aware workflow that asks the next bounded question, records the expected answer shape, and reports the next safe action. |
| Stage | A lifecycle phase such as discovery, requirements, design, tasks, implementation readiness, verification, promotion, or closure. |
| Open question | A missing decision, unknown, ambiguity, or user-feedback item that blocks or influences a later lifecycle stage. |
| Feedback disposition | The recorded outcome for user or review feedback: accepted, revise, deferred, rejected, or human decision required. |
| Preview-first | Behavior that reports proposed edits or decisions before changing repository files. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/spec-lifecycle-management.md` | Documents staged lifecycle flow, first-run guidance, bootstrap planning, stage readiness, and Agent Readiness Contract boundaries. | high | Baseline is agent-facing readiness, not a conversational wizard. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime commands, MCP tools, prompt definitions, and preview/read-only behavior. | high | New wizard should compose existing tools where possible. |
| `docs/reference/document-routing-and-expert-review-matrix.md` | Defines document routing, whole-package review, open decisions, durable targets, and expert roles. | high | Wizard should surface these review and routing choices as questions. |
| `docs/reference/plugin-comparison-improvements.md` | Records accepted prompt aliases, lifecycle triage, lifecycle gates, and deferred external-tool ideas. | high | Wizard should not reopen rejected autonomous execution loops. |
| `docs/backlog/README.md` | Tracks related candidates: spec candidate builder, phase gate check, semantic requirements lint, steering context, prompt scope triage, and feedback routing. | high | This spec consolidates the user-facing wizard slice rather than scattering it across those candidates. |
| `docs/history/spec-archive-index.md` | Records closed `024-staged-developer-onboarding` and its durable destinations. | high | Confirms staged onboarding landed but the active package was removed. |
| `skills/spec-lifecycle-manager/prompts/` | Contains current prompt definitions such as `developer-start`, `lifecycle-triage`, and `task-context`. | high | Wizard may add a new prompt or refine existing prompts. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Provides lifecycle guide, bootstrap plan, stage readiness, prompt validation, and supporting runtime tools. | high | Wizard runtime should extend this helper rather than duplicate parsing. |

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| design | clarify | `docs/design/spec-lifecycle-management.md` | Add the guided documentation workflow once accepted. |
| runtime reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document wizard command/tool/prompt behavior after implementation. |
| prompt guidance | add | `skills/spec-lifecycle-manager/prompts/` | Likely add `documentation-wizard` or equivalent guided prompt. |
| backlog | clarify | `docs/backlog/README.md` | Route or supersede overlapping candidate rows where this spec implements a slice. |
| skill guidance | clarify | `skills/spec-lifecycle-manager/SKILL.md` | Add stage-by-stage user-feedback and open-question guidance if implemented. |
| tests | add | `tests/runtime/` | Cover deterministic wizard output and prompt validation. |

## Staged Readiness

- **Current stage:** requirements
- **Next stage:** design
- **Ready to design when:** wizard scope, stage model, feedback dispositions,
  open-question handling, write boundary, and durable promotion targets are
  explicit.
- **Design-first exception:** no.
- **Optional artifacts recommended:** `change-impact.md`
- **Downstream review needed:** design, tasks, traceability, verification

## Requirements

### Requirement 1: Stage-Aware Wizard Entry Point

**User Story:** As a maintainer, I want a single guided documentation entry
point, so that I can move through the lifecycle without remembering which prompt
or runtime tool to call next.

#### Acceptance Criteria

1. GIVEN a repository with active specs, WHEN the wizard starts, THEN it SHALL
   report the current lifecycle stage, selected spec or selection need, and the
   next bounded documentation action.
2. GIVEN no active specs, WHEN the wizard starts, THEN it SHALL use durable docs,
   backlog, roadmap, closure log, and archive index rather than resurrecting
   removed packages.
3. WHEN multiple active specs exist, THEN the wizard SHALL ask for or report the
   required selection instead of guessing.
4. IF the repository is blank or near blank, THEN the wizard SHALL use
   preview-only bootstrap guidance and SHALL require user-confirmed project
   purpose before proposing durable structure.

### Requirement 2: Step-By-Step Documentation Flow

**User Story:** As a user shaping a spec, I want the wizard to ask one stage of
questions at a time, so that requirements, design, tasks, and verification do
not get mixed together prematurely.

#### Acceptance Criteria

1. GIVEN a rough idea, WHEN the wizard is in requirements mode, THEN it SHALL
   ask for problem, goals, non-goals, user stories, acceptance criteria,
   durable baseline, durable impact, correctness properties, and open questions.
2. WHEN requirements are incomplete, THEN the wizard SHALL recommend staying in
   requirements mode instead of drafting implementation tasks.
3. WHEN requirements are coherent enough for design, THEN the wizard SHALL
   summarize accepted requirements and ask the next design-stage questions.
4. WHEN design is coherent enough for task planning, THEN the wizard SHALL ask
   for task slices, dependencies, validation checkpoints, durable promotion
   targets, and human review points.

### Requirement 3: Open-Question Guidance

**User Story:** As a user answering unresolved questions, I want each question
to include guidance about the expected answer, so that decisions become usable
spec content.

#### Acceptance Criteria

1. GIVEN an open question, WHEN the wizard reports it, THEN it SHALL include why
   the question matters, the affected stage, candidate answer format, blocking
   status, and likely artifact destination.
2. IF a question blocks implementation readiness, THEN the wizard SHALL label it
   as blocking and SHALL NOT report the spec as ready to implement.
3. IF a question can be deferred, THEN the wizard SHALL recommend a destination
   such as backlog, roadmap, follow-up spec, or explicit non-goal.
4. WHEN the user answers a question, THEN the wizard SHALL recommend the exact
   artifact section that should be updated.

### Requirement 4: Feedback Disposition Workflow

**User Story:** As a user reviewing generated spec content, I want a clear
feedback workflow, so that accepted, rejected, revised, and deferred feedback is
tracked.

#### Acceptance Criteria

1. GIVEN user feedback on a spec artifact, WHEN the wizard classifies it, THEN
   it SHALL offer dispositions: accept, revise, defer, reject, or human decision
   required.
2. WHEN feedback is accepted, THEN the wizard SHALL identify the affected
   artifact sections and validation impact.
3. WHEN feedback is deferred, THEN the wizard SHALL identify one primary
   destination and residual risk.
4. WHEN feedback is rejected, THEN the wizard SHALL preserve the rationale
   without treating the rejected item as a requirement.

### Requirement 5: Preview-First Edit Plan

**User Story:** As a maintainer, I want proposed documentation edits before
files change, so that guided authoring remains inspectable and controlled.

#### Acceptance Criteria

1. WHEN the wizard proposes file changes, THEN it SHALL return a preview plan
   listing files, sections, change type, and rationale before any write.
2. IF write-capable behavior is added, THEN it SHALL require explicit write
   intent and SHALL stay scoped to active spec or durable documentation paths.
3. The first implementation SHALL be usable without adding new write-capable MCP
   tools.
4. The wizard SHALL use repo-relative paths in all user-facing output.

### Requirement 6: Existing Tool Composition

**User Story:** As a maintainer, I want the wizard to reuse current lifecycle
tools, so that it does not drift from existing scan, readiness, and validation
behavior.

#### Acceptance Criteria

1. The wizard SHALL compose existing scan, active preflight, lifecycle guide,
   stage readiness, prompt validation, task context, and traceability behavior
   where applicable.
2. The wizard SHALL NOT implement an independent spec parser when existing
   runtime helpers already provide the required data.
3. The wizard SHALL report the equivalent CLI recovery commands when MCP is not
   available.
4. Prompt definitions SHALL validate through `prompts_validate` after any prompt
   additions or modifications.

### Requirement 7: Durable Promotion And Closure Awareness

**User Story:** As a user completing guided documentation work, I want the
wizard to keep durable promotion visible, so that accepted behavior does not
remain only in the spec package.

#### Acceptance Criteria

1. WHEN the wizard reaches promotion or closure stages, THEN it SHALL report
   durable destinations, unresolved spec-only content, validation evidence, and
   closure blockers.
2. WHEN accepted behavior affects durable docs, THEN the wizard SHALL identify
   promotion targets before closure.
3. IF durable promotion is blocked, THEN the wizard SHALL recommend keeping the
   spec open or routing a follow-up with an owner and destination.
4. The wizard SHALL avoid presenting removed spec packages as active guidance.

## Correctness Properties

- **CP-001**: A wizard response must never report implementation readiness when
  blocking open questions or downstream artifact review needs remain.
- **CP-002**: A wizard response must preserve stage order unless the user
  explicitly chooses and records a design-first or task-first exception.
- **CP-003**: A feedback item must have exactly one primary disposition before it
  can be treated as accepted input, deferred work, or rejected scope.
- **CP-004**: A proposed edit plan must identify file path, target section,
  change type, and rationale before any write-capable flow changes files.
- **CP-005**: Removed or closed spec packages must be reported as historical
  evidence only, not as current implementation targets.

## Technical Context

- **Language/Version:** Python 3 standard library for runtime helpers; JSON
  prompt definitions.
- **Primary Dependencies:** Existing `spec_runtime.py`, `spec_mcp_server.py`,
  prompt definitions, and `unittest` tests.
- **Target Platform:** Local Codex skill/plugin workflow with optional MCP.
- **Constraints:** Preview-first, repo-relative paths, no autonomous write loop,
  no new dependency unless separately justified.
- **Performance Goals:** Wizard output should be deterministic and suitable for
  direct MCP/CLI use without scanning unrelated repository history.

## Success Criteria

- **SC-001**: A maintainer can ask for guided documentation help and receive a
  stage-specific next question plus expected answer guidance.
- **SC-002**: Open questions and feedback are classified with blocking status,
  disposition, artifact destination, and next action.
- **SC-003**: Prompt/runtime validation passes after the wizard surface is added.
- **SC-004**: Durable docs explain the guided wizard behavior after
  implementation and before closure.

## Related Artifacts

- Change Impact: [change-impact.md](change-impact.md)
- Design: [design.md](design.md)
- Tasks: [tasks.md](tasks.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
