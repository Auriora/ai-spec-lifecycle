---
title: Phase gate check design
doc_type: spec
artifact_type: design
status: accepted
authoring_mode: wizard
lifecycle_stage: design
owner: platform
last_reviewed: 2026-07-12
---

# Design

## Overview

Add a read-only `phase_gate_check` aggregate in shared lifecycle core code. It
infers one public phase, composes only phase-applicable authoritative signals,
preserves their severity and meaning, and renders the new Spec 036 compact
contract. Existing preflight, lint, task, validation, promotion, and closure
tools remain unchanged and authoritative expansion surfaces.

## High-Level Design

```text
spec artifacts + task state + recorded upstream fingerprints
                         |
                         v
              phase inference and gate policy
                         |
       applicable authoritative source checks (max 7)
                         |
                         v
 compact/full/section aggregate + evidence fingerprint
                         |
                 MCP or CLI provenance
```

### Public Phase Model

| Phase | Primary evidence | Next phase |
|-------|------------------|------------|
| `requirements` | requirements present; design absent | `design` |
| `design` | design present; tasks absent or design review pending | `tasks` |
| `tasks` | task plan/traceability being completed | `implementation` |
| `implementation` | runnable incomplete implementation tasks exist | `verification` |
| `verification` | tasks finished but required proof/review is incomplete | `promotion` |
| `promotion` | durable targets are unresolved or promotion evidence is incomplete | `closure` |
| `closure` | promotion evidence is satisfied; closure is ready or has closure-only blockers | null |
| `unknown` | phase cannot be inferred safely | null |

Archived packages return not-applicable rather than being inferred as closure.

## Low-Level Design

### Core Interface

```python
phase_gate_check(
    spec_path: Path,
    detail: str = "compact",
    section: str | None = None,
    expected_fingerprint: str | None = None,
) -> dict[str, Any]
```

The core stays caller-agnostic. Adapters add `lifecycle_metadata` and expose:

- MCP `phase_gate_check` with output schema;
- CLI `phase-gate-check SPEC_PATH` with matching detail arguments.

### Inference Order

1. Reject missing, ambiguous, or archived package references.
2. Missing/invalid requirements yields `unknown`; accepted requirements without
   design yields `requirements`.
3. Design without an accepted task/traceability plan yields `design` or `tasks`.
4. Runnable incomplete tasks yield `implementation`.
5. No runnable tasks plus unverified/evidence/review gaps yields `verification`.
6. Verified delivery plus missing durable promotion targets/evidence yields
   `promotion`.
7. Satisfied promotion evidence invokes authoritative closure checking and
   yields `closure`, preserving any closure-only blockers.

Early gates interpret only evidence relevant to the next transition; they do
not treat later implementation-readiness gaps as requirements-stage blockers.

### Source Composition

Signals appear in deterministic order and only when applicable:

1. `stage_readiness`
2. `lint_spec_package`
3. `next_task`
4. selected task/traceability context
5. `validation_plan`
6. `promotion_plan`
7. `closure_check`

Each summary carries source, decision/status, counts, blocker codes/references,
and expansion arguments. It never changes source severity, authority, or proof
meaning. Validation planning is advice, not proof that commands ran.

### Staleness Contract

Downstream artifacts may record normalized upstream fingerprints. Design records
the requirements fingerprint; tasks, traceability, and verification may record
requirements and design fingerprints. Gate status is:

- `current`: recorded fingerprint matches;
- `stale`: recorded fingerprint differs;
- `review_required`: no fingerprint exists;
- `not_applicable`: artifact is not yet relevant.

Modification times may explain `review_required` but never establish `stale` or
block advancement by themselves. V1 reads fingerprints but does not write them.

### Compact And Expansion Contract

Compact output uses the accepted Spec 036 envelope, caps findings at 20 and
actions at 10, and targets 32 KiB. Mandatory blockers are never removed merely
to meet the target. Full output remains a bounded aggregate rather than nested
source payloads. Section mode uses the closed enum:

- `source_signals`
- `coverage`
- `validation`
- `promotion`
- `closure`

Expansion calls the same tool with repo-relative spec path, section, and the
expected evidence fingerprint. A mismatch returns the shared stale response.

### Evidence Fingerprint

Use domain `phase-gate-check-v1` and canonical JSON over:

- repo-relative spec ID/path;
- phase, next phase, readiness;
- artifact presence and recorded upstream fingerprint states;
- normalized blocker severity/code/source/reference;
- bounded next actions;
- applicable source decision fields and counts.

Exclude timestamps, absolute paths, response provenance, host-sensitive
commands, full diagnostic wording, and file contents.

## Operational Considerations

### Performance

Do not run promotion or closure checks during early authoring phases. Closure is
the most expensive/noisy source and is invoked only for late-phase evidence.

### Compatibility

This is a new tool and may default compact. Existing tools and schemas are not
changed. MCP and CLI lifecycle decisions must match after transport metadata is
removed.

### Error Handling

- Invalid detail/section combinations fail schema or argument validation.
- Unknown phase returns concrete missing/ambiguous evidence.
- Stale expansion returns the accepted stale response and refreshed arguments.
- Source exceptions become bounded source diagnostics without being reclassified.

## Verification Strategy

Cover every phase transition, ambiguous/missing/archived references, unresolved
decisions, severity preservation, fingerprint match/mismatch/missing states,
mtime-only changes, bounds, deterministic ordering, stale expansion, privacy,
and MCP/CLI parity.

## Durable Promotion Targets

- `docs/design/spec-lifecycle-management.md`
- `docs/reference/spec-lifecycle-runtime.md`
- `skills/spec-lifecycle-manager/SKILL.md`
- backlog B031 and roadmap status

## Residual Risks

- Existing specs lack recorded upstream fingerprints and will initially report
  `review_required` rather than `current`.
- Promotion evidence remains conservative until durable promotion recording is
  made more structured.
- Source checks may still be moderately expensive in late phases.

## Open Questions

None blocking implementation.
