---
title: Operating model governance adoption design
doc_type: spec
artifact_type: design
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Technical Design

## Overview

Adopt the coding-agent operating model into governance selectively. The
constitution should gain enforceable lifecycle principles. The operating-model
design remains the durable source for workflow levels, roles, metrics, and
dogfood observations.

## High-Level Design

### Governance Additions

Add constitution principles for:

- full spec context before implementation;
- risk and decision gates;
- bounded parallel agent work;
- evidence and durable promotion before completion/closure.

### Design Doc Update

Update `docs/design/coding-agent-operating-model.md` to record the adoption
decision and clarify that flexible model mechanics remain design guidance.

### Planning Updates

Mark B005 and R003 complete and record the decision history.

## Low-Level Design

### Constitution Patch

Insert concise sections under `## Principles`:

- `Spec Context Before Implementation`
- `Risk Gates Require Decisions`
- `Parallel Agent Work Is Bounded`

Reuse existing `Evidence Before Completion` and `Durable Docs Reflect Current
State` principles rather than duplicating them.

### Non-Adopted Guidance

Keep these out of governance:

- the exact workflow-level table;
- agent-role table;
- local metrics list;
- dogfood examples.

## Operational Considerations

- This is a docs/governance change only.
- Runtime behavior and hooks do not change.
- Governance takes precedence over design guidance after this change.

## Open Questions

- None. The user requested implementation of R003 governance adoption.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Tasks: [tasks.md](tasks.md)
- Governance: [../../governance/constitution.md](../../governance/constitution.md)
- Operating model: [../../design/coding-agent-operating-model.md](../../design/coding-agent-operating-model.md)
