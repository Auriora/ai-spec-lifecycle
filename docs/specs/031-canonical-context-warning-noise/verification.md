---
title: Canonical context warning noise verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-07-05
---

# Verification

## Scope

This artifact records verification for spec 031, covering Requirements 1-5 and
Correctness Properties CP-001 through CP-005.

## Implemented Behavior

- `CANONICAL_CONTEXT_MISSING` is warning-level, advisory, and non-blocking.
- Canonical-context recommendations require concrete current-slice authority
  risk before suggesting `canonical-context.md`.
- Promotion-only, closure-log, archive-index, and historical package wording no
  longer create imported-source authority by themselves.
- Real imported-source, stale-doc, conflicting-authority, and ambiguous
  authority signals remain visible.
- `lint_spec_package`, `agent_readiness_packet`, MCP lint handling, and
  `closure_check` share the same advisory semantics.
- Source skill guidance, prompts, fallback spec-package wording, durable docs,
  backlog B058, and Codex/Claude plugin bundles are aligned.

## Task Evidence

| Task range | Evidence |
|------------|----------|
| T001-T013 | Focused runtime and MCP tests were added for advisory metadata, import-plan semantics, low-risk no-backfill behavior, false-positive filtering, positive risk-signal detection, ambiguous authority review guidance, readiness packet guidance, closure non-blocking behavior, and MCP diagnostic parity. |
| T014-T021 | Shared runtime implementation was added in `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`; compatibility wrapper, false-positive filters, diagnostic payload, readiness consumption, and closure blocker separation are covered by runtime tests. |
| T022-T029 | Source skill guidance, prompt definitions, fallback spec-package README, durable lifecycle docs, backlog B058, and bundled plugin copies were updated and validated with prompt, package-contract, and sync-guard checks. |
| T030 | This verification artifact records implementation evidence, validation commands, residual risk, and reload/install notes. |

## Quality Gates

| Gate | State | Notes |
|------|-------|-------|
| Runtime behavior | Passed | Focused and full tests cover canonical-context diagnostics, readiness, closure, and MCP parity. |
| Prompt and package parity | Passed | Prompt validation, package contract, sync guard, and npm pack dry-run passed through `npm run validate`. |
| Spec package lint | Passed | The spec package scan in `npm run validate` reports spec 031 health as pass with zero diagnostics. |
| Closure readiness | Passed | MCP `closure_check` reports ready with no blockers after T030-T032 completion. |

## Evidence Log

| Command or check | Result | Notes |
|------------------|--------|-------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Passed: 213 tests OK | Full Python runtime and MCP regression suite. |
| `npm run validate` | Passed | Repository validation bundle passed: Python tests, Node tests, lifecycle scan, archive index, prompt validation, package contract, sync guard, npm pack dry-run, and whitespace check. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/031-canonical-context-warning-noise` | Initial run returned verification-section warnings | Section headings were corrected before final validation. |
| `git diff --check` | Passed | Whitespace validation. |
| MCP `closure_check` | Passed | Closure readiness reports `ready: true`, no blockers, and lint summary error/warn/info all zero. |

## Implementation Review And Handoff

MCP `review_packet` was generated with `review_type: implementation`, resolved
to the canonical `implementation_review` packet. The packet used
`requirements.md`, `design.md`, `tasks.md`, `verification.md`, and
`traceability.md` as input artifacts and remained read-only.

No source changes outside the accepted spec scope are required before closure.
Spec lint reports zero diagnostics after verification artifact creation.
Durable behavior has been promoted to the source skill guidance, prompts,
fallback template README, durable lifecycle design/reference docs, backlog
entry, and bundled plugin copies. Closure cleanup should remove the active spec
package after a final spec commit records the complete package.

## Durable Promotion Map

| Accepted behavior | Durable destination | State |
|-------------------|---------------------|-------|
| Advisory canonical-context guidance and historical package handling | `skills/spec-lifecycle-manager/SKILL.md` | Promoted. |
| Prompt wording that preserves stage order and advisory canonical-context semantics | `skills/spec-lifecycle-manager/prompts/` | Promoted. |
| Fallback template wording for embedded durable-source context versus separate `canonical-context.md` | `skills/spec-lifecycle-manager/references/spec-package/README.md` | Promoted. |
| Runtime and lifecycle design semantics | `docs/design/spec-lifecycle-management.md`, `docs/reference/spec-lifecycle-runtime.md` | Promoted. |
| Backlog intake status for B058 | `docs/backlog/README.md` | Marked done. |
| Distributed plugin copies | `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/` | Synced from source. |

## Reload And Install Notes

- Codex plugin MCP tools are visible and callable in the reloaded session.
- `codex plugin list` showed `spec-lifecycle-manager@auriora-local` installed
  and enabled at version `0.2.1`.
- The user-level npm package was installed and exposes both
  `spec-lifecycle-manager` and `ai-spec-lifecycle` on PATH.
- The user-level npm package currently reflects released version `0.2.1`, which
  is older than this active spec work and still contains the retired
  `traceability_lookup.py` payload. Do not use that global package to refresh
  the local plugin for this spec's latest behavior until a new package is
  packed or released from current source.

## Residual Risks

| Risk | Disposition |
|------|-------------|
| Heuristic signal detection may still miss novel natural-language authority phrasing. | Accepted as non-blocking. The spec preserves positive detection for known imported-source, stale-doc, conflicting-authority, and ambiguous-authority patterns; future dogfooding findings should be routed to backlog. |
| Installed npm package version `0.2.1` is stale relative to current source. | Non-blocking for source and bundle closure. Package refresh/release belongs to the package/release workflow after this spec is closed. |
| Installed Codex plugin cache can require session reload after package reinstall. | Non-blocking. MCP tools are visible in the current session and sync checks verify source/bundle parity. |

## Closure Readiness

Final validation passed, task states T030-T032 are complete with evidence, and
MCP `closure_check` reports no blockers. Closure cleanup should use action
`removed` after a final spec commit preserves this package, then record the
closure log and archive index entries.
