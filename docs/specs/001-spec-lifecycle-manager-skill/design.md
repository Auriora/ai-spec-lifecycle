---
title: Spec lifecycle manager skill design
doc_type: spec
status: archived
owner: platform
last_reviewed: 2026-06-01
---

# Design

## Overview

The implementation will create a Codex skill named `spec-lifecycle-manager`. The skill will provide concise workflow instructions and refer to repository-local durable docs when present. It should not embed large examples or product-specific AWS data lake details.

The skill's behavior is organized around five phases:

1. Intake: locate repo instructions, docs structure, and active spec package.
2. Reconcile: compare spec, durable docs, code, tests, and config when useful.
3. Implement: select and complete a coherent task slice.
4. Promote: route accepted spec content into durable documentation.
5. Close: verify durable truth exists outside the spec and retire the active package.

## Components And Changes

| Component | Change required |
| --- | --- |
| Skill metadata | Define clear trigger terms for implementing, continuing, reconciling, promoting, reviewing, or closing spec packages. |
| `SKILL.md` workflow | Capture the five-phase lifecycle, `[###-slug]` default, reconciliation rules, task completion rules, promotion rules, expert review guidance, and closure criteria. |
| Supporting references | Include detailed document-routing and expert-review guidance as optional skill references so the local skill remains usable outside this repository. Keep validation targets in archived implementation evidence, not in the reusable skill package. |
| `agents/openai.yaml` | Include recommended UI metadata for the local skill. This is not required for runtime behavior, but keeps the skill discoverable and consistent with Codex skill conventions. |
| Validation fixtures or examples | Validate against one mature documentation repository and one smaller agent-runtime repository to test usefulness and portability without overloading context. |
| Repository skill source | Track the canonical skill package under `skills/spec-lifecycle-manager/`. |
| Local installation | Install a working copy as a personal local Codex skill in the user's Codex environment. |

## Data And Contract Impact

The skill does not change product runtime contracts. It defines process contracts for agent behavior:

- active specs default to `docs/specs/[###-slug]/`;
- specs are temporary;
- durable docs become final current-state truth;
- task completion must record validation or alternate verification;
- expert review roles are role-based and domain-neutral.

## Operational Considerations

The skill should be useful in repositories with different documentation layouts. It must instruct agents to inspect local documentation and AGENTS.md before applying default folder assumptions.

The skill should also avoid forcing heavyweight reconciliation for trivial work. Reconciliation is required when stale, resumed, partial, cross-cutting, or contract-affecting work is present; otherwise it may be brief.

The canonical implementation target is:

```text
skills/spec-lifecycle-manager/
```

The install target is the local Codex skills directory:

```text
$CODEX_HOME/skills/spec-lifecycle-manager/
```

If `$CODEX_HOME` is not set, use:

```text
~/.codex/skills/spec-lifecycle-manager/
```

The target repository skill structure is:

```text
skills/spec-lifecycle-manager/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
`-- references/
    `-- document-routing-and-expert-review.md
```

`SKILL.md` should contain only the essential workflow and tell the agent when
to read the reference files. The reference files should carry the larger
document-routing and expert-review tables.

## Open Questions

- None for packaging. Phase 3 may still revise exact wording while drafting the skill.
