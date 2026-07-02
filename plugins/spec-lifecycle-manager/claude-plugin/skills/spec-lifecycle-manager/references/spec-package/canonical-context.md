---
title: Canonical context
doc_type: spec
artifact_type: canonical-context
status: draft
owner: platform
last_reviewed: YYYY-MM-DD
---

# Canonical Context

## Purpose

State why this package needs explicit working-context authority. Use this
artifact when the spec imports or adapts durable docs, has broad durable-doc
impact, names stale-doc risk, or resumes work where older docs could be
mistaken for implementation authority.

## Authority Hierarchy

The spec-local context is canonical only for this active implementation slice.
It does not override system, developer, or user instructions, applicable
`AGENTS.md`, governance, policy, security, privacy or compliance rules,
generated contracts, source-code contracts, tests, or live/system evidence.

## Always-Canonical External Sources

| Source | Authority reason | Handling |
|--------|------------------|----------|
| `AGENTS.md` | Repository instructions | Read before changing governed paths. |
| `docs/governance/constitution.md` | Governance policy | Stop for a decision if this spec conflicts with it. |
| source code, tests, generated contracts, or live evidence | Implementation truth | Treat conflicts as reconciliation inputs, not spec override. |

## Spec-Canonical Working Sources

| Source | Role | Scope | Notes |
|--------|------|-------|-------|
| `requirements.md` | accepted intent | this spec | Replace with package-specific scope. |
| `design.md` | implementation approach | this spec | Replace with package-specific scope. |
| `tasks.md` | execution index | this spec | Do not implement from tasks alone. |

## Imported Sources

| Spec path | Source path | Source revision or date | Status | Canonical scope | Promotion target |
|-----------|-------------|-------------------------|--------|-----------------|------------------|
| `canonical-context.md` | `docs/path.md` | YYYY-MM-DD or commit | copied/adapted/summarized/background/supersedes | scope of authority | `docs/path.md` or route |

Status values:

- `copied`: content copied verbatim or near-verbatim.
- `adapted`: content edited for the active spec.
- `summarized`: content summarized rather than copied.
- `background`: context only, not canonical.
- `supersedes`: spec-local content supersedes the named durable source for the
  active slice.

## Non-Canonical Background Sources

| Source | Reason non-canonical | Handling |
|--------|----------------------|----------|
| `docs/old-or-stale.md` | stale, historical, or not imported for this slice | Use only as background or drift evidence. |

## Promotion Map

| Spec-local content | Durable destination or route | Required before closure |
|--------------------|------------------------------|-------------------------|
| accepted canonical context | `docs/path.md`, backlog, roadmap, follow-up spec, or discard rationale | yes/no |

## Related Artifacts

- Requirements: `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Change impact: `change-impact.md`
- Verification: `verification.md`
