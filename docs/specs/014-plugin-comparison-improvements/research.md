---
title: Plugin comparison improvements research
doc_type: spec
artifact_type: research
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Research

## Scope

This research records external plugin references for deeper analysis. The
repositories are advisory comparison inputs only. They do not become
requirements unless this spec explicitly accepts a bounded improvement.

## Reference Repositories

### Praxis

- URL: `https://github.com/ouonet/praxis`
- Stated purpose: "From idea to shipped code -- a praxis of engineering for AI
  agents."
- Initial observations:
  - Uses a lightweight startup/triage model before loading heavier skills.
  - Emphasizes "what, not how" and compact skills.
  - Maintains a living-doc/staging-doc split.
  - Includes cross-harness plugin layout for multiple agent systems.
- Candidate ideas:
  - Add lifecycle triage before full spec workflow.
  - Add a compact startup/default skill for "using spec lifecycle."
  - Keep skill guidance concise and route detailed behavior to MCP/runtime docs.
- Risks:
  - Praxis's staging model differs from this repository's active-spec and
    durable-doc promotion model.
  - Token-minimal guidance can become too terse for lifecycle governance.

### Spec Driven

- URL: `https://github.com/Habib0x0/spec-driven-plugin`
- Stated purpose: "Spec-driven development workflow with structured
  requirements, design, tasks, and autonomous execution."
- Initial observations:
  - Presents an explicit command surface for spec creation, status, validation,
    execution, loops, docs, release, verification, and retrospective.
  - Uses EARS requirements and a three-phase workflow.
  - Supports cross-spec dependencies and CI-friendly execution signals.
- Candidate ideas:
  - Add clearer Codex-facing status, validate, and complete prompt aliases.
  - Add explicit dependency-state modeling when multiple active specs exist.
  - Consider machine-readable lifecycle status output for CI/hooks.
- Risks:
  - Autonomous loop behavior is broader and riskier than this plugin's
    advisory/MCP-first model.
  - Its default `.claude/specs/` location conflicts with this repository's
    durable `docs/specs/` convention.

### Superpowers

- URL: `https://github.com/obra/superpowers`
- Stated purpose: "An agentic skills framework & software development
  methodology that works."
- Initial observations:
  - Uses mandatory skill workflows for brainstorming, planning, TDD, debugging,
    review, and branch finishing.
  - Emphasizes verification-before-completion and review gates.
  - Provides a broad skill library with specific triggers.
- Candidate ideas:
  - Add explicit lifecycle gate markers for ready-to-implement, ready-to-close,
    and ready-to-archive states.
  - Strengthen completion evidence language.
  - Add review-oriented prompt aliases without importing the full methodology.
- Risks:
  - Full Superpowers workflow is heavier than this repository needs.
  - Some workflows overlap with already installed Superpowers plugin skills and
    should not be duplicated.

### Codex Plugin Documentation

- Build docs: `https://developers.openai.com/codex/plugins/build`
- Overview docs: `https://developers.openai.com/codex/plugins`
- Current relevance:
  - Plugin components should be bundled under the plugin root.
  - `.mcp.json` and `hooks/hooks.json` are plugin-root component files.
  - Plugin installation should not depend on a separately synced skill copy.

## Initial Recommendation

Prioritize a small comparison-driven enhancement set:

1. Durable comparison artifact.
2. Lifecycle triage prompt/tool.
3. Status/validate/complete prompt aliases.
4. Explicit lifecycle gate markers.
5. Backlog/roadmap routing for deferred ideas.

Do not implement autonomous execution loops or replace the documentation model
as part of this spec.

## Open Research Questions

- Should lifecycle triage be a deterministic runtime/MCP tool, a prompt
  definition, or skill-only guidance?
- Which prompt aliases should be exposed first for Codex users?
- Should dependency modeling remain per spec package, or span backlog and
  roadmap items too?
