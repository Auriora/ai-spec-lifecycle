---
title: AI-native SDD framework landscape
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-02
---

# AI-Native SDD Framework Landscape

## Purpose

Capture current AI-native spec-driven development frameworks and adjacent AI
development methodologies for later comparison with the
`spec-lifecycle-manager` skill.

This reference focuses on systems that shape how AI coding agents move from
intent to specs, plans, tasks, implementation, review, and closure. It does not
cover classic contract-first tools such as OpenAPI, AsyncAPI, Smithy, Buf,
Pact, Cucumber, or Schemathesis except as background context.

## Source Of Truth

Canonical project sources remain the upstream repositories and documentation:

- GitHub Spec Kit: `https://github.com/github/spec-kit`
- OpenSpec: `https://github.com/Fission-AI/OpenSpec` and
  `https://openspec.dev/`
- Spec Kitty: `https://github.com/Priivacy-ai/spec-kitty`
- SpecDD: `https://github.com/specdd/specdd` and `https://specdd.ai/`
- SDD Pilot: `https://sdd-pilot.szaszattila.com/`
- SpecPulse: `https://github.com/specpulse/specpulse`
- OpenSDD: `https://opensdd.ai/`
- HiveSpec: `https://hivespec.dev/`
- Cliplin: `https://cliplin.dev/`
- Superpowers: `https://github.com/obra/superpowers`
- BMAD Method: `https://github.com/bmadcode/BMAD-METHOD` and
  `https://www.bmadcode.com/bmad-method/`
- Kiro: `https://kiro.dev/`

This snapshot was recorded on 2026-06-02.

## Study First List

Study these systems first when improving `spec-lifecycle-manager`:

1. OpenSpec
2. Spec Kitty
3. SpecDD
4. Superpowers
5. BMAD Method
6. Kiro

Rationale: these systems are closest to the lifecycle problem this repository
cares about: keeping specs, tasks, code, validation, review, and durable
documentation aligned across agent-assisted implementation. Kiro is included in
the first study set even though it is a commercial environment because it has a
native spec workflow and already has a local compatibility review in
[Kiro compatibility review](kiro-compatibility-review.md).

## AI-Native SDD Frameworks

| System | Type | Primary workflow or shape | Notable ideas to study |
| --- | --- | --- | --- |
| GitHub Spec Kit | Open source CLI and agent integration toolkit | `constitution -> specify -> clarify -> plan -> tasks -> analyze -> implement` | Constitution governance, checklists, cross-artifact analysis, agent integrations, extensions, presets, contracts, data models. |
| OpenSpec | Lightweight open source SDD framework | Repository specs organized by capability, proposal, design, task, and spec-delta workflow | Brownfield-friendly repo-native specs, explicit proposed changes, reviewable spec deltas before coding. |
| Spec Kitty | Open source CLI workflow | `spec -> plan -> tasks -> next -> review -> accept -> merge` | Work packages, lifecycle lanes, git worktrees, local dashboard, governance layer, retrospectives, multi-agent support. |
| SpecDD | Agent-agnostic specification-driven framework | Plain-file specs in Git used by any file-aware agent | Vendor-neutral format, language specification, repository-local specs as agent-readable source of truth. |
| SDD Pilot | Spec-driven feature delivery framework | Product vision, optional system design context, specification, implementation, quality control | Product-level context, reusable system design context, QC as a first-class phase, broad AI tool support. |
| SpecPulse | CLI-first AI-enhanced SDD framework | Specifications first, AI-assisted expansion, structured planning, task breakdown | Universal AI platform support, CLI foundation, template-oriented spec and task workflows. |
| OpenSDD | Open standards methodology and tooling ecosystem | Markdown, Git, YAML, specs before code, PR-sized tasks, captured learnings | Lightweight methodology, open standards emphasis, recipes and automations rather than heavy tool lock-in. |
| HiveSpec | Spec-driven delivery lifecycle for agent swarms | Spec, build, verify, ship across a multi-phase agent lifecycle | Agent swarm discipline, issue claiming, verification evidence, shipping risk classification. |
| Cliplin | Feature-centric SDD framework | Project initialization into feature docs, TDRs, ADRs, UI intent, reusable knowledge packages | Feature docs plus decision records, reusable framework knowledge packages, shared context across package specs and project specs. |

## Adjacent AI Development Methodologies

| System | Type | Primary workflow or shape | Notable ideas to study |
| --- | --- | --- | --- |
| Superpowers | Agentic skills framework and software development methodology | Brainstorm, spec, plan, test-driven implementation, review, subagent-assisted development | Spec-first behavior, TDD enforcement, two-stage review, composable skills, agent behavior discipline. |
| BMAD Method | AI-driven agile development methodology | Specialist agents, PRDs, architecture, stories, dev and QA flows | Role-specialized agents, agile planning artifacts, story-driven delivery, QA and review infrastructure. |
| Kiro | AI-powered development environment with native spec workflow | Requirements, design, tasks, execution, agent hooks | EARS-style acceptance criteria, `.kiro/specs/` conventions, task dependency graph, correctness properties, native IDE integration. |

## Comparison Notes

### Closest To `spec-lifecycle-manager`

OpenSpec, Spec Kitty, SpecDD, Superpowers, BMAD Method, and Kiro are the most
useful comparison targets. They all address the agent lifecycle problem rather
than only API contract generation or executable tests.

### Useful Concepts By System

- GitHub Spec Kit: governance checks, checklists, read-only analysis, artifact
  chains, extension and preset model.
- OpenSpec: capability-based spec library and proposal/spec-delta review.
- Spec Kitty: mission/work-package lifecycle, worktrees, review/accept/merge
  states, retrospective capture.
- SpecDD: agent-agnostic plain-file approach and formalized spec language.
- SDD Pilot: quality-control phase and reusable system design context.
- SpecPulse: CLI-first structure with AI enhancement rather than agent-only
  prompt files.
- OpenSDD: methodology portability and lightweight open-standard recipes.
- HiveSpec: swarm lifecycle, evidence-first verification, risk-aware shipping.
- Cliplin: feature-centric documentation, TDR/ADR split, reusable knowledge
  packages.
- Superpowers: enforce process discipline through reusable agent skills.
- BMAD Method: specialist role decomposition and story-oriented delivery.
- Kiro: EARS requirements, dependency-graph tasks, correctness properties, and
  native spec folder conventions.

### Relevance To This Repository

The current skill should remain a Codex skill focused on temporary specs,
reconciliation, durable-document promotion, role-based review, and closure.
These external systems are references for improving behavior and templates, not
replacement packaging targets unless a future decision changes that.

## How To Update

Review this file when:

- adding or changing `spec-lifecycle-manager` workflow behavior;
- revisiting Kiro compatibility;
- deciding whether to adopt additional artifact types such as requirements,
  data models, contracts, checklists, dependency graphs, or review gates;
- comparing this repository's lifecycle model with current AI-native SDD tools.

When updating, refresh upstream links and record the review date in frontmatter.

## Related Docs

- [Spec lifecycle management](../design/spec-lifecycle-management.md)
- [Document routing and expert review matrix](document-routing-and-expert-review-matrix.md)
- [Kiro compatibility review](kiro-compatibility-review.md)
- [Spec lifecycle manager skill validation evidence](../specs/001-spec-lifecycle-manager-skill/validation-evidence.md)
