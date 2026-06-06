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
- [Coding agent operating model](design/coding-agent-operating-model.md): risk-scaled workflow model for coding-agent implementation, evidence, review, metrics, and closure.
- [Agent development lifecycle constitution](governance/constitution.md): governance principles and decision gates for specs, evidence, migration, and durable docs.
- [Document routing and expert review matrix](reference/document-routing-and-expert-review-matrix.md): where spec content should land and which role-based experts should review it.
- [AI-native SDD framework landscape](reference/ai-native-sdd-frameworks.md): reference list of spec-driven AI development systems and adjacent methodologies to study.
- [Coding agent workflow research](reference/coding-agent-workflow-research.md): evidence and recommendations for operator-guided coding-agent workflows.
- [Spec lifecycle runtime](reference/spec-lifecycle-runtime.md): deterministic CLI helper surface for spec scanning, linting, task context, hooks, prompts, reconciliation, promotion planning, and review packets.
- [Spec lifecycle manager MCP install](reference/spec-lifecycle-manager-mcp-install.md): local host-level MCP install, validation, and Agent Workbench companion-server boundary.
- [Spec lifecycle dogfood evaluation](reference/spec-lifecycle-dogfood-evaluation.md): external verification and dogfood feedback for the skill, MCP server, runtime tools, and advisory hooks.
- [Backlog](backlog/README.md): proposed or deferred lifecycle work that is not yet a focused implementation spec.
- [Roadmap](roadmap/README.md): sequenced lifecycle work, adoption stages, and multi-spec dependencies.
- [Spec archive index](history/spec-archive-index.md): compact Git-backed index of closed spec package archive state.
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
  adapt when they do not already have their own `docs/templates/` system,
  including backlog and roadmap templates for deferred work.

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

The installed skill also includes a local read-only stdio MCP server:

```bash
python3 ~/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py /path/to/repo
```

Use the repository source path instead of `~/.codex` while developing this
repo:

```bash
python3 skills/spec-lifecycle-manager/scripts/spec_mcp_server.py "$PWD"
```

## Specs

Active implementation specs use `docs/specs/[###-slug]/` by default.

When working inside a repository with its own documentation approach, lifecycle
material may live under a named docs partition such as
`docs/<name>/specs/[###-slug]/` to keep the target repository's documentation
clean.

Specs are temporary delivery packages. Once implementation is complete,
accepted behavior must be promoted into durable documentation that represents
the actual current implementation. The completed spec package should then be
removed from the active docs tree unless a repository-specific policy explicitly
requires visible historical spec packages.

Closed specs are discoverable through a spec closure log, defaulting to
`docs/history/spec-closure-log.md` when no repository-specific closure record
exists. The closure log records the final spec commit, closure action, durable
destinations, verification summary, residual risks, and follow-up work.

Use `docs/history/spec-archive-index.md` as the compact lookup surface for
closed spec package archive state. The closure log remains the narrative
history; the archive index is the machine-checkable index for removed or
explicitly retained packages.
