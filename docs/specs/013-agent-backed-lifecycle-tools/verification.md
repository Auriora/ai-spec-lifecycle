---
title: Agent-backed lifecycle tools verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Verification

## Quality Gates

| Gate | Command or Review | Expected Result | Evidence |
|------|-------------------|-----------------|----------|
| Spec scan | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | One active spec, active lint pass or documented warnings. | Pending |
| Spec lint | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/013-agent-backed-lifecycle-tools` | No blocking diagnostics. | Pending |
| Traceability lookup | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/traceability_lookup.py docs/specs/013-agent-backed-lifecycle-tools --task T001 --format text` | Task context resolves with no unexpected gaps. | Pending |
| Unit tests | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Pass. | Pending |
| Prompt validation | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | No diagnostics. | Pending |
| Archive validation | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | No diagnostics before closure; updated after closure. | Pending |
| Whitespace | `git diff --check` | Clean. | Pending |
| Active spec preflight | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py active-spec-preflight . --task-id T001` | Returns active spec 013 and readiness packet for T001. | Passed 2026-06-06 |
| Agent readiness packet | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py agent-readiness-packet docs/specs/013-agent-backed-lifecycle-tools --task-id T001` | Returns bounded task context with no gaps. | Passed 2026-06-06 |

## Evidence Log

| Date | Task | Evidence |
|------|------|----------|
| 2026-06-06 | Spec creation | Initial requirements, design, change impact, tasks, traceability, verification, and open decisions created. |
| 2026-06-06 | T001-T006 deterministic foundation tools | Implemented `active_spec_preflight`, `agent_readiness_packet`, and `no_active_spec_context` in CLI/runtime and MCP surfaces. Focused runtime and MCP tests passed. |

## Residual Risks

- Agent runner integration may depend on Codex or MCP capabilities outside this
  repository's deterministic runtime.
- Cheap-agent outputs may appear plausible while being semantically weak; lead
  agent review remains required.
- Tool scope may expand too quickly if write-capable behavior is not kept in a
  separate future spec.
