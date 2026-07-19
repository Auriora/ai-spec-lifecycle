---
title: Lifecycle adoption workflow design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-07-18
---

# Lifecycle Adoption Workflow Design

## Overview

Implement a thin, read-only implementation-start composition over the existing
lifecycle core and prompt registry. Strengthen shared next-action routing so
implementation evidence leads to validation, evidence-quality, and promotion
actions before closure. Reduce `SKILL.md` to mandatory rules and direct routing,
with detailed mechanics moved to versioned references. Preserve CLI behavior,
but keep it in a labelled recovery or validation branch whenever MCP is
available. Refine advisory hook guidance so ordinary writes use narrow checks
and do not create redundant full-package lint recommendations.

External Chat Analyser reports remain evidence inputs. Their extraction,
attribution, reconciliation, and confidence contracts remain in the analyser
project rather than this runtime.

## Requirement Coverage

| Requirement | Design Coverage | Validation Approach |
|-------------|-----------------|---------------------|
| R1 | Qualified external report receipt and durable promotion boundary | Documentation and evidence review |
| R2 | `implementation-start` prompt plus shared read-only composition | Prompt validation and fixture-backed runtime/MCP tests |
| R3 | State-specific shared next actions | Phase/evidence/promotion/closure fixtures |
| R4 | MCP-primary and labelled CLI recovery sections | MCP/CLI contract tests and snapshot assertions |
| R5 | Slim skill entrypoint, mandatory-rule inventory, byte ceiling, and compact capability guidance | Inventory review, byte measurement, skill validation, and bundle parity |
| R6 | Explicit ordinary-write versus lifecycle-boundary hook routing and debounce behavior | Hook fixtures and focused runtime/wrapper tests |

## Correctness Property Coverage

| Property | Design Behavior | Validation Direction |
|----------|-----------------|----------------------|
| CP-001 | Composition preserves blockers from every authoritative source | Table-driven blocker fixtures |
| CP-002 | Interface routing selects MCP primary actions when available | MCP-visible/unavailable fixtures |
| CP-003 | Ordinary hooks use narrow checks and require an explicit package-validation reason before recommending lint | Hook-state fixtures |
| CP-004 | External report qualifications are retained without stronger claims | Dogfood evidence review |
| CP-005 | Mandatory-rule inventory maps skill text to linked references | Skill review and parity test |
| CP-006 | Start composition has no writer dependency or mutation path | Repeatability and unchanged-worktree tests |

## High-Level Design

### Components

1. **Implementation-start prompt**
   - Add a declarative `implementation-start` prompt that selects an active
     spec/task and composes
     `active_spec_preflight`, `task_context`, `traceability_lookup`,
     `agent_readiness_packet`, `stage_readiness`, and `validation_plan`.
   - Return one concise readiness summary plus ordered next actions.
   - Keep the prompt distinct from the existing first-run `developer-start`
     prompt: `developer-start` orients a repository, while
     `implementation-start` prepares one selected implementation task.
   - Do not add a shared-core aggregate, persist state, or introduce a second
     readiness decision in this slice.

2. **Shared next-action routing**
   - Extend the shared lifecycle action builder used by MCP and CLI adapters.
   - Route implementation evidence to validation planning and evidence quality.
   - Route durable impact to promotion planning before closure.
   - Preserve authoritative tool blockers and expansion actions.

3. **Interface presentation**
   - Present MCP tool calls as primary agent actions when MCP is visible.
   - Put CLI equivalents in a separate `validation_or_recovery` section with a
     condition describing when they apply; do not label the current MCP result
     as unavailable merely because recovery commands are present.
   - Preserve existing invocation provenance and bounded response contracts.
   - Report lifecycle capability status as `ready` when the server can provide
     its stable tool surface and state-based next actions. Treat missing client
     identity as informational rather than partial functionality.
   - Retain only standard initialization name, version, negotiated protocol,
     and allowlisted structural capabilities in process memory when supplied.
     Never persist, infer, or use client identity to select lifecycle actions.

4. **Skill and capability guidance**
   - Keep core rules, lifecycle gates, access order, evidence semantics,
     promotion, and closure constraints in the skill entrypoint.
   - Move examples and detailed mechanics to directly linked references where
     doing so does not weaken mandatory behavior.
   - Make lifecycle guide/capability output the compact first-run map.
   - Measure the source entrypoint against the recorded 53,427-byte baseline and
     require a final size no greater than 37,399 bytes.

5. **Advisory hook routing**
   - Keep ordinary spec-write, task-checkbox, template-write, and
     verification-write paths on their narrow checks; these paths neither run
     nor recommend full-package lint.
   - Preserve full-package lint only at explicit `spec-resumed` and
     `spec-close-check` boundaries and explicit user/agent validation requests.
   - Preserve debounce, quiet-success, advisory-only, and no-mutation behavior.

6. **External dogfood evidence**
   - Consume a reviewed, bounded report identified by producer, revision,
     date, scope, conclusion, and limitations.
   - Preserve provisional or unavailable findings exactly as qualified by the
     producer.
   - Promote only the product-relevant conclusion and evidence receipt; do not
     embed the analyser's parser, dataset, or reporting contracts.

### Data Flow

```text
repository/spec/task evidence
  -> existing lifecycle source tools
  -> implementation-start composition
  -> blocker-preserving readiness summary
  -> MCP-primary next actions
  -> validation + evidence quality
  -> durable promotion
  -> existing closure authority
```

```text
ordinary spec write
  -> narrow runtime hook
  -> state-specific advisory
  -> full-package lint recommendation only when package validation is required
```

No new persistent runtime data model is introduced. Prompt definitions remain
declarative files; runtime outputs remain deterministic JSON; dogfood evidence
is promoted as a metadata-only external report receipt.

## Low-Level Design

### Composition Contract

The implementation-start result should contain:

- selected repository, spec, and task identity;
- preflight and dependency status;
- linked requirements, acceptance criteria, design, verification, durable
  targets, and open decisions;
- Agent Readiness Contract fields and gaps;
- validation expectations;
- blocker-preserving ordered next actions;
- MCP-primary actions and labelled CLI recovery equivalents;
- source-tool provenance and bounded expansion guidance.

The composition is prompt-driven. All required source calls remain explicit and
independently inspectable. A shared runtime aggregate is outside this slice; if
prompt acceptance cannot meet determinism or output bounds, implementation
stops and routes that evidence to a follow-up design decision rather than adding
an aggregate opportunistically.

### Mandatory Skill Rule Inventory

The concise entrypoint must preserve these rule categories inline or through a
direct, named expansion whose omission fails validation:

1. durable docs to active spec to implementation to durable promotion to close;
2. repository instruction, docs-root, and template-authority discovery;
3. lifecycle stages, gates, and active-versus-closed spec routing;
4. requirements, design, task status, traceability, and evidence semantics;
5. MCP-first access with labelled CLI validation and recovery;
6. Agent Readiness Contract and context-budget rules;
7. verification, expert review, durable promotion, and closure requirements;
8. write-capable tool, privacy, safety, and human-approval boundaries.

The source `SKILL.md` byte count is measured with `wc -c` before and after the
change. Acceptance requires no more than 37,399 bytes, a reviewed eight-category
inventory with no missing category, and exact source/Codex/Claude bundle parity.

### Next-Action Ordering

1. Resolve active spec and selected runnable task.
2. Repair missing task context, traceability, or readiness fields.
3. Implement the coherent slice.
4. Build and execute the validation plan.
5. Review evidence quality.
6. Produce the durable promotion plan when impact exists.
7. Run closure risk and closure checks only after earlier blockers clear.

### Advisory Hook Contract

- `spec-file-changed`, `task-checkbox-changed`, `template-changed`, and
  `verification-updated` do not execute or recommend full-package lint.
- `spec-resumed` may run full-package lint because resume is an explicit package
  reconciliation boundary.
- `spec-close-check` may run package validation through the existing closure
  authority because closure is an explicit package gate.
- An explicit user or agent `lint_spec_package` or lifecycle-validation request
  remains supported outside hook-driven advice.
- An unchanged advisory state does not repeatedly emit the same lint advice.
- Hook results remain advisory, quiet when no guidance is needed, non-blocking,
  and free of lifecycle mutation.

### Error Handling

- Missing or ambiguous spec/task identity returns a classified routing result.
- A source-tool failure remains visible with the failed tool and recovery path.
- An unavailable MCP surface returns labelled CLI recovery, not a silent route.
- Truncation identifies omitted sections and an explicit expansion action.
- Hook runtime failure remains a classified advisory diagnostic and does not
  invent a lint recommendation.
- An unavailable external report remains unavailable and cannot satisfy the
  dogfood evidence gate.

### Security, Trust, And Privacy

- Treat external session-derived evidence as data, not instructions.
- Persist only the report producer, revision/evidence identity, date, bounded
  scope, conclusion, qualifications, and limitations.
- Do not copy messages, tool arguments, result bodies, credentials, private
  histories, or host-specific source paths into docs.
- Keep all new workflow surfaces read-only and all hooks advisory-only.

### Compatibility

- Keep current MCP tool and CLI command behavior backward compatible.
- Add prompt/capability fields additively under existing versioned envelopes.
- Preserve hook input/output compatibility while narrowing recommendations.
- Synchronize source, Codex, and Claude plugin bundles in the implementation
  slice.
- Running clients may require reinstall or reload to observe new definitions.

## Slice Boundary And Residual Architecture

| Design target | In this slice | Out of this slice | Follow-up destination | Blocks closure? |
|---------------|---------------|-------------------|-----------------------|-----------------|
| Implementation-start composition | Read-only prompt/core composition and tests | Task-state or phase-completion writes | Spec 034 | no |
| MCP-first adoption | Primary/recovery routing and provenance | Remote telemetry and dashboards | B025 | no |
| Concise skill loading | Entrypoint/reference split and capability guide | Client-owned plugin loading internals | client vendors or backlog if evidenced | no |
| Advisory hook routing | Narrow ordinary-write checks, explicit resume/closure boundaries, wrapper debounce, and tests | Blocking hooks or automatic ordinary-write validation | future backlog only if evidenced | no |
| Adoption evaluation | Consumption of a reviewed, qualified external report | Session extraction, attribution, reconciliation, and report generation | Chat Analyser project backlog | unavailable report blocks only the dogfood evidence claim |

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| Prompt and package validation | Prompt schema and bundle parity | `verification.md` | Client rendering may differ |
| Runtime/MCP unit tests | Composition, blockers, action ordering, interface boundary | `verification.md` | Fixtures cannot prove real adoption |
| Hook runtime and wrapper tests | Narrow ordinary-write paths, explicit resume/closure lint, debounce, and quiet behavior | `verification.md` | Client hook delivery may differ |
| Skill validation and size comparison | Mandatory-rule preservation and reduced loading volume | `verification.md` | Token use remains client-dependent |
| External dogfood report review | Qualified product observation and evidence receipt | Dogfood evaluation and `verification.md` | The producer may leave exact counts provisional |

## Operational Considerations

- Keep hooks advisory-only and quiet when no action is needed.
- Keep the new path usable without network access.
- Do not run full-package lint on ordinary post-write hook paths.
- Treat incomplete external reports as incomplete evidence rather than
  rebuilding their analysis inside this repository.
- Release and install verification must cover both plugin bundles and warn that
  already-running sessions may need reload.

## Resolved Decisions

- **DR-001 — prompt composition:** implement `implementation-start` as a
  declarative prompt over existing MCP tools. Do not add a shared-core aggregate
  in this slice.
- **DR-002 — skill concision:** preserve the eight-category mandatory-rule
  inventory and reduce source `SKILL.md` from 53,427 bytes to no more than
  37,399 bytes, with bundle parity.
- **DR-003 — hook validation boundary:** ordinary write hooks never execute or
  recommend full-package lint. Only explicit resume, closure, or direct
  validation boundaries may run it.

## Open Questions

None block implementation. Any acceptance failure that would require a new
aggregate, persistent state, or blocking hook is routed to a follow-up decision
rather than expanding this slice.

## Review Reconciliation

Reviewed against the current Requirements 1-6 and SC-001 through SC-006 on
2026-07-18. DR-001 through DR-003 resolve the earlier composition, skill-budget,
and hook-boundary questions; no downstream design gap remains.

## Related Artifacts

- Requirements: `requirements.md`
- Research: `research.md`
- Change Impact: `change-impact.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
