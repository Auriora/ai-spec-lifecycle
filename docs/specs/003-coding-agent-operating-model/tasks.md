---
title: Coding agent operating model tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-02
---

# Tasks

**Input**: `requirements.md`, `design.md`, and
`docs/reference/coding-agent-workflow-research.md`

## Task Dependency Graph

```text
T001 -> T002 -> T003
T003 -> T004
T003 -> T005
T004 + T005 -> T006
```

## Phase 1: Research Baseline

- [x] T001 Research effective coding-agent workflow patterns.
  - Depends on: none
  - Files: `docs/reference/coding-agent-workflow-research.md`
  - Acceptance: Reference doc cites current industry, vendor, and research
    sources and distinguishes evidence from recommendation.
  - Evidence: Research reference created with source links.

- [x] T002 Create exploration spec for the operating model.
  - Depends on: T001
  - Files: `docs/specs/003-coding-agent-operating-model/`
  - Acceptance: Spec includes requirements, design, and tasks.
  - Evidence: This spec package created.

## Phase 2: Model Refinement

- [ ] T003 Review the proposed principles with real project workflows.
  - Depends on: T002
  - Files: `docs/reference/coding-agent-workflow-research.md`,
    `docs/specs/003-coding-agent-operating-model/requirements.md`
  - Acceptance: Findings identify which practices are too heavy, too weak, or
    missing for target projects.
  - Evidence: Pending.
  - [ ] T003.1 Review against a low-risk direct patch.
  - [ ] T003.2 Review against a medium-risk bug fix.
  - [ ] T003.3 Review against a high-risk data/integration change.

- [ ] T004 Define local outcome metrics.
  - Depends on: T003
  - Files: `docs/specs/003-coding-agent-operating-model/design.md`
  - Acceptance: Metrics are practical to collect during agent-assisted work.
  - Evidence: Pending.

- [ ] T005 Decide durable destination for the operating model.
  - Depends on: T003
  - Files: `docs/governance/`, `docs/design/`, `skills/spec-lifecycle-manager/`
  - Acceptance: Decision identifies whether the model belongs in governance,
    durable design docs, skill references, or a combination.
  - Evidence: Pending.

## Phase 3: Dogfood And Close

- [ ] T006 Dogfood the model on a real change and decide next updates.
  - Depends on: T004, T005
  - Files: `docs/specs/003-coding-agent-operating-model/`
  - Acceptance: Dogfood evidence records workflow level, agent roles used,
    validation evidence, overhead, and recommended changes.
  - Evidence: Pending.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
- Research:
  [coding-agent-workflow-research.md](../../reference/coding-agent-workflow-research.md)
