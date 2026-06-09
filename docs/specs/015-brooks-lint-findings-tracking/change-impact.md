---
title: Brooks-Lint findings tracking change impact
doc_type: spec
artifact_type: change-impact
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Change Impact

## Durable Source Mapping

| Source | Proposed Change | Reason | Impact |
|--------|-----------------|--------|--------|
| `docs/reviews/brooks-lint/README.md` | Create durable Brooks findings register. | Preserve findings from Brooks skill runs. | New durable review artifact. |
| `.brooks-lint-history.json` | Document as optional supporting score-history evidence, not the durable finding source of truth. | Score history exists but may be environment-specific and does not preserve finding detail. | Governance decision recorded in D002. |
| `docs/backlog/README.md` | Add deferred Brooks findings that should survive spec closure. | Keep unresolved structural debt visible. | Backlog update if needed. |
| `docs/roadmap/README.md` | Add larger accepted remediation sequences if needed. | Avoid burying architectural work in one spec. | Roadmap update if needed. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Optional register validation if D001 accepts runtime support. | Enforce schema after repeated runs. | Runtime and tests update only if accepted. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Mirror optional runtime support into plugin. | Keep plugin self-contained. | Plugin update only if runtime support is accepted. |

## Proposed Changes

| Area | Proposed Change | Compatibility Notes |
|------|-----------------|---------------------|
| Durable register | Add `docs/reviews/brooks-lint/README.md` with seed findings and fixed fields. | Documentation-only and additive. |
| Triage workflow | Define accepted, deferred, dismissed, resolved, and needs-decision states. | Aligns with existing lifecycle tasks and backlog routing. |
| History relationship | Document how `.brooks-lint-history.json` relates to the durable register. | Score history can support trend interpretation, but the register must stand without it. |
| Optional validation | Consider runtime lint for register shape after the format stabilizes. | Deferred unless manual consistency proves insufficient. |

## Compatibility

- Initial implementation can be documentation-only.
- No third-party dependencies are expected.
- Runtime validation, if added later, must remain additive.
- Plugin packaging changes are required only if runtime behavior changes.

## Risks

| Risk | Mitigation |
|------|------------|
| Findings register becomes a stale debt list. | Require triage state and closure or promotion evidence. |
| Brooks score history and finding records diverge. | Document relationship and reconcile repeated runs through `last seen`. |
| Register becomes too heavy to maintain. | Start with Markdown and add validation only if needed. |
| Findings duplicate existing backlog items. | Link to backlog/roadmap rather than duplicating planned work. |

## Promotion Targets

- `docs/reviews/brooks-lint/README.md`
- `docs/backlog/README.md` for deferred findings.
- `docs/roadmap/README.md` for larger remediation sequences.
- `docs/history/spec-closure-log.md` and
  `docs/history/spec-archive-index.md` at closure.
