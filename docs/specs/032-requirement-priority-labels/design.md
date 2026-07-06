---
title: Requirement priority labels design
doc_type: spec
artifact_type: design
status: draft
authoring_mode: wizard
lifecycle_stage: design
owner: platform
last_reviewed: 2026-07-06
backlog_item: B057
---

# Technical Design

## Overview

Spec 032 adds MoSCoW requirement priority as a lightweight authoring and
runtime concept. The design keeps priority at requirement level using a simple
body metadata line:

```markdown
**Priority:** must-have
```

Valid persisted values are `must-have`, `should-have`, and `could-have`.
Excluded scope does not become an accepted requirement priority; it remains in
non-goals, out-of-scope text, rejected decisions, or routed residuals.

The runtime will parse priority when present through one shared requirement
parser used by readiness, closure, traceability lookup, and agent-readiness
paths. Unlabeled specs remain compatible. Priority is included in requirement
coverage outputs that already report requirements. Templates, prompts, source
skill guidance, runtime docs, and bundled plugin copies will be updated
together and validated with package-contract and sync checks.

MoE review on 2026-07-06 confirmed that spec 032's own requirements now carry
canonical requirement-level `**Priority:** must-have` metadata. This aligns the
design with the runtime source of truth and does not change the component or
data-flow design.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1, AC2, AC3 | Canonical persisted labels are `must-have`, `should-have`, and `could-have`; missing labels are allowed; any persisted non-canonical value is a lint diagnostic. | Unit tests for parsing each label and template review. |
| Requirement 1 | AC4, AC5 | `won't-have` is documented as exclusion vocabulary only; accepted requirements do not persist it as a priority. Shorthand guidance normalizes to canonical values. | Unit tests for normalization and docs/template review. |
| Requirement 1 | AC6 | Priority is requirement-level metadata; acceptance criteria inherit parent priority. | Unit tests for inherited priority in requirement blocks and coverage output. |
| Requirement 2 | AC1, AC3 | Missing priority is backward-compatible and non-blocking for active, closed, and removed specs. | Fixture tests with unlabeled active and historical specs; archive-index validation remains unchanged. |
| Requirement 2 | AC2 | Requirements template shows `**Priority:** must-have` without duplicating priority on every acceptance criterion. | Template lint and package-contract/sync-guard validation. |
| Requirement 3 | AC1, AC5 | A shared requirement coverage disposition helper treats accepted `must-have` gaps as blocking when priority is available. | Runtime tests for `stage_readiness`, `closure_check`, and closure coverage summaries. |
| Requirement 3 | AC2 | The shared coverage helper requires route, rationale, or accepted residual risk for unimplemented `should-have` requirements. | Runtime tests for requirement coverage disposition handling. |
| Requirement 3 | AC3 | The shared coverage helper allows `could-have` gaps to close when explicitly routed, rejected, or out of current scope. | Runtime tests for non-blocking routed optional coverage. |
| Requirement 3 | AC4 | `stage_readiness`, `closure_check`, traceability lookup, and agent readiness payloads preserve priority where they report requirements, using parsed requirement source rather than task-row duplication. | MCP/runtime structured-output tests. |
| Requirement 4 | AC1 | Documentation wizard asks for or infers priority at requirement level. | Prompt validation and review of `documentation-wizard.json`. |
| Requirement 4 | AC2 | Runtime output includes priority in structured contexts that already include requirement records. | Unit tests for JSON payload fields. |
| Requirement 4 | AC3 | Source and bundled plugin copies stay aligned. | `package-contract`, `sync-guard`, prompt validation. |
| Requirement 4 | AC4 | Test fixtures cover unlabeled, labeled, historical, and MCP/runtime output cases. | Python unit tests and focused fixture checks. |

## Correctness Property Coverage

The requirements artifact uses parser-compatible `CP-001:` bullets so runtime
readiness can track these properties before tasks and traceability are drafted.

| Property | Design Behavior | Validation Direction | Notes |
|----------|-----------------|----------------------|-------|
| CP-001 | Priority parsing returns `null` or equivalent absence for unlabeled requirements and does not emit blocking diagnostics solely for absence. | Legacy unlabeled fixture tests; lint and stage readiness checks. | Missing labels are compatibility-safe. |
| CP-002 | `must-have` coverage gaps remain blocking in readiness or closure contexts that evaluate requirement coverage. | Runtime coverage tests with missing `must-have` coverage. | Human rejection or supersession remains an explicit override. |
| CP-003 | `could-have` coverage gaps can be routed, rejected, or scoped out without blocking closure. | Runtime coverage tests with routed optional requirement rows. | Closure still requires explicit disposition. |
| CP-004 | Parsed priority is included in requirement block data and propagated into coverage-oriented outputs. | JSON payload tests for runtime and MCP tools. | Do not add priority to unrelated outputs. |
| CP-005 | Acceptance criteria inherit parent requirement priority; no AC-level priority parser is introduced. | Parser tests and traceability/coverage tests. | Avoids metadata duplication and parser complexity. |

## High-Level Design

### System Architecture

The change affects four layers:

1. Spec authoring surfaces: fallback requirements and traceability templates,
   documentation wizard prompt, and skill guidance.
2. Shared runtime parsing: requirement block extraction and priority
   diagnostics in a shared internal module used by both `lifecycle/core.py` and
   `lifecycle/traceability.py`.
3. Runtime/MCP reporting: structured outputs that already include requirement
   or coverage records.
4. Requirement coverage disposition: one helper used by readiness and closure
   paths to classify missing or partial requirement coverage by priority.
5. Packaging parity: bundled Codex and Claude plugin copies.

No new standalone CLI, MCP tool, dependency, or persistence file is required.
Priority is derived from Markdown source at runtime.

### Components and Changes

- Requirements template:
  Add a `**Priority:** must-have` example line under each requirement user story
  or immediately before acceptance criteria.
- Traceability template:
  Add a `Priority` column to requirement-level coverage rows where it reduces
  closure ambiguity. Do not require task-level duplication unless the task row
  already reports requirement context.
- Shared requirements parser:
  Add one internal parser for requirement sections, acceptance criteria, and
  optional priority metadata. `lifecycle/core.py` and `lifecycle/traceability.py`
  must consume that parser instead of maintaining separate requirement-section
  extraction behavior.
- Runtime core:
  Parse requirement priority into `requirement_blocks()` and reuse that parsed
  value in stage readiness, traceability-related context, agent readiness, and
  closure coverage summaries where requirement records are already emitted.
  Requirements lint must call the same parser diagnostics.
- Requirement coverage helper:
  Add a shared helper that reads the Requirement To Delivery Matrix coverage
  state, residual destination, tasks, verification, and parsed requirement
  priority. `stage_readiness`, `closure_check`, and closure-risk style outputs
  should consume this helper rather than duplicating priority semantics.
- Documentation wizard prompt:
  Ask for priority at requirement level in requirements mode and normalize
  shorthand to canonical labels when writing artifacts.
- Skill guidance:
  Document MoSCoW semantics in staged authoring and closure review guidance.
- Runtime reference:
  Document the accepted syntax, compatibility behavior, and affected structured
  output fields.
- Bundled plugins:
  Mirror source skill, prompt, template, and script updates into Codex and
  Claude plugin bundles.

### Data Models

Requirement records gain one optional field:

```json
{
  "id": "Requirement 1",
  "priority": "must-have",
  "text": "...",
  "acceptance_criteria": []
}
```

Accepted values:

| Value | Meaning | Closure default |
|-------|---------|-----------------|
| `must-have` | Required accepted scope. | Missing coverage blocks unless explicitly rejected or superseded by a human decision. |
| `should-have` | Expected accepted scope. | Missing coverage needs route, rationale, or accepted residual risk. |
| `could-have` | Optional accepted enhancement scope. | Missing coverage can close when routed, rejected, or out of current scope. |
| absent | Legacy or intentionally unlabeled requirement. | Existing compatibility behavior; absence alone does not block. |

`won't-have` is not an accepted value in requirement records for this spec.

### Data Flow

1. Author writes a requirement with optional `**Priority:** value`.
2. Runtime scans `requirements.md` and extracts requirement blocks.
3. Parser normalizes accepted values to canonical lowercase labels and returns
   diagnostics for duplicate, unknown, shorthand, or exclusion-only persisted
   priority values.
4. Coverage/readiness/closure functions consume requirement records and the
   shared requirement coverage disposition helper.
5. Traceability lookup collects requirement context from the shared parser, so
   task context inherits priority from the requirement source even when the task
   traceability row has no `Priority` column.
6. MCP handlers expose the same structured data through existing tool payloads.
7. Templates, prompts, and docs guide future specs to use the same convention.

## Low-Level Design

### Algorithms and Logic

Priority extraction is local to shared requirement block parsing.

```text
function parse_requirement_priority(block_text):
    find first line matching "**Priority:** <value>"
    normalize whitespace and lowercase value
    if value is exactly one of "must-have", "should-have", "could-have":
        return canonical priority
    if value is shorthand such as "must", "should", "could",
      "must have", "should have", or "could have":
        return diagnostic asking the authoring surface to persist the
        canonical hyphenated label
    if value is "won't-have" or equivalent:
        return unsupported exclusion value diagnostic in authoring/audit context
    if value is unknown:
        return unknown priority diagnostic in authoring/audit context
    return absent priority
```

Requirement coverage disposition is separate from priority parsing:

```text
function requirement_coverage_disposition(requirement, traceability_row):
    read priority from parsed requirement
    read Coverage State and Residual Destination from Requirement To Delivery Matrix
    if priority is "must-have" and coverage is not complete:
        block unless row records rejected or human-superseded rationale
    if priority is "should-have" and coverage is not complete:
        require route, rationale, or accepted residual risk
    if priority is "could-have" and coverage is not complete:
        allow closure only when routed, rejected, or marked out-of-scope
    if priority is absent:
        preserve existing compatibility behavior
```

Initial implementation should be conservative:

- Missing priority produces no blocking diagnostic.
- Persisted shorthand such as `must`, `should`, `could`, `must have`,
  `should have`, or `could have` should be a lint diagnostic with guidance to
  rewrite it to the canonical hyphenated label.
- Unknown persisted priority should be a lint diagnostic because it creates
  unreliable scope semantics.
- `won't-have` in a requirement priority line should be a lint diagnostic with
  guidance to move the item to non-goals, out-of-scope, rejected decisions, or
  routed residuals.
- Shorthand values may be normalized by prompts before writing, but templates
  and tests should persist canonical labels.

### Function Signatures and Interfaces

Likely shared internal helpers:

```python
def requirement_priority(block_text: str, requirement_id: str) -> tuple[str | None, list[dict[str, Any]]]:
    ...

def requirement_blocks(spec_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ...

def requirement_coverage_dispositions(spec_path: Path) -> list[dict[str, Any]]:
    ...
```

Each requirement block should include priority:

```python
{
    "id": "Requirement 1",
    "priority": "must-have",
    "text": "...",
    "acceptance_criteria": [...]
}
```

Structured outputs that include requirement records should preserve
`priority` when available. Outputs that only include task IDs, artifact
inventory, or high-level spec metadata do not need priority fields.

`lifecycle/traceability.py` should use the shared requirement parser when
building task lookup payloads. Task lookup payloads should attach priority to
each returned requirement object; task rows do not need a duplicate priority
column for this to work.

`closure_check()` should include requirement-coverage blockers from
`requirement_coverage_dispositions()` alongside task, verification,
traceability, lint, and canonical-context blockers.

### Error Handling

- Missing priority: no error and no warning by default.
- Persisted shorthand priority: lint diagnostic with the requirement ID and the
  canonical replacement.
- Unknown priority value: lint diagnostic with the requirement ID and the
  accepted canonical labels.
- `won't-have` priority value: lint diagnostic explaining that excluded scope
  belongs outside accepted requirement records.
- Duplicate priority lines in one requirement: lint diagnostic; parser should
  use the first value for payload stability and report the duplicate.

Requirements lint must call the shared parser diagnostics from `lint_doc()` or
`lint_spec_package()` when the active artifact is `requirements.md`.
Diagnostics must remain advisory-compatible with legacy specs and must not ask
agents to edit closed or removed historical packages.

### Security, Trust, and Access

Spec Markdown remains untrusted input. Priority parsing must be deterministic,
local, and free of code execution. MCP handlers should continue to call shared
runtime functions directly rather than shelling out to scripts.

### Migration and Compatibility

No migration is required for existing active, closed, or removed specs. New
templates guide authors toward priority labels, but unlabeled specs remain
valid. Archived historical checks must not require priority labels unless an
explicit future audit mode asks for authoring modernization.

The implementation must update source and generated/bundled copies together:

- `skills/spec-lifecycle-manager/`
- `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
- `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`

### Slice Boundary And Residual Architecture

| Design target | In this slice | Out of this slice | Follow-up destination | Blocks closure? |
|---------------|---------------|-------------------|-----------------------|-----------------|
| MoSCoW requirement metadata syntax | `**Priority:** must-have` convention, parser, templates, docs, tests | Alternate persisted syntaxes such as frontmatter or heading suffixes | none | yes |
| Runtime/MCP priority propagation | Existing outputs that already report requirements or coverage; traceability lookup gets priority from parsed requirement source | New MCP tools or standalone priority audit command | backlog if later needed | no |
| Closure semantics | Shared priority-aware requirement coverage disposition helper consumed by `stage_readiness`, `closure_check`, and closure-risk style outputs | Reworking task status semantics | future spec if needed | no |
| Historical compatibility | No priority requirement for existing or removed specs | Retrofitting closed specs | none | yes |
| Excluded scope | Non-goals/out-of-scope/rejected/routed guidance | Persisted `won't-have` accepted requirement value | future spec only if strong evidence appears | no |

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| Unit tests for priority parsing and diagnostics | Requirement 1, CP-001, CP-005 | `tests/runtime/test_spec_runtime.py` or focused runtime test file | Parser may miss uncommon Markdown formatting. |
| Fixture tests for unlabeled specs | Requirement 2, CP-001 | `tests/fixtures/` and runtime tests | None if fixtures cover active and historical paths. |
| Runtime/MCP structured output tests | Requirement 3, Requirement 4, CP-004 | `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py` | Ensure only relevant payloads grow fields. |
| Traceability lookup priority tests | Requirement 3 AC4, CP-004 | `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py` | Priority must come from parsed requirement source, not task-row duplication. |
| Closure/readiness coverage tests | Requirement 3, CP-002, CP-003 | Runtime tests with traceability fixtures | Shared helper must preserve legacy unlabeled behavior while enforcing labeled semantics. |
| Prompt/template validation | Requirement 4 | `spec_runtime.py prompts`, `package-contract`, `sync-guard` | Bundled copy drift if sync is missed. |
| Full validation bundle | Cross-surface regression | `npm run validate` | Existing package release may remain stale until package workflow runs. |

## Downstream Task Guidance

- Required checkpoints before implementation:
  requirements review, design review, tasks plus traceability, focused runtime
  tests, package-contract, sync-guard, prompt validation, and full validation.
- Properties or acceptance criteria that need explicit task coverage:
  CP-001 through CP-005 and every acceptance criterion in Requirements 1-4.
- Optional artifacts needed before implementation:
  create `traceability.md` with tasks; create `verification.md` before closure.
- Optional artifacts needed before implementation:
  `traceability.md` and `verification.md` are created. Keep both updated when
  task IDs, coverage rows, quality gates, or evidence expectations change.
- Downstream review needed if this design changes after tasks are drafted:
  tasks, traceability, and verification must be reviewed before implementation
  continues.

## Operational Considerations

This is a local authoring/runtime behavior change. There is no external
deployment or data migration. Operational risk is mainly agent-facing:
diagnostics must stay low-noise, output shape changes must be covered by tests,
and plugin bundle copies must stay aligned with source before closure.

## Open Questions

- None for design. Implementation may refine exact diagnostic codes and field
  placement while preserving the design contract.

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: embedded in `requirements.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
