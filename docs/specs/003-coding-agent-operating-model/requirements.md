---
title: Coding agent operating model requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-02
---

# Requirements

## Introduction

This exploration spec defines requirements for a tailored operating model for
coding agents. The model should preserve the QA spine shared by established
software development approaches while adapting it to agent speed, broader model
knowledge, parallel exploration, and developer-operator judgment.

Related reference:
[Coding agent workflow research](../../reference/coding-agent-workflow-research.md).

## Goals

- Define a practical operator-agent workflow for this environment.
- Preserve durable software quality gates while reducing unnecessary ceremony.
- Clarify when specs, durable docs, review, and validation are required.
- Identify measurements that show where coding agents are net beneficial.

## Non-Goals

- Replace developer judgment with autonomous agent acceptance.
- Mandate heavyweight specs for every change.
- Standardize on one external coding-agent product.
- Modify the current skill implementation in this exploration step.

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/reference/coding-agent-workflow-research.md` | Research and recommendations for supervised, evidence-driven coding-agent workflows. | high | Primary research baseline for this model. |
| `docs/design/spec-lifecycle-management.md` | Existing lifecycle model for temporary specs, durable docs, closure, and evidence. | high | The operating model must align with this lifecycle. |
| `skills/spec-lifecycle-manager/SKILL.md` | Practical agent workflow instructions used in this repository. | high | Durable skill behavior should stay compatible with the model. |
| `docs/governance/constitution.md` | Governance constraints for lifecycle changes and evidence. | high | Governance remains higher priority than active specs. |

## Requirements

### Requirement 1: Risk-Scaled Workflow

**User Story:** As a developer operator, I want the workflow to scale with
change risk, so that small changes remain fast while high-risk work gets proper
QA gates.

#### Acceptance Criteria

1. GIVEN a low-risk change, WHEN the workflow is selected, THEN it supports a
   direct patch path with evidence.
2. GIVEN a medium- or high-risk change, WHEN the workflow is selected, THEN it
   requires explicit baseline, plan, verification, and review gates.
3. IF a change affects security, production data, contracts, migrations, or
   cross-module behavior, THEN the workflow SHALL require human decision gates.

### Requirement 2: Durable Documentation Boundary

**User Story:** As a maintainer, I want specs to remain temporary and durable
docs to remain authoritative, so that future agents and developers read current
truth rather than stale implementation scaffolding.

#### Acceptance Criteria

1. GIVEN an active spec, WHEN implementation completes, THEN accepted behavior
   is promoted into durable docs before closure.
2. GIVEN a completed spec, WHEN closure is requested, THEN the workflow checks
   that no durable behavior exists only inside the spec package.
3. IF durable promotion is blocked, THEN the workflow SHALL keep the spec open
   or create a follow-up with owner, destination, and blocker.

### Requirement 3: Evidence-Based Completion

**User Story:** As a reviewer, I want agents to provide evidence for completed
work, so that review can focus on real risk instead of re-discovering what was
done.

#### Acceptance Criteria

1. GIVEN a completed task, WHEN the agent marks it complete, THEN evidence is
   recorded.
2. WHERE automated tests apply, THE SYSTEM SHALL prefer command output over
   unsupported claims.
3. IF validation cannot run, THEN the workflow SHALL record residual risk and
   alternate verification before accepting completion.

### Requirement 4: Operator-Guided Agent Parallelism

**User Story:** As a developer operator, I want to use subagents for bounded
exploration and review, so that agent parallelism improves confidence without
creating coordination noise.

#### Acceptance Criteria

1. GIVEN independent exploration or review work, WHEN subagents are used, THEN
   each subagent has a bounded question and output.
2. GIVEN implementation work, WHEN multiple agents are used, THEN write scopes
   do not overlap unless explicitly coordinated.
3. IF a subagent result conflicts with main-session evidence, THEN the operator
   or lead agent SHALL reconcile before implementation proceeds.

### Requirement 5: Local Outcome Measurement

**User Story:** As a process owner, I want local measurements of agent-assisted
work, so that workflow decisions are based on observed project outcomes.

#### Acceptance Criteria

1. GIVEN agent-assisted tasks, WHEN they complete, THEN cycle time, rework,
   evidence quality, and review findings can be recorded.
2. GIVEN repeated use of the workflow, WHEN outcomes are reviewed, THEN the team
   can identify which task classes benefit most from agents.
3. IF a workflow adds overhead without improving quality or speed, THEN it SHALL
   be simplified or reserved for higher-risk work.

## Correctness Properties

- Workflow level selection must scale with change risk and must not force full
  spec ceremony onto low-risk direct patches.
- Durable docs remain the source of truth after spec closure.
- Completed agent tasks require evidence or explicitly recorded residual risk.
- Parallel agent work must have bounded questions or non-overlapping write
  scopes.
- Local metrics must be lightweight enough that measurement does not dominate
  the work being measured.

## Success Criteria

- A documented operating model exists.
- The model maps classic QA gates to agent-adapted equivalents.
- The model defines when to use direct patch, lightweight spec, full spec, and
  durable-doc promotion.
- A validation plan exists for dogfooding on future skill and project changes.

## Open Questions

- Should the operating model become a durable governance document, a skill
  reference, or both?
- What minimal metrics can be collected without slowing the operator down?
- Which task categories should be explicitly marked as unsafe for autonomous
  implementation?
