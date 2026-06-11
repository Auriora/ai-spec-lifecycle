---
title: Hierarchical spec authoring hooks design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Design

## Overview

Change ordinary spec markdown write feedback from package-wide lint to
contextual authoring guidance. The hook runtime will inspect the affected spec
tree, classify the authoring mode, and return focused next-action diagnostics.
Explicit validation, resume, and closure hooks keep their full-package behavior.

## High-Level Design

- Add a spec artifact hierarchy model to the runtime.
- Add a read-only spec-tree context helper that reports changed artifacts,
  existing artifacts, missing prerequisites, downstream artifacts, and
  recommended helper surfaces.
- Update `spec-file-changed` so ordinary authoring uses the hierarchy-aware
  helper instead of unconditional full package lint.
- Preserve full package lint for explicit validation commands and lifecycle
  events such as resume and closure.
- Update the Codex hook wrapper context builder to prefer next-action guidance
  over a flat diagnostic dump when the runtime returns authoring guidance.

## Low-Level Design

- Define artifact order in `spec_runtime.py`, for example:
  `research.md`, `requirements.md`, `design.md`, `tasks.md`,
  `traceability.md`, `verification.md`, and closure artifacts.
- Introduce a helper shaped like
  `spec_authoring_context(repo_root, changed_files, hook_name)` that returns:
  - `mode`;
  - `changed_artifacts`;
  - `existing_artifacts`;
  - `missing_prerequisites`;
  - `next_authoring_step`;
  - `downstream_review`;
  - `recommended_tools`;
  - `diagnostics`.
- Treat `requirements.md` and `design.md` revisions as upstream edits when
  downstream artifacts already exist. The result recommends downstream review
  but does not label those files as the next step.
- Keep task evidence checks in `task-checkbox-changed`,
  `implementation-task-complete`, and `agent-response-check`. If `tasks.md` is
  changed by ordinary file write, only task-shape diagnostics should be included
  unless task completion is detected or the hook event is explicitly
  task-focused.
- Extend the Codex wrapper's `build_context` logic to include a compact message
  from authoring guidance fields when present, then fall back to diagnostic
  lines for older runtime payloads.

## Operational Considerations

- The hook remains advisory and exits successfully.
- The change should reduce false-positive fatigue without weakening explicit
  validation paths.
- The hierarchy must be configurable only through code in this slice; repo-local
  hook profiles can be considered later if needed.
- Bundled plugin copies must be mirrored because installed hooks execute from
  bundled skill paths.

## Open Questions

- Whether task-diff awareness can reliably isolate changed task IDs from Codex
  hook payloads may need implementation proof. If not, the task-focused mode
  should clearly label when it falls back to full task lint.
