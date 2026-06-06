---
title: Operating model governance adoption requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Requirements

## Introduction

The coding-agent operating model has been dogfooded across documentation,
runtime, hook, MCP, closure, and archive-index work. It is now useful to adopt
the hard rules into governance while keeping flexible workflow guidance in the
durable design doc.

## Goals

- Promote mandatory operating-model rules into the constitution.
- Keep workflow levels, role descriptions, and metrics in durable design
  guidance instead of governance policy.
- Update backlog and roadmap status for R003/B005.
- Close the implementation spec with durable evidence.

## Non-Goals

- Promoting blocking hooks.
- Changing runtime behavior.
- Adding new MCP tools.
- Making every operating-model recommendation mandatory.

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/coding-agent-operating-model.md` | Defines risk-scaled workflow guidance, decision gates, evidence, parallelism, metrics, and durable-doc boundary. | high | Source for candidate governance rules. |
| `docs/governance/constitution.md` | Current mandatory lifecycle principles. | high | Governance destination for hard rules. |
| `docs/roadmap/README.md` | R003 tracks operating-model governance adoption. | high | Planning source. |
| `docs/backlog/README.md` | B005 tracks the same adoption decision. | high | Backlog source. |

## Requirements

### Requirement 1: Select Hard Rules

**User Story:** As a lifecycle maintainer, I want only hard operating-model
rules promoted into governance, so that governance stays enforceable.

#### Acceptance Criteria

1. GIVEN the operating model, WHEN governance adoption is performed, THEN
   mandatory rules are separated from flexible guidance.
2. GIVEN flexible workflow mechanics exist, WHEN governance is updated, THEN
   they remain in durable design docs unless they are policy constraints.
3. IF a rule cannot be enforced or reviewed, THEN it SHALL remain guidance
   rather than constitution text.

### Requirement 2: Adopt Mandatory Agent Workflow Rules

**User Story:** As an agent using specs, I want governance to require full
context, evidence, and durable promotion, so that implementation does not drift
from accepted specs.

#### Acceptance Criteria

1. GIVEN an active spec exists, WHEN implementation starts, THEN agents SHALL
   use relevant requirements, design, verification, durable baseline, and
   traceability context rather than tasks alone.
2. GIVEN a task is marked complete, WHEN completion is recorded, THEN evidence
   SHALL be present or residual risk documented.
3. GIVEN lasting behavior changes, WHEN closure occurs, THEN durable docs,
   backlog, roadmap, issue tracker, or follow-up spec destinations SHALL be
   updated before closure.

### Requirement 3: Adopt Decision Gate And Parallelism Rules

**User Story:** As a developer operator, I want governance to define when
agents must stop or constrain delegation, so that risky work remains
accountable.

#### Acceptance Criteria

1. GIVEN work affects security, production data, contracts, migrations,
   governance, hooks, MCP surfaces, or cross-module boundaries, WHEN an agent
   proceeds, THEN explicit decision-gate handling SHALL be recorded.
2. GIVEN subagents or parallel work are used, WHEN write scopes overlap or
   findings conflict, THEN the lead agent SHALL reconcile before implementation
   or closure proceeds.
3. IF governance conflicts with a spec or durable design doc, THEN governance
   SHALL take precedence unless the user explicitly requests a governance
   update.

## Correctness Properties

- Governance contains mandatory, reviewable rules only.
- Design docs remain the home for flexible workflow levels, roles, metrics, and
  dogfood guidance.
- R003/B005 status reflects the adopted decision.
- Closure evidence records that no runtime behavior changed.

## Success Criteria

- Constitution includes selected operating-model governance rules.
- Operating-model design records that selected rules were adopted.
- Roadmap/backlog mark R003/B005 complete.
- Spec 012 closes with passing lint, scan, archive-index validation, tests, and
  diff hygiene.
