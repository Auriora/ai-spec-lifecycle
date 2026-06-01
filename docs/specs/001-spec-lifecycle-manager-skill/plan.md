---
title: Spec lifecycle manager skill implementation plan
doc_type: spec
status: archived
owner: platform
last_reviewed: 2026-06-01
---

# Implementation Plan

## Summary

Implement a reusable Codex skill that manages temporary implementation specs and durable documentation consistency. The skill will be generic across repositories, with `docs/specs/[###-slug]/` as the default active spec convention.

## Technical Context

- **Language/Version**: Markdown skill instructions; optional shell or Python validation helpers only if needed.
- **Primary Dependencies**: Codex skill format.
- **Storage**: Local Codex skill directory and repository docs.
- **Testing**: Manual validation against one mature documentation repository and one smaller agent-runtime repository; optional scripted checks for skill files.
- **Target Platform**: Codex local skills.
- **Project Type**: Agent workflow/process tooling.
- **Performance Goals**: Skill body remains concise enough for normal Codex context use.
- **Constraints**: Must not encode product-specific subject-matter assumptions.
- **Scale/Scope**: One reusable skill plus supporting docs.

## Governance Check

Final archived result:

- [x] SOLID boundaries defined: lifecycle workflow, review matrix, and repository-specific instructions remain separate.
- [x] DRY plan defined: detailed routing tables live in supporting docs or references, not duplicated throughout the skill.
- [x] Test strategy defined: validation prompts and target repositories verified the skill's behavior.
- [x] UX consistency impact assessed: skill instructions align with Codex skill conventions and repository AGENTS.md behavior.
- [x] Performance budgets defined: skill body stays concise; large routing and review tables remain in references.

## Project Structure

### Documentation

```text
docs/
|-- README.md
|-- design/
|   `-- spec-lifecycle-management.md
|-- reference/
|   `-- document-routing-and-expert-review-matrix.md
|-- specs/
|   `-- 001-spec-lifecycle-manager-skill/
|       |-- spec.md
|       |-- design.md
|       |-- plan.md
|       |-- tasks.md
|       `-- validation-evidence.md
`-- templates/
    |-- README.md
    `-- spec-package/
```

### Repository Skill Source

```text
skills/
`-- spec-lifecycle-manager/
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    `-- references/
        `-- document-routing-and-expert-review.md
```

### Skill

The repository-owned canonical skill source lives at:

```text
skills/spec-lifecycle-manager/
```

The skill can be installed as a personal local Codex skill:

```text
$CODEX_HOME/skills/spec-lifecycle-manager/SKILL.md
```

If `$CODEX_HOME` is unset, use:

```text
~/.codex/skills/spec-lifecycle-manager/SKILL.md
```

**Structure Decision**: Track the canonical skill package in this repository and install a working copy in the local Codex environment. Keep this repository's docs/spec package as the planning and traceability source for the implementation.

The skill package will contain:

```text
skills/spec-lifecycle-manager/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
`-- references/
    `-- document-routing-and-expert-review.md
```

Required runtime file:

- `SKILL.md`: metadata and concise operating workflow.

Supporting files:

- `references/document-routing-and-expert-review.md`: durable document routing, expert role matrix, whole-package review, and review evidence guidance.
- `agents/openai.yaml`: recommended UI metadata. This file is not required for skill execution but should be included for discoverability and consistency with Codex skill conventions.

## Phases

1. Finalize lifecycle and expert review docs.
2. Define local Codex skill files and optional references.
3. Draft `SKILL.md`.
4. Validate against representative mature and smaller repositories.
5. Revise, install, and document usage.

## Dependencies

- Codex skill file format.
- Representative mature and smaller repository spec packages for validation.

## Risks

- Skill becomes too verbose and consumes too much context.
- Skill over-applies process to small tasks.
- Expert review guidance becomes subject-matter-specific instead of role-based.
- Spec closure guidance accidentally removes useful history instead of promoting it.

## Validation Strategy

Validate the skill by applying it to both representative target repositories:

| Repository class | Validation purpose |
| --- | --- |
| Mature documentation repository | Mature documentation lifecycle with active specs, durable docs, data-flow/API/runbook/ADR promotion, and completed-spec closure behavior. |
| Smaller agent-runtime repository | Portability check against a different repository with an active `docs/specs/[###-slug]/` package, runtime docs, and local agent-development workflow. |

For each target, check whether the skill:

- locates the spec package;
- inspects repository-specific instructions;
- identifies durable doc inputs and outputs;
- produces a concise reconciliation summary when useful;
- selects a coherent implementation slice;
- gives correct task verification guidance;
- routes durable content to the right document classes;
- recommends relevant expert review roles;
- defines closure checks.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None currently identified | N/A | N/A |
