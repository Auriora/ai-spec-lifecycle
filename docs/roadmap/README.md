---
title: Agent development lifecycle roadmap
doc_type: roadmap
status: active
owner: platform
last_reviewed: 2026-06-11
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
| R005 | delivered | done | Commit sync guard | B016, MCP-first installed skill workflow | Runtime `sync-guard` detects source/bundled plugin drift, installed cache drift, running MCP reload advisories, and recent skill-changing commits that lack package or install evidence. | platform | `docs/backlog/README.md`, `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `docs/reference/spec-lifecycle-manager-mcp-install.md` |
| R006 | now | active | Validation plan builder | B023, active spec `019-validation-plan-builder` | Runtime and MCP can return a focused read-only validation plan from changed files, task context, risk level, and durable-doc impact. | platform | `docs/specs/019-validation-plan-builder/` |
| R007 | next | active | Evidence quality check | B012, R006, active spec `020-evidence-quality-check` | Completed task and verification evidence can be classified as concrete, vague, missing, stale, or unverifiable with deterministic references. | platform | `docs/specs/020-evidence-quality-check/` |
| R008 | next | active | Closure risk review | B008, R006, R007, active spec `021-closure-risk-review` | Closure readiness can incorporate validation-plan and evidence-quality signals before a package is removed. | platform | `docs/specs/021-closure-risk-review/` |
| R009 | next | active | npm publish and release workflow | B044, B026, active spec `022-npm-publish-release-workflow` | GitHub Actions validates, packages, and gates npm publish/release artifacts with documented rollback and install verification. | platform | `docs/specs/022-npm-publish-release-workflow/` |

## Decision History

| Date | Decision | Impact | Evidence |
|------|----------|--------|----------|
| 2026-06-06 | Create a durable roadmap before opening new lifecycle work. | Gives future agents an explicit sequencing surface instead of inferring priorities from archived specs. | `docs/backlog/README.md`, archive index entry `011-spec-archive-index-runtime` |
| 2026-06-06 | Promote spec archive index work before blocking hook promotion. | Archive/index support reduces closure ambiguity and gives hooks/runtime a stronger evidence surface. | B003, R001 |
| 2026-06-06 | Complete archive index runtime before considering blocking hooks. | R001 is complete; R002 remains deferred until advisory hook noise is reviewed. | Archive index entry `011-spec-archive-index-runtime`, closure log |
| 2026-06-06 | Adopt selected coding-agent operating-model rules into governance. | R003 is complete; flexible workflow mechanics remain design guidance. | `docs/governance/constitution.md`, `docs/design/coding-agent-operating-model.md` |
| 2026-06-06 | Keep lifecycle hooks advisory-only. | R002 is complete as a no-promotion decision; future blocking hooks require a new focused spec and explicit approval. | `docs/reference/spec-lifecycle-dogfood-evaluation.md` |
| 2026-06-06 | Make commit sync guard the next lifecycle hardening horizon. | B007, B017, and B018 are delivered by the runtime/MCP surface; B016 is the highest-priority open friction item. | `docs/backlog/README.md`, R005 |
| 2026-06-11 | Promote validation and release-readiness work after specs 017 and 018 closed. | R006-R009 sequence validation planning, evidence quality, closure risk, and npm publish/release workflow specs. | `docs/backlog/README.md`, active specs 019-022 |

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
