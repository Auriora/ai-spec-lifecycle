---
title: Agent development lifecycle roadmap
doc_type: roadmap
status: active
owner: platform
last_reviewed: 2026-06-06
---

# Roadmap

This roadmap sequences lifecycle work that spans multiple specs, backlog items,
or adoption stages. It is a planning view, not a changelog and not a substitute
for active implementation specs.

## Scope

- **Roadmap owner:** platform
- **Planning horizon:** near-term lifecycle hardening
- **Review cadence:** after each spec closure or when backlog priorities change
- **Backlog source:** `docs/backlog/README.md`
- **Decision authority:** user and platform maintainer

## Horizons

| ID | Horizon | Status | Outcome | Dependencies | Exit Criteria | Owner | Evidence |
|----|---------|--------|---------|--------------|---------------|-------|----------|
| R001 | now | complete | Spec archive index and closure-log runtime support | B003, `docs/specs/011-spec-archive-index-runtime/` | Runtime can validate closure index entries and removed or explicitly retained spec cleanup decisions. | platform | `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md` |
| R002 | next | complete | Lifecycle hooks remain advisory-only | Advisory hook dogfood evidence, R001 | Decision recorded to keep hooks advisory; any future blocking behavior requires a new focused spec and explicit approval. | platform | `docs/reference/spec-lifecycle-dogfood-evaluation.md` |
| R003 | later | complete | Coding agent operating model governance adoption | Repeated model use, review evidence | Governance update accepted or explicitly rejected after operating model dogfood. | platform | `docs/governance/constitution.md`, `docs/specs/012-operating-model-governance-adoption/` |
| R004 | later | superseded | Archived spec audit report | Default archived scan behavior, B006 | Superseded by removal-by-default policy for completed specs. | platform | `docs/backlog/README.md` |

## Decision History

| Date | Decision | Impact | Evidence |
|------|----------|--------|----------|
| 2026-06-06 | Create a durable roadmap before opening new lifecycle work. | Gives future agents an explicit sequencing surface instead of inferring priorities from archived specs. | `docs/backlog/README.md`, `docs/specs/011-spec-archive-index-runtime/` |
| 2026-06-06 | Promote spec archive index work before blocking hook promotion. | Archive/index support reduces closure ambiguity and gives hooks/runtime a stronger evidence surface. | B003, R001 |
| 2026-06-06 | Complete archive index runtime before considering blocking hooks. | R001 is complete; R002 remains deferred until advisory hook noise is reviewed. | `docs/specs/011-spec-archive-index-runtime/`, closure log |
| 2026-06-06 | Adopt selected coding-agent operating-model rules into governance. | R003 is complete; flexible workflow mechanics remain design guidance. | `docs/governance/constitution.md`, `docs/design/coding-agent-operating-model.md` |
| 2026-06-06 | Keep lifecycle hooks advisory-only. | R002 is complete as a no-promotion decision; future blocking hooks require a new focused spec and explicit approval. | `docs/reference/spec-lifecycle-dogfood-evaluation.md` |

## Routing Rules

- Use active specs for implementation-ready work with acceptance criteria.
- Use backlog for candidate or deferred work that needs more scope.
- Use this roadmap when work affects sequencing, adoption, or multi-spec
  dependencies.
- Keep completed delivery evidence in spec verification records and the closure
  log.

## Related Artifacts

- Backlog: [../backlog/README.md](../backlog/README.md)
- Active specs: [../specs/](../specs/)
- Closure log: [../history/spec-closure-log.md](../history/spec-closure-log.md)
