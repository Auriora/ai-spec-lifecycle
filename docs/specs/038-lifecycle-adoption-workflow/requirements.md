---
title: Lifecycle adoption workflow requirements
doc_type: spec
artifact_type: requirements
status: draft
owner: platform
last_reviewed: 2026-07-18
---

# Lifecycle Adoption Workflow Requirements

## Introduction

A bounded external Chat Analyser study found genuine structured use of
`spec-lifecycle-manager` and a validation-heavy provisional usage pattern. A
follow-up hook review found that advisory hook guidance can influence later lint
calls even though ordinary hooks do not execute full-package lint directly. The
analysis producer also found an attribution defect, so exact operation counts
remain qualified external evidence rather than a lifecycle-manager contract.

This spec implements the lifecycle-manager improvements suggested by that
evidence. It composes existing lifecycle authority, strengthens state-specific
hook guidance, preserves MCP as the primary agent-facing interface, and consumes
external dogfood findings without taking ownership of Chat Analyser extraction,
classification, reconciliation, or reporting behavior.

## Goals

- Consume qualified external dogfood evidence without overstating exactness,
  causality, correctness, or usefulness.
- Give an implementation agent one concise start workflow that composes
  preflight, task context, traceability, readiness, and validation expectations.
- Route agents from implementation and validation into evidence-quality and
  durable-promotion checks before closure.
- Keep MCP primary for agent-facing work while retaining CLI use for hooks, CI,
  validation, debugging, and explicit recovery.
- Reduce the amount of skill text an agent must load while keeping governing
  rules discoverable and authoritative.
- Make advisory hook recommendations proportional to lifecycle state and avoid
  redundant full-package lint recommendations after ordinary writes.
- Keep checkout development repository-local, keep user-wide deployment on
  packaged artifacts, and make removed-cache hook entrypoints quiet.

## Non-Goals

- Implement the phase-completion writer owned by
  `docs/specs/034-phase-completion-helper/`.
- Replace `active_spec_preflight`, `task_context`, `traceability_lookup`,
  `agent_readiness_packet`, `stage_readiness`, `validation_plan`,
  `evidence_quality_check`, `promotion_plan`, or `closure_check`.
- Add blocking hooks or automatically change task state, durable docs, or spec
  lifecycle state.
- Add OpenTelemetry, remote observability, or a general event store; B025
  remains the owner of emitted telemetry.
- Implement session import or extraction, invocation-origin classification,
  native-to-normalized reconciliation, operation attribution, or analysis
  report confidence semantics. Those are Chat Analyser responsibilities.
- Treat invocation frequency as proof of correctness, usefulness, success,
  independent preference, or causal improvement.
- Require private session histories in CI or persist semantic chat content in
  this repository.

## Glossary

- **Adoption evidence:** A qualified external observation about lifecycle use,
  not proof that the work or product behavior was correct.
- **Implementation-start workflow:** A concise, read-only entry point that
  composes existing authoritative lifecycle context before source edits.
- **CLI fallback:** Direct `spec_runtime.py` use for validation, CI, runtime
  debugging, or recovery when MCP is unavailable.
- **Advisory hook guidance:** Non-blocking, state-specific guidance returned by
  a narrow hook path; it neither performs full validation nor mutates state.

## Requirements

### Requirement 1: Qualified External Dogfood Evidence

**User Story:** As a lifecycle maintainer, I want external adoption evidence
retained with its qualifications, so that product decisions remain reviewable
without importing the analyser's implementation contract.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN an external session-analysis finding informs implementation, WHEN the
   finding is recorded, THEN THE SYSTEM SHALL preserve the producer, analysis
   date, revision or evidence identity, bounded scope, conclusion, and known
   limitations without retaining semantic session content.
2. IF the external producer labels a count or conclusion provisional or
   unavailable, THEN THE SYSTEM SHALL preserve that qualification and SHALL NOT
   reconstruct or override it inside this repository.
3. Invocation evidence SHALL NOT be presented as proof of correctness,
   usefulness, independent preference, or causal improvement.

### Requirement 2: Composed Implementation Start

**User Story:** As an implementation agent, I want one concise start workflow,
so that I load the selected task's complete lifecycle context before editing.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN an active spec and selected task, WHEN the implementation-start
   workflow runs, THEN THE SYSTEM SHALL compose active preflight, task context,
   traceability, stage or agent readiness, and validation expectations from the
   existing authoritative surfaces.
2. GIVEN a required source surface reports a blocker or incomplete context,
   WHEN the workflow responds, THEN THE SYSTEM SHALL preserve that blocker and
   name the smallest next action rather than reporting agent readiness.
3. GIVEN no active spec or no selected runnable task, WHEN the workflow runs,
   THEN THE SYSTEM SHALL route to no-active context or task selection without
   inventing a task.
4. THE SYSTEM SHALL keep the workflow read-only and SHALL NOT change task state,
   edit documents, or treat planned validation as completed evidence.

### Requirement 3: Evidence And Promotion Routing

**User Story:** As a lead agent, I want phase-appropriate next actions, so that
validation-heavy usage does not skip evidence quality or durable promotion.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN implementation evidence exists, WHEN lifecycle next actions are
   generated, THEN THE SYSTEM SHALL route through validation planning and
   evidence-quality review before a closure claim.
2. GIVEN accepted behavior or deferred work has durable-document impact, WHEN a
   spec approaches promotion or closure, THEN THE SYSTEM SHALL surface
   `promotion_plan` or an equivalent durable-routing action.
3. GIVEN evidence or promotion is incomplete, WHEN closure is requested, THEN
   THE SYSTEM SHALL preserve the blocker and its evidence requirement.
4. THE SYSTEM SHALL compose the existing evidence, promotion, phase-gate, and
   closure authorities rather than implementing a competing readiness model.

### Requirement 4: Effective MCP-First Guidance

**User Story:** As a plugin user, I want agent-facing guidance to prefer MCP
unambiguously, so that the direct CLI remains a deliberate recovery surface.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN the MCP server is available, WHEN agent-facing next actions are
   returned, THEN THE SYSTEM SHALL name MCP tools as the primary lifecycle
   actions and SHALL separate CLI equivalents into a labelled validation or
   recovery section.
2. GIVEN MCP is unavailable, WHEN recovery guidance is returned, THEN THE
   SYSTEM SHALL provide equivalent repo-relative CLI commands and identify the
   fallback reason.
3. WHERE an aggregate response already carries invocation provenance, THE
   SYSTEM SHALL preserve the MCP or CLI surface identity without collecting
   semantic prompt or document content.
4. THE SYSTEM SHALL retain direct CLI behavior required by CI, validation,
   installed-runtime debugging, hooks, and no-MCP recovery.

### Requirement 5: Concise Skill And Capability Context

**User Story:** As a coding agent, I want a compact authoritative entrypoint, so
that lifecycle rules are available without repeatedly loading a large workflow
manual.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN the skill is activated, WHEN the entrypoint is loaded, THEN THE SYSTEM
   SHALL keep mandatory governing rules and routing in `SKILL.md` while moving
   detailed reference material to directly linked references where safe.
2. GIVEN first-run or capability guidance is requested, WHEN the runtime or MCP
   responds, THEN THE SYSTEM SHALL return a bounded capability summary with the
   correct primary actions for the current repository state.
3. WHERE detail is omitted for compactness, THE SYSTEM SHALL provide explicit
   references or expansion actions rather than silently dropping a lifecycle
   constraint.
4. Source, Codex bundle, Claude bundle, and installed-package validation SHALL
   enforce equivalent skill and prompt behavior.
5. GIVEN the 2026-07-18 source `SKILL.md` baseline is 53,427 bytes, WHEN the
   concise entrypoint is accepted, THEN THE SYSTEM SHALL reduce that source
   entrypoint to no more than 37,399 bytes while preserving the reviewed
   mandatory-rule inventory in the entrypoint or an explicit linked expansion.

### Requirement 6: State-Specific Advisory Hook Guidance

**User Story:** As an authoring agent, I want hook guidance proportional to the
current lifecycle state, so that ordinary writes do not trigger redundant
full-package validation advice.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN an ordinary spec write, task-checkbox write, template write, or
   verification write, WHEN its post-write hook runs, THEN THE SYSTEM SHALL use
   the corresponding narrow check and SHALL NOT execute or recommend
   full-package lint.
2. Full-package lint MAY run from an explicitly invoked `spec-resumed` or
   `spec-close-check` lifecycle boundary, or from an explicit user or agent
   validation request; no other hook state SHALL execute or recommend it.
3. GIVEN the same unchanged advisory state is observed repeatedly, WHEN hooks
   run again, THEN THE SYSTEM SHALL preserve debounce behavior and SHALL NOT
   repeatedly recommend the same lint action.
4. Hooks SHALL remain advisory, SHALL be quiet when no guidance or diagnostics
   are needed, and SHALL NOT mutate lifecycle state or block the underlying
   write.
5. GIVEN a running session retains a versioned plugin hook path whose script has
   been removed, WHEN the hook entrypoint runs, THEN THE SYSTEM SHALL return
   success without feedback rather than report a blocked post-tool hook.

### Requirement 7: Development And Package Isolation

**User Story:** As a lifecycle maintainer, I want checkout testing isolated to
the owning repository, so that active agents and user-wide packaged installs are
not disrupted by development refreshes.

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN a Codex development session for this repository, WHEN it starts through
   the supported development entrypoint, THEN THE SYSTEM SHALL load the skill,
   MCP server, and advisory hook from repository-owned source surfaces without
   calling plugin installation or modifying user-wide Codex state.
2. GIVEN a packaged lifecycle plugin is installed user-wide, WHEN a source-backed
   development session starts, THEN THE SYSTEM SHALL prevent packaged plugin
   components from running alongside the repository-owned lifecycle surfaces.
3. GIVEN the installer source is a Git checkout and the destination is the
   default user-wide Codex home, WHEN installation is requested, THEN THE SYSTEM
   SHALL refuse the deployment and direct the maintainer to repository-local
   development or a packaged artifact.
4. GIVEN installer behavior needs local validation, WHEN explicit non-user Codex
   and marketplace roots are supplied, THEN THE SYSTEM SHALL retain isolated
   dry-run and smoke-test support.

## Correctness Properties

- **CP-001:** No workflow reports implementation readiness when any composed
  authoritative source reports a blocking gap.
- **CP-002:** Agent-facing MCP-first output never presents a direct CLI command
  as the primary action while MCP is known to be available.
- **CP-003:** Ordinary write hooks never execute or recommend full-package lint;
  only explicit resume, closure, or validation boundaries may run it.
- **CP-004:** External dogfood qualifications are preserved and are never
  converted into correctness, independent-preference, or causal claims.
- **CP-005:** Compact skill and capability guidance preserves every mandatory
  lifecycle constraint through inline text or an explicit linked expansion.
- **CP-006:** The implementation-start workflow is deterministic and read-only
  for the same repository and task evidence.
- **CP-007:** Source-backed development and packaged user deployment never share
  a mutable plugin-cache refresh operation.

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/spec-lifecycle-management.md` | Defines the staged lifecycle, phase gates, Agent Readiness Contract, and context-budget rules. | high | Current lifecycle authority. |
| `docs/reference/spec-lifecycle-runtime.md` | Defines MCP-first usage and the current tool, CLI, and hook contracts. | high | Direct CLI is validation/recovery-only for agents. |
| `docs/reference/spec-lifecycle-dogfood-evaluation.md` | Stores qualitative dogfood outcomes and current advisory-hook policy. | high | Receives only qualified external findings. |
| `docs/design/coding-agent-operating-model.md` | Defines lightweight evidence, review, hook-noise, and closure-readiness metrics. | high | Metrics are guidance rather than telemetry requirements. |
| `docs/backlog/README.md` | Owns B014, B015, B025, B050, and related deferred lifecycle work. | high | B025 remains outside this spec. |
| `docs/specs/034-phase-completion-helper/requirements.md` | Defines the separate phase-completion bookkeeping writer. | high | Explicitly excluded from this spec. |

## Canonical Context

No spec-local source import is required. The durable-source table above links
the current authorities directly, the proposed changes are explicit deltas,
and no legacy or conflicting document is being copied or adapted into this
package. Implementation tasks must refresh the linked durable sources and
code-derived contracts before editing; this decision waives creation of a
duplicative `canonical-context.md` unless a concrete authority conflict is
discovered later.

## Durable Impact

| Durable area | Action | Target | Notes |
|--------------|--------|--------|-------|
| design | modify | `docs/design/spec-lifecycle-management.md` | Add the accepted implementation-start composition and routing behavior. |
| runtime reference | modify | `docs/reference/spec-lifecycle-runtime.md` | Document MCP-first start, recovery separation, capability output, and state-specific hook guidance. |
| dogfood evidence | modify | `docs/reference/spec-lifecycle-dogfood-evaluation.md` | Promote the qualified external baseline and follow-up result. |
| backlog | modify | `docs/backlog/README.md` | Mark the promoted item complete and route residual telemetry or measurement work once. |
| roadmap | modify | `docs/roadmap/README.md` | Track adoption workflow delivery and sequencing with Spec 034. |
| skill and bundles | modify | `skills/spec-lifecycle-manager/` and plugin mirrors | Keep mandatory rules concise and behavior synchronized. |

## Staged Readiness

- **Current stage:** agent-ready review
- **Next stage:** implementation
- **Ready to implement when:** the reconciled package passes lifecycle lint,
  explicit task-context lookup, and stage-readiness checks with no blocking
  requirement, acceptance, decision, or validation-context gaps.
- **Design-first exception:** no
- **Optional artifacts included:** `research.md`, `change-impact.md`,
  `verification.md`
- **Downstream review needed:** design, tasks, traceability, verification,
  implementation

## Technical Context

- **Language/Version:** Python 3 standard library runtime, JSON MCP responses,
  Markdown and JSON prompt/skill definitions.
- **Primary Dependencies:** Existing lifecycle shared core, prompt registry,
  MCP adapter, CLI adapter, hook runtime, plugin bundle synchronization, and a
  reviewed external dogfood report.
- **Target Platform:** Codex and Claude Code plugin users; direct CLI for CI,
  hooks, validation, and recovery.
- **Constraints:** Read-only start workflow; advisory-only hooks; deterministic
  output; no private session content; no new telemetry or analysis subsystem.
- **Performance Goals:** Compact start and capability responses remain within
  the existing bounded-output contract and avoid loading unrelated artifacts;
  ordinary hook paths avoid full-package lint.

## Success Criteria

- **SC-001:** One documented start workflow returns or routes to preflight,
  task context, traceability, readiness, and validation expectations.
- **SC-002:** Next-action routing preserves evidence-quality, promotion, and
  closure blockers from existing authorities.
- **SC-003:** MCP-visible output keeps CLI commands in a labelled validation or
  recovery branch.
- **SC-004:** Mandatory lifecycle guidance remains equivalent across source and
  installed bundles while source `SKILL.md` is reduced from 53,427 bytes to no
  more than 37,399 bytes.
- **SC-005:** Ordinary write-hook fixtures neither execute nor recommend
  full-package lint; explicit resume, closure, and validation fixtures preserve
  their defined package-validation behavior.
- **SC-006:** Promoted dogfood documentation preserves the external producer's
  qualifications without importing analyser implementation requirements.
- **SC-007:** A source-backed Codex development session exposes only the
  repository lifecycle skill, MCP server, and hook; checkout installation to
  the default user Codex home is refused; packaged user installation remains
  unchanged.

## Related Artifacts

- Research: `research.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
- Change Impact: `change-impact.md`
