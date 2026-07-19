---
title: Spec closure log
doc_type: history
status: active
owner: platform
last_reviewed: 2026-07-06
---

# Spec Closure Log

This log records compact closure entries for completed spec packages. Full spec
package history is preserved by Git unless a repository-specific archive policy
requires visible archived docs.

## Entries

### 2026-07-19 - 038-lifecycle-adoption-workflow

- **Spec:** `docs/specs/038-lifecycle-adoption-workflow/`
- **Title:** Lifecycle adoption workflow requirements
- **Final spec commit:** `3731ddb`
- **Closure cleanup commit:** `2a15ec2`
- **Closure action:** removed
- **Durable docs updated:**
  - `README.md`
  - `docs/backlog/README.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reference/spec-lifecycle-dogfood-evaluation.md`
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/roadmap/README.md`
  - `skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
- **Verification summary:** `npm run validate` passed 321 Python and 26 Node
  tests plus scan, archive-index, prompt, package-contract, sync-guard, pack,
  and whitespace checks. Final MCP package lint, evidence quality,
  reconciliation, task-state audit, closure-risk review, and closure check had
  no findings or blockers; closure risk was low.
- **Residual risks:**
  - Exact external operation distributions remain unavailable until the Chat
    Analyser project resolves attribution and reconciliation defects.
  - Client loaders can still reread the compact skill, and developers must use
    the documented source-development launcher to avoid packaged duplication.
- **Follow-up:** B014 and B015 retain future bounded discovery/friction studies;
  B025 retains telemetry; Spec 034 retains phase-completion mutation; Chat
  Analyser retains analysis defects; release notes remain with the next
  packaged release workflow.

### 2026-07-12 - 037-closure-response-contract

- **Spec:** `docs/specs/037-closure-response-contract/`
- **Title:** Closure Response Contract
- **Final spec commit:** `c9be2cf`
- **Closure cleanup commit:** `60d0098`
- **Closure action:** removed
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
- **Verification summary:** Full validation passed with 307 Python and 25 Node tests; package, bundle, runtime, pack, diff, installed MCP sequence, stale-plan, and non-duplicating envelope checks passed.
- **Residual risks:**
  - Retained CLI plan-file recovery still contains complete planned file content; the agent-facing MCP boundary does not return it.
- **Follow-up:** none

### 2026-07-12 - 036-compact-output-and-invocation-telemetry

- **Spec:** `docs/specs/036-compact-output-and-invocation-telemetry/`
- **Title:** Compact lifecycle output and invocation provenance requirements
- **Final spec commit:** `4c7da1e`
- **Closure cleanup commit:** `07b731f`
- **Closure action:** removed
- **Durable docs updated:**
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `docs/design/spec-lifecycle-management.md`
- **Verification summary:** All eight tasks are complete and verified. MCP
  `closure_check` reported ready with no blockers and complete coverage for all
  four must-have requirements. `npm run validate` passed with 303 Python and
  25 Node tests plus lifecycle scan, archive/prompt/package/sync validation,
  npm dry-pack, and `git diff --check`. Source, Codex, and Claude bundles are
  in sync.
- **Residual risks:**
  - Git-derived repository identity is intentionally correlatable with known
    repository history. Legacy packages without build data report `unknown`.
    Running Codex or Claude sessions require reinstall/reload to consume the
    refreshed plugin cache.
- **Follow-up:** B025 remains the owner of emitted telemetry and remote
  observability; no implementation scope remains in Spec 036.

### 2026-07-12 - 035-spec-id-allocation-and-creation-plan

- **Spec:** `docs/specs/035-spec-id-allocation-and-creation-plan/`
- **Title:** Spec ID allocation and creation plan requirements
- **Final spec commit:** `0efc405`
- **Closure cleanup commit:** `8213417`
- **Closure action:** removed
- **Durable docs updated:**
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/design/spec-lifecycle-management.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
- **Verification summary:** All seven tasks are complete and verified. Source
  `closure-check` reports ready with complete coverage for all five prioritized
  requirements; promotion planning reports no missing targets. Full validation
  passes with 297 Python and 25 Node tests plus lifecycle/archive/prompt/
  package/sync checks, npm dry-pack, and `git diff --check`. Cleanup scan no
  longer lists Spec 035; final archive validation follows hash resolution.
- **Residual risks:** Allocation remains provisional and non-reserving. A
  future write-capable helper must atomically claim the directory. Running
  Codex or Claude sessions require plugin reinstall/reload for the new tools.
- **Follow-up:** none

### 2026-07-12 - 033-phase-gate-check

- **Spec:** `docs/specs/033-phase-gate-check/`
- **Title:** Phase gate check requirements
- **Final spec commit:** `ac690d4`
- **Closure cleanup commit:** `c97cb20`
- **Closure action:** removed
- **Durable docs updated:**
  - `docs/backlog/README.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reference/spec-lifecycle-runtime.md`
- **Verification summary:** The final package recorded all six tasks complete
  and verified. Source `closure-check` reported ready with no blockers;
  promotion planning found all four durable targets. Full pre-cleanup
  validation passed with 278 Python and 25 Node tests plus lifecycle,
  archive/prompt/package/sync, npm dry-pack, and diff checks. Cleanup scan no
  longer lists Spec 033; final archive validation follows cleanup-hash
  resolution.
- **Residual risks:** Already-running Codex or Claude sessions need the updated
  package installed and reloaded before their MCP process recognizes multiline
  verification evidence and table-form promotion baselines.
- **Follow-up:** none

### 2026-07-06 - 032-requirement-priority-labels

- **Spec:** `docs/specs/032-requirement-priority-labels/`
- **Title:** Requirement priority labels
- **Final spec commit:** `6bdc2a2`
- **Closure cleanup commit:** `1b65421`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/backlog/README.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/prompts/`
  - `skills/spec-lifecycle-manager/references/spec-package/`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/requirements.py`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py`
  - `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
  - `tests/traceability/test_traceability_lookup.py`
- **Verification summary:** Spec 032 reached 27 complete and verified tasks.
  MCP `closure_check` reported ready with no blockers and complete coverage for
  all four `must-have` requirements. The implementation evidence included
  parser/lint tests, priority-aware readiness and closure checks,
  traceability/MCP/agent-context propagation tests, prompt validation,
  package-contract and source/bundle parity checks, archive-index validation,
  and full repository validation with `SPEC_LIFECYCLE_PYTHON=python3 npm run validate`.
- **Residual risks:** Installed plugin caches and released packages may lag
  source behavior until local install/reload or release packaging runs. Plain
  `npm run validate` may require `SPEC_LIFECYCLE_PYTHON=python3` in shells
  where installer tests cannot otherwise resolve Python.
- **Follow-up:** none

### 2026-07-05 - 031-canonical-context-warning-noise

- **Spec:** `docs/specs/031-canonical-context-warning-noise/`
- **Title:** Canonical context warning noise requirements
- **Final spec commit:** `2bf6348`
- **Closure cleanup commit:** `f0b1dc5`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/prompts/`
  - `skills/spec-lifecycle-manager/references/spec-package/`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
- **Verification summary:** Full `npm run validate` passed, including Python
  unit discovery, Node tests, lifecycle scan, archive-index validation, prompt
  validation, package-contract validation, sync-guard, npm pack dry-run, and
  `git diff --check`. Spec 031 lint and task-state audit reported zero
  diagnostics. MCP `closure_check` reported ready with no blockers before
  removal.
- **Residual risks:** The released user-level npm package at version `0.2.1`
  is stale relative to this source and still contains the retired
  `traceability_lookup.py` payload; package refresh/release belongs to the
  package workflow after closure. Future dogfooding may still find novel
  authority wording that should be routed to backlog.
- **Follow-up:** none

### 2026-07-05 - 029-spec-closure-helper

- **Spec:** `docs/specs/029-spec-closure-helper/`
- **Title:** Spec closure helper
- **Final spec commit:** `1f718aa`
- **Closure cleanup commit:** `36e5524`
- **Closure action:** removed
- **Durable docs updated:**
  - `docs/backlog/README.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `docs/design/spec-lifecycle-management.md`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/runtime_adapter.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
- **Verification summary:** Spec closure helper review completed with
  `closure-check` ready, `promotion-plan` reporting 0 missing targets, and
  `closure-risk-review` reporting low risk with 0 findings. Cleanup validation
  removed active specs from scan output; archive-index validation passed after
  cleanup hash resolution; full `npm run validate` passed.
- **Residual risks:**
  - none
- **Follow-up:** none

### 2026-07-05 - 030-mcp-first-runtime-migration

- **Spec:** `docs/specs/030-mcp-first-runtime-migration/`
- **Title:** MCP-first runtime migration
- **Final spec commit:** `3e4b472`
- **Closure cleanup commit:** `bba369b`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/backlog/README.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/prompts/documentation-wizard.json`
  - `skills/spec-lifecycle-manager/references/spec-package/`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/runtime_adapter.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - `tests/runtime/test_spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
- **Verification summary:** Focused runtime and MCP regression tests passed
  with 137 tests. Full `npm run validate` passed, including lifecycle scan,
  archive-index validation, prompt validation, package-contract validation,
  sync-guard, npm pack dry-run, and `git diff --check`. Spec 030 lint and
  closure-check passed before removal; closure-check reported ready with no
  blockers.
- **Residual risks:** Already-running Codex or Claude sessions may need plugin
  reinstall/reload to use the refreshed installed MCP server, skill guidance,
  prompts, templates, and runtime adapter. Dynamic MCP tool-list refresh remains
  intentionally deferred; v1 uses a stable tool surface with
  `available_next_actions`.
- **Follow-up:** `B057` later closed through spec
  `032-requirement-priority-labels`; `B058` later closed through spec
  `031-canonical-context-warning-noise`.

### 2026-07-04 - 026-guided-documentation-wizard

- **Spec:** `docs/specs/026-guided-documentation-wizard/`
- **Title:** Guided documentation wizard
- **Final spec commit:** `de3aa4f`
- **Closure cleanup commit:** `481def5`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/prompts/`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - `tests/runtime/test_spec_runtime.py`
- **Verification summary:** Focused prompt regression tests passed with 3
  tests. Full `npm run validate` passed with 168 Python tests, 17 Node tests,
  active scan, archive-index validation, prompt validation, package-contract
  validation, sync-guard, npm pack dry-run, and `git diff --check`. Spec 026
  lint, task-state audit, evidence-quality, and closure-check passed before
  removal.
- **Residual risks:** Prompt-only wizard behavior depends on agent compliance
  and should be dogfooded for conversational quality. Already-running Codex or
  Claude sessions need package install/reload before installed plugin caches
  expose the new prompt.
- **Follow-up:** none

### 2026-07-04 - 022-npm-publish-release-workflow

- **Spec:** `docs/specs/022-npm-publish-release-workflow/`
- **Title:** npm publish and release workflow
- **Final spec commit:** `cae3a10`
- **Closure cleanup commit:** `f048239`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `.github/workflows/cross-platform.yml`
  - `.github/workflows/release.yml`
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `package.json`
  - `tests/runtime/test_github_workflows.py`
- **Verification summary:** Focused workflow regression tests passed with 2
  tests. Full `npm run validate` passed with 167 Python tests, 2 Node tests,
  lifecycle scan, archive-index validation, prompt validation,
  package-contract validation, sync-guard, npm pack dry-run, and whitespace
  checks. Spec 022 lint, task-state audit, evidence-quality, closure-check, and
  closure-risk review passed; closure-risk reported low risk with no findings.
- **Residual risks:** Local `actionlint` was unavailable, so dedicated workflow
  parser validation is deferred to GitHub Actions on push. Actual npm publish
  and remote `npx @auriora/ai-spec-lifecycle install` verification require
  configured npm access and the manual `publish=true` plus `NPM_TOKEN` gate.
- **Follow-up:** none

### 2026-07-04 - 025-dev-cli-workflow-tools

- **Spec:** `docs/specs/025-dev-cli-workflow-tools/`
- **Title:** Developer CLI workflow tools
- **Final spec commit:** `fe5aaaa`
- **Closure cleanup commit:** `9b03e1a`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `package.json`
  - `tools/README.md`
  - `tools/devcli/README.md`
  - `tools/devcli/pyproject.toml`
  - `tools/devcli/src/auriora_dev/`
  - `tests/runtime/test_devcli_cli.py`
  - `tests/runtime/test_devcli_runner.py`
- **Verification summary:** Focused dev CLI tests passed with 13 tests.
  Full Python unit discovery passed with 165 tests. Dev CLI dry-runs passed
  for `slc check`, `slc release preflight --allow-dirty`, and
  `slc package install-local --dry-run --skip-plugin-add` with
  `SPEC_LIFECYCLE_PYTHON=python3`. Package-contract validation, npm pack
  dry-run, MCP active-spec preflight, MCP closure-check, MCP closure-risk
  review, spec lint, lifecycle scan, archive-index validation, prompt
  validation, and `git diff --check` passed before removal.
- **Residual risks:** `slc package install-local` and `slc sync bundles` were
  validated in dry-run mode only; live install or bundle sync should still be
  performed deliberately. `sync-guard` reported source and bundle parity, with
  expected installed-cache drift until the packaged plugin is installed and
  already-running sessions reload.
- **Follow-up:** `B056` proposes a dedicated closure helper for final commit,
  durable promotion, package removal, and closure/archive metadata sequencing.

### 2026-07-02 - 027-spec-local-canonical-context

- **Spec:** `docs/specs/027-spec-local-canonical-context/`
- **Title:** Spec-local canonical context
- **Final spec commit:** `93766d1`
- **Closure cleanup commit:** `8f77bff`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/design/spec-lifecycle-management.md`
  - `docs/design/coding-agent-operating-model.md`
  - `docs/reference/kiro-compatibility-review.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/prompts/`
  - `skills/spec-lifecycle-manager/references/migration-guide.md`
  - `skills/spec-lifecycle-manager/references/spec-package/README.md`
  - `skills/spec-lifecycle-manager/references/spec-package/canonical-context.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - `tests/runtime/test_spec_runtime.py`
- **Verification summary:** Full unit suite passed with 151 tests. Spec 027
  lint had zero diagnostics; active spec scan reported four active specs, all
  pass; prompt validation had zero diagnostics; archive-index validation had
  zero diagnostics; package-contract passed; promotion-plan had no missing
  targets; task-state audit passed; evidence-quality reported all 14 records
  concrete; closure-risk review reported low risk with no findings;
  closure-check reported ready with no blockers; `git diff --check` passed.
- **Residual risks:** Already-running Codex or Claude sessions may need plugin
  reinstall/reload to use the refreshed skill, MCP prompt, runtime, and hook
  guidance. Installed-cache sync guard may still report expected
  installer-normalized config differences (`python` to `python3`, `30.0` to
  `30`) in MCP and hook metadata.
- **Follow-up:** none

### 2026-06-29 - 028-cross-platform-packaging

- **Spec:** `docs/specs/028-cross-platform-packaging/`
- **Title:** Cross-platform packaging
- **Final spec commit:** `1ca961d`
- **Closure cleanup commit:** `42a79c9`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `.github/workflows/cross-platform.yml`
  - `packaging/spec-lifecycle-manager/installer.mjs`
  - `packaging/spec-lifecycle-manager/resolve-python.mjs`
  - `packaging/spec-lifecycle-manager/clean-pycache.mjs`
  - `packaging/spec-lifecycle-manager/npm-install.js`
  - `packaging/spec-lifecycle-manager/npm-package.json`
  - `packaging/spec-lifecycle-manager/package-manifest.json`
  - `package.json`
  - `plugins/spec-lifecycle-manager/.mcp.json`
  - `plugins/spec-lifecycle-manager/claude-plugin/.mcp.json`
  - `plugins/spec-lifecycle-manager/hooks/hooks.json`
  - `plugins/spec-lifecycle-manager/claude-plugin/hooks/hooks.json`
  - `scripts/install-spec-lifecycle-manager-package.sh`
  - `tests/runtime/installer.test.mjs`
  - `tests/runtime/resolve-python.test.mjs`
  - `tests/runtime/smoke_cross_platform.mjs`
  - `tests/runtime/test_spec_plugin_package.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/traceability/test_traceability_lookup.py`
- **Verification summary:** Full local suite green (`npm run validate`: 147
  Python + 17 Node tests, package-contract, `npm pack` dry-run; `git diff
  --check` clean). Cross-platform CI matrix (run 28398785192) green on
  ubuntu/macos/windows × Python 3.10 & 3.12: shell-free install, MCP
  `initialize` handshake, and both hook copies (Codex shell-form and Claude
  exec-form) executed exit 0 per OS, with the Windows interpreter resolving to
  the `py` launcher as designed. The first matrix run (28386954873) went red and
  surfaced two real defects — a pre-existing Python 3.10 floor and a Windows
  test-harness `WinError 193` — both fixed. MCP spec lint and `closure_check`
  clean (0/0/0, ready=true).
- **Residual risks:** Codex exec-form hook support is unconfirmed against a live
  Codex runtime; the Codex hook ships shell-form with the resolved interpreter
  pinned in (design.md Resolved Decisions §4) — non-blocking, the fallback
  stands. The Python floor was raised 3.9 → 3.10 to match the runtime's actual
  requirement (3.9 is EOL); backporting to 3.9 remains possible if a hard need
  arises.
- **Follow-up:** none

### 2026-06-13 - 024-staged-developer-onboarding

- **Spec:** `docs/specs/024-staged-developer-onboarding/`
- **Title:** Staged developer onboarding
- **Final spec commit:** `4a2d5c8`
- **Closure cleanup commit:** `acc92ba`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reference/document-routing-and-expert-review-matrix.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
- **Verification summary:** Full unit suite passed with 141 tests. MCP spec
  lint, MCP prompt validation, MCP archive-index validation, CLI scan, CLI
  prompt validation, CLI archive-index validation, package-contract
  validation, stage-readiness validation, and `git diff --check` passed before
  removal.
- **Residual risks:** Already-running MCP sessions and hooks may need install
  and reload to use the refreshed `stage_readiness` tool. `sync-guard`
  reported source-to-bundle parity in sync and installed-cache drift before
  install.
- **Follow-up:** None.

### 2026-06-13 - 021-closure-risk-review

- **Spec:** `docs/specs/021-closure-risk-review/`
- **Title:** Closure risk review
- **Final spec commit:** `36d0135`
- **Closure cleanup commit:** `0a9e547`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
- **Verification summary:** Full unit suite passed with 133 tests. Lifecycle
  scan, spec lint, evidence-quality check, closure-check, closure-risk review,
  archive-index validation, prompt validation, package-contract validation,
  sync-guard after install, and `git diff --check` passed before removal.
- **Residual risks:** Already-running MCP sessions may need reload to pick up
  the refreshed closure-risk tool. Closure-risk output is advisory and human
  judgment remains required for semantic closure decisions.
- **Follow-up:** None.

### 2026-06-13 - 020-evidence-quality-check

- **Spec:** `docs/specs/020-evidence-quality-check/`
- **Title:** Evidence quality check
- **Final spec commit:** `ac93f24`
- **Closure cleanup commit:** `28a9cef`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
- **Verification summary:** Full unit suite passed with 128 tests. Lifecycle
  scan, spec lint, evidence-quality check, closure-check, archive-index
  validation, prompt validation, package-contract validation, sync-guard after
  install, and `git diff --check` passed before removal.
- **Residual risks:** Already-running MCP sessions may need reload to pick up
  the refreshed evidence-quality tool. Implementation-file inspection remains
  deferred to B037.
- **Follow-up:** B037 should add implementation-file inspection when that
  backlog item is ready.

### 2026-06-13 - 023-task-state-management-tools

- **Spec:** `docs/specs/023-task-state-management-tools/`
- **Title:** Task state management tools
- **Final spec commit:** `83c09ae`
- **Closure cleanup commit:** `126d08b`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/references/spec-package/`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
  - `tests/traceability/test_traceability_lookup.py`
- **Verification summary:** Full unit suite passed with 125 tests. Lifecycle
  lint, task-state audit, closure-check, package-contract parity, prompt
  validation, scan, archive-index validation, and `git diff --check` passed
  before removal.
- **Residual risks:** Already-running MCP sessions may need reload to pick up
  the newly exposed task-state tools and updated guidance.
- **Follow-up:** None.

### 2026-06-13 - 019-validation-plan-builder

- **Spec:** `docs/specs/019-validation-plan-builder/`
- **Title:** Validation plan builder
- **Final spec commit:** `d43166f`
- **Closure cleanup commit:** `b70019b`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
- **Verification summary:** Full unit suite passed with 111 tests. Lifecycle
  scan, archive-index validation, prompt validation, package-contract
  validation, npm pack dry-run, sync-guard after install, closure-check, and
  `git diff --check` passed. After install, `sync-guard` reported source
  skill, Codex bundle, Claude bundle, and installed cache all in sync with no
  findings.
- **Residual risks:** Project-specific validation profiles remain future work.
  Already-running MCP sessions may need reload to pick up the refreshed
  installed runtime.
- **Follow-up:** Add repository-specific validation profiles only after the
  generic planner proves useful across target repositories.

### 2026-06-11 - 023-hierarchical-spec-authoring-hooks

- **Spec:** `docs/specs/023-hierarchical-spec-authoring-hooks/`
- **Title:** Hierarchical spec authoring hooks
- **Final spec commit:** `c9caebe`
- **Closure cleanup commit:** `5e75d44`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_codex_spec_lifecycle_hook.py`
- **Verification summary:** Focused runtime and Codex hook wrapper tests passed;
  full unit suite passed with 94 tests. Lifecycle scan, archive-index
  validation, prompt validation, package-contract validation, npm pack dry-run,
  sync-guard after install, closure-check, and `git diff --check` passed.
- **Residual risks:** Hook payloads may not include enough diff detail to
  isolate changed task IDs. The implementation must keep fallback task scope
  explicit and avoid noisy package-wide output during ordinary authoring.
- **Follow-up:** None.

### 2026-06-11 - 018-mcp-ergonomics-observability

- **Spec:** `docs/specs/018-mcp-ergonomics-observability/`
- **Title:** MCP ergonomics and observability hardening
- **Final spec commit:** `e4703ff`
- **Closure cleanup commit:** `613f9bf`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
  - `tests/runtime/test_spec_plugin_package.py`
- **Verification summary:** Full unit suite passed; lifecycle scan, archive
  index validation, prompt validation, package-contract validation, npm pack
  dry-run, sync-guard, and `git diff --check` passed. After install,
  `sync-guard` reported source skill, Codex bundle, Claude bundle, and
  installed cache all in sync with no findings.
- **Residual risks:** Existing already-running MCP sessions may need reload to
  pick up the installed runtime. `mcp_audit` is a deterministic log triage
  signal and not proof that a tool executed because session logs can contain
  copied prompts or user-pasted errors.
- **Follow-up:** Consider hook-log input for `mcp_audit` only if future review
  workflows need first-class hook evidence.

### 2026-06-11 - 017-npm-distribution-packaging

- **Spec:** `docs/specs/017-npm-distribution-packaging/`
- **Title:** npm distribution packaging
- **Final spec commit:** `e4703ff`
- **Closure cleanup commit:** `613f9bf`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `package.json`
  - `packaging/spec-lifecycle-manager/npm-package.json`
  - `packaging/spec-lifecycle-manager/npm-install.js`
  - `packaging/spec-lifecycle-manager/package-manifest.json`
  - `plugins/spec-lifecycle-manager/claude-plugin/`
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
  - `tests/runtime/test_spec_plugin_package.py`
- **Verification summary:** Full unit suite passed; package-contract
  validation passed; npm pack dry-run included the npm installer, Codex plugin
  bundle, and Claude plugin payload; lifecycle scan, archive index validation,
  prompt validation, sync-guard after install, and `git diff --check` passed.
- **Residual risks:** npm publishing, registry authentication, remote `npx`
  install validation, release tagging policy, and publish automation remain
  future work. Docker/GHCR distribution is explicitly superseded as the useful
  install path.
- **Follow-up:** Plan a release/publish slice when npm registry publishing is
  required.

### 2026-06-11 - 016-commit-sync-guard

- **Spec:** `docs/specs/016-commit-sync-guard/`
- **Title:** Commit sync guard
- **Final spec commit:** `0522ea9`
- **Closure cleanup commit:** `43dd031`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `tests/runtime/test_spec_runtime.py`
- **Verification summary:** Full unit suite passed; focused runtime and plugin
  package tests passed; spec lint and closure check passed; `git diff --check`
  passed. After install and reload, `sync-guard` reported applicable, source
  and bundled plugin in sync, installed cache in sync, commit evidence ok, and
  no findings.
- **Residual risks:** `sync-guard` is a maintainer validation command for this
  repository only. It reports `not_applicable` outside the Spec Lifecycle
  Manager package repository and does not automate install or reload.
- **Follow-up:** None.

### 2026-06-11 - 015-brooks-lint-findings-tracking

- **Spec:** `docs/specs/015-brooks-lint-findings-tracking/`
- **Title:** Brooks-Lint findings tracking
- **Final spec commit:** `4b73823`
- **Closure cleanup commit:** `160b582`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reviews/brooks-lint/README.md`
  - `docs/backlog/README.md`
- **Verification summary:** Full unit suite passed; lifecycle scan, archive
  index validation, prompt validation, focused spec lint, closure check, and
  `git diff --check` passed before the final spec commit.
- **Residual risks:** Brooks findings remain Markdown-maintained by decision
  D001; runtime validation is deferred until repeated Brooks runs show real
  register drift. Deferred remediation is routed to B016/R005, B026, B042, and
  B043.
- **Follow-up:** Promote B016/R005 next if commit/install drift remains the
  highest-priority lifecycle hardening item.

### 2026-06-09 - 014-plugin-comparison-improvements

- **Spec:** `docs/specs/014-plugin-comparison-improvements/`
- **Title:** Plugin comparison improvements
- **Final spec commit:** `356c335`
- **Closure cleanup commit:** `d7edc98`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/plugin-comparison-improvements.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/README.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/prompts/`
  - `skills/spec-lifecycle-manager/references/spec-package/`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/prompts/`
  - `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/references/spec-package/`
  - `docs/backlog/README.md`
  - `tests/runtime/test_spec_runtime.py`
- **Verification summary:** Spec lint and closure-check passed; full unit
  suite passed; lifecycle scan, prompt validation, archive-index validation,
  plugin validation, and `git diff --check` passed before cleanup.
- **Residual risks:** Lifecycle triage and gate fields are documented guidance
  and prompt aliases, not deterministic runtime schema. Runtime phase-gate
  checks, workflow mode contracts, approval policies, Kiro import support, and
  hook-derived audits remain backlog candidates.
- **Follow-up:** Implement roadmap `R005` / backlog `B016` commit sync guard
  next, then `B026` distribution packaging if still accepted.

### 2026-06-06 - 013-agent-backed-lifecycle-tools

- **Spec:** `docs/specs/013-agent-backed-lifecycle-tools/`
- **Title:** Agent-backed lifecycle tools
- **Final spec commit:** `bb6c436`
- **Closure cleanup commit:** `6d23a40`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reviews/spec-lifecycle-manager/README.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - `tests/runtime/test_spec_runtime.py`
  - `tests/runtime/test_spec_mcp_server.py`
- **Verification summary:** Full unit suite, spec scan, spec lint, review-doc
  lint, prompt validation, archive-index validation, closure-check, and
  `git diff --check` passed before cleanup.
- **Residual risks:** Local Codex CLI runner remains intentionally deferred;
  persisted review records are a dogfood aid and not source-of-truth behavior.
- **Follow-up:** Add a focused local Codex CLI adapter spec if real secondary
  execution is needed.

### 2026-06-06 - 001-spec-lifecycle-manager-skill

- **Spec:** `docs/specs/001-spec-lifecycle-manager-skill/`
- **Title:** Spec lifecycle manager skill
- **Final spec commit:** `3f0ab61`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/README.md`
- **Verification summary:** Historical package predates the archive-index
  workflow; final commit `3f0ab61` preserves the package before removal.
- **Residual risks:** Original package uses the old spec format and should not
  be migrated as part of removal.
- **Follow-up:** None.

### 2026-06-06 - 012-operating-model-governance-adoption

- **Spec:** `docs/specs/012-operating-model-governance-adoption/`
- **Title:** Operating model governance adoption
- **Final spec commit:** `2d17440`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/governance/constitution.md`
  - `docs/design/coding-agent-operating-model.md`
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
- **Verification summary:** Spec 012 lint, closure-check, scan, archive-index validation, full tests, traceability lookup, and `git diff --check` passed.
- **Residual risks:** Governance adoption is documentation policy; runtime and hooks do not add new enforcement in this spec.
- **Follow-up:** None.

### 2026-06-06 - 011-spec-archive-index-runtime

- **Spec:** `docs/specs/011-spec-archive-index-runtime/`
- **Title:** Spec archive index runtime
- **Final spec commit:** `4712010`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/history/spec-archive-index.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/backlog/README.md`
  - `docs/roadmap/README.md`
  - `docs/README.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
- **Verification summary:** Archive index validation, spec 011 lint, closure-check, full runtime tests, focused MCP/runtime tests, scan, and `git diff --check` passed.
- **Residual risks:** Commit fields are syntax-checked, but Git object history is not inspected; spec 001 remains a documented legacy gap.
- **Follow-up:** Consider stricter Git object validation only if removal of retained archived packages is planned.

### 2026-06-06 - 003-coding-agent-operating-model

- **Spec:** `docs/specs/003-coding-agent-operating-model/`
- **Title:** Coding agent operating model
- **Final spec commit:** `7ee157b`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/design/coding-agent-operating-model.md`
  - `docs/reference/coding-agent-workflow-research.md`
  - `docs/README.md`
- **Verification summary:** Spec 003 lint, closure-check, traceability lookups, full runtime tests, focused Codex hook tests, and `git diff --check` passed.
- **Residual risks:** The model is durable guidance, not mandatory governance; metrics remain lightweight/manual.
- **Follow-up:** None.

### 2026-06-06 - 010-codex-hook-dogfood

- **Spec:** `docs/specs/010-codex-hook-dogfood/`
- **Title:** Codex hook dogfood
- **Final spec commit:** `d1eb6b3`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`
- **Verification summary:** Focused Codex hook tests, full runtime tests, spec 010 lint, closure-check, representative hook payload dogfood, and `git diff --check` passed.
- **Residual risks:** Real-world template edit evidence remains limited; blocking hook promotion remains out of scope.
- **Follow-up:** Revisit only if repeated hook noise appears or blocking hook promotion is proposed.

### 2026-06-06 - 002-spec-lifecycle-validation

- **Spec:** `docs/specs/002-spec-lifecycle-validation/`
- **Title:** Spec lifecycle validation
- **Final spec commit:** `d1eb6b3`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/references/spec-package/`
  - `skills/spec-lifecycle-manager/references/durable-doc-templates/`
- **Verification summary:** Full runtime tests, spec 002 lint, closure-check, traceability matrix, and `git diff --check` passed.
- **Residual risks:** Prompt trials were read-only mental applications of the skill; future scripted validation can be added if workflow churn justifies it.
- **Follow-up:** None.

### 2026-06-06 - 009-archived-spec-scan-hygiene

- **Spec:** `docs/specs/009-archived-spec-scan-hygiene/`
- **Title:** Archived spec scan hygiene
- **Final spec commit:** `1095b7f`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/design/spec-lifecycle-management.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
- **Verification summary:** Full runtime tests, spec 009 lint, closure-check, default scan, archived scan audit, MCP reload smoke tests, installed skill sync, and `git diff --check` passed.
- **Residual risks:** Existing third-party scan consumers must treat archived scan health as a skipped historical state.
- **Follow-up:** `docs/specs/010-codex-hook-dogfood/` tracks advisory Codex hook dogfooding.

### 2026-06-06 - 006-backlog-roadmap-templates

- **Spec:** `docs/specs/006-backlog-roadmap-templates/`
- **Title:** Backlog and roadmap templates
- **Final spec commit:** `1095b7f`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `skills/spec-lifecycle-manager/references/durable-doc-templates/backlog.md`
  - `skills/spec-lifecycle-manager/references/durable-doc-templates/roadmap.md`
  - `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/backlog/README.md`
- **Verification summary:** Runtime tests, spec 006 lint, closure-check, and `git diff --check` passed before closure.
- **Residual risks:** Templates remain fallback guidance; repository-specific planning systems stay authoritative.
- **Follow-up:** None.

### 2026-06-06 - 005-spec-closure-log-management

- **Spec:** `docs/specs/005-spec-closure-log-management/`
- **Title:** Spec closure log management
- **Final spec commit:** `1095b7f`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/design/spec-lifecycle-management.md`
  - `docs/README.md`
  - `docs/history/spec-closure-log.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `skills/spec-lifecycle-manager/references/durable-doc-templates/spec-closure-log.md`
- **Verification summary:** Runtime tests, spec 005 lint, closure-check, and `git diff --check` passed before closure.
- **Residual risks:** Automated verification that a final spec commit contains the retained or removed package remains future hook/MCP work.
- **Follow-up:** None.

### 2026-06-05 - 008-agent-workbench-spec-lifecycle-install

- **Spec:** `docs/specs/008-agent-workbench-spec-lifecycle-install/`
- **Title:** Agent Workbench spec lifecycle install
- **Final spec commit:** `59359bb`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/backlog/README.md`
  - `docs/reference/spec-lifecycle-manager-mcp-install.md`
- **Verification summary:** MCP `scan_specs`, `prompts_validate`, and `closure_check`; spec 008 lint and closure-check; duplicate host-level MCP entry check; `git diff --check` in both repos.
- **Residual risks:** Install guidance includes local host-level paths; blocking spec lifecycle hooks remain future work.
- **Follow-up:** Create a later focused spec only if blocking hook promotion is desired.

### 2026-06-05 - 007-spec-lifecycle-mcp-server

- **Spec:** `docs/specs/007-spec-lifecycle-mcp-server/`
- **Title:** Spec lifecycle MCP server
- **Final spec commit:** `e7485bd`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/README.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
  - `docs/backlog/README.md`
  - `docs/history/spec-closure-log.md`
- **Verification summary:** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`; `git diff --check`; `spec_runtime.py closure-check docs/specs/007-spec-lifecycle-mcp-server` reported ready before cleanup.
- **Residual risks:** Agent Workbench plugin packaging and hook installation remain future work tracked in backlog B002.
- **Follow-up:** `docs/backlog/README.md` B002 for Agent Workbench MCP packaging and hook install.

### 2026-06-05 - 004-spec-management-mcp

- **Spec:** `docs/specs/004-spec-management-mcp/`
- **Title:** Spec management MCP
- **Final spec commit:** `86687b6`
- **Closure cleanup commit:** `af3c344`
- **Closure action:** removed
- **Closed by:** platform
- **Durable docs updated:**
  - `docs/reference/spec-lifecycle-runtime.md`
  - `docs/design/spec-lifecycle-management.md`
  - `docs/README.md`
- **Verification summary:** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`; `git diff --check`; `spec_runtime.py closure-check docs/specs/004-spec-management-mcp` reported ready before cleanup.
- **Residual risks:** MCP server adapter delivered later in `docs/specs/007-spec-lifecycle-mcp-server/`; hook installation remains future work.
- **Follow-up:** `docs/specs/005-spec-closure-log-management/` for closure-log workflow completion.
