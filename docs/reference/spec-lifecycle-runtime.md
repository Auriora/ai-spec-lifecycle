---
title: Spec lifecycle runtime
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-07-05
---

# Spec Lifecycle Runtime

The spec lifecycle runtime is a dependency-free helper surface shipped with the
`spec-lifecycle-manager` skill. It provides deterministic JSON outputs that
agents, hooks, and the MCP server can use without replacing the skill's
workflow judgment.

Current implementation:

```text
skills/spec-lifecycle-manager/scripts/lifecycle/core.py
skills/spec-lifecycle-manager/scripts/lifecycle/runtime_adapter.py
skills/spec-lifecycle-manager/scripts/lifecycle/
skills/spec-lifecycle-manager/scripts/spec_runtime.py
skills/spec-lifecycle-manager/scripts/spec_mcp_server.py
skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py
skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py
skills/spec-lifecycle-manager/prompts/
```

Shared lifecycle logic lives under
`skills/spec-lifecycle-manager/scripts/lifecycle/`, with the broad retained
runtime implementation in import-only `lifecycle/core.py`. MCP handlers import
shared internals directly. CLI parsing for the retained recovery surface lives
behind `spec_runtime.py` in `lifecycle/runtime_adapter.py`; `lifecycle/core.py` is not an
executable command surface. Retained Python scripts are adapters for
validation, package checks, hooks, MCP server startup, and no-MCP recovery;
they are not competing public lifecycle tool contracts. For Codex sessions with
the MCP server configured, MCP tools are the preferred agent-facing interface.
Shell out to scripts only for CI, repository validation, MCP debugging,
install/package checks, hook execution, or explicit recovery when MCP tools are
not available.

## Developer CLI Convenience Wrapper

This repository also ships a maintainer convenience CLI under `tools/devcli/`.
Install it from the checkout with:

```bash
pip install --no-build-isolation -e tools/devcli
```

The `slc` command is a thin wrapper over the authoritative runtime scripts,
npm commands, installer, and Git checks. It does not parse spec packages
itself. Use it to repeat common local workflows:

```bash
slc check
slc spec scan
slc spec archive-index
slc spec prompts
slc spec lint docs/specs/NNN-active-spec
slc sync guard
slc package check
slc release preflight --allow-dirty
```

`slc check` runs the same local validation family documented below: Python
unit tests, lifecycle scan, archive-index validation, prompt validation,
package-contract validation, npm pack dry-run, and whitespace checks.
Mutating helpers such as `slc sync bundles` and `slc package install-local`
must make mutation boundaries explicit and support dry-run behavior where the
underlying workflow supports it.

## Runtime Commands

| Command | Purpose |
| --- | --- |
| `scan` | Discover spec packages, classify current versus old-format packages, and report artifact inventory, lifecycle, active-health summary, health, and template authority. |
| `spec-id-inventory` | Return docs-root-scoped evidence and the next provisional monotonic spec number without writing files. |
| `spec-creation-plan` | Preview a slugged ID/path, template/artifact plan, preconditions, validation, and stale-plan fingerprint without reserving or writing. |
| `summary` | Return a `specs://{spec_id}/summary`-style payload with task counts, artifact state, open decisions, durable-source references, and health. |
| `lint` | Run deterministic document or package lint checks for frontmatter, required sections, task IDs, dependencies, evidence, optional artifacts, and waivers. |
| `next-task` | Select the next runnable task whose dependencies are complete with evidence and include traceability context when available. |
| `list-tasks` | Return grouped task records with normalized state, dependency readiness, evidence summaries, parent/subtask relationships, cross-spec references, and advisory findings. |
| `task-details` | Return one parsed task with parent/subtask detail, dependency state, traceability context, linked requirements, verification, durable targets, gaps, and advisory split suggestions. |
| `task-state-audit` | Audit task state, evidence depth, metadata, parent/child consistency, broad-task shape, and cross-spec dependency trust. |
| `set-task-state` | Preview or write a guarded task-state update scoped to one task block in an active spec package `tasks.md`; defaults to dry-run and requires explicit write intent for mutation. |
| `active-spec-preflight` | Return the active spec, next task, readiness context, no-active context, guidance, and validation commands. |
| `lifecycle-guide` | Return first-run repository classification, docs readiness, lifecycle tooling, active-spec readiness summaries, bootstrap recommendations, and next actions. |
| `bootstrap-plan` | Preview minimal lifecycle docs/spec bootstrap writes for blank or near-blank repositories without mutating files. |
| `stage-readiness` | Return staged artifact readiness, downstream review needs, context-budget gaps, correctness-property coverage, acceptance-criteria coverage, and Agent Readiness Contract status for one spec package. |
| `phase-gate-check` | Return a bounded, read-only aggregate of the current lifecycle phase, advancement decision, blockers, next actions, source summaries, and fingerprint-guarded expansion state. |
| `validation-plan` | Plan read-only validation checks from changed files and optional spec/task context, including check applicability, validation state, and a validation contract. |
| `evidence-quality` | Review task and verification evidence quality, classify evidence strength, and return advisory diagnostics without mutating files. |
| `closure-risk-review` | Aggregate closure readiness, promotion, validation, evidence, follow-up, decision, live-doc risk, and recovery signals into an advisory low/medium/high closure risk payload. |
| `agent-readiness-packet` | Return bounded implementation context for a specific task before coding. |
| `no-active-spec-context` | Return durable docs, backlog, roadmap, closure-log, and archive-index context when no active spec exists. |
| `closure-check` | Report whether a spec is ready to close and list blockers. |
| `prompts` | Validate declarative prompt definitions under `skills/spec-lifecycle-manager/prompts/`. |
| `reconcile` | Produce classified drift findings with observed facts, inferred diagnosis, recommended action, and blind spots. |
| `promotion-plan` | Return durable documentation targets inferred from durable baselines and traceability rows. |
| `review-packet` | Generate a bounded read-only review packet for fast or cheap agent review. |
| `agent-backed-tool` | Run an advisory agent-backed tool through the disabled runner interface and return structured `unavailable` output until a runner adapter is configured. |
| `review-result-template` | Emit the expected review-result disposition shape. |
| `validate-review-result` | Validate accepted, rejected, deferred, and human-decision review-result disposition records. |
| `hook` | Run lifecycle hook checks over changed files, selected specs, selected task IDs, or review-result files. |
| `archive-index` | Validate `docs/history/spec-archive-index.md` entries, retained/removed package state, closure-log consistency, commit evidence fields, and durable destination references. |
| `resolve-spec` | Resolve an active, archived, missing, or ambiguous spec reference without requiring callers to parse path lookup exceptions. |
| `mcp-audit` | Summarize spec lifecycle MCP mentions, explicit errors, and interaction comments in Codex session JSONL logs. |
| `sync-guard` | Report read-only source skill, bundled plugin, installed cache, MCP reload, and recent commit sync state. |
| `package-contract` | Validate the Spec Lifecycle Manager npm package distribution contract, required package files, source/bundle parity, and provenance. |

## MCP Server

Run the local stdio MCP server from the repository source:

```bash
python3 skills/spec-lifecycle-manager/scripts/spec_mcp_server.py /path/to/repo
```

Run it from the bundled plugin source:

```bash
python3 plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py /path/to/repo
```

The Codex plugin defines the installed MCP server in
`plugins/spec-lifecycle-manager/.mcp.json` through the portable
`mcp-launch.mjs` shim. Plugin MCP config must not set `cwd`: the MCP launch cwd
is the target repository, and the shim forwards it as
`SPEC_LIFECYCLE_DEFAULT_REPO_ROOT` while resolving the bundled Python server
from the plugin root. Direct CLI invocation is for local validation, CI, or MCP
debugging. The first optional argument, or `--repo-root`, is the repository root
whose specs should be exposed.

### MCP-First Usage

Agents should call MCP tools before invoking the direct `.py` scripts whenever
the `spec-lifecycle-manager` server is visible. Use the direct CLI commands
only as validation, CI, runtime debugging, or no-MCP recovery surfaces.
Generated agent-facing validation guidance uses MCP tool names for lifecycle
operations such as `scan_specs`, `lint_spec_package`, `next_task`, and
`closure_check`; script equivalents are retained only as recovery/admin
commands.

### MCP Tools

The server exposes lifecycle tools backed by shared runtime internals. Most
tools are read-only. Write-capable tools are narrow, preview-first exceptions:
`set_task_state` is limited to one selected task block in an active spec
package `tasks.md`, while `closure_apply` and `closure_resolve` are limited to
previewed closure record, package cleanup, and cleanup-hash resolution actions.
Write-capable tools default to dry-run and require explicit `write_intent` when
`dry_run` is false.

- `scan_specs`
- `spec_id_inventory`
- `spec_creation_plan`
- `active_spec_preflight`
- `lifecycle_guide`
- `bootstrap_plan`
- `stage_readiness`
- `phase_gate_check`
- `validation_plan`
- `evidence_quality_check`
- `closure_risk_review`
- `agent_readiness_packet`
- `no_active_spec_context`
- `spec_summary`
- `lint_spec_package`
- `lint_doc`
- `next_task`
- `list_tasks`
- `task_details`
- `task_state_audit`
- `set_task_state`
- `closure_check`
- `closure_plan`
- `closure_apply`
- `closure_resolve`
- `archive_index`
- `resolve_spec_reference`
- `mcp_audit`
- `reconcile_spec`
- `promotion_plan`
- `review_packet`
- `agent_backed_tool`
- `task_context`
- `traceability_lookup`
- `prompts_validate`

### Phase Gate Check

Use MCP `phase_gate_check` as the normal agent-facing decision facade. The
retained CLI equivalent is available for validation, CI, MCP debugging, and
explicit no-MCP recovery:

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py phase-gate-check docs/specs/123-example
```

The result reports `requirements`, `design`, `tasks`, `implementation`,
`verification`, `promotion`, `closure`, or `unknown`, with
`ready_to_advance`, bounded findings and actions, applicable authoritative
source summaries, and an evidence fingerprint. Runnable implementation work is
a blocker: `PHASE_GATE_TASK_REMAINS` keeps advancement false and directs the
caller to `continue_task`.

`detail` accepts `compact`, `full`, or `section`. Section expansion uses the
closed set `source_signals`, `coverage`, `validation`, `promotion`, and
`closure` together with the expected evidence fingerprint. A mismatch returns
`stale` and refreshed expansion arguments. Normal output is bounded to 20
findings and 10 actions with a 32 KiB target; blockers are ordered before
advisory findings, and truncation/limit state plus expansion expose omitted
detail.

Artifact freshness is content-based. An `Upstream Fingerprints` table can
produce `current`, `stale`, `review_required`, or `not_applicable`; file
modification time is not proof. The shared core is caller-agnostic, while the
MCP and CLI adapters attach their own invocation provenance. The aggregate does
not replace `lint_spec_package`, task context, validation, promotion, or closure
tools as the authoritative detailed evidence surfaces.

Record accepted upstream evidence in a downstream artifact using exact
repo-relative paths and lowercase SHA-256 values:

```markdown
## Upstream Fingerprints

| Upstream Artifact | Fingerprint |
|---|---|
| `docs/specs/123-example/requirements.md` | `sha256:<64 lowercase hex>` |
```

### Spec ID Inventory And Creation Planning

Use MCP `spec_id_inventory` to obtain `next_available_spec_number` for one
selected docs root. It inventories active and historical prefixes, explicit
legacy upper bounds, confidence, and diagnostics. The result is provisional:
lower gaps are not reused, empty scopes return `000`, and another agent may
claim the number after the call.

Known historical prefix collisions may be recorded in
`[docs-root]/history/spec-id-collision-acknowledgements.json`. An acknowledgement
must name the exact set of colliding spec IDs and explain both the cause and
disposition. A matching acknowledgement preserves a visible
`SPEC_ID_PREFIX_DUPLICATE_ACKNOWLEDGED` informational diagnostic without
reducing allocation confidence; missing, malformed, or stale acknowledgements
remain warnings. Every colliding prefix remains consumed and is never reused.

Use MCP `spec_creation_plan` with an ASCII lower-kebab `slug` to obtain the
proposed ID/path, template fallback chain, artifact set, required values,
preconditions, validation commands, and evidence fingerprint. `reservation` is
always false. Revalidate immediately before creation; stale evidence or
collision returns refreshed arguments and a fresh proposal. A future writer
must atomically claim the directory.

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py spec-id-inventory . --docs-root docs
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py spec-creation-plan my-feature --repo-root . --docs-root docs
```

`scan_specs`, no-active context, and bootstrap reuse the same allocator and
expose the provisional next number and creation-plan action when safe.

`scan_specs` accepts optional `repo_root`, `docs_root`, and
`include_archived_lint` arguments. By default, archived packages remain visible
in scan inventory but are excluded from active authoring lint. Set
`include_archived_lint` to `true` only when intentionally auditing historical
packages against the current templates.

MCP write capability remains intentionally bounded. The server does not create
specs, approve durable promotion, decide residual-risk acceptance, make final
closure decisions, or commit. Closure write tools may update the previewed
closure-log/archive-index targets or remove/archive the previewed spec package
only when the caller supplies an accepted plan, a specific action ID, and
explicit write intent.

### Closure Helper Tools

`closure_plan` previews closure metadata, blockers, validation commands,
recovery commands, active-reference findings, and scriptable closure actions.
It does not mutate files.

`closure_apply` previews or applies one planned closure action from a
`closure_plan` payload. Supported v1 actions are deterministic closure record
rendering and package cleanup actions generated by the shared closure helper.
The tool defaults to dry-run and rejects writes without `write_intent`.
For `closure_action=archived`, the generated cleanup action moves the package
from `docs/specs/<spec-id>/` to `docs/history/archived-specs/<spec-id>/` and
records archive-index status `retained` with closure action `archived`.

`closure_resolve` previews or applies cleanup-commit resolution for matching
closure records after the cleanup commit exists. It defaults to dry-run and
rejects writes without `write_intent`.

The retained no-MCP recovery commands use the same shared implementation:

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-plan docs/specs/123-example --final-spec-commit <commit>
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-apply docs/specs/123-example --plan-file closure-plan.json --action-id render_records
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-resolve . --spec-id 123-example --cleanup-commit <commit>
```

Direct runtime commands are for validation, CI, MCP debugging, and no-MCP
recovery. Normal agent workflows should prefer the MCP tools when the server is
available.

`lifecycle_guide` is the first-run and resume entry point. It classifies the
repository as `active_specs`, `closed_only`, `documented_no_specs`,
`near_blank`, or `blank`; reports docs readiness, template authority, prompt
and hook availability, active-spec readiness summaries, and next actions; and
returns equivalent validation commands for direct CLI recovery.

`bootstrap_plan` is preview-only. It reports the smallest useful lifecycle
foundation for blank or near-blank repositories, including proposed docs paths,
template sources, required user values such as project purpose, validation
commands, assumptions, and deferred architecture or pattern-discovery work. It
does not create files through MCP or CLI.

`stage_readiness` reports whether a spec is ready for a worker agent and
whether it is ready to implement. It checks required artifacts, optional
traceability and verification artifacts, downstream review needs when
requirements or design changed after dependent artifacts, context-budget gaps,
correctness-property mappings to design/task/verification, and explicit
acceptance-criteria coverage. Coverage gaps appear before implementation
readiness so callers can repair traceability instead of discovering missing
proof at closure.

Requirement blocks may include optional MoSCoW priority metadata:

```markdown
**Priority:** must-have
```

Accepted persisted values are `must-have`, `should-have`, and `could-have`.
Missing priority remains compatible and is not a diagnostic by itself.
Persisted shorthand, unknown values, duplicate priority lines, and
`won't-have` values are lint diagnostics; excluded scope should be recorded in
non-goals, out-of-scope text, rejected decisions, or routed residuals.
Acceptance criteria inherit their parent requirement priority because the
runtime does not implement acceptance-criterion-level priority overrides.

When priority is present, requirement coverage records preserve it in
`stage-readiness`, `closure-check`, `closure-risk-review`,
`agent-readiness-packet`, `task-details`, `task-context`, and
`traceability-lookup` payloads wherever those outputs already include parsed
requirement objects or requirement coverage. `must-have` gaps are blocking
unless rejected or human-superseded, `should-have` gaps require route or
residual-risk rationale, and `could-have` gaps may close only when routed,
rejected, or out of current scope. Historical or closed packages without
priority labels do not need migration.

When a package declares broad durable-doc impact, stale-doc risk, imported
sources, or canonical-context intent, lint and readiness surfaces also check for
`canonical-context.md` or embedded `## Canonical Context` sections. Missing
context is warning-level and advisory during authoring/readiness, includes
`advisory: true` and `blocking: false`, and may include an import plan derived
from durable-source references. `canonical-context.md` is optional for small
packages that do not need it. Promotion-only, closure-log, archive-index, or
historical package wording should not be treated as imported-source authority
by itself.

`active_spec_preflight`, `agent_readiness_packet`, and
`no_active_spec_context` are deterministic workflow tools. They compose scan,
next-task, traceability, durable-doc, closure-log, and archive-index context so
agents can decide what to read before implementation. They do not invoke
secondary agents and do not mutate files.

The Agent Readiness Contract is separate from implementation readiness.
`agent_readiness_packet` returns bounded task context for a selected task:
required artifacts, linked requirements and acceptance criteria, design
sections, verification expectations, durable targets, open decisions,
validation commands, and guardrails. `stage_readiness` combines that compact
contract with staged artifact and coverage checks. A payload can be
`ready_for_agent` while `ready_to_implement` is false when downstream review or
coverage gaps still need lead-agent repair.

When `canonical-context.md` exists, the readiness packet includes it in the
review artifact set and adds a guardrail to read it before broad durable-doc
scans. Always-canonical external authorities still outrank spec-local context:
system/developer/user instructions, applicable `AGENTS.md`, governance, policy,
security, generated contracts, source-code contracts, tests, and live/system
evidence.

Context-budget rules favor the smallest complete context: use `task_context`,
`traceability_lookup`, or `agent_readiness_packet` for the selected task before
loading whole packages; avoid archived packages unless doing historical audit;
refresh at phase boundaries after requirements changes, after design changes,
before implementation, and before closure. Agent Workbench or equivalent
repo-evidence providers may add freshness, diagnostics, impact, or validation
planning signals, but they remain optional evidence inputs. They do not prove
completion, decide lifecycle state, promote durable docs, close specs, or
override governance.

`validation_plan` is a read-only planning surface. It accepts:

- `repo_root`: repository root. Defaults to the server-bound workspace.
- `changed_files`: repo-relative or absolute file paths. Empty input returns a
  baseline lifecycle plan for the repository/spec context.
- `spec_path`: optional active spec package path or ID.
- `task_id`: optional task ID used to include traceability and task evidence.
- `risk_level`: optional caller-supplied risk label, preserved in output for
  clients that already classify risk.

Call the MCP `validation_plan` tool for normal agent workflows:

```text
MCP tool: validation_plan
changed_files:
  - skills/spec-lifecycle-manager/scripts/spec_runtime.py
  - docs/specs/019-validation-plan-builder/tasks.md
spec_path: docs/specs/019-validation-plan-builder
task_id: T001
```

The MCP tool returns the same structured payload after normalizing repository
paths for client display.

The planner classifies changed files into path groups such as `runtime`, `mcp`,
`hook`, `tests`, `docs`, `package`, `plugin_bundle`, `spec_package`,
`history`, and `prompts`. Each check includes:

- `id`: stable check ID such as `scan`, `lint-spec`, `unit-tests`,
  `archive-index`, `prompts`, `package-contract`, `sync-guard`,
  `npm-pack-dry-run`, or `git-diff-check`.
- `required`: whether the check is required by the changed-file/task context.
- `applicability`: `required`, `recommended`, `optional`, `not_applicable`, or
  `not_run`.
- `validation_state`: `planned`, `executed`, `blocked`, `inspection_only`, or
  `not_applicable`.
- `reason`: why the check is included.
- `covers`: risks or contracts the check covers.
- `command` or `mcp_tool`: how to run the proof when applicable.
- `blocker` and `residual_risk`: present when an applicable check cannot be
  planned or run because required inputs, tools, credentials, or environment
  are unavailable.

`not_applicable` means the current change/task context does not require that
check. It is not missing validation. `not_run` means the check applies but an
input or environment blocker prevents it from being planned or executed.

Validation state is separate from applicability. `planned` means the proof
method is recommended but has not run. `executed` is used only when task,
verification, or review context supplies concrete evidence. `blocked` means an
applicable proof cannot run. `inspection_only` is reserved for manual review or
inspection proof. `not_applicable` means the proof does not apply.

When task context is available, `validation_plan` may include a
`validation_contract` with:

- `status`: `planned` or `executed`.
- `automated_proof`: check IDs and commands/tools that should prove the task.
- `manual_proof`: inspection-only proof targets.
- `evidence_location`: task or verification locations where evidence should be
  recorded.
- `executed_evidence`: preserved task, verification, or review evidence
  references.
- `residual_risk_if_not_run`: risks left if required planned or blocked checks
  are not completed.
- `false_positive_risk` and `false_negative_risk`: proof risks derived from
  task and changed-file context.
- `gaps`: missing fields or traceability gaps. The planner reports gaps instead
  of inventing generic proof criteria.

Documentation-only changes normally require lifecycle/document checks such as
scan, package lint when a spec is selected, archive or prompt validation when
those files changed, and `git diff --check`. They classify unrelated code
runtime checks as `not_applicable` unless the selected task or evidence context
requires code validation.

`evidence_quality_check` is a read-only advisory MCP check for completed task
evidence and `verification.md` evidence-log entries:

```text
MCP tool: evidence_quality_check
spec_path: docs/specs/020-evidence-quality-check
```

The payload includes:

- `records`: task and verification evidence records with source path, line,
  source type, evidence text, classification, signals, and reason.
- `diagnostics`: warnings or errors for completed tasks and verification rows
  whose evidence is `missing`, `vague`, `weak`, or `not_run`.
- `summary`: counts by classification and source type plus diagnostic totals.
- `advisory: true` and `mutates_files: false`.

Classifications are deterministic heuristics:

- `concrete`: cites commands, file paths, commits, test counts, or explicit
  passing validation signals.
- `vague`: says work is done, complete, implemented, fixed, or passed without
  a concrete proof signal.
- `missing`: evidence is absent or still pending.
- `waived`: records an explicit waiver or accepted risk.
- `deferred`: routes proof to a follow-up, backlog item, or future work.
- `not_applicable`: evidence states validation does not apply and the task is
  docs-only or explicitly tied to a not-applicable validation-plan context.
- `not_run`: evidence says the applicable validation was skipped or could not
  run.
- `weak`: evidence is present but does not meet a stronger classification.

`not_applicable` is intentionally narrow. A bare "N/A" on a code or runtime
task is reported as weak evidence unless surrounding task files or validation
context prove that automated validation does not apply.

`closure_risk_review` is a read-only advisory MCP check for deciding whether a
completed package is ready for durable promotion and cleanup:

```text
MCP tool: closure_risk_review
spec_path: docs/specs/021-closure-risk-review
```

Inputs:

- `spec_path`: active package path or ID through MCP; package path through the
  direct CLI.
- `repo_root`: optional MCP repository root. Defaults to the server-bound
  workspace.

The payload includes:

- `risk_level`: `low`, `medium`, or `high`.
- `recommended_action`: a deterministic next action for the reported level.
- `findings`: classified risk items with severity, source, message, and
  recommended action.
- `blind_spots`: unavailable or untrustworthy signals, such as missing evidence
  records or archive-index errors.
- `signals`: summarized source payloads from `closure_check`,
  `promotion_plan`, `evidence_quality_check`, `validation_plan`, open
  decisions, live documentation scanning, and historical recoverability.
- `summary`: finding counts by severity and classification.
- `advisory: true` and `mutates_files: false`.

Risk levels are intentionally conservative:

- `high`: closure blockers, missing durable promotion targets, unresolved
  decisions, evidence errors, or high-severity live documentation risk.
- `medium`: weak evidence, validation gaps, routed follow-up work, or
  medium-severity live documentation risk.
- `low`: no findings after all available signals are aggregated.

Historical recoverability is reported as a signal, not as permission to keep
misleading live guidance. Matching closure-log and archive-index entries lower
the concern that deleted package details are unrecoverable, but they do not
override current closure blockers, missing durable promotion, unresolved
decisions, weak evidence, or live documentation that may mislead agents or
search users.

Limitations:

- The live documentation scan is heuristic. It looks for lines that combine
  aged-status terms with current-guidance wording under `docs/`, excluding
  `docs/history/` and active package directories.
- The archive recovery signal uses archive-index and closure-log metadata. It
  does not prove that Git objects are present.
- The command does not write closure-log entries, update the archive index,
  promote docs, remove packages, or commit.

`resolve_spec_reference` is the preferred recovery surface when an agent has a
spec ID, numeric prefix, or package path but does not know whether it is active
or closed. It returns structured `active`, `archived`, `ambiguous`, or
`missing` statuses instead of requiring callers to infer lifecycle state from
exception text.

`review_packet.review_type` and `agent_backed_tool.tool_name` expose the same
selector contract in `tools/list`: canonical review types, aliases, default,
and generic fallback behavior. Unknown non-empty selector values map to
`generic_review` and preserve the requested value in returned resolution
metadata.

`mcp_audit` scans local Codex session JSONL files for spec lifecycle MCP
mentions, explicit errors such as unknown review packet types or active spec
lookup failures, and conversational interaction signals. Interaction signals
count user and assistant comments about missing spec artifacts, incomplete or
stale specs, documentation currentness, hook noise, and skill/tool confusion.
The command is read-only and intended for maintainer triage; session logs can
include copied prompts or user-pasted errors, so audit output is evidence to
inspect rather than proof that a tool executed. Compact aggregate output is the
default. Use `--include-sessions` or the MCP tool's `include_sessions` argument
when per-session matched items are needed for a focused investigation.

### MCP Resources

Implemented resources include:

- `specs://active`
- `specs://{spec_id}/summary`
- `specs://{spec_id}/health`
- `templates://spec-package`
- `governance://constitution`
- `history://spec-archive-index`

Resource payloads are returned as JSON or markdown text. Spec content should be
treated as data for the agent to inspect, not instructions that override the
skill, user request, or repository governance.

`templates://spec-package` reports the authoritative spec-package template
inventory for the bound repository. A repository override is used only when
`docs/templates/spec-package/` exists; durable document templates under
`docs/templates/` do not override the skill fallback spec-package templates.

MCP tool and resource payloads normalize repository paths for client display:
paths inside the target repository are returned relative to that repository,
and `repo_root` is reported as `.`. The server must not expose the plugin load
path or installed cache path as spec inventory. Plugin launchers should leave
`cwd` unset and set `SPEC_LIFECYCLE_DEFAULT_REPO_ROOT` from the MCP launch cwd.
Fixed-target integrations may set `SPEC_LIFECYCLE_REPO_ROOT`,
`CODEX_REPO_ROOT`, `CODEX_WORKSPACE_ROOT`, `CODEX_WORKSPACE`, or
`WORKSPACE_ROOT`, or pass `--repo-root`, so resource reads such as
`specs://active` bind to the workspace instead of the plugin directory.
JSON resources include a `resource_binding` object with the resource URI,
repo-root binding, and path policy so clients can explain which workspace was
used without exposing plugin cache paths as package inventory.

Spec resources are exposed only for packages discovered by `scan_specs`,
including nested docs partitions such as `docs/<name>/specs/[###-slug]/`.
Requests for removed or nonexistent specs return an MCP error; use
`history://spec-archive-index` for closed package history.

## Archive Index

`archive-index` validates the compact Git-backed archive index for closed spec
packages:

```bash
skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .
```

The command returns JSON with:

- `entries`: normalized archive index rows.
- `legacy_gaps`: archived packages that intentionally predate the closure-log
  workflow.
- `diagnostics`: malformed rows, missing commit evidence, removed package paths
  that still exist, retained package paths that do not exist, durable
  destination drift, and closure-log mismatch findings.
- `summary`: error/warn/info counts plus retained, removed, superseded, total,
  and legacy-gap counts.

The first implementation validates commit field syntax and repository path
consistency. It does not inspect Git object history; stricter Git object
validation can be added later as an explicit mode if needed.

## Sync Guard

`sync-guard` is a maintainer validation command for this
`agent-dev-lifecycle` repository. Run it after changing the source skill,
bundled plugin, package manifests, installer, or install/runtime docs, and
before claiming the local Codex plugin install is current.

It is not a generic lifecycle check for target repositories that merely use the
skill. When run outside the Spec Lifecycle Manager package repository, it
returns `status: "not_applicable"` instead of reporting missing package paths as
drift.

The command validates local packaging and install freshness without mutating
files, Codex config, installed caches, or runtime sessions:

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .
```

The command returns JSON with:

- `applicability`: reports whether the current repository is the Spec Lifecycle
  Manager package repository.
- `source_bundle_parity`: compares `skills/spec-lifecycle-manager/` with
  `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`.
- `source_claude_parity`: compares `skills/spec-lifecycle-manager/` with
  `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`.
- `bundle_cache_parity`: compares `plugins/spec-lifecycle-manager/` with the
  newest installed cache candidate under
  `$CODEX_HOME/plugins/cache/*/spec-lifecycle-manager/*/`. Installer-managed
  local config files such as `.mcp.json` and `hooks/hooks.json` may differ
  after install because the installer resolves host-specific command details;
  those paths are reported as `allowed_content_differences` and do not by
  themselves create a cache-drift finding.
- `reload_advisory`: reports whether parity state suggests Codex should be
  reloaded after sync and install.
- `commit_evidence`: reviews recent commits touching
  `skills/spec-lifecycle-manager/` and reports whether the same commit touched
  package, installer, manifest, or install/runtime documentation evidence.
- `findings`, `summary`, and `recommendations`: advisory next actions such as
  syncing the bundled plugin, running the package installer, or reloading Codex
  after install.

Use `--codex-home <path>` for fixture validation or non-default Codex homes,
and `--commits <N>` to adjust recent commit evidence depth.

## Package Contract

`package-contract` validates this repository's Spec Lifecycle Manager npm
distribution contract without publishing, installing, or mutating a registry:

```bash
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .
```

The command checks:

- `package.json` is valid JSON and exposes the `ai-spec-lifecycle` bin, plus
  the `spec-lifecycle-manager` compatibility bin.
- `packaging/spec-lifecycle-manager/npm-package.json` is valid JSON and
  includes package name, install command, bin path, registry, publish status,
  payload root, and required path list.
- `packaging/spec-lifecycle-manager/package-manifest.json` and
  `plugins/spec-lifecycle-manager/.codex-plugin/plugin.json` are readable.
- every required package input exists, including the plugin manifest, MCP
  config, hook config, skill scripts, prompts, references, package manifest,
  npm package contract, npm bin, and installer script.
- source skill, bundled plugin skill, and Claude plugin skill contents are in
  sync.
- Git HEAD provenance is reported when available.

The current npm status is `pack-ready-not-published`. CI validates the
candidate package with the same command family exposed by `npm run validate`:
Python tests, Node tests, lifecycle scan, archive-index validation, prompt
validation, package-contract, sync-guard, `npm pack --dry-run --json`, and
`git diff --check`. Validate the tarball contents before publishing with:

```bash
npm pack --dry-run --json
```

The release workflow builds the real tarball with `npm pack`, uploads the
tarball plus `npm-pack.json` and `release-summary.md` as GitHub Actions
artifacts, and publishes to npm only when manually dispatched with
`publish=true` and `NPM_TOKEN` configured. When publish is skipped, the artifact
metadata is still the release evidence. After publish, the intended user
install command is:

```bash
npx @auriora/ai-spec-lifecycle install
```

## Traceability Lookup

The MCP `traceability_lookup` tool resolves a task, requirement, or design
section through `traceability.md` and verifies referenced artifacts where
possible. It is the first deterministic guardrail against implementing from
`tasks.md` alone.

The public tool owner is MCP. The implementation lives in
`skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py` and is used
by MCP tool handlers and retained validation/recovery code. There is no
replacement public CLI command for the retired traceability executable.

Inputs:

- `repo_root`: optional repository root.
- `spec_path`: active spec package ID or path.
- one of `task_id`, `requirement`, or `design`.

Output:

- `spec_path`
- `lookup`
- `traceability_row`
- `task`, when looking up a task
- `requirements`, when referenced requirements are found
- `acceptance_criteria`
- `design_sections`
- `change_impact`
- `verification`
- `durable_targets`
- `open_decisions`
- `gaps`

If MCP is unavailable, run retained `spec_runtime.py` validation commands such
as `lint`, `next-task`, and `closure-check`, then read `traceability.md` and
linked source artifacts directly. Do not call a separate traceability lookup
script.

## Prompt Definitions

Prompt contracts live under `skills/spec-lifecycle-manager/prompts/`.

Implemented definitions:

- `reconcile-spec`
- `choose-next-task`
- `task-context`
- `lint-spec`
- `documentation-wizard`
- `lifecycle-status`
- `lifecycle-validate`
- `lifecycle-complete`
- `lifecycle-triage`

The definitions include names, descriptions, arguments, resource references,
tool references, instructions, return formats, and client-support recovery
guidance. The stdio MCP server exposes these definitions through
`prompts/list` and `prompts/get`.

Lifecycle prompts are convenience aliases:

- `documentation-wizard` guides stage-aware documentation authoring over the
  existing read-only lifecycle tools. It asks one bounded question at a time by
  default, classifies open questions and feedback, keeps edit application
  preview-first, reports durable promotion and closure blockers, and treats
  removed spec packages as historical evidence only. Wizard mode is the default
  for backlog-to-spec and new-spec creation; full-package scaffolding is used
  only when the user explicitly asks for all artifacts at once. Same-stage
  artifact pairs are allowed for `requirements.md` plus `change-impact.md`,
  `tasks.md` plus `traceability.md`, and `verification.md` plus `quickstart.md`
  when those paired artifacts are relevant. `open-decisions.md` remains
  optional and is used only for numerous or cross-cutting decisions.
- `lifecycle-status` routes "what next" and status requests to active preflight
  or no-active-spec context.
- `lifecycle-validate` routes validation requests to scan, lint, prompts,
  archive-index, and closure checks.
- `lifecycle-complete` routes completion requests through durable promotion and
  closure readiness before cleanup.
- `lifecycle-triage` classifies requests as `trivial`, `small`,
  `spec-needed`, `review`, or `closure` before choosing a workflow.

## Hook Modes

The hook runner supports advisory and blocking profiles.

Task parsing recognizes the checklist markers used by `tasks.md`: `[ ]`
pending, `[~]` in progress, `[/]` partial, `[>]` follow-up or routed, `[-]`
no-op or deferred, `[?]` review or decision needed, `[!]` attention needed, and
`[x]` complete. Compatibility markers remain readable during migration: `[Y]`
maps to `partial`, while `[*]` and `[e]` map to `attention` and preserve a
`legacy_marker` payload value for consumers that need the old distinction. Only
`[x]` is treated as complete. `next-task` can select pending, in-progress, and
partial tasks when dependencies are satisfied; follow-up, no-op, review-needed,
and attention tasks are reported as blocked until their marker is changed.

Parsed task payloads include normalized state, the source marker,
`legacy_marker` when applicable, parent and child task IDs, status notes, and
the optional metadata fields used for routed work and evidence-depth tracking:
`Evidence mode:`, `Follow-up:`, `Destination:`, `Decision owner:`,
`Upstream specs:`, and `Downstream specs:`.

Evidence mode is part of the completion contract. `implementation` and
`validation` can complete ordinary implementation tasks when task acceptance is
met. `planner`, `contract`, `dry_run`, `routing`, `no_op`, and
`blocked_output` evidence modes are advisory or non-implementation evidence
unless the task acceptance explicitly says that mode satisfies the task.
`task-state-audit` reports broad tasks with `split_task_suggestions` when one
checkbox spans multiple source families, evidence modes, implementation
outcomes, validation surfaces, profiles, or cross-spec dependencies.

## Canonical Context Diagnostics

`canonical-context.md` is an optional spec artifact for working-context
authority. The runtime reports advisory diagnostics when a package names stale
or non-canonical docs, imported or adapted durable sources, supersession,
durable source mapping, broad durable-doc impact, or canonical-context intent
without providing `canonical-context.md` or embedded `## Canonical Context`
sections.

Agents should inspect the concrete risk before creating `canonical-context.md`;
the missing-context diagnostic is not a closure blocker by itself.

The canonical-context template uses these stable sections:

- `Purpose`
- `Authority Hierarchy`
- `Always-Canonical External Sources`
- `Spec-Canonical Working Sources`
- `Imported Sources`
- `Non-Canonical Background Sources`
- `Promotion Map`

Lint warns when imported canonical sources with `copied`, `adapted`,
`summarized`, or `supersedes` status lack source path, canonical scope, or
promotion target metadata. Closure check blocks when a promotion-map row is
marked required before closure but has no durable destination, route, or discard
rationale. `promotion-plan` treats canonical-context promotion-map destinations
as candidate durable targets.

| Hook | Purpose |
| --- | --- |
| `spec-file-changed` | Return hierarchy-aware authoring guidance for affected spec packages from changed files. |
| `task-checkbox-changed` | Check completed tasks for evidence. |
| `template-changed` | Lint changed markdown templates. |
| `implementation-task-complete` | Check selected or completed tasks for evidence, file metadata, and changed-file alignment. |
| `verification-updated` | Check verification artifact structure and references to task and requirement IDs. |
| `spec-resumed` | Run resume checks for lint, old-format packages, closed status, and stale review dates. |
| `spec-close-check` | Convert closure readiness blockers into hook diagnostics. |
| `set-task-state` | Audit the changed task after a guarded state update. |
| `agent-slice-start` | Check selected task traceability before an agent starts implementation. |
| `agent-response-check` | Check claimed task completion against evidence and changed files. |
| `review-packet-dispatch` | Validate bounded read-only review packet shape before dispatch. |
| `review-result-recorded` | Validate review-result disposition records. |

These runtime checks are reusable by Git hooks, Codex hooks, Agent Workbench
hooks, or direct CLI invocations. Blocking profile adoption should remain a
separate dogfood and promotion decision.

Noise policy: hooks stay quiet when state and evidence agree, collapse repeated
task-audit findings by task ID and classification, and reserve repeated
reminders for state contradictions, preflight summaries, or explicit
task-state writes. In ordinary `tasks.md` authoring, `[~]` with
`Evidence: Pending.` is an expected task-start state, not a completion-evidence
failure. `task-checkbox-changed` should therefore avoid warning on that pattern
unless the edit is an explicit task-state audit or part of a resume, completion,
or close check. Advisory mode is the default; blocking use remains an explicit
repository adoption choice.

Path policy: hook payloads and user-facing hook context use repo-relative paths
for files inside the target repository. Absolute host paths are allowed only
when the referenced file is outside the repository boundary.

`spec-file-changed` is intentionally narrower than full package lint. During
ordinary authoring it inspects the changed artifact in the context of the spec
tree and reports:

- the authoring mode, such as `initial_authoring`, `revision`, `task_update`,
  `verification_update`, or `closure_check`;
- changed artifacts and existing artifacts in the package;
- missing prerequisite artifacts for the changed file;
- existing downstream artifacts that may need review after an upstream
  revision;
- the next useful authoring step when there is one;
- relevant helper surfaces such as `templates://spec-package`, `scan_specs`,
  `active_spec_preflight`, `task_context`, or `traceability_lookup`.

Wizard authoring lint is also staged by default. Use MCP `lint_spec_package`
for normal package lint; it validates the current wizard stage instead of
requiring all downstream artifacts:

```text
MCP tool: lint_spec_package
spec_path: docs/specs/123-example
```

Use full-package validation only when explicitly needed for closure, recovery,
or a requested full scaffold. Through MCP, request full package lint where the
client exposes the mode argument:

```text
MCP tool: lint_spec_package
spec_path: docs/specs/123-example
mode: full
```

If one write creates artifacts from multiple wizard stages, the hook reports
`WIZARD_BATCH_ARTIFACT_CREATION` to ask the agent to confirm the user requested
full scaffolding before continuing.

When an upstream artifact such as `requirements.md` or `design.md` is revised
after downstream artifacts already exist, the hook reports those downstream
files as review candidates. It does not present them as the next missing step.
Use explicit `lint`, `spec-resumed`, `verification-updated`, or
`spec-close-check` when full package health is the desired signal.

## Codex Hook Wrapper

`codex_spec_lifecycle_hook.py` is an advisory Codex `PostToolUse` wrapper. It
parses Codex write-tool payloads, extracts changed files, and calls the
runtime hook checks for relevant spec lifecycle files:

| Changed file | Runtime hook |
| --- | --- |
| `docs/**/specs/**/*.md` | `spec-file-changed` |
| `docs/**/specs/**/tasks.md` | `task-checkbox-changed` |
| `docs/templates/**/*.md` or `skills/spec-lifecycle-manager/references/**/*.md` | `template-changed` |

The wrapper is quiet when checks pass. When advisory diagnostics are found, it
emits Codex `additionalContext` for the current turn and exits with status 0.
For ordinary spec authoring writes, the wrapper can also emit concise
next-action guidance even when there are no lint errors. It does not block
edits, modify files, update task evidence, or install itself.

To avoid repeating the same advisory output when a client emits duplicate
post-write events, the wrapper keeps a short debounce cache for identical
post-write file states. The default window is 45 seconds. The cache key includes
the repository, hook name, spec package, changed file set, and changed file
content fingerprint, so a new edit in the same spec package is checked again
instead of being hidden by the debounce.

Debounce settings:

| Environment variable | Default | Behavior |
| --- | --- | --- |
| `SPEC_LIFECYCLE_HOOK_DEBOUNCE_SECONDS` | `45` | Set to `0` to disable duplicate-event debounce. |
| `SPEC_LIFECYCLE_HOOK_DEBOUNCE_PATH` | Next to the hook log | Override the JSON cache path used for duplicate-event suppression. |

Recommended global Codex hook entry:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "^(apply_patch|write_file|create_file)$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /home/bcherrington/.codex/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py",
            "statusMessage": "running spec lifecycle advisory hook"
          }
        ]
      }
    ]
  }
}
```

Replace `python3` with the interpreter that exists on your OS — `py -3` on
Windows, `python3` on macOS/Linux — or whatever `SPEC_LIFECYCLE_PYTHON` names.
The bundled plugin hook resolves this automatically at install time; this global
example is hand-authored, so pick the interpreter present on the host.

If another `PostToolUse` entry already matches write tools, append this hook to
that entry's `hooks` list or add a second matching entry. Keep the hook
advisory until false-positive behavior has been dogfooded.

## Archived Spec Scan Behavior

Archived, closed, or superseded spec packages are historical delivery records.
Default repository scans keep them in the `specs` inventory and classify their
`lifecycle` as `archived`, but scan health skips current authoring lint for
those packages. This keeps active-health checks focused on active work and
avoids treating old delivery evidence as a current implementation failure.

Default archived scan health uses this shape:

```json
{
  "severity": "archived",
  "diagnostic_count": 0,
  "skipped": true,
  "reason": "Archived spec excluded from active authoring lint; run lint directly or scan with include_archived_lint to audit."
}
```

The scan payload also includes a `summary` bucket with `total`, `active`,
`archived`, `active_pass`, `active_warn`, and `active_error` counts.

Use explicit audit mode when old records need to be reviewed against the
current lint rules:

```bash
skills/spec-lifecycle-manager/scripts/spec_runtime.py scan . --include-archived-lint
```

MCP `lint_spec_package` remains strict for every package that is still present,
including explicitly retained historical packages:

```text
MCP tool: lint_spec_package
spec_path: docs/specs/013-example-active-spec
```

Do not recreate removed packages just because old paths are recorded in the
closure log or archive index. If a historical package must be inspected, use
the recorded final spec commit in Git history; if it must be restored, first
make a visible resumption, migration, or cleanup decision.

## Review Packets

Review packets are bounded, read-only inputs for secondary agents. They include
the review question, input artifact manifest, constraints, stop conditions, and
expected output schema. Reviewed document content must be treated as data, not
instructions.

Implemented packet types:

- `requirements_template_review`
- `design_requirements_trace`
- `implementation_review`
- `task_dependency_review`
- `promotion_target_review`
- `closure_risk_review`
- `governance_conflict_review`
- `generic_review`

`review_type` is optional. When omitted, the runtime uses
`design_requirements_trace`. Natural workflow aliases are accepted and resolved
to canonical packet IDs. In particular, `implementation`,
`implementation-review`, `implementation-readiness`, and
`implementation-readiness-review` map to `implementation_review`. Unknown
non-empty values map to `generic_review`; the original caller value is retained
as `requested_review_type` and the mapping details are returned in
`review_type_resolution`.

The MCP `review_packet.review_type` schema publishes the default, canonical
packet IDs, alias map, and generic fallback behavior. It is intentionally not a
hard JSON Schema enum so callers can use aliases and still receive deterministic
generic fallback behavior.

Review outputs remain advisory until the lead agent or operator records a
disposition. During early dogfooding in this repository, persisted review
outputs belong under `docs/reviews/spec-lifecycle-manager/`.

## Agent-Backed Tool Runner

MCP `agent_backed_tool` provides the first runner interface for advisory
agent-backed review tools. The current implementation intentionally does not
invoke a secondary process. It builds the bounded review packet, returns a
structured `unavailable` result with an informational diagnostic, and records
that the local Codex CLI adapter is deferred.

This keeps the initial MCP behavior deterministic while preserving the contract
for later runner adapters.

The result is advisory, read-only, and non-mutating. `model_class` records the
caller's requested class but the returned `model_class` is `disabled` while no
runner is configured.

Schema helpers for review packets, review-result dispositions, and disabled
runner results live in `spec_agent_schemas.py` so contracts stay
dependency-free without expanding the main runtime file.

When a later runner returns a useful but incomplete result, route follow-up work
to backlog, roadmap, a focused follow-up spec, or a human decision record. Do
not treat secondary-agent recommendations as accepted repository state until a
lead agent or maintainer records the disposition.

Write-capable agent-backed tools are out of scope for this runtime contract
until a separate spec defines sandboxing, permission boundaries, review,
rollback, and evidence requirements.

## Operational Notes

- The runtime does not edit files.
- The runtime does not execute commands found in spec text.
- JSON outputs are intended to be stable enough for hooks and MCP wrapping.
- Archived or old-format specs are detected but not migrated automatically.
- Archived packages are excluded from active-health scan lint by default;
  explicit lint and scan audit modes remain available.
- Closure-log and Git-backed archive behavior is covered by the separate
  `005-spec-closure-log-management` spec.
- The stdio MCP adapter is read-only and dependency-free. It is not yet packaged
  as an Agent Workbench plugin installer.
