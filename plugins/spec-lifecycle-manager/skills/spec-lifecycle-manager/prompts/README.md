---
title: Spec lifecycle MCP prompt definitions
doc_type: reference
status: draft
owner: platform
last_reviewed: 2026-07-18
---

# Prompt Definitions

These JSON files define MCP prompt contracts for spec lifecycle workflows.
They are declarative so a future MCP adapter can expose them through
`prompts/list` and `prompts/get` without duplicating prompt policy.

Prompts are convenience entry points. The `spec-lifecycle-manager` skill remains
the authoritative workflow guide, and the deterministic runtime helpers remain
the source for scanner, lint, next-task, closure, and traceability payloads.

Implemented prompt definitions:

- `choose-next-task`
- `developer-start`
- `documentation-wizard`
- `implementation-start`
- `lifecycle-complete`
- `lifecycle-status`
- `lifecycle-triage`
- `lifecycle-validate`
- `lint-spec`
- `reconcile-spec`
- `task-context`
