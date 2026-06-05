---
title: Agent development lifecycle docs
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-02
---

# Agent Development Lifecycle Docs

This documentation describes reusable agent workflows for managing implementation work from requirements through specs, code, validation, and durable documentation.

## Start Here

- [Spec lifecycle management](design/spec-lifecycle-management.md): current lifecycle model for temporary implementation specs and durable docs.
- [Agent development lifecycle constitution](governance/constitution.md): governance principles and decision gates for specs, evidence, migration, and durable docs.
- [Document routing and expert review matrix](reference/document-routing-and-expert-review-matrix.md): where spec content should land and which role-based experts should review it.
- [AI-native SDD framework landscape](reference/ai-native-sdd-frameworks.md): reference list of spec-driven AI development systems and adjacent methodologies to study.
- [Coding agent workflow research](reference/coding-agent-workflow-research.md): evidence and recommendations for operator-guided coding-agent workflows.
- [Spec lifecycle manager skill spec](specs/001-spec-lifecycle-manager-skill/spec.md): archived implementation and validation history for the reusable skill.

## Skill Source And Install

The canonical `spec-lifecycle-manager` skill source is tracked in this repository:

```text
skills/spec-lifecycle-manager/
```

It may be installed into the local Codex environment for use in a session:

```text
~/.codex/skills/spec-lifecycle-manager/
```

Treat the repository copy as the source of truth and the `~/.codex` copy as an
installed artifact. Use the skill when creating, continuing, reconciling,
reviewing, implementing from, promoting, or closing implementation spec
packages.

The skill includes fallback templates under:

- `skills/spec-lifecycle-manager/references/spec-package/` for temporary
  implementation spec packages.
- `skills/spec-lifecycle-manager/references/durable-doc-templates/` for
  optional durable documentation classes that selected projects can copy or
  adapt when they do not already have their own `docs/templates/` system.

This repository's `docs/` tree documents the skill and its validation history;
reusable project templates live with the skill source.

Run this from the repository root to install or update the local working copy
from the repository source:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete skills/spec-lifecycle-manager/ "$CODEX_HOME/skills/spec-lifecycle-manager/"
```

Example invocation:

```text
Use $spec-lifecycle-manager to reconcile this active spec package, choose the
next implementation slice, and identify durable documentation updates.
```

## Specs

Active implementation specs use `docs/specs/[###-slug]/` by default.

When working inside a repository with its own documentation approach, lifecycle
material may live under a named docs partition such as
`docs/<name>/specs/[###-slug]/` to keep the target repository's documentation
clean.

Specs are temporary delivery packages. Once implementation is complete, accepted behavior should be promoted into durable documentation and the spec should be closed, archived, or removed according to the target repository's document lifecycle.
