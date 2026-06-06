---
title: Codex hook dogfood design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Design

## Overview

Dogfood the installed advisory Codex hook by collecting bounded evidence from
real lifecycle edits and representative smoke checks. The implementation is
primarily documentation and evaluation; hook code changes are only made when
evidence shows a concrete refinement is needed.

## High-Level Design

### System Architecture

Codex invokes the global `PostToolUse` hook after write tools. The wrapper
extracts changed files, calls runtime hook checks, logs decisions, and emits
additional context only when diagnostics are present.

### Components And Changes

| Component | Role |
|-----------|------|
| `~/.codex/hooks.json` | Host-level hook configuration; already installed. |
| `codex_spec_lifecycle_hook.py` | Advisory wrapper under the installed skill. |
| `spec_runtime.py hook` | Deterministic lifecycle checks. |
| `verification.md` | Dogfood evidence and policy decision record. |
| `docs/backlog/README.md` | Destination for follow-up work if needed. |

### Data Flow

1. Codex write tool completes.
2. Codex passes hook payload on stdin.
3. Wrapper extracts changed file paths.
4. Wrapper routes relevant files to runtime hook modes.
5. Wrapper logs results and emits concise additional context only for
   diagnostics.
6. Dogfood evidence classifies the hook result.

## Low-Level Design

### Algorithms

Evidence classification uses these outcomes:

| Outcome | Meaning |
|---------|---------|
| quiet-pass | Hook ran and produced no user-facing context. |
| useful-finding | Hook finding was actionable and correctly scoped. |
| false-positive | Hook finding was not useful for the edit. |
| duplicate | Hook finding duplicated already-clear feedback without adding value. |
| unavailable | Hook could not run or timed out. |

### Function Signatures And Interfaces

No new public interface is planned unless dogfood evidence identifies a needed
refinement.

### Error Handling

During dogfooding, hook failures remain advisory. The wrapper should never
block Codex work; runtime failures should be logged and surfaced only as
concise advisory context when relevant.

## Operational Considerations

The hook is host-level Codex configuration, not repository configuration. Repo
source documents the wrapper and expected install shape, but user-level config
changes remain outside Git.

## Validation Strategy

- Run full runtime tests.
- Run focused Codex hook tests.
- Record at least three hook evidence rows.
- Re-run spec lint and closure-check before closing this dogfood spec.

## Open Questions

- Does the advisory hook produce useful enough context to keep enabled
  globally?
- Should template checks stay in the same hook or be split into a separate
  matcher later?
