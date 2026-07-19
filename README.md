<!--
Copyright 2026 Auriora

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Spec Lifecycle Manager

Spec Lifecycle Manager helps people and coding agents take a change from an
initial idea through requirements, design, implementation, verification, and
durable documentation without losing the reasoning that connects those stages.

It is available as a plugin for Codex and Claude Code. The plugin provides an
agent skill, structured MCP tools, guided prompts, reusable templates, and
advisory hooks for repositories that use AI-assisted development.

## Why Use It?

Implementation specs are useful while a change is being built, but they should
not become a second, increasingly stale documentation system. Spec Lifecycle
Manager treats them as temporary delivery scaffolding:

```text
durable docs -> active spec -> code, tests, and config -> durable docs -> close spec
```

This gives you a repeatable way to:

- turn an idea or backlog item into clear requirements, design, and tasks;
- give an agent a bounded, traceable implementation slice;
- reconcile a spec with the repository before resuming work;
- connect requirements, tasks, code changes, and verification evidence;
- identify decisions, blockers, residual risks, and required reviews;
- promote accepted behavior into durable documentation; and
- close temporary spec packages without losing their history.

The workflow scales down for small changes and adds detail only when risk,
scope, or governance requires it.

## Install

You need Node.js 18 or newer and Python 3.10 or newer. Windows, macOS, and Linux
are supported.

The supported distribution is the npm package tarball attached to a GitHub
release. Install the latest released package globally:

```bash
npm install -g https://github.com/Auriora/ai-spec-lifecycle/releases/download/v0.5.0/auriora-ai-spec-lifecycle-0.5.0.tgz
```

### Codex

Install or refresh the plugin:

```bash
slm install
```

Confirm that Codex can see it:

```bash
codex plugin list
```

The installer resolves a compatible Python interpreter, installs the
self-contained plugin, and removes older managed standalone skill, MCP, and
hook entries. To target a different Codex home, run:

```bash
slm install --codex-home ~/.codex
```

### Claude Code

Add the version-pinned marketplace and install the plugin:

```bash
claude plugin marketplace add https://raw.githubusercontent.com/Auriora/ai-spec-lifecycle/main/packaging/spec-lifecycle-manager/marketplace-pinned.json
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

Confirm that it is installed and enabled:

```bash
claude plugin list
```

For offline installation, download and unpack the release tarball, then use its
bundled marketplace:

```bash
tar -xzf auriora-ai-spec-lifecycle-0.5.0.tgz
claude plugin marketplace add ./package
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

See the [installation reference](docs/reference/spec-lifecycle-manager-mcp-install.md)
for interpreter selection, package boundaries, repository-local development, and
troubleshooting.

### Develop from this checkout

Run the public CLI directly from source without installing or changing the
user-wide package:

```bash
./slm --help
./slm specs
./slm tasks 039
./slm -C /path/to/another-repository specs
```

The root launcher delegates to the same Node dispatcher and bundled Python CLI
as the package. It needs only the documented Node and Python prerequisites; no
virtual environment or npm install is required. To use `slm` without `./` for
the current shell:

```bash
export SLM_SOURCE_ROOT="$PWD"
export PATH="$SLM_SOURCE_ROOT:$PATH"
slm specs
```

Start a source-backed Codex session without replacing the user-wide packaged
plugin:

```bash
scripts/codex-spec-lifecycle-dev.sh
```

That session disables packaged plugins, discovers the lifecycle skill from
`.agents/skills`, and loads the MCP server and advisory hook from `.codex/`.
User-wide installation is reserved for npm or GitHub release artifacts.

## Inspect Lifecycle State With `slm`

The installed package exposes one public executable, `slm`. Its inspection
commands are read-only; `slm install` is the explicit package-install action.
Bare `slm` is equivalent to `slm specs`.

```bash
slm                         # active specs, health, task progress, and next task
slm specs --all             # active and historic specs
slm tasks 039               # tasks for one active spec
slm tasks 039 --pending     # literal [ ] tasks only
slm tasks 039 --open        # every non-terminal open task state
slm tasks 039 --complete
slm tasks 039 --next        # dependency-aware next task
slm next 039                # equivalent next-task form
slm requirements 039
slm requirements 039 --priority must-have
slm requirements 039 --missing-priority
slm history --removed --limit 10
```

Use a full ID, unique numeric prefix, slug, or package path where a command
accepts `SPEC`. If the argument is omitted, `slm` selects the only active spec;
when several are active it lists candidates and asks you to choose. Filters are
unions: task selectors and repeatable `--state STATE` may be combined, except
that `--next` is exclusive. `--pending` means literal pending, while `--open`
also includes in-progress, partial, review-needed, and attention states.

Add `--json` for one deterministic, versioned JSON document, and use `-C PATH`
or `--repo PATH` to inspect a repository explicitly:

```bash
slm -C ../example-repository specs --json
```

The package no longer exposes the unused `spec-lifecycle-manager` or
`ai-spec-lifecycle` executable aliases. Update scripts to call `slm`. The
checkout-only `slc` command remains a separate maintainer wrapper for tests,
bundle synchronization, packaging, release checks, and other development
operations. Coding agents should continue to prefer the plugin's structured
MCP tools for lifecycle context and decisions.

## Use It as a Person

Ask your coding agent for the outcome you want. You do not need to know the
runtime command names or choose every lifecycle artifact yourself.

Example requests:

```text
Use the spec lifecycle manager to turn this feature idea into an implementation-ready spec.
```

```text
Reconcile the active spec with the code and durable docs, then tell me the next safe task.
```

```text
Give an agent the context and validation contract for task T004 before implementation starts.
```

```text
Check whether this spec is ready to close and show me every remaining blocker.
```

```text
Promote the accepted behavior into durable docs and close the completed spec.
```

For guided spec creation, the agent should use the documentation wizard. It
moves through discovery, requirements, design, and tasks one stage at a time,
asking focused questions where your decision is needed. Ask for a compact pass
if you prefer a shorter checklist-style interaction.

You remain the decision maker for product intent, tradeoffs, approvals,
accepted residual risk, and irreversible actions. The plugin supplies structure
and evidence; it does not silently make those decisions for you.

## How to Do Spec-Based Coding

Spec-based coding means agreeing what should be built before asking an agent to
change code, then implementing the agreed work in small, verifiable slices. The
spec connects intent to design, tasks, code, tests, and documentation; it is not
just a long prompt saved in a file.

The following workflow is suitable for a feature, bug fix, refactor, migration,
or other non-trivial change.

### 1. Start with the outcome

Describe the problem, the users affected, the result you want, and important
constraints. Ask the plugin to inspect the repository before proposing a spec:

```text
Use the spec lifecycle manager to create a spec for adding CSV export to the
reporting screen. Preserve current permissions, support exports up to 50,000
rows, and do not change the report filters. Guide me through the decisions.
```

The agent discovers repository instructions, existing behavior, durable docs,
templates, governance, active specs, and relevant code. If the idea is not yet
ready for implementation, it should remain in the backlog rather than becoming
an artificial full spec.

### 2. Agree the requirements

The agent creates or updates `requirements.md` with user stories, goals,
non-goals, testable acceptance criteria, and correctness properties. Review the
behavioral contract before moving on.

At this stage, answer product questions and correct scope. A useful instruction
is:

```text
Walk me through the requirements one decision at a time. Do not write the
design until I approve the required behavior and non-goals.
```

The requirements describe *what must be true*, without prematurely locking in
the implementation.

### 3. Review the design

Once requirements are accepted, the agent develops `design.md`. It should map
the requirements to components, interfaces, data flow, failure handling,
security, operations, and a validation strategy. Existing architectural and
code-derived contracts still take precedence over invented design choices.

Ask the agent to make tradeoffs and open decisions explicit:

```text
Propose the design for the accepted requirements. Show alternatives, risks,
affected interfaces, and any decision I must make before task planning.
```

Do not proceed to implementation while a blocking design or governance decision
is unresolved.

### 4. Approve the implementation plan

The agent turns the approved requirements and design into ordered tasks in
`tasks.md`. Larger changes also use `traceability.md` so each task points back
to its requirements, design sections, validation, and durable documentation
targets.

Tasks should be small enough to implement and verify coherently, with explicit
dependencies, likely files, acceptance criteria, and expected evidence. Ask:

```text
Create the implementation tasks and traceability. Identify the first
dependency-complete slice, but do not change source code yet.
```

This is the final point to correct sequencing or scope before coding begins.

### 5. Implement one slice

Ask the agent to implement one selected task or closely related group of tasks:

```text
Implement T004 from the active spec. Read its linked requirements, design,
traceability, verification, and durable sources first. Show the scope and
validation contract before editing, then complete and verify only that slice.
```

Before editing, the agent should establish an Agent Readiness Contract covering
scope, required context, allowed files and actions, validation, review needs,
and documentation impact. During implementation it marks the task in progress,
changes code and tests, runs repository-native validation, and records concrete
evidence. Passing a planned check must not be assumed merely because the check
was suggested.

Repeat this step for each dependency-complete slice. If code, requirements, or
design change during implementation, reconcile the affected spec artifacts
before continuing.

### 6. Verify the completed behavior

After the implementation tasks are complete, ask for a fresh verification pass:

```text
Reconcile the active spec with the implementation. Run its required validation,
map evidence to the acceptance criteria, and report blockers, waivers, and
residual risks. Do not close the spec yet.
```

Verification should cover the actual code, tests, config, migrations, manual
checks, and required reviews. A checked task is not sufficient evidence by
itself. Missing validation, uncovered must-have behavior, or unresolved review
findings keep the spec open unless an authorized person explicitly accepts the
risk.

### 7. Promote and close

Finally, move lasting knowledge out of the temporary spec and into the
repository's durable documentation:

```text
Prepare the promotion plan for this completed spec. Update the durable docs,
route any unfinished work, run the closure checks, and show me the closure
action before applying it.
```

Accepted requirements, architecture, interfaces, operating instructions, and
decisions go to the repository's normal documentation. Deferred work gets one
clear destination such as the backlog, roadmap, issue tracker, or a smaller
follow-up spec. The agent then records the final spec commit and closure
history, and removes or archives the temporary package according to repository
policy.

The result is a codebase whose implementation, tests, and durable docs describe
the accepted current state, while the closed spec remains traceable through
Git and the lifecycle history.

## Use It as an Agent

When the skill is available, invoke `spec-lifecycle-manager` for work that
creates, continues, reconciles, implements from, reviews, promotes, or closes
an implementation spec.

Before changing files:

1. Read the repository's `AGENTS.md` files and documentation index.
2. Use `active_spec_preflight` or `scan_specs` to establish current lifecycle
   state.
3. Read the relevant requirements, design, traceability, verification, open
   decisions, and durable sources of truth. Do not implement from `tasks.md`
   alone.
4. Select one coherent task slice and establish its scope, context,
   permissions, validation, review, and documentation impact.
5. Preview planned documentation edits before applying them.

During and after implementation:

1. Keep task state and evidence aligned with actual code, tests, and config.
2. Run repository-native validation and record concrete results.
3. Reconcile affected requirements, design, traceability, and verification.
4. Route unfinished work to a named task, backlog item, roadmap item, issue, or
   follow-up spec.
5. Promote accepted behavior into durable docs before closure.
6. Run closure checks, preserve the closure and archive records, and remove or
   archive temporary scaffolding according to repository policy.

Active specs normally live under `docs/specs/[###-slug]/`. If no active spec
exists, use durable docs, backlog, roadmap, the closure log, and the archive
index as current context. Do not recreate a removed package merely to resume
ordinary work.

## Agent Tools and Prompts

The plugin exposes structured MCP tools for lifecycle context and deterministic
checks. Agents should prefer them when available:

- `lifecycle_guide`, `active_spec_preflight`, and `scan_specs` for orientation;
- `spec_summary`, `next_task`, `task_context`, and `traceability_lookup` for
  bounded implementation context;
- `lint_spec_package`, `lint_doc`, and `prompts_validate` for validation;
- `reconcile_spec`, `promotion_plan`, and `review_packet` for lifecycle
  transitions; and
- `closure_check` and `archive_index` for closure readiness and history.

The plugin also provides guided prompts for starting work, choosing a task,
reconciling a package, validating lifecycle state, creating documentation, and
closing a completed spec.

Most runtime tools are read-only. Narrow write-capable operations are
preview-first and never replace human judgment, repository permissions, code
review, validation, or final closure decisions. Advisory hooks report relevant
lifecycle findings after edits but do not prove that work is complete.

If the MCP server is unavailable, agents can use the bundled
`spec_runtime.py` helper for validation, CI, recovery, or runtime debugging.
The [runtime reference](docs/reference/spec-lifecycle-runtime.md) documents the
tool and recovery surfaces.

## Documentation

- [Documentation index](docs/README.md): the full map of lifecycle guidance,
  governance, research, history, backlog, and roadmap.
- [Lifecycle design](docs/design/spec-lifecycle-management.md): the operating
  model and artifact lifecycle.
- [Coding-agent operating model](docs/design/coding-agent-operating-model.md):
  risk-scaled agent execution and review.
- [Governance constitution](docs/governance/constitution.md): principles and
  decision gates.
- [Runtime reference](docs/reference/spec-lifecycle-runtime.md): MCP tools,
  prompts, hooks, and recovery commands.
- [Installation reference](docs/reference/spec-lifecycle-manager-mcp-install.md):
  supported installation and troubleshooting.
- [Backlog](docs/backlog/README.md) and [roadmap](docs/roadmap/README.md): planned
  and deferred improvements.
- [Closure log](docs/history/spec-closure-log.md) and
  [archive index](docs/history/spec-archive-index.md): completed-spec history.

## License

This project is licensed under the GNU General Public License v3.0 or later.
The SPDX identifier is `GPL-3.0-or-later`.
