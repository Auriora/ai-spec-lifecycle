---
title: Spec management MCP design
doc_type: spec
artifact_type: design
status: archived
owner: platform
last_reviewed: 2026-06-05
---

# Design

## Overview

The proposed system is a repository-local "spec lifecycle runtime" exposed
through MCP. It complements the `spec-lifecycle-manager` skill by making the
current lifecycle state machine observable, lintable, and easier to invoke from
clients.

The design deliberately separates five concerns:

| Concern | Best Surface | Reason |
| --- | --- | --- |
| Stable agent behavior and judgment | Skill | Skills package durable workflow instructions and can be invoked even when a client does not expose MCP prompts. |
| Current repository context | MCP resources | Resources expose active specs, templates, governance, and status as read-oriented context. |
| Deterministic checks and parsing | MCP tools | Tools return structured reports and can be tested without model judgment. |
| User-invoked workflow starters | MCP prompts | Prompts are useful for discoverable, parameterized workflows when the client supports them. |
| Local event gates | Hooks | Hooks catch lifecycle mistakes at file-change, commit, task-completion, and closure time. |

MCP prompts are useful, but they are not a replacement for Skills in this
project. A Skill is better for standing agent behavior because it travels with
the agent environment and can contain progressive references. MCP prompts are
better for client-visible commands such as "reconcile this spec" or "generate a
review packet" when the user explicitly invokes them. MCP tools and resources
should carry the enforceable behavior.

## Design Decision: Skills Versus MCP Prompts

### Recommendation

Use both, but assign them different jobs:

- Keep `spec-lifecycle-manager` as the authoritative workflow skill.
- Add MCP prompts as optional user-facing workflow shortcuts.
- Put deterministic behavior in MCP tools.
- Put current state and templates in MCP resources.
- Use hooks for local guardrails.

### Comparison

| Capability | Skill | MCP prompt |
| --- | --- | --- |
| Trigger model | Agent-selected by task description or explicit invocation. | User-controlled invocation exposed by MCP client UI. |
| Portability | Portable across agents that support Skills or can read `SKILL.md`. | Portable across MCP clients that expose prompts well. |
| Best use | Standing process rules, judgment gates, progressive references, coding-agent behavior. | Parameterized workflow starters, slash-command-like flows, review packet generation. |
| Weakness | Not a structured runtime API; agents may still need to inspect files manually. | Client support varies; prompts are not automatically applied and should not hide policy. |
| Risk | Skill instructions can become stale if not updated with durable docs. | Prompt output can be treated as authoritative prose unless paired with tool/resource evidence. |
| Fit here | Required. | Useful, optional layer. |

### Prompt Design Rule

MCP prompts should not duplicate the entire skill. Each prompt should:

1. Name the workflow entry point.
2. Accept explicit arguments.
3. Instruct the agent to read the skill.
4. Reference the relevant MCP resources.
5. Call or recommend deterministic MCP tools.
6. Produce a bounded output format.

Example prompt role:

```text
reconcile-spec(spec_id, docs_root?)
```

The prompt should not try to encode every reconciliation rule. It should guide
the agent to use `specs://{id}/summary`, `governance://constitution`, and
`reconcile_spec`.

## High-Level Design

### Components

| Component | Responsibility |
| --- | --- |
| Spec scanner | Discovers docs roots, active specs, old-format packages, artifact inventories, and indexes. |
| Template resolver | Finds repository templates when available and falls back to skill templates only with an explicit authority decision. |
| Markdown parser | Parses frontmatter, headings, links, task checkboxes, task IDs, dependency notes, evidence fields, and waiver markers. |
| Lint engine | Runs artifact-specific deterministic checks and emits structured diagnostics. |
| Reconciliation engine | Compares spec state with durable docs, code/test evidence, task status, and governance constraints. |
| Task planner | Selects next safe task slices from `tasks.md` based on dependencies and verification status. |
| Promotion planner | Maps accepted spec content to durable documentation destinations. |
| Review packet generator | Emits bounded prompts and context manifests for cheap-agent semantic review. |
| Hook runner | Provides CLI-compatible checks for changed files, task-completion gates, and closure gates. |
| MCP adapter | Exposes resources, tools, prompts, and prompt/resource change notifications where supported. |

### Data Flow

```text
repo files
  -> spec scanner
  -> template resolver
  -> markdown parser
  -> resources
  -> lint/reconcile/task/promotion tools
  -> prompts and review packets
  -> agent/operator decisions
  -> hooks and evidence logs
```

The MCP server should not silently edit spec packages in the MVP. It may
generate proposed patches or structured edit plans later, but first behavior
should be read-heavy and deterministic.

### Implementation Packaging Decision

Deterministic lifecycle helpers may start as dependency-free scripts inside the
`spec-lifecycle-manager` skill when they are useful before the MCP server
exists. The future MCP adapter should wrap these tested helpers where practical
instead of duplicating parsing logic.

The traceability lookup MVP lives at
`skills/spec-lifecycle-manager/scripts/traceability_lookup.py`. It provides the
`task_context` and `traceability_lookup` behavior as a CLI now and establishes
the payload shape for a future MCP tool.

## MCP Resources

### Static And Dynamic Resource URIs

| URI | Purpose |
| --- | --- |
| `specs://active` | Active spec inventory with IDs, paths, status, artifact inventory, old-format flag, and health summary. |
| `specs://{spec_id}/summary` | Requirements, design status, task counts, open decisions, verification state, durable-source references. |
| `specs://{spec_id}/tasks` | Parsed task graph, checkboxes, dependencies, files, acceptance, evidence, blockers. |
| `specs://{spec_id}/traceability` | Parsed or inferred requirement/design/task/verification/durable-target matrix. |
| `specs://{spec_id}/health` | Lint and lifecycle health diagnostics. |
| `specs://{spec_id}/promotion-targets` | Candidate durable docs and missing promotion destinations. |
| `templates://spec-package/{artifact_type}` | Effective spec template for an artifact type plus authority decision. |
| `templates://durable-doc/{doc_type}` | Effective durable-doc template when available. |
| `governance://constitution` | Active governance principles and decision gates. |
| `hooks://spec-lifecycle/config` | Hook configuration and severity policy. |

### Resource Payload Shape

Resources should return JSON where possible, with markdown snippets included as
fields rather than as unstructured whole documents. For example:

```json
{
  "spec_id": "004-spec-management-mcp",
  "path": "docs/specs/004-spec-management-mcp",
  "status": "draft",
  "format": "current",
  "artifacts": {
    "requirements": "present",
    "design": "present",
    "tasks": "present",
    "research": "present"
  },
  "health": {
    "severity": "warn",
    "findings": []
  }
}
```

## MCP Tools

### Core Tools

| Tool | Input | Output |
| --- | --- | --- |
| `scan_specs` | `repo_root`, optional `docs_root` | Active package inventory and format classification. |
| `lint_spec_package` | `spec_path`, optional severity profile | Diagnostics grouped by artifact and lifecycle gate. |
| `lint_doc` | `path`, optional `artifact_type` | Artifact-specific diagnostics. |
| `reconcile_spec` | `spec_path`, optional scope flags | Drift report with classifications and evidence gaps. |
| `next_task` | `spec_path`, optional phase or user story | Next safe task slice with dependencies, files, evidence needs, and traceability context. |
| `task_context` | `spec_path`, `task_id` | Requirements, acceptance criteria, design sections, change impact, verification expectations, durable targets, and open decisions for a task. |
| `traceability_lookup` | `spec_path`, lookup by task, requirement, or design section | Forward and reverse mappings across spec artifacts, with gaps and stale references reported. |
| `promotion_plan` | `spec_path` | Durable-doc routing plan and missing promotion targets. |
| `closure_check` | `spec_path` | Closure readiness, blockers, residual risk, active-index status. |
| `generate_review_packet` | `spec_path`, `review_type`, optional model class | Bounded review packet with inputs, question, output schema, and stop conditions. |

### Task Planner And Closure Checks

The CLI-first MVP exposes `next-task` and `closure-check` through
`skills/spec-lifecycle-manager/scripts/spec_runtime.py`.

`next-task` parses `tasks.md`, checks dependency IDs, requires completed
dependencies to have evidence, and returns the first runnable incomplete task
with traceability context when `traceability.md` exists.

`closure-check` reports whether a spec is ready to close. It currently blocks
closure when tasks are incomplete or lack evidence, required verification or
traceability artifacts are missing, or linter errors remain.

### Future Tools

| Tool | Purpose |
| --- | --- |
| `create_spec_package` | Scaffold a package from effective templates after a template authority decision. |
| `update_task_evidence` | Add evidence to a task by ID with validation of task state. |
| `propose_promotion_patch` | Generate patch plans for durable docs. |
| `record_review_result` | Attach cheap-agent review results and disposition. |
| `record_metric` | Record cycle-time and review-value data. |
| `update_traceability_matrix` | Propose or apply traceability matrix updates after requirements, design, or tasks change. |

Write tools should remain out of the MVP unless the deterministic read tools
prove useful.

## MCP Prompts

MCP prompts are user-invoked templates. They should expose common workflows as
client-visible commands while delegating validation to tools.

| Prompt | Arguments | Expected Use |
| --- | --- | --- |
| `start-spec` | `title`, `risk_level`, optional `docs_root` | Guide the agent through creating a new spec package. |
| `reconcile-spec` | `spec_id` or `spec_path` | Produce a reconciliation summary before resumed work. |
| `choose-next-task` | `spec_id`, optional `phase` | Select a safe task slice and validation plan. |
| `task-context` | `spec_id`, `task_id` | Return the spec context that must be reviewed before implementing a task. |
| `lint-spec` | `spec_id`, optional `severity_profile` | Run deterministic lint and explain actionable findings. |
| `review-requirements` | `spec_id`, optional `review_depth` | Generate a bounded requirements review packet. |
| `review-design` | `spec_id`, optional `review_depth` | Generate a bounded design review packet. |
| `promotion-plan` | `spec_id` | Map accepted content into durable docs. |
| `close-spec` | `spec_id` | Check verification, promotion, unresolved decisions, and active index status. |

The CLI-first prompt contracts live under
`skills/spec-lifecycle-manager/prompts/`. `spec_runtime.py prompts` validates
the required definitions, arguments, resource references, tool references,
return format, and client-support fallback text.

### Prompt Template Pattern

Each prompt should produce instructions in this shape:

```text
Use the spec-lifecycle-manager skill.
Read these resources:
- specs://{spec_id}/summary
- specs://{spec_id}/tasks
- governance://constitution

Run these MCP tools:
- lint_spec_package(spec_path)
- reconcile_spec(spec_path)

Return:
- selected workflow
- findings by severity
- required decisions
- next action
- evidence or residual risk
```

### Client Support Fallback

If MCP prompts are not visible in the client, equivalent behavior should remain
available through natural-language requests that trigger the Skill plus MCP
tools. Prompts are convenience entry points, not a governance dependency.

## Linter Design

### Diagnostic Model

```json
{
  "severity": "error|warn|info",
  "code": "TASK_EVIDENCE_MISSING",
  "path": "docs/specs/004-spec-management-mcp/tasks.md",
  "line": 42,
  "message": "Completed task T003 has no evidence.",
  "artifact_type": "tasks",
  "lifecycle_gate": "completion",
  "waivable": true,
  "recommendation": "Add evidence or mark the task incomplete."
}
```

### Artifact Rules

| Artifact | Key Rules |
| --- | --- |
| `requirements.md` | Frontmatter, durable source baseline, goals, non-goals, glossary when useful, user stories, EARS criteria, correctness properties, success criteria. |
| `design.md` | Frontmatter, overview, high-level design, low-level design, interfaces, error handling, operational concerns, open questions. |
| `tasks.md` | Frontmatter, dependency graph or dependency notes, stable task IDs, checkboxes, acceptance criteria, evidence for completed tasks, valid dependencies. |
| `traceability.md` | Task IDs, requirement references, design section references, verification references, durable targets, open-decision references, and bidirectional consistency. |
| `change-impact.md` | Durable source mapping, delta classification, promotion target, remove/rename/bug-fix handling. |
| `verification.md` | Quality gates, evidence log, residual risk, closure or release readiness. |
| `research.md` | Scope, sources, findings, tradeoffs, recommendation, uncertainty. |
| `quickstart.md` | Temporary setup or validation notes and promotion/discard destination. |
| `open-decisions.md` | Decision owner, blocking scope, options, current recommendation, due trigger. |

### Waivers

Waivers should be explicit and local:

```markdown
<!-- spec-lint-disable TASK_EVIDENCE_MISSING: manual review recorded in PR -->
```

The linter should report waivers in summaries so they remain visible.

## Reconciliation Design

The reconciliation engine combines deterministic parsing with optional semantic
review. Deterministic checks run first:

1. Parse tasks and evidence.
2. Validate links to durable docs.
3. Check package format.
4. Check old-format migration decision.
5. Check unresolved decisions.
6. Check verification and promotion readiness.
7. Check traceability matrix freshness when present.

Semantic review can then be delegated to review packets:

- Does the requirements doc describe the real problem?
- Does the design satisfy every acceptance criterion?
- Are durable promotion targets plausible?
- Are risks and non-goals coherent?

Reports must separate:

- observed facts;
- inferred diagnosis;
- recommended action.

The CLI-first MVP exposes this report through
`skills/spec-lifecycle-manager/scripts/spec_runtime.py reconcile`. Findings use
the documented drift classifications and include separate observed facts,
inferred diagnosis, recommended action, source diagnostics, and blind spots.

## Traceability Design

Traceability is the deterministic guardrail against implementing from task text
alone. The MCP runtime should support both a package-local `traceability.md`
artifact and inferred traceability from the core artifacts.

### Matrix Inputs

- `requirements.md`: requirement IDs, user stories, acceptance criteria,
  correctness properties, success criteria, durable-source baseline.
- `design.md`: section headings, requirement coverage table, interfaces,
  algorithms, validation strategy, security, migration, operational concerns.
- `tasks.md`: task IDs, dependencies, files, acceptance, evidence, user-story
  tags.
- `change-impact.md`: durable deltas and promotion targets.
- `verification.md`: gates, requirement coverage, task evidence, residual risk.
- `open-decisions.md`: decision IDs and blocking impact.
- `traceability.md`: explicit forward and reverse mappings when present.

### Lookup Output

`task_context(spec_path, task_id)` should return:

```json
{
  "task_id": "T004",
  "task": "Add tests for user story 1",
  "requirements": ["Requirement 1"],
  "acceptance_criteria": ["Requirement 1 AC1", "Requirement 1 AC2"],
  "design_sections": ["design.md#low-level-design"],
  "change_impact": ["change-impact.md#durable-delta"],
  "verification": ["verification.md#requirement-coverage"],
  "durable_targets": ["docs/requirements/example.md"],
  "open_decisions": [],
  "files": ["tests/path/to/test"],
  "gaps": []
}
```

If the explicit matrix disagrees with source artifacts, the tool should report
both the observed source facts and the stale matrix entry.

### Matrix Freshness Rules

- Every task ID in `tasks.md` should have a row when `traceability.md` exists.
- Every requirement should map to at least one design section, task, or
  documented deferral before implementation starts.
- Every completed task should map to verification evidence before closure.
- Open decisions that block a task should appear in task context.
- Durable targets should be present for implemented behavior before closure.

## Review Packet Design

Review packets allow cheap agents to help without writing into the repository.

### Packet Types

| Packet Type | Question |
| --- | --- |
| `requirements_template_review` | Does the requirements artifact satisfy required sections and EARS clarity? |
| `design_requirements_trace` | Does the design cover every requirement and success criterion? |
| `task_dependency_review` | Are task dependencies safe and executable? |
| `promotion_target_review` | Which durable docs need updates before closure? |
| `closure_risk_review` | What closure blockers or residual risks remain? |
| `governance_conflict_review` | Does the spec conflict with constitution or repo instructions? |

### Packet Output Schema

```json
{
  "review_type": "design_requirements_trace",
  "summary": "short finding summary",
  "findings": [
    {
      "severity": "error|warn|info",
      "artifact": "design.md",
      "reference": "Requirement 3",
      "finding": "Design does not describe evidence capture.",
      "recommendation": "Add evidence storage behavior to low-level design."
    }
  ],
  "confidence": "low|medium|high",
  "blind_spots": []
}
```

The CLI-first MVP exposes review packets through
`skills/spec-lifecycle-manager/scripts/spec_runtime.py review-packet`. Packets
are read-only, include an artifact manifest, frame document content as
untrusted data, define stop conditions, and include the expected output schema.
`review-result-template` and `validate-review-result` provide the disposition
shape for accepted, rejected, deferred, and human-decision findings.

## Hook Design

Hooks should call the same linter and closure-check core used by MCP tools.
They should be adopted in phases so the workflow gets useful feedback before
blocking gates are introduced.

| Hook | Trigger | Blocking Policy |
| --- | --- | --- |
| `spec-file-changed` | Changed files under `docs/specs/` or skill templates | Advisory by default; blocking for parse errors and completed tasks without evidence. |
| `task-checkbox-changed` | Task checkbox changes from `[ ]` to `[x]` | Blocking when evidence is absent unless waiver exists. |
| `spec-close-check` | Closure command or archive/removal attempt | Blocking until promotion, verification, and unresolved decisions are handled. |
| `template-changed` | Template edits or package creation | Advisory unless required metadata is removed. |

The hook runner should support:

- `--changed-files`
- `--spec-path`
- `--severity-profile`
- `--json`
- `--advisory`

The CLI-first hook runner is exposed through
`skills/spec-lifecycle-manager/scripts/spec_runtime.py hook`. The MVP supports
`spec-file-changed`, `task-checkbox-changed`, advisory and blocking severity
profiles, changed-file package detection, direct spec-path checks, and JSON
reports with diagnostics, summary, affected specs, and blocking findings.

Completion and lifecycle gate hooks extend the same runner:

- `implementation-task-complete` checks a selected task or completed tasks for
  evidence, files, and changed-file alignment.
- `verification-updated` checks `verification.md` structure and whether
  verification evidence references task and requirement IDs.
- `spec-resumed` runs package lint, flags old-format packages, warns when
  resuming closed specs, and detects stale review dates.
- `spec-close-check` wraps closure readiness blockers into hook diagnostics.

### Hook Roadmap

#### Phase 1: Advisory Hooks

| Hook | Trigger | Behavior |
| --- | --- | --- |
| `spec-file-changed` | Any changed spec artifact | Runs artifact-specific lint on affected packages only; checks frontmatter, required sections, local links, task IDs, and dependencies. |
| `task-checkbox-changed` | Checkbox state changes in `tasks.md` | Warns when a task moves to `[x]` without evidence, with incomplete subtasks, or without acceptance criteria. |
| `template-changed` | Skill or repository template edits | Lints the changed template and runs representative fixture checks; warns if required lifecycle fields are removed. |

Phase 1 should be advisory except for parse errors that prevent later checks
from understanding the document.

#### Phase 2: Completion Gates

| Hook | Trigger | Behavior |
| --- | --- | --- |
| `pre-commit-spec-check` | Commit with changed spec files | Blocks invalid frontmatter, broken relative links, duplicate task IDs, missing dependency targets, and completed tasks without evidence. |
| `implementation-task-complete` | Parent task marked complete | Compares task `Files:` against changed files where possible; checks evidence quality and validation command or residual-risk notes. |
| `verification-updated` | `verification.md` or evidence fields changed | Checks evidence maps back to requirement IDs, task IDs, acceptance criteria, or success criteria. |

Phase 2 can block high-confidence lifecycle errors. Vague evidence should warn
first unless the repository explicitly chooses stricter gates.

#### Phase 3: Lifecycle Gates

| Hook | Trigger | Behavior |
| --- | --- | --- |
| `spec-created` | New package under `docs/specs/` | Verifies package path, core artifacts, metadata, and template authority decision. |
| `spec-resumed` | User or agent resumes an existing package | Runs reconciliation, detects old-format packages, stale dates, checked tasks, open decisions, and changed durable docs. |
| `spec-close-check` | Closure, archive, or removal attempt | Blocks until verification, promotion, unresolved decisions, residual risk, and active-index status are handled. |

Phase 3 hooks protect lifecycle transitions rather than ordinary editing.

#### Phase 4: Agent-Oriented Hooks

| Hook | Trigger | Behavior |
| --- | --- | --- |
| `agent-slice-start` | Agent starts implementation from a spec | Requires selected task IDs and returns dependency state, likely files, validation expectations, and blockers. |
| `agent-response-check` | Agent claims completion | Checks whether claimed tests, evidence, changed files, and task updates are present; flags unsupported completion claims. |
| `review-packet-dispatch` | Cheap-agent review packet is generated | Enforces bounded read-only scope, output schema, input artifact manifest, and stop conditions. |
| `review-result-recorded` | Cheap-agent review returns findings | Records accepted, rejected, deferred, and human-decision findings; prevents automatic task completion from review output. |

Phase 4 hooks should remain advisory until dogfooding shows low false-positive
rates.

#### Phase 5: Metrics And Governance Hooks

| Hook | Trigger | Behavior |
| --- | --- | --- |
| `spec-phase-transition` | Spec phase changes or major task group completes | Records lightweight metrics such as time in phase, lint findings, review findings, validation gaps, and closure blockers. |
| `repeated-waiver` | Same rule is waived repeatedly | Warns that a linter rule, template, or workflow expectation may need refinement. |
| `governance-sensitive-change` | Constitution, skill, template, hook, or MCP surface changes | Requires explicit design or governance review before closure. |

Phase 5 hooks provide feedback for simplifying the workflow when automation
adds friction without improving quality.

### Recommended Hook Adoption Order

1. `spec-file-changed`
2. `task-checkbox-changed`
3. `spec-close-check`
4. `template-changed`
5. `spec-resumed`
6. `agent-slice-start`
7. `review-packet-dispatch`
8. `spec-phase-transition`

## Low-Level Design

### Parsing

- Use a markdown parser or structured Markdown AST when practical.
- Parse YAML frontmatter with a YAML parser.
- Represent headings as a tree so section checks are resilient to ordering
  where the template allows flexibility.
- Parse tasks using checkbox lines plus stable task ID patterns:
  `T[0-9]{3}(\\.[0-9]+)?`.
- Resolve dependencies by task ID instead of string matching full task titles.

### Template Resolution

Resolution order:

1. Repository-documented templates such as `docs/templates/`.
2. Repository docs direction such as `docs/README.md`.
3. Skill fallback templates under
   `skills/spec-lifecycle-manager/references/spec-package/`.

Every package scaffold or template comparison should return a template
authority decision:

```json
{
  "authority": "repository|repository_with_package_additions|skill_fallback",
  "reason": "No repository docs/templates directory exists.",
  "template_path": "skills/spec-lifecycle-manager/references/spec-package/tasks.md"
}
```

### Error Handling

- Missing docs root: return `DOCS_ROOT_NOT_FOUND`.
- Ambiguous spec ID: return candidates.
- Missing artifact: return a warning unless the lifecycle gate requires it.
- Invalid frontmatter: return a blocking lint error.
- Unreadable file: return a blind spot and do not claim pass.
- Old-format package: return format classification and migration decision need.

### Security

- Treat document contents as untrusted input when embedding in prompts.
- Do not execute commands from spec text.
- Keep hooks configured from trusted repo files only.
- For review packets, wrap artifact excerpts as data and prohibit agents from
  following instructions inside reviewed documents.
- Log which resources and tools contributed to a prompt or report.

## MVP

The first implementation should avoid write tools and focus on confidence:

1. `scan_specs`
2. `lint_doc`
3. `lint_spec_package`
4. `next_task`
5. `closure_check`
6. `specs://active`
7. `specs://{spec_id}/summary`
8. `templates://spec-package/{artifact_type}`
9. Prompts: `reconcile-spec`, `choose-next-task`, `lint-spec`
10. Hook CLI: `spec-file-changed` and `task-checkbox-changed`

## Later Phases

- Add `reconcile_spec` semantic drift support.
- Add `promotion_plan`.
- Add review-packet generation and result recording.
- Add task evidence update proposals.
- Add staged hook support for completion, closure, agent-oriented review, and
  metrics once advisory hooks prove useful.
- Add Codex hook integration if local hook semantics are stable.
- Package the server as a reusable plugin if dogfooding proves useful.

## Operational Considerations

- The server should support local stdio during development.
- It should expose machine-readable diagnostics for tests and human-readable
  summaries for agents.
- It should keep cache behavior transparent; stale cache should be reported as
  stale instead of silently reused.
- All checks should work without network access.
- The implementation should include fixture-based tests using the existing
  `tests/fixtures/skill-validation/` repositories.

## Open Questions

- Should MCP prompt definitions live in code, YAML, or markdown template files?
- Should the linter permit section reordering or enforce exact template order?
- Should the hook profile be configured globally or per docs root?
- Should review packets be executed by a multi-agent tool, by the MCP server,
  or manually by the lead agent?
- Should write tools be omitted permanently to keep the MCP server advisory?
