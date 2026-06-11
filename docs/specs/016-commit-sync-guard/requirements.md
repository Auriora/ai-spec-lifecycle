---
title: Commit sync guard requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Commit Sync Guard Requirements

## Introduction

Changes to `skills/spec-lifecycle-manager/` can leave the bundled plugin,
installed plugin cache, or active Codex session stale. Agents need a
deterministic read-only check before claiming packaging, install, or lifecycle
runtime work is complete.

The guard is specific to this `agent-dev-lifecycle` repository because it
validates the maintained Spec Lifecycle Manager source tree, bundled plugin
tree, package manifests, installer, and local Codex plugin cache.

## Goals

- Report source skill versus bundled plugin parity.
- Report bundled plugin versus installed plugin cache parity.
- Report whether Codex/MCP may need reload after install.
- Report whether recent commits touching `skills/spec-lifecycle-manager/` also
  touched package or install evidence.
- Keep the first implementation read-only and deterministic.
- Return a clear not-applicable result outside this package repository.

## Non-Goals

- Do not automatically install, sync, restart, kill, or reload anything.
- Do not enforce a blocking Git hook.
- Do not inspect private transcript or shell history.
- Do not require Codex to be installed for repository validation.
- Do not run as a generic target-repository lifecycle check.

## Glossary

| Term | Definition |
| --- | --- |
| Source skill | Maintained skill source under `skills/spec-lifecycle-manager/`. |
| Bundled plugin | Repository plugin package under `plugins/spec-lifecycle-manager/`. |
| Installed cache | Codex plugin cache copy under `~/.codex/plugins/cache/`. |
| Sync evidence | Package, installer, manifest, or install/runtime documentation touched with a skill-changing commit. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
| --- | --- | --- | --- |
| `docs/backlog/README.md` B016 | Tracks commit sync guard as a candidate backlog item. | high | Source of requested backlog scope. |
| `docs/roadmap/README.md` R005 | Identifies commit sync guard as the next lifecycle hardening horizon. | high | Source of sequencing. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Documents supported plugin install model, plugin cache location, validation checklist, and reload troubleshooting. | high | Promotion target. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime commands and MCP surface behavior. | high | Promotion target. |
| `tests/runtime/test_spec_plugin_package.py` | Already verifies source skill and bundled plugin skill parity. | high | Existing deterministic test baseline. |

## Requirements

### Requirement 1: Source And Bundle Parity

**User Story:** As a lifecycle maintainer, I want to compare the source skill
with the bundled plugin skill, so that package drift is visible before install.

#### Acceptance Criteria

1. GIVEN the source skill and bundled plugin skill exist, WHEN the sync guard
   runs, THEN it SHALL report whether their non-generated file sets and file
   contents match.
2. IF either path is missing, THEN the sync guard SHALL return a structured
   finding instead of failing with an unhandled exception.
3. WHERE generated cache artifacts such as `__pycache__` exist, THE SYSTEM
   SHALL exclude them from parity checks.

### Requirement 1A: Repository Applicability

**User Story:** As a maintainer, I want the sync guard to identify whether it
is running in the package repository, so that target repositories do not receive
irrelevant package drift warnings.

#### Acceptance Criteria

1. GIVEN a repository does not contain the Spec Lifecycle Manager source,
   bundled plugin, package manifest, and installer paths, WHEN the sync guard
   runs, THEN it SHALL return `status: "not_applicable"`.
2. IF the guard is not applicable, THEN it SHALL return no parity drift
   findings.
3. WHERE the package repository paths exist, THE SYSTEM SHALL continue with
   parity, cache, reload advisory, and commit evidence checks.

### Requirement 2: Bundle And Installed Cache Parity

**User Story:** As a lifecycle maintainer, I want to compare the bundled plugin
with the installed plugin cache, so that reinstall drift is visible.

#### Acceptance Criteria

1. GIVEN an installed Codex plugin cache candidate exists, WHEN the sync guard
   runs, THEN it SHALL report whether the bundled plugin and cache candidate
   match at file-set and content level.
2. IF no installed cache candidate exists, THEN the sync guard SHALL report the
   cache as missing or unknown without treating repository validation as a
   crash.
3. WHERE multiple cache candidates exist, THE SYSTEM SHALL identify the
   candidate used for comparison and report the candidate count.

### Requirement 3: MCP Reload Advisory

**User Story:** As a lifecycle maintainer, I want package drift translated into
a reload advisory, so that I can reload Codex when needed without relying on
OS-specific process inspection.

#### Acceptance Criteria

1. GIVEN source/bundle or bundle/cache drift exists, WHEN the sync guard runs,
   THEN it SHALL report that Codex/MCP may need reload after sync and install.
2. GIVEN source, bundled plugin, and installed cache parity checks are clean,
   WHEN the sync guard runs, THEN it SHALL report that reload is not required by
   the guard.
3. THE SYSTEM SHALL NOT enumerate OS process tables to determine reload state.

### Requirement 4: Commit Evidence Review

**User Story:** As a lifecycle maintainer, I want recent skill-changing commits
checked for package/install evidence, so that commits do not silently omit the
sync step.

#### Acceptance Criteria

1. GIVEN recent Git commits exist, WHEN a commit touched
   `skills/spec-lifecycle-manager/`, THEN the sync guard SHALL report whether
   the same commit touched bundled plugin files, installer files, package
   manifests, or install/runtime documentation.
2. IF Git history is unavailable, THEN the sync guard SHALL report a structured
   unknown state.
3. WHERE no recent commit touched the source skill, THE SYSTEM SHALL report that
   no commit evidence finding applies.

## Success Criteria

- `spec_runtime.py sync-guard .` returns deterministic JSON.
- Running `sync-guard` outside this package repository returns
  `not_applicable`.
- Existing plugin parity tests continue to pass.
- Install/runtime docs include the new validation command.

## Correctness Properties

- **CP-001**: Parity reports are deterministic for the same file trees and
  ignore only documented generated artifacts.
- **CP-002**: The sync guard never mutates repository files, Codex config,
  installed caches, or running processes.
- **CP-003**: Missing optional external state, such as Codex cache or Git
  history, is reported as structured unknown or missing evidence.

## Technical Context

- **Language/Version:** Python 3.9+ standard library.
- **Primary Dependencies:** None beyond Git for commit evidence when available.
- **Target Platform:** Local repository and local Codex plugin installation.
- **Constraints:** Read-only, deterministic, repo-relative reporting where
  possible.
- **Performance Goals:** Complete within normal validation command latency for
  this repository-sized package.

## Related Artifacts

- Change Impact: `change-impact.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
