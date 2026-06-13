---
title: Feature change impact title
doc_type: spec
artifact_type: change-impact
status: draft
owner: team-or-person
last_reviewed: YYYY-MM-DD
---

# Change Impact

## Purpose

Describe how this feature, bug fix, refactor, migration, or operational change
alters durable behavior and which source-of-truth documents must be updated.

Use this file when the active spec changes existing behavior. Skip it for tiny
new work where `requirements.md` already captures the full durable impact.

## Durable Source Mapping

List the durable docs, contracts, code-derived references, schemas, runbooks, or
governance files that describe the current behavior before this change. Durable
docs should describe current accepted state unless explicitly labeled proposed,
planned, deferred, or historical.

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/path/to/doc.md` | Current behavior summary | high | |

If no durable source exists, record the gap and the promotion target that will
become the durable source after implementation.

## Change Type

- **Primary type:** feature | bug_fix | refactor | migration | operational | documentation | clarification
- **Breaking change:** no
- **Durable docs required:** yes
- **External behavior affected:** no

## Proposed Changes

| Change | Type | Source of truth | New durable destination | Promotion required |
|--------|------|-----------------|-------------------------|-------------------|
| Change summary | add\|modify\|remove\|rename\|bug_fix\|clarify | `docs/path/to/doc.md` | `docs/path/to/doc.md` | yes |

## Promotion Targets

List the durable documents that must be updated before closure.

| Spec content | Durable destination | Promotion status | Notes |
|--------------|---------------------|------------------|-------|
| Accepted requirement or design change | `docs/path/to/doc.md` | pending | |

## Unchanged Durable Areas

List relevant durable areas reviewed and intentionally left unchanged. This
prevents agents from assuming omission means no review occurred.

| Durable area | Reviewed source | Reason unchanged |
|--------------|-----------------|------------------|
| architecture | `docs/architecture/path.md` | No boundary or component changes. |

## Bug Fix Details

Use this section for bug fixes.

- **Observed behavior:**
- **Expected behavior:**
- **Root cause evidence:**
- **Regression risk:**
- **Durable doc update needed:**

## Open Questions

- Question

## Related Artifacts

- Requirements:
- Design:
- Tasks:
- Verification:
