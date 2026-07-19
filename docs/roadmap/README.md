---
title: Agent development lifecycle roadmap
doc_type: roadmap
status: active
owner: platform
last_reviewed: 2026-07-19
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
| R006 | delivered | done | Validation plan builder | B023, archive index entry `019-validation-plan-builder` | Runtime and MCP can return a focused read-only validation plan from changed files, task context, risk level, and durable-doc impact. | platform | `docs/history/spec-archive-index.md`, `docs/history/spec-closure-log.md` |
| R007 | delivered | done | Evidence quality check | B012, R006, archive index entry `020-evidence-quality-check` | Completed task and verification evidence can be classified as concrete, vague, missing, waived, deferred, not-applicable, not-run, or weak with deterministic references. | platform | `docs/history/spec-archive-index.md`, `docs/history/spec-closure-log.md` |
| R008 | delivered | done | Closure risk review | B008, R006, R007, archive index entry `021-closure-risk-review` | Closure readiness incorporates validation-plan, evidence-quality, live-doc risk, and recovery signals before a package is removed. | platform | `docs/history/spec-archive-index.md`, `docs/history/spec-closure-log.md` |
| R009 | delivered | done | npm publish and release workflow | B044, B026, archive index entry `022-npm-publish-release-workflow` | GitHub Actions validates, packages, and gates npm publish/release artifacts with documented rollback and install verification. | platform | `docs/history/spec-archive-index.md`, `docs/history/spec-closure-log.md` |
| R010 | delivered | done | Task state and implementation-readiness tools | B037, B038, archive index entry `023-task-state-management-tools` | Runtime and MCP can identify stale-open tasks, plan-only completion, blocked-output completion, broad-task splits, and required task context before implementation. | platform | `docs/history/spec-archive-index.md`, `docs/history/spec-closure-log.md` |
| R011 | delivered | done | Guided documentation wizard | B049, archive index entry `026-guided-documentation-wizard` | Prompt-only wizard guides stage-specific questions, open-question routing, feedback dispositions, preview-first edit plans, and closure awareness by composing existing lifecycle surfaces. | platform | `docs/history/spec-archive-index.md`, `docs/history/spec-closure-log.md` |
| R012 | delivered | done | Lifecycle phase gate check | B031, Spec 033 implementation evidence | MCP and retained CLI report eight-phase readiness, conservative blockers, bounded expansion, artifact freshness, and adapter provenance without replacing authoritative source tools. | platform | `docs/design/spec-lifecycle-management.md`, `docs/reference/spec-lifecycle-runtime.md` |
| R013 | delivered | done | Provisional spec ID allocation and creation planning | B061, Spec 035 implementation evidence | Agents obtain docs-root-scoped next numbers and safe preview plans through MCP/orientation without manual arithmetic or false reservation claims. | platform | `docs/design/spec-lifecycle-management.md`, `docs/reference/spec-lifecycle-runtime.md` |
| R014 | delivered | done | Lifecycle adoption workflow | B014, B015, B064; Spec 038 delivery evidence; existing task-context, evidence-quality, promotion, capability, and advisory-hook surfaces | Delivered the declarative MCP-first start prompt, evidence-before-promotion routing, a 69.2% smaller source skill entrypoint, bounded client observation, narrow advisory hooks, quiet removed-cache behavior, repository-local source development, packaged-only user deployment, and qualified dogfood promotion without importing analyser contracts. | platform | `docs/design/spec-lifecycle-management.md`, `docs/reference/spec-lifecycle-runtime.md`, `docs/reference/spec-lifecycle-dogfood-evaluation.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md` |

## Decision History

| Date | Decision | Impact | Evidence |
|------|----------|--------|----------|
| 2026-06-06 | Create a durable roadmap before opening new lifecycle work. | Gives future agents an explicit sequencing surface instead of inferring priorities from archived specs. | `docs/backlog/README.md`, archive index entry `011-spec-archive-index-runtime` |
| 2026-06-06 | Promote spec archive index work before blocking hook promotion. | Archive/index support reduces closure ambiguity and gives hooks/runtime a stronger evidence surface. | B003, R001 |
| 2026-06-06 | Complete archive index runtime before considering blocking hooks. | R001 is complete; R002 remains deferred until advisory hook noise is reviewed. | Archive index entry `011-spec-archive-index-runtime`, closure log |
| 2026-06-06 | Adopt selected coding-agent operating-model rules into governance. | R003 is complete; flexible workflow mechanics remain design guidance. | `docs/governance/constitution.md`, `docs/design/coding-agent-operating-model.md` |
| 2026-06-06 | Keep lifecycle hooks advisory-only. | R002 is complete as a no-promotion decision; future blocking hooks require a new focused spec and explicit approval. | `docs/reference/spec-lifecycle-dogfood-evaluation.md` |
| 2026-06-06 | Make commit sync guard the next lifecycle hardening horizon. | B007, B017, and B018 are delivered by the runtime/MCP surface; B016 is the highest-priority open friction item. | `docs/backlog/README.md`, R005 |
| 2026-06-11 | Promote validation and release-readiness work after specs 017 and 018 closed. | R006-R009 sequence validation planning, evidence quality, closure risk, and npm publish/release workflow specs. | `docs/backlog/README.md`, archive entries for 019, 020, 021, 022, and 023 |
| 2026-06-13 | Prioritize runtime packets that reduce implementation loops before conversation-history mining. | Validation planning, task-state audit, evidence quality, closure risk, and staged preflight address observed agent inefficiency more directly than another history scan. | `docs/backlog/README.md`, archive entries for 019, 020, 021, and 023, active specs 022 and 024 |
| 2026-06-13 | Treat misleading live documentation as higher risk than Git-history recoverability. | Closure risk must prefer removing or marking misleading live documents before cleanup. Git history and archive indexes provide recovery for removed package detail. | Archive index entry `021-closure-risk-review` |
| 2026-07-12 | Separate business priority from dependency build order for Specs 033-036. | Spec 034 remains the P1 friction item, but its guarded writer follows the read-only gate contract. Spec 036's minimum envelope design must be accepted before Specs 033 and 035 freeze public response schemas. | B031, B050, B061, B062; active Specs 033-036 |
| 2026-07-12 | Mark the read-only phase-gate dependency delivered. | Spec 033's MCP/CLI gate and the minimum Spec 036 envelope slice are shipped. Specs 035 and 036 remain active; this does not claim their broader work complete. | B031, Specs 033, 035, and 036 |
| 2026-07-12 | Deliver runtime-owned provisional spec numbering. | Spec 035 removes agent-side arithmetic while preserving multi-root confidence, stale-plan detection, and the future atomic-writer boundary. | B061, R013 |

## Suggested Build Sequence

1. Continue `034-phase-completion-helper` now that the read-only Spec 033 gate
   contract is stable, so guarded completion writes consume accepted gate
   semantics rather than defining a competing readiness model.

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
