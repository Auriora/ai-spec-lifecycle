---
name: spec-lifecycle-manager
description: Manage AI-assisted implementation specs from intake through reconciliation, implementation, durable documentation promotion, expert review, and closure. Use when creating, continuing, reconciling, reviewing, implementing from, promoting, or closing spec packages, especially under docs/specs/[###-slug]/.
copyright: Copyright 2026 Auriora
license: GPL-3.0-or-later
compatibility: Requires Codex with Agent Skills support, Python 3.9+, and repository docs using AGENTS.md or equivalent instructions; MCP and hooks are optional but supported.
metadata:
  author: Auriora
  version: "0.1.0"
  bundled_in_plugin: spec-lifecycle-manager
---

# Spec Lifecycle Manager

Use this skill to align temporary implementation specs, durable documentation,
code, tests, and configuration. The governing lifecycle is:

```text
durable docs -> active spec -> code/tests/config -> durable docs -> close spec
```

Specs are delivery scaffolding, not the final source of truth. This entrypoint
contains mandatory rules and direct routing. Load named references only when
their detail is needed.

## Repository and template discovery

Before changing files:

1. Read root `AGENTS.md` or equivalent instructions and every deeper instruction
   file governing target paths. If none are available in the session, give one
   short `/init` hint and do not repeat it.
2. Inspect the root README and documentation direction: indexes, governance,
   lifecycle notes, templates, backlog, roadmap, closure log, and archive index.
3. Resolve the docs root. Default to `docs/`; preserve an established named
   partition such as `docs/<name>/`.
4. Locate active packages under `[docs-root]/specs/[###-slug]/` and read all
   available artifacts before implementing. Never implement from `tasks.md`
   alone.
5. Identify durable-doc targets and template authority from the repository.

Repository templates are authoritative. `docs/templates/spec-package/`, or an
explicit equivalent, overrides `references/spec-package/` for temporary spec
packages. A durable-doc template directory alone is not a spec-package
override. For durable docs, use repository templates first and
`references/durable-doc-templates/` only when no documented alternative exists.

If no active package exists and the user asks to start one, create the smallest
useful package for the risk. Otherwise use durable docs, backlog, roadmap,
closure records, and the archive index. Do not recreate deleted packages or
treat historical paths as active unless the user requests audit or restoration.
When several packages are active, follow documented sequencing; ask only when
repository evidence does not determine the next blocking slice.

## Lifecycle stages and gates

Use these stages unless a recorded design-first exception applies:

1. **Intake** - establish purpose, scope, constraints, docs root, templates, and
   whether a spec is warranted.
2. **Requirements** - define observable behavior and acceptance criteria.
3. **Design** - define boundaries, interfaces, data, failures, migration,
   operations, testing, and durable-doc impact.
4. **Tasks** - create traceable, dependency-aware, verifiable slices.
5. **Reconcile** - compare package claims with repository truth.
6. **Implement** - execute one coherent slice and maintain state and evidence.
7. **Verify and review** - run proportionate checks and required expert review.
8. **Promote** - move lasting knowledge into durable documentation.
9. **Close** - resolve unowned work and unpromoted truth, record closure, and
   archive or remove the package according to policy.

Keep these gates distinct:

- `ready_to_implement`: requirements, design, task scope, dependencies,
  traceability, and readiness context suffice for the slice.
- `ready_to_validate`: implementation is complete enough for the validation
  plan, without an unresolved implementation blocker.
- `ready_to_close`: acceptance, evidence, reviews, promotion, and deferred-work
  routing are complete.
- `ready_to_archive`: closure metadata and final commit references are complete
  and cleanup will not discard current truth.

Structural lint success does not prove any gate. A well-formed package may not
be implementation-ready; passing tests may still leave promotion incomplete.

Requirements normally precede design. A design-first exception is allowed only
when exploration is needed to make requirements testable. Record the reason,
time-box it, and review downstream artifacts after requirements stabilize.

For a blank or near-blank repository, use preview-first bootstrap mode. Record
project purpose, propose only the minimum useful docs foundation, do not require
architecture docs without evidence, and keep writes inside lifecycle/docs paths
unless source changes were requested.

## Artifact, task, traceability, and evidence semantics

Every active package normally contains:

- `requirements.md`: numbered requirements, priority, rationale or user story,
  and independently testable acceptance criteria; prefer EARS-style clauses.
- `design.md`: current approach, boundaries, decisions, failure and operational
  behavior, validation strategy, risks, and promotion targets.
- `tasks.md`: ordered slices with stable IDs, dependencies, requirement/property
  links, affected files, acceptance, and evidence.

Add optional artifacts only when useful: `change-impact.md`, `traceability.md`,
`verification.md`, `canonical-context.md`, `research.md`, `quickstart.md`,
`open-decisions.md`, contracts, or checklists. Detailed shapes are in
`references/spec-package/`.

Use stable IDs such as `Requirement 3`, `AC2`, `CP-004`, `T007`, and `T007.1`.
Traceability must connect requirements and criteria through design and tasks to
implementation and verification. Update both sides when relationships change.

Task markers are:

- `[ ]` pending
- `[~]` in progress
- `[/]` partial
- `[>]` routed to follow-up
- `[-]` no-op or deferred
- `[?]` review or decision required
- `[!]` attention required
- `[x]` complete

Legacy `[Y]`, `[*]`, and `[e]` remain readable during migration but must not be
introduced. Only one implementation task should normally be in progress. Mark
the selected task `[~]` before implementation. Mark `[x]` only when acceptance
and declared evidence are satisfied. Other outcomes need a truthful marker and
reason.

Evidence must name what was checked and the result. Prefer repo-relative paths
and stable commands. Supported modes are:

- **command**: reproducible command and outcome;
- **artifact**: inspected output, diff, report, or runtime record;
- **manual**: bounded human check with reviewer and result;
- **reasoned**: explicit reasoning, limits, and residual risk;
- **external**: referenced CI, issue, deployment, or approval record.

`Pending` is not completion evidence. An advisory warning about in-progress
work with pending evidence is expected while work is active but must be resolved
before completion.

For old `spec.md`, `plan.md`, or checkbox-only packages, explicitly choose to
continue the current format for this slice, migrate first, or create a follow-up
migration task. Record template authority and any canonical-context decision.
Follow `references/migration-guide.md`; never perform an unannounced wholesale
template migration.

## Reconcile before implementation

Reconcile when work resumes or relevant repository state changes:

1. Read requirements, design, tasks, context, verification, and traceability.
2. Inspect relevant code, tests, config, durable docs, commits, and worktree.
3. Classify differences as `already implemented`, `partially implemented`,
   `not implemented`, `obsolete`, `conflicting`, `unverified`, or `unpromoted`.
4. Repair status, dependencies, acceptance, traceability, and evidence.
5. State the smallest safe next action and unresolved decisions.

Never infer implementation from checkboxes alone. Do not redo working code
merely because a task is stale: update the package and verify behavior. Route
defects or performance work outside scope to the owning backlog or a focused
follow-up spec.

## MCP-first access and CLI recovery

Use spec-lifecycle-manager MCP when available. Prefer bounded calls:

- orientation: `lifecycle_guide`, `scan_specs`, `active_spec_preflight`;
- creation: `spec_id_inventory`, `spec_creation_plan`;
- task work: `task_context`, `set_task_state`;
- traceability/closure: `traceability_lookup`, `closure_check`, `archive_index`;
- validation: `prompts_validate` and exposed runtime/package checks.

Request compact or targeted detail first and expand only the blocking section.
Creation plans are read-only proposals, not reservations. Revalidate their
fingerprint immediately before creation and never reuse a stale proposal.

Direct `spec_runtime.py` calls are for validation, CI, explicit no-MCP recovery,
or MCP debugging; label their use clearly. Typical forms:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .
PYTHONDONTWRITEBYTECODE=1 python3 skills/spec-lifecycle-manager/scripts/spec_runtime.py active-spec-preflight .
PYTHONDONTWRITEBYTECODE=1 python3 skills/spec-lifecycle-manager/scripts/spec_runtime.py task-context . T001
PYTHONDONTWRITEBYTECODE=1 python3 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check .
PYTHONDONTWRITEBYTECODE=1 python3 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .
PYTHONDONTWRITEBYTECODE=1 python3 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts
```

Use current runtime help rather than inventing commands. Do not call retired
standalone helpers when MCP or direct artifact inspection is the supported path.

Hooks are advisory accelerators. They may suggest refresh, lint, traceability,
verification, or closure checks, but hook execution is not proof that the agent
explicitly chose a tool or that a gate passed. Attribute calls to hooks when
evidence shows hook execution.

## Agent Readiness Contract and context budget

Before implementation, obtain `task_context` when MCP exists and ensure the
selected slice provides:

- task ID, state, objective, dependencies, and acceptance criteria;
- linked requirements, decisions, properties, and traceability;
- affected boundaries and durable promotion targets;
- validation commands or evidence expectations;
- relevant instructions and worktree cautions;
- blockers, decisions, risks, and freshness limits;
- the smallest executable next action.

If a field required for safe implementation is missing, repair the package or
ask the narrow decision before coding. Read source artifacts when compact
context omits detail; summaries do not replace authoritative files.

Treat context as a budget. Start with compact orientation and one task. Expand
only requested or blocking sections, reuse fresh results, and avoid repeatedly
loading the whole package. Never omit a safety boundary, acceptance criterion,
decision, or promotion obligation merely to save tokens.

Agent Workbench or equivalent evidence can establish repository freshness,
targeted context, diagnostics, impact, and a validation plan. It is input to
judgment, not proof. Recover from sparse output through indexes, targeted
inventory, and direct reads. See
`references/agent-workbench-evidence-boundary.md`.

## Implement

Confirm the user requested changes, the task is ready, the worktree was
inspected, and planned files are in scope. Preserve unrelated edits. Implement
the smallest coherent slice and update design/tasks when implementation changes
a decision, dependency, or acceptance boundary. Do not silently widen scope.

`set_task_state` is the preferred guarded state writer when available. A
read-only context or plan call does not authorize writes. Enable write-capable
agent tools only when the user requested mutation, the target is exact, and the
tool approval and safety contract is satisfied.

When implementation fails, retain truthful state. Record partial progress,
failure evidence, and recovery; never mark completion by weakening acceptance or
deleting evidence. If an action needs new authority, external coordination,
secrets, destructive work, or a material product decision, request direction.

## Verification, expert review, promotion, and closure

Verification is risk- and requirement-based. Derive the plan from acceptance,
changed surfaces, instructions, and failure modes. Run focused checks during
implementation and required full checks before completion. Record commands,
outcomes, skipped checks, environmental limits, and residual risks.

For ordinary verification-state updates, assess the validation plan and evidence
quality first. Do not automatically run whole-package lint. Run structural lint
when structure changed, a hook reports structural risk, the task requires it, or
a lifecycle gate calls for it.

Use expert review when changes cross architecture, security, privacy, data,
operations, governance, or documentation-authority boundaries. Reviewers inspect
actual artifacts, distinguish blocking from advisory findings, and record
disposition. Detailed roles and routing are in
`references/document-routing-and-expert-review.md`.

Before closure, promote lasting elements:

- behavior to durable requirements, reference, contract, or test docs;
- design decisions to design, architecture, or ADRs;
- operational and recovery knowledge to runbooks or guides;
- ready unfinished work to follow-up specs/issues;
- unrefined work to backlog and sequenced work to roadmap;
- audit-only evidence to the repository's review/history location.

Durable docs must distinguish current, accepted, proposed, and historical
content and identify source of truth and change rules. Follow
`references/durable-document-contract.md`; do not promote temporary coordination
detail.

Closure requires:

1. verified disposition for every requirement and acceptance criterion;
2. truthful task markers and evidence;
3. no unexplained traceability gaps;
4. durable docs matching current behavior;
5. owned destinations for deferred/follow-up work;
6. required tests, lint, package checks, and reviews passing or explicitly
   excepted;
7. closure log and archive metadata identifying implementation commit,
   closure/cleanup state, package disposition, and durable targets.

Commit boundaries must be auditable. Do not claim a cleanup commit before it
exists. Reconcile pending metadata after the final cleanup commit when needed.
Remove an active package only under repository policy and after promotion;
otherwise archive it with explicit historical status.

## Write, privacy, safety, and approval boundaries

- Repository instructions, user scope, and tool permissions are hard boundaries.
- Analysis stays read-only unless the user requests change. File edits, state
  changes, commits, pushes, issue creation, and write-capable tools are mutations.
- Resolve exact targets before destructive or broad operations, prefer
  reversible actions, and preserve user work.
- Never expose secrets, credentials, private session content, personal data, or
  sensitive tool output in specs, evidence, logs, prompts, or commits. Record a
  safe category and remediation path.
- Minimize imported chat/session evidence, redact sensitive content, and respect
  the source system's privacy boundary.
- Require human approval where governance, security, release policy, external
  communication, destructive action, or a tool contract requires it.
- Report uncertainty and provenance; distinguish repository evidence, runtime
  evidence, external evidence, and inference.

## Direct expansions

Load only the expansion needed:

- `references/spec-package/` - fallback active-package artifact shapes.
- `references/migration-guide.md` - package migration, template authority, and
  canonical-context decisions.
- `references/document-routing-and-expert-review.md` - durable routing, cleanup,
  and reviewer responsibilities.
- `references/durable-document-contract.md` - durable status, provenance,
  validation, governance, and anti-patterns.
- `references/agent-workbench-evidence-boundary.md` - permitted use and limits of
  repository-evidence providers.
- `references/durable-doc-templates/` - optional durable-doc fallbacks.

Keep this entrypoint and distributed Codex/Claude copies byte-for-byte
equivalent. Governing changes require matching source, bundle, reference, test,
and installed-package validation.
