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
| R001 | now | complete | Spec archive index and closure-log runtime support | B003, archive index entry `011-spec-archive-index-runtime` | Runtime can validate closure index entries and removed or explicitly retained spec cleanup decisions. | platform | `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md` |
| R002 | next | complete | Lifecycle hooks remain advisory-only | Advisory hook dogfood evidence, R001 | Decision recorded to keep hooks advisory; any future blocking behavior requires a new focused spec and explicit approval. | platform | `docs/reference/spec-lifecycle-dogfood-evaluation.md` |
| R003 | later | complete | Coding agent operating model governance adoption | Repeated model use, review evidence | Governance update accepted or explicitly rejected after operating model dogfood. | platform | `docs/governance/constitution.md`, archive index entry `012-operating-model-governance-adoption` |
| R004 | later | superseded | Archived spec audit report | Default archived scan behavior, B006 | Superseded by removal-by-default policy for completed specs. | platform | `docs/backlog/README.md` |
| R005 | next | planned | Commit sync guard | B016, MCP-first installed skill workflow | Source and installed skill/plugin drift is detectable after commits that touch `skills/spec-lifecycle-manager/`, and agents report whether `~/.codex` is current before claiming lifecycle packaging work is complete. | platform | `docs/backlog/README.md`, `scripts/install-spec-lifecycle-manager-package.sh` |

## Decision History

| Date | Decision | Impact | Evidence |
|------|----------|--------|----------|
| 2026-06-06 | Create a durable roadmap before opening new lifecycle work. | Gives future agents an explicit sequencing surface instead of inferring priorities from archived specs. | `docs/backlog/README.md`, archive index entry `011-spec-archive-index-runtime` |
| 2026-06-06 | Promote spec archive index work before blocking hook promotion. | Archive/index support reduces closure ambiguity and gives hooks/runtime a stronger evidence surface. | B003, R001 |
| 2026-06-06 | Complete archive index runtime before considering blocking hooks. | R001 is complete; R002 remains deferred until advisory hook noise is reviewed. | Archive index entry `011-spec-archive-index-runtime`, closure log |
| 2026-06-06 | Adopt selected coding-agent operating-model rules into governance. | R003 is complete; flexible workflow mechanics remain design guidance. | `docs/governance/constitution.md`, `docs/design/coding-agent-operating-model.md` |
| 2026-06-06 | Keep lifecycle hooks advisory-only. | R002 is complete as a no-promotion decision; future blocking hooks require a new focused spec and explicit approval. | `docs/reference/spec-lifecycle-dogfood-evaluation.md` |
| 2026-06-06 | Make commit sync guard the next lifecycle hardening horizon. | B007, B017, and B018 are delivered by the runtime/MCP surface; B016 is the highest-priority open friction item. | `docs/backlog/README.md`, R005 |

## Routing Rules

- Use active specs for implementation-ready work with acceptance criteria.
- Use backlog for candidate or deferred work that needs more scope.
- Use this roadmap when work affects sequencing, adoption, or multi-spec
  dependencies.
- Keep completed delivery evidence in durable docs, the closure log, and the
  archive index. Removed package paths are historical evidence, not active
  navigation targets.

## Related Artifacts

- Backlog: [../backlog/README.md](../backlog/README.md)
- Spec archive index: [../history/spec-archive-index.md](../history/spec-archive-index.md)
- Closure log: [../history/spec-closure-log.md](../history/spec-closure-log.md)
