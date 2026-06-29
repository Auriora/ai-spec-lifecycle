---
title: Spec-local canonical context design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-19
---

# Technical Design

## Overview

Add a spec-local canonical context layer to the lifecycle model. The active spec
package remains temporary scaffolding, but while work is active it can declare
the working documents that agents must treat as canonical for the slice. This
narrows implementation context without giving specs authority over governance,
policy, security, `AGENTS.md`, generated contracts, source-code contracts, or
live/system evidence.

The first implementation should be documentation-and-runtime-guidance focused:
skill guidance, durable design docs, fallback template support, lint/readiness
warnings, and closure/promotion checks. It should not introduce a background
document synchronization engine.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1-AC4 | Canonical context artifact and readiness rules | Template lint, runtime lint fixture, manual review |
| Requirement 2 | AC1-AC4 | Authority hierarchy and external exception list | Unit tests for diagnostics; docs review |
| Requirement 3 | AC1-AC4 | Imported-source metadata table and validation | Runtime lint fixture; template review |
| Requirement 4 | AC1-AC4 | Agent Readiness Contract and task-context integration | Unit tests for readiness output or documented manual check |
| Requirement 5 | AC1-AC4 | Promotion-plan and closure-check additions | Unit tests for closure blocker or warning |
| Requirement 6 | AC1-AC4 | Fallback template and migration behavior | `prompts_validate`, full unittest suite, scan/lint |
| Requirement 7 | AC1-AC4 | Spec creation and resume flow context projection | Prompt/runtime tests or dogfood creation scenario |

## Correctness Property Coverage

| Property | Design Behavior | Validation Direction | Notes |
|----------|-----------------|----------------------|-------|
| CP-001 | Authority hierarchy always ranks external sources above spec-local context. | Unit test or focused docs review for conflict wording. | Governance and policy are never copied into a spec as the sole authority. |
| CP-002 | Imported-source rows require source path and promotion target when canonical. | Runtime lint fixture. | Source revision/date can be warning-level if unavailable. |
| CP-003 | Closure guidance reports residual canonical context not promoted, routed, or discarded. | Closure-check fixture or manual verification. | Exact severity may be warning initially if compatibility requires it. |
| CP-004 | Task/readiness guidance lists spec-local canonical sources before stale background sources. | Readiness or task-context fixture. | Background docs may still appear as non-canonical context. |
| CP-005 | Creation/resume flows create canonical context or return an import plan with spec-local target paths. | Prompt/runtime fixture and dogfood scenario. | Automatic copying may remain preview-first when source authority is ambiguous. |

## High-Level Design

### System Architecture

The lifecycle authority hierarchy becomes:

1. System, developer, and direct user instructions.
2. Applicable `AGENTS.md` files.
3. Governance, policy, security, privacy, compliance, and repository operating
   rules.
4. Generated contracts, source-code contracts, schemas, tests, and live/system
   evidence where applicable.
5. Active spec canonical context for the implementation slice.
6. Durable docs explicitly imported, adapted, summarized, or referenced by the
   active spec.
7. Other durable docs as background, drift evidence, or historical context.
8. Archived specs and history as historical evidence only.

The existing lifecycle chain remains:

```text
durable docs -> active spec -> code/tests/config -> durable docs -> close spec
```

The refinement is that the `active spec` step can include a curated projection
of relevant durable docs. That projection is canonical for the active slice and
must be promoted, routed, or discarded before closure.

### Components and Changes

- `skills/spec-lifecycle-manager/SKILL.md`:
  Add rules for spec-local canonical context during discovery,
  reconciliation, Agent Readiness Contract generation, implementation,
  promotion, and closure.
- `docs/design/spec-lifecycle-management.md`:
  Document the model and authority hierarchy durably.
- `docs/design/coding-agent-operating-model.md`:
  Add a concise agent operating rule for active-spec working context.
- `skills/spec-lifecycle-manager/references/spec-package/`:
  Add `canonical-context.md` or add a canonical-context section to package
  templates. Prefer a separate optional artifact because imported source lists
  can become substantial.
- `skills/spec-lifecycle-manager/prompts/`:
  Update spec-creation, developer-start, lifecycle-triage, reconcile, or
  task-context prompts where they shape new/resumed package behavior so agents
  proactively create or propose canonical context.
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py`:
  Add advisory diagnostics for active specs that declare broad durable impact,
  imported sources, or stale-doc risk without sufficient canonical context.
- `tests/runtime/` and `tests/fixtures/`:
  Add fixtures for canonical context lint/readiness/closure behavior.

### Data Models

Canonical context can be represented as Markdown with stable headings:

```markdown
# Canonical Context

## Purpose

## Authority Hierarchy

## Always-Canonical External Sources

| Source | Authority reason | Handling |
|--------|------------------|----------|

## Spec-Canonical Working Sources

| Source | Role | Scope | Notes |
|--------|------|-------|-------|

## Imported Sources

| Spec path | Source path | Source revision or date | Status | Canonical scope | Promotion target |
|-----------|-------------|-------------------------|--------|-----------------|------------------|

## Non-Canonical Background Sources

| Source | Reason non-canonical | Handling |
|--------|----------------------|----------|

## Promotion Map

| Spec-local content | Durable destination or route | Required before closure |
|--------------------|------------------------------|-------------------------|
```

`Status` values for imported sources should be small and readable:

- `copied`: content copied verbatim or near-verbatim.
- `adapted`: content edited for the active spec.
- `summarized`: content summarized rather than copied.
- `background`: context only, not canonical.
- `supersedes`: spec-local content supersedes the named durable source for the
  active slice.

### Data Flow

1. Lead agent identifies durable baseline and stale-doc risk.
2. During new-spec creation or resumption, the lead agent creates
   `canonical-context.md`, embeds canonical context sections, or returns a
   proposed import plan with target spec-local paths.
3. Lead agent copies, adapts, summarizes, or records proposed imports under the
   active spec package according to the template authority decision.
4. Worker agents use task context and canonical context before broader durable
   doc scans.
5. Reconciliation treats conflicts between canonical context and durable docs
   as explicit drift, not as silent implementation choice.
6. Promotion plan maps accepted spec-local content back to durable docs,
   backlog, roadmap, follow-up specs, or discard rationale.
7. Closure check reports unresolved spec-local canonical content.

## Low-Level Design

### Algorithms and Logic

Runtime support should stay advisory and deterministic:

```text
function lint_canonical_context(spec):
    context = read optional canonical-context.md
    impact = read change-impact and requirements durable impact
    stale_risk = find non-canonical/stale declarations if present

    if broad durable impact and no context:
        warn missing canonical context

    for each imported source row:
        if canonical status and missing source path:
            warn missing source path
        if canonical status and missing promotion target:
            warn missing promotion target

    if always-canonical section missing:
        info or warn depending on package risk

function propose_canonical_context_imports(spec_intake):
    sources = durable sources identified during discovery
    for each source:
        classify as external authority, spec-canonical, imported, or background
        choose target path under active spec package
        record import mode, canonical scope, and promotion target
    return preview plan or created canonical-context artifact

function closure_check(spec):
    existing closure blockers
    if canonical context has promotion rows still pending:
        add blocker or warning based on status
```

The first version can avoid deep Markdown table parsing if that creates
fragility. It can check stable headings and simple required phrases first, then
add table-field validation in a later slice if needed.

### Function Signatures and Interfaces

Likely internal helpers in `spec_runtime.py`:

```text
collect_canonical_context(spec_path) -> dict
propose_canonical_context_imports(spec_path, sources) -> dict
lint_canonical_context(spec, artifacts) -> list[Diagnostic]
canonical_context_readiness(spec, next_task) -> list[ReadinessGap]
canonical_context_closure_gaps(spec) -> list[ClosureGap]
```

No new MCP tool is required for the first implementation. Existing MCP tools
can expose the added diagnostics through existing scan, lint, preflight,
summary, readiness, promotion-plan, and closure-check payloads.

### Error Handling

- Missing `canonical-context.md` should not fail every small spec.
- Missing context should warn for broad durable-doc-impacting specs, specs with
  imported sources, or specs that explicitly name stale-doc risk.
- Conflicts with governance or policy should remain decision-gate blockers in
  guidance even if runtime only reports them as diagnostics.
- Runtime diagnostics should use repo-relative paths and avoid absolute host
  paths.

### Security, Trust, and Access

Spec-local context is not a privilege escalation mechanism. A copied policy,
security instruction, `AGENTS.md`, generated contract, or live evidence summary
inside a spec is not enough to override the durable or live source. When a spec
is about changing governance or policy, it must explicitly name that higher
authority as the target durable source and require the existing governance
decision path.

### Migration and Compatibility

Existing active specs should continue to pass unless modified or explicitly
migrated. Runtime diagnostics should start as advisory warnings for relevant
packages rather than forcing all packages to add `canonical-context.md`.

The migration guide should be updated when this behavior ships so old packages
know whether to add a canonical-context artifact, embed the data in
`requirements.md`, or leave the package unchanged.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Runtime and existing behavior | `verification.md`, task evidence | Broad but may not cover every wording rule. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | Active spec health | `verification.md` | Advisory diagnostics can still need manual review. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/027-spec-local-canonical-context` | This spec package | `verification.md` | Lint is structural, not semantic proof. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | Prompt definitions if changed | `verification.md` | Only needed if prompt files change. |
| `git diff --check` | Whitespace | `verification.md` | None expected. |

## Downstream Task Guidance

- Add durable design and skill guidance first so the model is explicit before
  runtime diagnostics encode it.
- Add template support before runtime checks become noisy.
- Add creation/resume prompt guidance before relying on users to ask for
  document imports after package creation.
- Keep runtime diagnostics warning-level until fixtures prove the false-positive
  rate is acceptable.
- Update traceability and verification when task scope changes.

## Operational Considerations

The most likely failure mode is over-enforcement: small specs get forced to
create a context artifact that adds ceremony without reducing risk. Keep the
first diagnostics scoped to broad durable-impact and stale-doc-risk packages.

The second likely failure mode is under-enforcement: agents continue to scan
legacy docs and treat them as authority. The Agent Readiness Contract wording
and task-context output need to put canonical context in the worker's must-read
set.

## Open Questions

- D001: Should the fallback template add a separate `canonical-context.md`, or
  should small packages embed canonical context in `requirements.md` and
  `change-impact.md`? Proposed answer: add an optional separate template and
  allow embedded sections for small packages.
- D002: Should missing promotion targets for canonical imported sources be a
  lint warning or closure blocker? Proposed answer: warning during authoring,
  blocker during closure when content is accepted and still canonical.

## Related Artifacts

- Requirements:
  `docs/specs/027-spec-local-canonical-context/requirements.md`
- Change Impact:
  `docs/specs/027-spec-local-canonical-context/change-impact.md`
- Tasks: `docs/specs/027-spec-local-canonical-context/tasks.md`
- Traceability:
  `docs/specs/027-spec-local-canonical-context/traceability.md`
- Verification:
  `docs/specs/027-spec-local-canonical-context/verification.md`
