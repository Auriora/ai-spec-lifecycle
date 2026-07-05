---
title: Canonical context warning noise design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-07-05
---

# Technical Design

## Overview

Canonical-context diagnostics will remain warning-level guidance, but their
payloads and wording will distinguish advisory review signals from required
artifact creation. The runtime will normalize canonical-context risk analysis in
one shared path, then reuse that path from lint, readiness, and closure surfaces.
Prompt, template, reference, and bundled plugin text will be aligned to the same
semantics.

The design resolves the requirements-stage open questions as follows:

- Runtime signal detection handles concrete risk classification and false
  positive reduction.
- Prompts, templates, skill guidance, and durable docs handle wording and
  agent-response expectations.
- All prompt surfaces that mention canonical context are in scope, not only
  `documentation-wizard`.
- `agent_readiness_packet` and `closure_check` should consume normalized shared
  canonical-context diagnostics instead of computing separate meanings.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1, AC2, AC3 | Add advisory fields and messages to normalized canonical diagnostics; keep archived or historical packages out of active artifact guidance. | Unit tests for diagnostic payloads and package lint output. |
| Requirement 2 | AC1, AC2, AC3 | Classify concrete context triggers and suppress `canonical-context.md` recommendations when a package already embeds sufficient canonical context or has no authority risk. | Unit tests for small specs, embedded context, stale-doc risk, and imported-source risk. |
| Requirement 3 | AC1, AC2, AC3 | Refine risk-signal matching so ordinary promotion and closure wording is not treated as imported-source authority by itself, and represent ambiguous matches as advisory review signals rather than artifact requirements. | Regression tests for promotion-only wording, true imported/adapted source wording, and ambiguous authority wording. |
| Requirement 4 | AC1, AC2, AC3 | Update all canonical-context prompt/template/docs surfaces and run prompt plus package parity checks. | `prompts`, `package-contract`, `sync-guard`, and focused text review. |
| Requirement 5 | AC1, AC2, AC3, AC4 | Reuse normalized diagnostics in `lint_spec_package` and `agent_readiness_packet`; ensure `closure_check` blocks only unresolved canonical-context promotion rows, not missing optional context. | CLI/MCP parity checks and closure regression tests. |

## Correctness Property Coverage

| Property | Design Behavior | Validation Direction | Notes |
|----------|-----------------|----------------------|-------|
| CP-001 | `CANONICAL_CONTEXT_MISSING` remains `warn` and carries `advisory: true`. | Assert warning severity and advisory metadata. | No closure blocker is derived directly from missing optional context. |
| CP-002 | Historical or archived package references are not converted into active write guidance. | Add regression text with archive/closure references and, where practical, archived inventory fixtures. | Guidance should route to current lifecycle stage. |
| CP-003 | Promotion targets, closure logs, and archive-index references alone do not emit `imported-source-risk`. | Add promotion-only false-positive test. | Durable impact can still be documented without requiring canonical context. |
| CP-004 | Stale durable docs, copied/adapted sources, supersession, and conflicting authority still emit concrete risk signals. | Add positive tests for each accepted signal class. | Detection should be precise, not removed. |
| CP-005 | Lint, readiness, and closure surfaces agree on advisory versus blocking semantics. | Compare runtime payloads across direct CLI-equivalent functions and MCP handlers where practical. | Closure may still block unresolved required promotion from an existing `canonical-context.md`. |

## High-Level Design

### System Architecture

Canonical-context behavior stays inside the existing lifecycle runtime boundary:

```text
spec package markdown
  -> canonical_context_texts
  -> canonical_context_risk_signals
  -> canonical_context_diagnostics
  -> lint_spec_package
  -> agent_readiness_packet
  -> stage_readiness / active_spec_preflight guidance

canonical-context.md Promotion Map
  -> canonical_context_closure_blockers
  -> closure_check

archived or historical package references
  -> historical_reference_filter
  -> advisory review note or no signal
```

The MCP server continues to call shared runtime functions directly. The direct
CLI remains a validation, CI, MCP-debugging, and no-MCP recovery adapter over
the same shared functions. No separate MCP-only or CLI-only diagnostic logic is
introduced.

### Components and Changes

- `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`:
  Refine canonical-context risk classification and diagnostic construction.
  Add stable advisory metadata to canonical-context diagnostics and filter
  historical package references before artifact guidance is produced.
- `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`:
  No semantic branching expected. Existing handlers should continue to return
  shared runtime payloads.
- `skills/spec-lifecycle-manager/scripts/lifecycle/runtime_adapter.py`:
  No semantic branching expected. CLI output should remain the shared JSON
  payload rendered by the adapter.
- `tests/runtime/test_spec_runtime.py`:
  Add focused regression tests for advisory metadata, false-positive reduction,
  positive signal preservation, ambiguous authority review guidance,
  historical-reference handling, readiness guidance, and closure behavior.
- `tests/runtime/test_spec_mcp_server.py`:
  Add or extend parity coverage only where the MCP JSON shape needs explicit
  protection beyond shared runtime tests.
- `skills/spec-lifecycle-manager/SKILL.md`:
  Clarify that `canonical-context.md` is optional and risk-triggered, not a
  default backfill artifact.
- `skills/spec-lifecycle-manager/prompts/`:
  Update every prompt that mentions canonical context so it preserves stage
  order and describes advisory guidance.
- `skills/spec-lifecycle-manager/references/spec-package/`:
  Clarify fallback templates and package README wording for embedded canonical
  context versus separate `canonical-context.md`.
- `docs/design/spec-lifecycle-management.md` and
  `docs/reference/spec-lifecycle-runtime.md`:
  Promote accepted behavior into durable design/reference documentation.
- `plugins/spec-lifecycle-manager/`:
  Sync bundled Codex and Claude plugin copies after source changes.

### Data Models

Canonical-context diagnostics remain ordinary diagnostic dictionaries. The
normalized diagnostic for missing optional canonical context should include:

```text
{
  "severity": "warn",
  "code": "CANONICAL_CONTEXT_MISSING",
  "message": "... advisory ... concrete trigger ...",
  "lifecycle_gate": "agent_ready",
  "artifact_type": "canonical-context",
  "advisory": true,
  "blocking": false,
  "signals": ["stale-doc-risk" | "imported-source-risk" | "durable-doc-impact" | "canonical-context-intent" | "authority-review"],
  "recommendation": "inspect context risk before creating canonical-context.md",
  "confidence": "clear" | "review",
  "import_plan": [...]
}
```

The existing `import_plan` structure remains unchanged when durable-source
references can produce a useful plan. Consumers must not infer that an
`import_plan` makes artifact creation mandatory.

### Data Flow

1. Runtime reads the active spec artifacts through `canonical_context_texts`.
2. `canonical_context_signal_context` returns precise signal identifiers and a
   confidence class for clear versus review-needed matches. The existing
   `canonical_context_risk_signals` interface may remain as a compatibility
   wrapper that returns only the signal list.
3. `canonical_context_diagnostics` converts signals into normalized advisory
   diagnostics when no separate or embedded canonical context exists.
4. `lint_spec_package` appends those diagnostics to package lint output.
5. `agent_readiness_packet` adds the same diagnostics to `gaps` and
   `canonical_context.diagnostics`, preserving advisory semantics.
6. `closure_check` consumes lint errors and canonical promotion blockers. It
   does not turn warning-level `CANONICAL_CONTEXT_MISSING` into a blocker.
7. MCP and CLI adapters return the same shared payloads.

## Low-Level Design

### Algorithms and Logic

Risk classification should separate positive evidence from ordinary lifecycle
wording:

```text
function canonical_context_signal_context(spec):
    text = normalized text from active spec artifacts
    signals = []
    confidence = "clear"

    if text contains stale-doc or conflicting-authority evidence:
        signals.append("stale-doc-risk")

    if text contains copied/adapted/imported/supersedes source authority:
        signals.append("imported-source-risk")

    if text declares broad durable-doc impact:
        signals.append("durable-doc-impact")

    if text explicitly declares canonical-context intent:
        signals.append("canonical-context-intent")

    if text uses weak authority words without a source path, import verb,
    supersession claim, or stale-doc evidence:
        signals.append("authority-review")
        confidence = "review"

    remove imported-source-risk when the only evidence is historical package
    references, closure records, archive indexes, promotion targets, durable
    destinations, or ordinary promotion wording

    do not add imported-source-risk for promotion targets, closure logs,
    archive indexes, durable destinations, or ordinary promotion wording alone

    return {signals: stable unique signals, confidence: confidence}
```

Diagnostic construction should make the agent response explicit:

```text
function canonical_context_diagnostics(spec):
    context = canonical_context_signal_context(spec)
    signals = context.signals
    confidence = context.confidence

    if no signals or has_canonical_context(spec):
        return metadata diagnostics for existing canonical-context.md only

    diagnostic = warning CANONICAL_CONTEXT_MISSING
    diagnostic.advisory = true
    diagnostic.blocking = false
    diagnostic.signals = signals
    diagnostic.confidence = confidence
    diagnostic.message = "Advisory: inspect concrete context risk before adding canonical-context.md."

    if confidence is "review":
        diagnostic.recommendation = "Review authority wording; do not create canonical-context.md unless concrete source risk is confirmed."

    if durable-source refs produce import plan:
        diagnostic.import_plan = plan

    return [diagnostic]
```

`closure_check` should keep its current separation:

```text
function closure_check(spec):
    blockers = task, verification, traceability, lint-error blockers
    blockers += canonical_context_closure_blockers(spec)
    return ready if no blockers
```

Only `canonical_context_closure_blockers` may add canonical-context closure
blockers, and only from an existing promotion map row marked required before
closure.

Historical package handling should be explicit and conservative:

```text
function historical_reference_filter(signals, matched_text):
    if matched_text only points at closed specs, archive indexes, closure logs,
    removed package paths, or cleanup records:
        return signals without artifact-creation signals

    return original signals
```

The filter returns only a signal list. Review-only wording is added later by
`canonical_context_diagnostics` when the remaining signal context has
`confidence: "review"`. This filter does not hide active-spec stale-doc or
imported-source evidence.

### Function Signatures and Interfaces

No new public CLI or MCP tool is required. Internal signatures may remain stable:

```text
canonical_context_risk_signals(spec_path: Path) -> list[str]
canonical_context_signal_context(spec_path: Path) -> dict[str, Any]
canonical_context_diagnostics(spec_path: Path) -> list[dict[str, Any]]
canonical_context_closure_blockers(spec_path: Path) -> list[dict[str, Any]]
lint_spec_package(spec_path: Path, include_summary: bool = True, mode: str | None = None) -> dict[str, Any] | list[dict[str, Any]]
agent_readiness_packet(spec_path: Path, task_id: str) -> dict[str, Any]
closure_check(spec_path: Path) -> dict[str, Any]
```

If implementation benefits from a small helper, add it as private shared
runtime logic, for example:

```text
canonical_context_advisory_message(signals: list[str]) -> str
historical_reference_filter(signals: list[str], text: str) -> list[str]
```

### Error Handling

Malformed or incomplete spec artifacts should continue to produce ordinary lint
diagnostics. Canonical-context false-positive reduction must not suppress
unrelated frontmatter, stage, task, traceability, or closure errors.

Uncertain canonical-context matches should return review guidance as warning
metadata instead of raising exceptions or adding closure blockers.

### Security, Trust, and Access

This change reads local Markdown and JSON prompt files only. It does not add
network access, credential handling, subprocess execution, or write-capable MCP
behavior. The primary trust boundary is untrusted spec text being interpreted as
diagnostic input; the runtime should keep output deterministic and avoid
executing or interpolating spec content into shell commands.

### Migration and Compatibility

Existing callers that read `severity`, `code`, `message`, `path`, and
`artifact_type` continue to work. New advisory fields are additive. Existing
tests expecting `CANONICAL_CONTEXT_MISSING` as a warning should be updated to
assert the richer advisory shape.

Bundle synchronization is required because users may run the source skill, the
Codex plugin copy, or the Claude plugin copy. Source changes must be mirrored
into bundled plugin paths before closure.

### Slice Boundary And Residual Architecture

| Design target | In this slice | Out of this slice | Follow-up destination | Blocks closure? |
|---------------|---------------|-------------------|-----------------------|-----------------|
| Advisory diagnostic semantics | Runtime diagnostic metadata, wording, and tests | Making canonical context a hard phase gate | None | yes |
| Risk signal precision | False-positive reduction for promotion/closure/archive wording and positive coverage for imported/stale/conflict signals | Full natural-language authority extraction | Backlog if needed after dogfooding | no |
| Runtime surface alignment | `lint_spec_package`, `agent_readiness_packet`, `closure_check`, CLI/MCP shared payload parity | New MCP tools or write-capable authoring tools | None | yes |
| Prompt/template/docs alignment | Skill, prompts, templates, runtime reference, lifecycle design docs | Rewriting all lifecycle docs unrelated to canonical context | None | yes |
| Bundle parity | Codex and Claude plugin copies synced from source | Installed cache mutation on the user's machine | Install/sync guidance if needed | yes |

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| `python3 -m unittest discover -s tests -p 'test_*.py'` | Runtime, MCP, and regression behavior | Task evidence and `verification.md` if created | None expected. |
| Focused runtime tests for `canonical_context_risk_signals` and `canonical_context_diagnostics` | Requirements 1-3 and CP-001 through CP-004 | `tests/runtime/test_spec_runtime.py` | Heuristics may still miss novel phrasing. |
| Historical-reference regression tests | Requirement 1 AC3 and CP-002 | `tests/runtime/test_spec_runtime.py` | Archived-package inventory behavior may need extra MCP/server coverage if runtime behavior differs. |
| Focused readiness and closure tests | Requirement 5 and CP-005 | `tests/runtime/test_spec_runtime.py` | MCP parity depends on shared handler coverage. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts` | Prompt JSON validity after wording changes | Task evidence | None expected. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/031-canonical-context-warning-noise` | Spec package authoring health | Task evidence | None expected. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` and `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` | Source and bundled plugin parity | Task evidence | Installed runtime may still need reload outside repo. |
| `git diff --check` | Whitespace safety | Task evidence | None expected. |

## Downstream Task Guidance

- Required checkpoints before implementation: preserve this design's shared
  diagnostic path, update tests before or with runtime changes, and validate
  bundle parity before closure.
- Properties or acceptance criteria that need explicit task coverage: CP-001
  through CP-005, especially promotion-only false positives and closure
  non-blocking behavior.
- Optional artifacts needed before implementation: none. `tasks.md` plus
  `traceability.md` should be created together in the next stage.
- Downstream review needed if this design changes after tasks are drafted:
  update tasks and traceability before implementation continues.

## Operational Considerations

The change should be invisible to normal users except for clearer guidance and
fewer false-positive artifact recommendations. Agents may need the MCP server or
installed plugin reloaded after bundle/source changes. Closure should include
prompt validation, package contract validation, sync guard output, and explicit
notes about whether local installed copies were refreshed or only source/bundle
copies were updated.

## Open Questions

- None for task planning. Implementation may choose exact helper names while
  preserving the shared-runtime boundary and public payload compatibility.

## Related Artifacts

- Requirements: `docs/specs/031-canonical-context-warning-noise/requirements.md`
- Backlog: `docs/backlog/README.md` B058
- Tasks: not created yet
- Verification: not created yet
