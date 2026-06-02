---
title: Spec lifecycle validation design
doc_type: design
status: draft
owner: platform
last_reviewed: 2026-06-02
---

# Technical Design

## Overview

Validation uses static checks, fixture repositories, sub-agent prompt trials,
and independent review passes. Evidence is recorded inside this active spec
package and can later be promoted into durable docs if the validation process
becomes standard.

## High-Level Design

### System Architecture

- Validation package: `docs/specs/002-spec-lifecycle-validation/`
- Fixture repositories: `tests/fixtures/skill-validation/`
- Skill under test: `.codex/skills/spec-lifecycle-manager/` for this session
  and `skills/spec-lifecycle-manager/` as canonical source.
- Evidence: `verification.md` plus `validation-evidence.md`.

### Components and Changes

- Spec package describes requirements, tasks, and evidence for validation.
- Fixture repos model scenario-specific documentation structures.
- Sub-agents run prompt trials and review passes independently.

### Data Models

Validation evidence is markdown tables keyed by scenario, prompt, expected
behavior, observed behavior, result, and follow-up.

### Data Flow

Fixture docs and skill references feed sub-agent prompt trials. Sub-agent
findings are summarized into `validation-evidence.md` and `verification.md`.

## Low-Level Design

### Algorithms and Logic

```text
create fixtures
run static checks
spawn prompt-trial agents
spawn review agents
collect findings
record evidence and follow-up
```

### Function Signatures and Interfaces

No runtime interfaces are introduced. The validation interface is the skill's
natural-language workflow.

### Error Handling

If a sub-agent cannot complete a prompt trial, record the failure, residual
risk, and whether a manual review substitutes for the trial.

## Operational Considerations

The updated skill remains local to this repository's `.codex/` path and should
not be copied into `~/.codex/skills/` during validation.

## Open Questions

- Whether future validation should be scripted after the workflow stabilizes.
- Whether fixture repos should remain committed or move to generated temporary
  fixtures later.

## Related Artifacts

- Requirements: requirements.md
- Change Impact:
- Tasks: tasks.md
- Verification: verification.md
