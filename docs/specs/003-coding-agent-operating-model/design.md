---
title: Coding agent operating model design
doc_type: spec
artifact_type: design
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Technical Design

## Overview

The proposed operating model is a risk-scaled workflow for coding agents. It
keeps the classic QA lifecycle intact but compresses and automates parts that
agents can perform quickly: exploration, drafting, implementation, test
generation, verification collection, and review passes.

The developer operator remains the accountable decision-maker.

## High-Level Design

### Workflow Levels

| Level | Use When | Required Gates |
|-------|----------|----------------|
| Direct patch | Low-risk, local, easily verified change | intent, patch, evidence |
| Lightweight spec | Small behavior change or bug fix | durable baseline, tasks, verification |
| Full spec | Cross-module, data, integration, or user-facing change | requirements, design, tasks, change impact, verification, review, durable promotion |
| Governance gate | Security, production data, contracts, migrations, policy conflicts | explicit human decision before implementation |

### Agent Roles

| Role | Responsibility |
|------|----------------|
| Lead agent | Maintains context, selects workflow level, owns reconciliation. |
| Explore agent | Performs read-only code/doc investigation. |
| Worker agent | Implements bounded, non-overlapping slices. |
| Review agent | Reviews for correctness, risk, architecture, tests, or docs. |
| Verification agent | Runs or designs validation and records evidence. |
| Developer operator | Owns intent, constraints, acceptance, tradeoffs, and final judgment. |

### QA Gate Mapping

| Traditional gate | Agent-adapted equivalent |
|------------------|--------------------------|
| Requirements review | Intent plus EARS acceptance criteria or concise task acceptance. |
| Design review | Lightweight design or explicit implementation plan. |
| Implementation control | Bounded task slices with dependencies and file ownership. |
| Test/QA | Agent-run validation plus evidence capture. |
| Code review | Human review plus optional adversarial subagent review. |
| Release readiness | Verification record with risk, rollback, and residual issues. |
| Documentation handoff | Durable promotion before spec closure. |

### Decision Gates

Escalate to an explicit human decision when work affects security, production
data, contracts, migrations, governance, lifecycle policy, hooks, MCP surfaces,
or cross-module architecture.

### Evidence Rules

Completed work needs nearby evidence, either in task entries or in
`verification.md`. Evidence can be command results, manual verification,
review disposition, screenshots or logs where relevant, or explicit residual
risk when validation cannot run.

### Parallelism Rules

Parallel agents are appropriate for bounded read-only investigation,
independent review, validation design, or non-overlapping implementation
slices. Conflicting findings must be reconciled before implementation or
closure continues.

### Metrics

Metrics should stay lightweight: cycle time, rework, evidence quality, review
findings, hook noise, and closure readiness are useful only when they influence
future workflow choices.

### Durable Documentation Boundary

The durable destination for the operating model is
`docs/design/coding-agent-operating-model.md`. Governance updates are deferred
until the model becomes mandatory policy rather than operating guidance.

### Dogfood Decision

Dogfood on lifecycle cleanup, runtime behavior changes, and Codex hook
installation showed the model is useful as durable guidance without requiring
an immediate governance or skill behavior change.

## Low-Level Design

### Intake Algorithm

1. Read repo instructions and durable docs.
2. Classify requested change by risk.
3. Select workflow level.
4. Identify durable source-of-truth docs or gaps.
5. Decide whether to create or update a spec.
6. Select one implementation or research slice.

### Closure Algorithm

1. Re-read active spec artifacts.
2. Map accepted spec content to durable destinations.
3. Promote or explicitly defer each lasting element.
4. Verify tests and review evidence.
5. Update active indexes so the spec no longer appears active.
6. Archive or remove the spec according to document lifecycle rules.
7. Record residual risk and follow-up owners.

## Operational Considerations

- Subagents should be used for bounded side tasks, not vague delegation.
- Evidence should be recorded close to the task or in `verification.md`.
- Process overhead must be measured; the workflow should get lighter when it
  does not improve outcomes.
- External repos with their own templates must remain authoritative.

## Open Questions

- Which metrics are worth collecting automatically rather than recording in
  task or verification evidence?
- Should future workflow changes update governance, the skill, or durable
  design docs first?
- Which hook findings should remain advisory even after dogfooding?

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Research reference:
  [coding-agent-workflow-research.md](../../reference/coding-agent-workflow-research.md)
- Tasks: [tasks.md](tasks.md)
