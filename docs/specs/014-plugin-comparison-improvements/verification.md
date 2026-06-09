---
title: Plugin comparison improvements verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Verification

## Quality Gates

| Gate | Command or Review | Required Evidence |
|------|-------------------|-------------------|
| Spec package scan | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | Active spec has no blocking diagnostics. |
| Unit tests | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Tests pass. |
| Archive index | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | No diagnostics. |
| Prompt definitions | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | No diagnostics. |
| Plugin validation | `python3 /home/bcherrington/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/spec-lifecycle-manager` | Plugin validates. |
| Whitespace | `git diff --check` | No whitespace errors. |
| Comparison review | Manual review of durable comparison artifact | External references preserved and each idea routed. |

## Evidence Log

| Date | Task | Evidence | Result |
|------|------|----------|--------|
| 2026-06-06 | Spec creation | Created initial spec package. | pending validation |
| 2026-06-07 | T010 | Added Agent Skills optional metadata to source and bundled `SKILL.md`; added source/bundled skill drift tests; routed `skills-ref validate` integration to backlog B028. Focused package tests, plugin validation, spec lint, next-task traceability, and whitespace check passed. | pass |
| 2026-06-09 | T001-T002 | Added `docs/reference/plugin-comparison-improvements.md` and resolved D001-D005 in `open-decisions.md`. | pass |
| 2026-06-09 | T003-T007 | Added lifecycle status, validate, complete, and triage prompt definitions; added lifecycle triage and gate guidance; mirrored changes into bundled plugin. | pass |
| 2026-06-09 | Template guidance | Added checkpoint-task and property-test task guidance to source and bundled skill templates in commit `41bdf92`. Focused template lint, full tests, scan, prompt validation, archive index validation, plugin validation, and whitespace checks passed. | pass |
| 2026-06-09 | T008 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`, focused prompt/runtime tests, and `git diff --check` passed after prompt additions. | pass |

## Closure Readiness

Before closure:

- All tasks in `tasks.md` have evidence.
- Open decisions are resolved or explicitly deferred.
- Accepted comparison findings are promoted to durable docs, runtime, prompts,
  skill guidance, backlog, or roadmap.
- Plugin package validation passes if plugin files changed.
- Closure log and archive index entries can be prepared.

## Residual Risks

| Risk | Status | Notes |
|------|--------|-------|
| External repositories may change after analysis. | open | Preserve commit URLs or dated notes during implementation if exact evidence is needed. |
| Prompt aliases may overlap with existing skills/plugins. | accepted risk | Aliases are lifecycle-specific MCP prompt definitions and validate through the runtime. |
| Triage may be too subjective for deterministic runtime. | mitigated | D001 selected prompt and skill guidance; deterministic runtime triage is deferred to backlog. |
