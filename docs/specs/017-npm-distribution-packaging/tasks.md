---
title: npm distribution packaging tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-11
---

# npm Distribution Packaging Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004 -> T005 -> T006 -> T007 -> T008 -> T009
```

## Tasks

- [x] T001 Define focused distribution packaging spec.
  - Depends on: none
  - Requirement: Requirement 1; Requirement 2; Requirement 3; Requirement 4
  - Files: `docs/specs/017-npm-distribution-packaging/`
  - Acceptance: Spec defines npm package contract, layout, installer,
    validation, provenance, docs, and non-goals for publishing.
  - Evidence: Created and reconciled this spec package; GHCR/Docker framing was
    superseded by the npm pivot.

- [x] T002 Add npm package contract artifacts.
  - Depends on: T001
  - Requirement: Requirement 1; Requirement 3
  - Files: `package.json`, `packaging/spec-lifecycle-manager/npm-package.json`,
    `packaging/spec-lifecycle-manager/npm-install.js`,
    `packaging/spec-lifecycle-manager/package-manifest.json`
  - Acceptance: Contract defines package name, version source, payload root,
    install command, bin path, required paths, provenance, and publish status.
  - Evidence: Added root npm manifest, npm contract, executable installer bin,
    and npm distribution metadata.

- [x] T003 Remove superseded Docker/GHCR package artifacts.
  - Depends on: T002
  - Requirement: Requirement 4
  - Files: `packaging/spec-lifecycle-manager/Containerfile`,
    `packaging/spec-lifecycle-manager/ghcr-package.json`
  - Acceptance: Docker image packaging is no longer presented as the active
    package target.
  - Evidence: Removed the GHCR image contract and Containerfile from the active
    package tree.

- [x] T004 Add deterministic package contract validation.
  - Depends on: T002
  - Requirement: Requirement 1; Requirement 2; Requirement 3
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_plugin_package.py`
  - Acceptance: `package-contract` reports npm package metadata, required path
    status, source/bundle parity, provenance, diagnostics, and summary; tests
    verify npm package metadata and `npm pack --dry-run` payload.
  - Evidence: Added npm-aware validation and package tests.

- [x] T005 Promote install and distribution docs.
  - Depends on: T004
  - Requirement: Requirement 4
  - Files: `docs/reference/spec-lifecycle-manager-mcp-install.md`,
    `docs/reference/spec-lifecycle-runtime.md`, `docs/backlog/README.md`
  - Acceptance: Docs describe local install and npm package install, identify
    npm publish as future work, and avoid presenting Docker/GHCR as the useful
    distribution path.
  - Evidence: Updated runtime docs, install docs, and B026 backlog wording.

- [x] T006 Validate and prepare closure.
  - Depends on: T005
  - Requirement: Requirement 1; Requirement 2; Requirement 3; Requirement 4
  - Files: `docs/specs/017-npm-distribution-packaging/verification.md`
  - Acceptance: Focused tests, full tests, package-contract, npm pack dry-run,
    sync-guard, spec lint, closure check, and whitespace validation are
    recorded.
  - Evidence: Focused runtime/package tests passed; full unittest suite
    passed; `package-contract` passed; `npm pack --dry-run --json` produced
    the expected tarball payload without bytecode artifacts; `sync-guard`
    reported source/bundle in sync and installed cache drift pending reinstall;
    spec lint and whitespace checks passed.

- [x] T007 Add Claude Code plugin wrapper.
  - Depends on: T006
  - Requirement: Requirement 5
  - Files: `plugins/spec-lifecycle-manager/claude-plugin/`,
    `packaging/spec-lifecycle-manager/package-manifest.json`,
    `packaging/spec-lifecycle-manager/npm-package.json`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`,
    `tests/runtime/test_spec_plugin_package.py`
  - Acceptance: Claude plugin manifest, MCP config, hook config, skill payload,
    package metadata, and package tests are present.
  - Evidence: Added Claude plugin wrapper, package metadata, install docs, and
    package tests.

- [x] T008 Validate Claude plugin packaging.
  - Depends on: T007
  - Requirement: Requirement 1; Requirement 2; Requirement 5
  - Files: `docs/specs/017-npm-distribution-packaging/verification.md`
  - Acceptance: Focused package tests, full tests, package-contract, npm pack
    dry-run, spec lint, closure check, and whitespace validation are recorded
    after Claude plugin packaging.
  - Evidence: Focused Claude/package tests passed; package-contract passed;
    npm pack dry-run included the Claude plugin payload; full unittest suite
    passed; sync-guard reported source/bundle parity with installed cache drift
    pending reinstall; whitespace validation passed.

- [x] T009 Fix review packet type mapping.
  - Depends on: T008
  - Requirement: Requirement 6
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`,
    `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`,
    `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`,
    `docs/reference/spec-lifecycle-runtime.md`,
    `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: `implementation` and `implementation-readiness` map to
    `implementation_review`; unknown non-empty values map to `generic_review`;
    MCP schema publishes canonical IDs, aliases, default, and fallback
    behavior.
  - Evidence: Focused runtime/MCP tests passed; direct CLI review-packet calls
    for `implementation-readiness` and `release-polish` returned
    `implementation_review` and `generic_review` respectively.
