---
title: Staged developer onboarding design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Design

## Overview

Add a staged developer onboarding and repository-readiness workflow to the
spec-lifecycle-manager. The workflow should make the first action obvious,
handle blank repositories gracefully, and preserve the existing runtime/MCP
tooling model as the authoritative way to inspect lifecycle state.

The design adapts CLU's useful process shape without copying its packaging,
fixed foundation list, or architecture-first assumption.

## High-Level Design

The implementation has five parts:

- A first-run lifecycle entry point that orients the developer and selects the
  next stage.
- A blank-repo bootstrap planner that previews minimal docs/spec scaffolding.
- A staged artifact state model for requirements, design, tasks,
  implementation, verification, promotion, and closure.
- An Agent Readiness Contract that sits before implementation readiness and
  constrains context, permissions, validation, review, and closure impact.
- Runtime/MCP readiness output that reports stage health, foundations,
  traceability gaps, and next actions.
- Guidance/template updates for agent directives, execution recovery,
  properties-to-tests coverage, numbered findings, and learning-loop routing.

Existing packaging, plugin install behavior, and discovery layout are
unchanged.

## Stage Model

| Stage | Purpose | Primary artifacts | Ready when |
| --- | --- | --- | --- |
| `discover` | Orient to repo state and available tools. | Runtime scan, docs inventory, governance/template authority. | Readiness and next actions are known. |
| `bootstrap` | Establish minimal lifecycle foundation for blank or near-blank repos. | Previewed docs root, project summary/runbook, optional first spec package. | User confirms foundation writes or chooses no-write guidance. |
| `requirements` | Capture problem, scope, user stories, acceptance criteria, and correctness properties. | `requirements.md`; optional `research.md`. | Requirements are coherent enough to design. |
| `design` | Decide how accepted requirements will be implemented. | `design.md`; optional `open-decisions.md`, `change-impact.md`. | Design maps requirements to components, decisions, and validation strategy. |
| `tasks` | Create ordered, traceable implementation and validation work. | `tasks.md`, `traceability.md`, optional `verification.md`. | Tasks cover requirements/properties and identify checkpoints. |
| `agent_ready` | Package bounded context and constraints for a worker agent. | Readiness contract from preflight, task context, validation planner, governance, and durable sources. | The agent has must-read context, do-not-read guidance, permissions, validation contract, review needs, and closure impact. |
| `implement` | Execute one coherent task slice at a time. | Code/tests/docs/config plus task evidence. | Selected task has evidence and status matching reality. |
| `verify` | Record validation evidence and residual risk. | `verification.md`, task evidence, review records. | Required checks/reviews are complete or explicitly waived. |
| `promote` | Move accepted behavior to durable docs. | Durable docs, backlog, roadmap, ADRs, runbooks, reference docs. | Durable docs describe current behavior or deferrals. |
| `close` | Remove or archive active spec scaffolding with a durable breadcrumb. | Closure log, archive index, final spec commit. | Spec no longer acts as active source of truth. |

Architecture and pattern documentation can appear in `discover`, `bootstrap`, or
`promote` when evidence supports them. They are not mandatory first-stage
artifacts.

## Runtime And MCP Design

### Lifecycle Guide

Add a runtime helper tentatively named `lifecycle_guide(repo_root, docs_root=None,
mode="auto")`.

The helper returns:

- repository classification: `blank`, `near_blank`, `documented_no_specs`,
  `active_specs`, or `closed_only`;
- available lifecycle tooling: MCP-visible tools, CLI fallback commands, prompt
  definitions, hook configuration status;
- docs readiness: docs root, template authority, governance files, durable doc
  classes detected, missing-but-optional docs, missing-blocking docs;
- spec readiness: active spec list, current stage per spec, next blocking
  artifact, traceability/verification gaps, closure candidates;
- bootstrap recommendation when repo is blank or near blank;
- next actions ordered by usefulness and risk.

MCP tool: `lifecycle_guide`.

Prompt: add or update a prompt such as `developer-start.json` or extend
`lifecycle-triage.json` only if the prompt can call out the same runtime-backed
data shape. The runtime remains the source of deterministic state.

### Bootstrap Plan

Add a preview-first runtime helper tentatively named
`bootstrap_plan(repo_root, docs_root="docs", project_summary=None,
create_spec=False, spec_slug=None)`.

The helper returns a write plan, not immediate edits:

- paths to create;
- file purpose;
- template source;
- required user-provided values;
- validation commands after apply;
- risks and assumptions;
- whether architecture/pattern docs are recommended now or deferred.

Write application can be manual through normal agent edits in v1. A future
write helper may be added only after the same preview-first and path-boundary
rules used by task-state management are accepted.

MCP tool: `bootstrap_plan`.

### Stage Readiness

Extend scan/preflight or add `stage_readiness(spec_path)` with:

- current stage;
- required artifacts for the next stage;
- optional artifacts recommended by risk;
- blocking gaps;
- downstream review needs when upstream artifacts changed;
- requirements property coverage;
- acceptance criteria coverage;
- design/task/verification traceability status.

MCP exposure may be either a new `stage_readiness` tool or an additional field
in `active_spec_preflight`. Prefer extending existing preflight if the payload
remains readable.

### Agent Readiness Contract

Extend `active_spec_preflight`, `agent_readiness_packet`, or stage readiness
with a compact `agent_readiness_contract` payload. The contract is distinct from
implementation readiness: a task can be coherent but still unsafe for an agent
if context, permissions, validation, review, or durable-doc impact are unclear.

The payload should include:

- scope: selected task or requirement, risk level, likely affected files, and
  explicit out-of-scope files;
- context: must-read artifacts, optional artifacts, durable sources of truth,
  stale or historical documents not to treat as current, and refresh points;
- validation: required commands, expected pass/fail signal, manual proof,
  evidence location, and residual risk from `validation_plan` when available;
- permissions: allowed edits, forbidden edits, external services or secrets,
  and human approval points;
- review: required packet type, fresh-context review flag, and
  security/privacy review flag;
- closure impact: durable docs affected, backlog/roadmap/issue routing, and
  release-note expectation.
- optional repo evidence: provider name, repository freshness, confidence,
  capability level, evidence kinds, diagnostics status, validation-plan status,
  skipped evidence, and residual risk when Agent Workbench or an equivalent
  provider is available.

Context-budget rules should prefer `task_context` and traceability lookups over
full-document loading, avoid archived specs unless historical audit or
restoration is requested, and refresh context at phase boundaries. The contract
should name missing fields as gaps instead of padding them with generic advice.
Repo-evidence providers are advisory. Their outputs can guide context and
validation planning, but they must not decide completion, promotion, closure, or
governance outcomes.

## Low-Level Design

### Runtime Commands

Add CLI subcommands to `spec_runtime.py` where they map directly to
runtime-backed MCP behavior:

```text
spec_runtime.py lifecycle-guide [repo_root] [--docs-root docs]
spec_runtime.py bootstrap-plan [repo_root] [--docs-root docs] [--project-summary TEXT] [--create-spec] [--spec-slug SLUG]
spec_runtime.py stage-readiness SPEC_PATH
```

Each command should return JSON by default or follow the runtime's existing
format conventions where similar commands already support text mode. The JSON
payloads should be stable enough for MCP tools, tests, and prompt guidance to
consume without parsing human prose.

### Data Shapes

`lifecycle_guide` payload:

```json
{
  "repo_classification": "blank | near_blank | documented_no_specs | active_specs | closed_only",
  "tooling": {
    "mcp_available": true,
    "cli_commands": [],
    "prompt_definitions": [],
    "hooks": []
  },
  "docs_readiness": {
    "docs_root": "docs",
    "template_authority": {},
    "governance": [],
    "durable_docs": [],
    "missing": []
  },
  "spec_readiness": [],
  "bootstrap": {},
  "next_actions": []
}
```

`bootstrap_plan` payload:

```json
{
  "mode": "preview",
  "repo_classification": "blank | near_blank",
  "writes": [],
  "required_user_values": [],
  "validation_commands": [],
  "deferred_recommendations": [],
  "assumptions": []
}
```

`stage_readiness` payload:

```json
{
  "spec_id": "024-example",
  "stage": "requirements | design | tasks | implement | verify | promote | close",
  "blocking_gaps": [],
  "recommended_optional_artifacts": [],
  "downstream_review_needed": [],
  "coverage": {
    "properties": [],
    "acceptance_criteria": []
  },
  "agent_readiness_contract": {
    "status": "ready | blocked | partial",
    "scope": {},
    "context": {},
    "validation": {},
    "permissions": {},
    "review": {},
    "closure_impact": {},
    "gaps": []
  }
}
```

### Repository Classification

Classification should reuse existing scan inputs where possible:

- docs root existence and known durable-doc files;
- active spec inventory;
- closure log and archive index presence;
- source files or package metadata;
- governance/template files;
- README or project metadata.

The classifier should be conservative. If it cannot distinguish blank from
near-blank, use `near_blank` and report the evidence that led to that
classification.

### Stage Readiness Rules

Stage readiness should be derived from artifacts, not from frontmatter alone:

- requirements stage checks requirements status, acceptance criteria,
  correctness properties, and open questions;
- design stage checks design coverage of requirements/properties and unresolved
  design decisions;
- tasks stage checks task coverage, dependencies, checkpoints, and traceability;
- implement stage checks selected task state, dependencies, and required
  context;
- verify stage checks validation evidence and residual risks;
- promote stage checks durable-doc destinations and deferrals;
- close stage checks closure log/archive-index needs and active index cleanup.

Downstream review signals should be emitted when upstream artifacts change after
dependent artifacts exist.

## Guidance And Template Design

### Skill Guidance

Update `skills/spec-lifecycle-manager/SKILL.md` to add:

- a `First Run` section that tells agents to use `lifecycle_guide` before
  creating docs in an unfamiliar repo;
- a blank-repo bootstrap rule that avoids architecture-first assumptions;
- a staged artifact progression rule that names valid transitions and
  design-first handling;
- a context-budget rule that tells agents what to read, what not to load unless
  needed, and when to refresh context;
- an execution recovery rule: one meaningfully different recovery attempt,
  then blocker evidence;
- a directive-generation rule: durable agent directives must be evidence-derived
  or user-confirmed;
- an instruction-as-code rule: repeated failures from missing or stale
  instructions become candidate `AGENTS.md`, durable-doc, backlog, roadmap, or
  follow-up spec updates;
- a numbered-findings rule for persisted review/audit outputs.

### Templates

Update fallback templates selectively:

- `requirements.md`: include correctness properties and a staged readiness note.
- `design.md`: include property-to-design mapping and downstream task guidance.
- `tasks.md`: include checkpoint tasks and evidence expectations for
  properties/acceptance criteria.
- `traceability.md`: include properties-to-tests rows.
- `verification.md`: include coverage, residual risk, and staged readiness.

Do not add every possible optional artifact to new packages by default.

### Durable Docs

Update durable doc templates where appropriate:

- runbook/getting-started templates can include a compact agent-directives
  section when there is evidence.
- review/audit guidance can include stable finding IDs and extension behavior.
- document lifecycle guidance can mention first-run bootstrap and staged
  artifact progression.

## Blank-Repo Behavior

Blank-repo detection should be conservative:

- `blank`: no meaningful source files and no docs root.
- `near_blank`: minimal repo files such as README, license, package metadata,
  or empty source tree, but no durable lifecycle docs.
- `documented_no_specs`: durable docs exist, no active specs.
- `active_specs`: one or more active specs exist.
- `closed_only`: no active specs, but closure log/archive index indicate prior
  lifecycle work.

For `blank` and `near_blank`, `lifecycle_guide` should not fail because
`docs/specs` is absent. It should say what is missing, why that is normal, and
what minimal next action is available.

The initial bootstrap should favor:

1. `docs/README.md` or equivalent lifecycle index when the repo has no docs.
2. A project summary/runbook target if the user can confirm purpose and basic
   commands.
3. A first spec package only if the user has an actual change or feature to
   capture.

## Review Findings Model

Persisted review/audit records should support a stable finding format:

```markdown
#### F-001 Short title

| Field | Value |
| --- | --- |
| Status | Open |
| Impact | Medium |
| Effort | Small |
| Source | `path/to/file` or review packet |
| Routing | Backlog / spec / durable doc / none |

**Finding:** ...
**Direction:** ...
```

Runtime support can start as lint guidance for review records rather than a
full review-management tool. Follow-up implementation can add structured review
finding parsing if this proves useful.

## Learning Loop And Failure Taxonomy

Readiness and review outputs should classify repeated agent failures so metrics
lead to concrete lifecycle changes. Initial categories:

- misunderstood requirement;
- missed durable source;
- stale spec followed;
- insufficient validation;
- over-broad implementation;
- invented behavior;
- dependency or environment failure;
- context overflow or noise;
- unsafe tool use;
- review missed defect;
- documentation promotion missed.

The runtime should report these as advisory learning-loop signals. It should
not automatically rewrite `AGENTS.md`, durable docs, backlog, roadmap, or specs;
the lead agent routes accepted changes to the right surface.

## Traceability And Validation

Property and acceptance coverage should be checked before
`ready_to_implement`:

- every correctness property has a design mapping;
- every correctness property maps to a task, test, or explicit manual
  verification method;
- every acceptance criterion maps to at least one task or verification note;
- every uncovered item appears as a blocker or explicit residual risk.

The lint/preflight payload should surface coverage gaps without requiring a new
testing dependency.

## Operational Considerations

- Keep all new MCP tools read-only for this spec unless a later accepted design
  explicitly adds guarded writes.
- Runtime output must remain useful in CI and local debugging without MCP.
- First-run guidance should be low-noise: summarize normal missing docs as
  normal for blank/near-blank repos instead of producing warning-heavy output.
- Existing scan, lint, prompt validation, closure, archive-index, hook, and
  traceability commands must continue to behave for current specs.
- Bundle parity remains an implementation requirement because this repo tests
  source and plugin copies, but packaging behavior is not redesigned here.
- Bootstrap output should be safe to show to a user before any file is written.

## Files Affected

Likely files:

- `skills/spec-lifecycle-manager/SKILL.md`
- `skills/spec-lifecycle-manager/prompts/`
- `skills/spec-lifecycle-manager/references/spec-package/`
- `skills/spec-lifecycle-manager/references/durable-doc-templates/`
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
- `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
- `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py`
- `docs/reference/spec-lifecycle-runtime.md`
- `docs/design/spec-lifecycle-management.md`
- `docs/reference/document-routing-and-expert-review-matrix.md`
- `plugins/spec-lifecycle-manager/`
- `tests/runtime/`
- `tests/fixtures/`

## Open Questions

- Should `lifecycle_guide` be a new MCP tool, or should it be implemented as an
  enriched `active_spec_preflight` plus a prompt?
- Should blank-repo bootstrap remain preview-only in v1, with writes performed
  by the lead agent, or should v1 include a guarded apply tool?
- Which durable doc template is the best home for reusable agent directives:
  runbook, project principles, architecture overview, or a new lightweight
  project guide?
- Should numbered review findings be introduced as a review-record template
  first, or should runtime parsing/linting be included in the first slice?
