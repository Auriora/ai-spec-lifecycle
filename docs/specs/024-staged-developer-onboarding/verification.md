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

## Closure Requirements

- Durable docs updated: `docs/reference/spec-lifecycle-runtime.md`,
  `docs/design/spec-lifecycle-management.md`, and any affected routing/review
  guidance.
- Source and bundled skill/plugin copies synchronized where existing tests
  require parity.
- Validation evidence recorded in this file or task evidence.
- Follow-up work routed to backlog, roadmap, or a smaller follow-up spec.
