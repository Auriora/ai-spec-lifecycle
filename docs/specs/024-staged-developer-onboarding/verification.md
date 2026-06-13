---
title: Staged developer onboarding verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Verification

## Validation Plan

| ID | Validation | Covers | Evidence |
| --- | --- | --- | --- |
| V001 | Run full unit suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`. | Runtime behavior, parser/readiness changes, regression coverage. | Pending. |
| V002 | Lint the spec package and changed templates through MCP or CLI. | Artifact shape, staged guidance, template validity. | Pending. |
| V003 | Run runtime scan: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`. | Active spec inventory and template authority. | Pending. |
| V004 | Add focused runtime tests for `lifecycle_guide`, stage readiness, and bootstrap planning. | Deterministic output, blank-repo behavior, tooling preservation. | Pending. |
| V005 | Add traceability/coverage tests for correctness-property and acceptance-criteria gaps. | Properties-to-tests readiness. | Pending. |
| V006 | Add MCP tests or direct server dispatch tests for new read-only tools. | MCP exposure, read-only behavior, repo-root handling. | Pending. |
| V007 | Validate prompt definitions: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts`. | First-run prompt definitions and schema compatibility. | Pending. |
| V008 | Review durable docs and skill guidance manually against the accepted eight ideas and non-goals. | Guidance quality and scope control. | Pending. |
| V009 | Run `git diff --check`. | Whitespace and patch hygiene. | Pending. |

## Quality Gates

- `ready_to_implement`: requirements, design, tasks, traceability, and this
  verification plan are coherent; open questions are either answered or assigned
  to implementation tasks.
- `ready_to_validate`: runtime/MCP changes have focused tests and docs claiming
  tool behavior have matching implementation evidence.
- `ready_to_close`: accepted behavior is promoted to durable docs, bundle parity
  is complete, validation evidence is recorded, and residual work is routed.

## Residual Risks

- Adding too much bootstrap automation could create unwanted docs in blank repos.
  Mitigation: v1 bootstrap remains preview-first unless a later task explicitly
  designs guarded writes.
- Adding stage readiness to existing preflight could make payloads noisy.
  Mitigation: prefer concise summary fields and detailed diagnostics only when
  blockers exist.
- Agent directives could become invented conventions in young repositories.
  Mitigation: require evidence-derived or user-confirmed directives.
- Runtime and prompt behavior could drift if prompt guidance is updated without
  matching tool output.
  Mitigation: validate prompt definitions and add focused runtime tests before
  durable docs claim behavior.

## Evidence Log

| Date | Evidence | Result | Notes |
| --- | --- | --- | --- |
| 2026-06-13 | MCP `scan_specs` before spec creation. | Pass | Existing active specs were healthy; fallback template authority was reported. |
| 2026-06-13 | MCP `lint_spec_package` after initial draft. | Warn | Authoring warnings identified missing expected sections; this package was updated to add them. |
| 2026-06-13 | MCP `lint_spec_package` for `docs/specs/024-staged-developer-onboarding`. | Pass | Phase 1 task states and traceability updates produced 0 diagnostics. |
| 2026-06-13 | MCP `traceability_lookup` for T001, T002, and T003. | Pass | Phase 1 task-context rows resolved with no gaps after normalizing traceability column names and requirement references. |
| 2026-06-13 | MCP `lint_doc` for changed fallback spec-package templates. | Pass | `requirements.md`, `design.md`, `tasks.md`, `traceability.md`, and `verification.md` returned 0 diagnostics. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`. | Pass | Active spec inventory reported 2 active specs, both passing, and skill-fallback template authority. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts`. | Pass | Prompt definitions returned 0 diagnostics. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`. | Pass | 133 tests passed after syncing source skill changes to bundled Codex and Claude plugin copies. |
| 2026-06-13 | `git diff --check`. | Pass | No whitespace errors. |
| 2026-06-13 | Focused runtime and MCP tests for lifecycle guide and bootstrap plan. | Pass | 6 focused tests passed for blank/near-blank bootstrap previews, active-spec readiness, CLI JSON output, MCP tool listing, and read-only MCP tool calls. |
| 2026-06-13 | MCP `lint_spec_package` for `docs/specs/024-staged-developer-onboarding`. | Pass | Phase 2 task evidence and state produced 0 diagnostics. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`. | Pass | Active spec inventory reported 2 active specs, both passing, and skill-fallback template authority after phase 2. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`. | Pass | Prompt definitions returned 0 diagnostics with `developer-start` included. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`. | Pass | 138 tests passed after lifecycle guide, bootstrap plan, MCP, and prompt updates. |
| 2026-06-13 | Focused runtime and MCP tests for stage readiness. | Pass | 7 focused tests passed for ready coverage, property and acceptance gaps, downstream review needs, CLI JSON output, MCP tool listing, and MCP `stage_readiness` calls. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py stage-readiness docs/specs/024-staged-developer-onboarding`. | Pass | Stage readiness reported 0 blocking, context, downstream, property, and acceptance gaps after traceability coverage was updated. |
| 2026-06-13 | MCP `lint_doc` for `docs/reference/spec-lifecycle-runtime.md`, `docs/design/spec-lifecycle-management.md`, and `docs/reference/document-routing-and-expert-review-matrix.md`. | Pass | Durable docs returned 0 diagnostics after lifecycle guide, bootstrap, stage readiness, Agent Readiness Contract, coverage, directive, numbered-finding, learning-loop, and recovery guidance updates. |
| 2026-06-13 | MCP `lint_spec_package` for `docs/specs/024-staged-developer-onboarding`. | Pass | Phase 3 task evidence, traceability coverage, and durable-doc promotion produced 0 diagnostics. |
| 2026-06-13 | Final validation for T010. | Pass | MCP spec lint, MCP prompts, MCP archive index, CLI scan, CLI prompts, CLI archive-index, package-contract, full unit suite, and `git diff --check` passed; full unit suite ran 141 tests. |
| 2026-06-13 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .`. | Advisory | Source-to-Codex-bundle and source-to-Claude-bundle parity passed; installed Codex cache drift remains and requires reinstall/reload if current-session MCP or hooks must use the refreshed package. |

## Closure Requirements

- Durable docs updated: `docs/reference/spec-lifecycle-runtime.md`,
  `docs/design/spec-lifecycle-management.md`, and any affected routing/review
  guidance.
- Source and bundled skill/plugin copies synchronized where existing tests
  require parity.
- Validation evidence recorded in this file or task evidence.
- Follow-up work routed to backlog, roadmap, or a smaller follow-up spec.
