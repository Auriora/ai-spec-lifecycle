---
title: Spec lifecycle manager skill validation evidence
doc_type: review
status: archived
owner: platform
last_reviewed: 2026-06-01
---

# Validation Evidence

## Summary

Phase 4 validation used sub-agents to apply the installed
`spec-lifecycle-manager` skill to the two identified target repositories and to
synthetic lifecycle scenarios in this repository. The skill is available in this
session as `spec-lifecycle-manager`, and sub-agents received it as an attached
skill item during validation.

Validation result: pass with follow-up wording improvements. The skill produced
useful guidance for active spec detection, reconciliation, coherent task
selection, durable documentation promotion, expert review roles, and closure
blockers. The validation did not modify either target repository.

## Validation Targets

| Target | Result | Evidence source |
| --- | --- | --- |
| Mature documentation repository | Pass with notes | Read-only sub-agent validation against mature docs and multiple active specs. |
| Smaller agent-runtime repository | Pass with notes | Read-only sub-agent validation against a single active runtime spec. |
| Local synthetic checks | Pass with notes | Read-only sub-agent validation against the installed skill, references, and this spec package. |

## Mature Documentation Repository Evidence

The validation found multiple candidate spec packages under `docs/specs/`.
`docs/README.md` identifies active implementation or stabilization packages,
while `docs/specs/implementation-sequencing.md` expands the active platform set
and gives dependency order. The skill correctly needs to avoid choosing the
highest numbered package by default; it should select by user goal or by the
first blocking slice in sequencing guidance.

Repository-specific instructions and durable docs were identified:

- `AGENTS.md` defines repo scripts, validation expectations, containerized
  deployment checks, and configuration-family conventions.
- `docs/README.md` maps durable doc classes including architecture,
  requirements, design, API contracts, data-flow docs, runbooks, ADRs,
  references, backlog, and reviews.
- `docs/templates/README.md` reinforces that current-state content belongs in
  durable docs rather than active specs.

Reconciliation was required because the repository has multiple active specs,
checked and unchecked tasks, cross-spec dependencies, and frontmatter/status
signals that do not fully describe implementation state.

Sample drift classifications from the validation:

- `implemented but unverified`: spec `044` has many completed phases, but a
  manual backfill lock-conflict verification task remains open.
- `code incomplete`: spec `044` still has open dispatch/runtime execution work.
- `decision unresolved`: spec `042` has source-owner and business semantics
  decisions still open.
- `intentionally deferred`: spec `043` defers production coverage audit until
  deployment, replay, or backfill creates new curated outputs.
- `durable docs stale`: completed spec content must be promoted before closure;
  the repository already documents this pattern for closed packages.

The next coherent slice identified by the validation was spec `044` Phase 5,
especially dispatching queued refresh requests through the correct runtime and
adding PostgreSQL, failure, and correlation tests. Durable promotion targets
included analytics ETL configuration docs, curated-to-processed data-flow docs,
processed refresh docs, analytics processing placement references, and
deployment/runbook docs.

Relevant expert review roles were data and integration architecture, API and
contract, operations/SRE, security/compliance, QA/test strategy, documentation
architecture, and software architecture. Repository-specific stakeholder labels
also exist in its review matrix, but the skill's generic role-based routing
still mapped cleanly.

Closure blockers were correctly identified for specs `044`, `023`, and `038`:
open implementation tasks, unverified runtime behavior, incomplete durable docs,
and active index/sequencing references.

## Smaller Agent-Runtime Repository Evidence

The validation found a single active package:
`docs/specs/001-agent-ide-runtime/`, with the expected `spec.md`, `plan.md`,
`design.md`, `research.md`, `quickstart.md`, and `tasks.md` artifacts.

Repository-specific instructions and durable docs were identified:

- `AGENTS.md` defines TypeScript source and Vitest test locations, current docs
  under `docs/design/`, MVP spec package guidance, `.cache/` exclusion, and
  rules for preserving draft, accepted, and open-question distinctions.
- `docs/reference/documentation-map.md` maps durable docs.
- Durable promotion targets include runtime requirements, system architecture,
  runtime contracts, MVP proof matrix, MCP surface design, runtime operations
  design, observability/debugging design, coding-agent integration design, and
  native dependency runbooks.

Reconciliation was required because the active package is partially completed
and some task state appears stale relative to code and tests.

Sample drift classifications from the validation:

- `spec stale`: unchecked context-tool tasks appear implemented in
  `src/application/use-cases/get-task-context.ts` and covered by MCP tests.
- `implemented but unverified`: runtime operation pieces have tests, but broader
  warm-up, degraded, and concurrency tasks remain unchecked.
- `code incomplete`: several `T204` runtime operations tasks remain open.
- `durable docs stale`: runtime requirements evidence still has placeholder
  sections despite implementation and tests.
- `intentionally deferred`: broader post-MVP semantic/runtime features are
  explicitly deferred in the task list.

The validation recommended a reconciliation/verification slice first: verify
the apparently implemented context tasks against code and tests, then update
task state if validation passes. The next implementation slice after that is
the `T204` runtime operations proof work because it gates MVP closure.

Relevant expert review roles were developer process expert, software architect,
QA/test strategy expert, operations/SRE expert, documentation architect, and API
and contract expert.

Closure blockers were correctly identified: many unchecked tasks remain,
durable requirements evidence is incomplete, and proof matrix acceptance gates
still need fixture-backed evidence.

## Fresh Small Spec Check

Result: pass with notes.

The skill explicitly allows fresh, small, low-risk work to keep reconciliation
brief and proceed. This satisfies the requirement to avoid unnecessary ceremony.
The validation noted one improvement: fresh spec creation guidance is implied by
the skill metadata but could be made more explicit in `SKILL.md`.

## Partially Completed Stale Spec Check

Result: pass.

The skill requires reconciliation when resuming existing or partially completed
specs, when tasks are already checked, when evidence is old or partial, when
code or docs changed outside the task list, or when durable docs disagree with
the spec. It also provides the required drift classifications:

- `spec stale`
- `code incomplete`
- `durable docs stale`
- `decision unresolved`
- `implemented but unverified`
- `intentionally deferred`

## Durable Doc Routing And Expert Review Check

Result: pass.

The skill routes accepted spec content into durable docs before closure and
links to `references/document-routing-and-expert-review.md` for detailed routing
and review roles. The reference covers durable doc classes, spec-to-doc routing,
expert roles, document-class review matrices, whole-package review, and review
evidence fields.

## Skill Availability Check

Result: pass.

The installed package exists at:

```text
~/.codex/skills/spec-lifecycle-manager/
```

`SKILL.md` is readable, the skill is listed in this session, and the installed
package contains `agents/openai.yaml`. Sub-agents used the skill through
attached skill items during the Phase 4 validation runs. The canonical source is
now tracked in this repository at `skills/spec-lifecycle-manager/`; the
`~/.codex` copy is an installed artifact.

## Residual Risks And Follow-Up

Validation found useful wording improvements, but no blocker to local use:

- Add explicit handling for multiple active specs: read `docs/README.md` and
  sequencing docs, then ask the user to choose or select the first blocking
  slice from sequencing guidance.
- Add guidance not to trust frontmatter status alone; reconcile status against
  docs indexes, sequencing docs, and task state.
- Add explicit guidance to compare checked and unchecked tasks against actual
  code/tests before choosing the next slice.
- Add a validation output field for task-state stale candidates.
- Add guidance to inspect durable docs' evidence sections, not only prose.
- Add a reminder that closure may require removing or demoting active-index
  references to completed specs.
- Make fresh-spec creation guidance explicit and state that a one- or two-line
  reconciliation is enough for fresh, small, low-risk work with no conflicting
  evidence.

Follow-up status: implemented in the installed skill after Phase 4 closure.
The tracked and installed `SKILL.md` copies now cover multiple active specs,
frontmatter/status reconciliation, task-state stale candidates, durable-doc
evidence sections, fresh-spec lightweight creation, and active-index cleanup.
The reusable skill package intentionally does not include the implementation
validation target repositories; those remain only in this archived validation
evidence.

## Spec Kit Investigation - 2026-06-02

### Investigation Source

The user requested investigation of GitHub Spec Kit to identify improvements to
the `spec-lifecycle-manager` skill:

```text
https://github.com/github/spec-kit
```

Sources reviewed:

- GitHub repository README and release metadata for `github/spec-kit`.
- Spec Kit documentation site at `https://github.github.io/spec-kit/`.
- Current command templates from the repository for `specify`, `clarify`,
  `plan`, `tasks`, `analyze`, and `implement`.
- Spec Kit reference pages for integrations, extensions, and presets.

Observed version context: GitHub showed latest release `0.9.0` on
2026-06-01. This evidence was captured on 2026-06-02.

### Findings

Spec Kit's current core workflow is broader than a simple
`spec -> plan -> tasks -> implement` sequence. The observed flow includes:

```text
constitution -> specify -> clarify -> plan -> tasks -> analyze -> implement
```

Spec Kit creates and uses `.specify/` project state, including constitution
memory, templates, scripts, extension configuration, and active feature
metadata. Its default feature package path is `specs/[###-slug]/`, while this
repository's lifecycle skill intentionally defaults to
`docs/specs/[###-slug]/`.

Spec Kit supports additional artifacts beyond this skill's baseline package:

- `checklists/` for requirements and quality gates;
- `data-model.md` for entities, fields, relationships, validation rules, and
  state transitions;
- `contracts/` for public API, CLI, UI, grammar, or service contracts;
- `.specify/memory/constitution.md` for governing principles;
- `.specify/extensions.yml` for before/after command hooks;
- `.specify/templates/overrides/`, presets, and extensions for workflow
  customization.

Spec Kit's `clarify` workflow asks targeted questions before planning and
writes accepted answers back into the spec. Its `analyze` workflow performs a
read-only consistency pass across `spec.md`, `plan.md`, and `tasks.md`,
checking ambiguity, duplication, coverage gaps, unmapped tasks, and conflicts
with the project constitution. Its `implement` workflow checks checklist status
before implementation, loads available design artifacts, respects task
dependencies, and marks tasks complete as work is verified.

Spec Kit task generation uses a strict checklist format:

```text
- [ ] T001 [P] [US1] Description with exact file path
```

Tasks are organized by independently testable user stories, with setup,
foundational prerequisites, story phases, and polish or cross-cutting work.

Spec Kit can be adapted through presets or extensions. Presets are best for
template, terminology, and command override changes. Extensions are best for
new capabilities, domain-specific commands, external integrations, quality
gates, and additional workflow phases.

### Suggestions Reviewed With User

The investigation produced eight suggested improvements. The user responded to
each numbered item on 2026-06-02:

| # | Suggestion | User response | Interpretation |
| --- | --- | --- | --- |
| 1 | Add Spec Kit project detection for `.specify/feature.json`, `.specify/memory/constitution.md`, and default `specs/[###-slug]/` packages. | No | Do not broaden this skill's default package detection to Spec Kit's `specs/` path or active-feature metadata. Keep `docs/specs/[###-slug]/` as the only default assumed path. |
| 2 | Add a "Spec Kit Compatibility" section that uses Spec Kit artifacts first when `.specify/` exists, then applies durable-doc promotion and closure rules. | Maybe | Treat as undecided. Do not implement without a later explicit request. |
| 3 | Expand artifact intake to include `data-model.md`, `contracts/`, `checklists/`, `.specify/extensions.yml`, template overrides, and constitution memory. | Expand on this | Needs a more detailed proposal before implementation. The most useful subset for this skill is likely `data-model.md`, `contracts/`, `checklists/`, and a repository governance file when present; extension hooks and template override resolution may be too Spec Kit-specific for the generic skill. |
| 4 | Add clarification and checklist gates. | Yes | Accepted. Add guidance to ask high-impact clarification questions before planning when the spec is materially underspecified, and inspect checklist status before implementation or closure when checklists exist. |
| 5 | Add read-only cross-artifact analysis after `tasks.md`. | Yes | Accepted. Add a read-only analysis/reconciliation step across spec, design, plan, tasks, durable docs, code evidence, validation evidence, and governance constraints before implementation. |
| 6 | Tighten task rules to require Spec Kit's exact task format. | No | Do not require Spec Kit's exact task syntax. The skill should continue accepting repository task formats while encouraging stable IDs, file paths, requirement/story mapping, dependency order, and independently verifiable slices. |
| 7 | Treat constitution or equivalent governance as authoritative. | Yes | Accepted. If a repository has constitution, AGENTS, documented principles, policy, or governance files, treat conflicts with those sources as blockers unless the user explicitly asks to update that governance source. |
| 8 | Consider publishing this as a Spec Kit extension or preset. | No | Do not pursue Spec Kit extension or preset packaging. Keep this as a Codex skill. |

### Recommended Follow-Up Scope

Based on the user's responses, the next skill improvement pass should focus on
three accepted areas:

1. Clarification and checklist gates.
2. Read-only cross-artifact analysis.
3. Governance-authority handling.

The expanded artifact-intake idea needs a narrower design before editing the
skill. A pragmatic proposal is:

- Always keep `docs/specs/[###-slug]/` as the default active package path.
- When present inside the active package, also read `data-model.md`,
  `contracts/`, `checklists/`, and any clearly named governance or decision
  files.
- Treat `data-model.md` as durable-data and state-transition evidence.
- Treat `contracts/` as API, CLI, UI, integration, schema, grammar, or public
  behavior evidence.
- Treat `checklists/` as readiness and quality-gate evidence, not as
  implementation proof by itself.
- Treat repository governance files as higher-priority constraints during
  reconciliation.
- Avoid implementing Spec Kit-specific hook dispatch, preset resolution,
  `.specify/feature.json` active-feature detection, or extension/preset
  packaging unless the user later changes the decisions above.

### Potential Skill Wording Changes

The accepted follow-up could be reflected in `SKILL.md` with these concise
additions:

- In `Start`: read package-local `data-model.md`, `contracts/`,
  `checklists/`, governance files, and decision records when present.
- In `Reconcile`: perform read-only cross-artifact analysis for ambiguity,
  duplication, coverage gaps, unmapped tasks, stale task state, and governance
  conflicts before implementation.
- In `Implement`: if checklists exist, summarize complete and incomplete items
  before editing; ask or stop when an incomplete checklist blocks the selected
  slice.
- In `Close`: closure cannot proceed while required checklist, governance,
  contract, durable-doc, or validation evidence remains incomplete.

## Closure Recommendation

Phase 4 is complete. The skill is validated enough for local use, with
non-blocking wording improvements recorded above. This implementation spec can
be retained with `status: archived` as validation and decision history; durable
current-state guidance now lives in `docs/design/`, `docs/reference/`,
`docs/README.md`, and the tracked skill source under
`skills/spec-lifecycle-manager/`.
