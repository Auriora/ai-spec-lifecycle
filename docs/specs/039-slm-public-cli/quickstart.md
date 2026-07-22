---
title: Public slm CLI quickstart
doc_type: spec
artifact_type: quickstart
status: draft
owner: platform
last_reviewed: 2026-07-22
---

# Quickstart

## Purpose

Record the implemented user journey and packaged smoke scenarios for `slm`.

## Prerequisites

- Node.js 18 or newer.
- Python 3.10 or newer, or a valid `SPEC_LIFECYCLE_PYTHON` override.
- A built Spec Lifecycle Manager release tarball containing the `slm` bin.
- A repository with lifecycle docs for non-empty examples.

## Steps

1. Install a built release tarball into an isolated npm prefix or use the
   equivalent release-install command documented by the implementation.
2. Confirm command discovery:

   ```bash
   slm --help
   slm install --help
   ```

3. From a lifecycle-enabled repository, list active specs:

   ```bash
   slm spec
   slm spec open
   slm spec all
   slm spec closed
   slm specs
   slm specs --json
   ```

4. Select an active spec and inspect tasks:

   ```bash
   slm spec 039
   slm spec 039 tasks --pending
   slm spec 039 next
   slm spec 039 requirements
   slm tasks 039
   slm tasks 039 --pending
   slm tasks 039 --open
   slm tasks 039 --complete
   slm tasks 039 --next
   slm next 039
   ```

5. Inspect requirements and priorities:

   ```bash
   slm requirements 039
   slm requirements 039 --priority must-have
   slm requirements 039 --missing-priority
   ```

6. Inspect durable closed-spec history:

   ```bash
   slm history
   slm history --removed --limit 10
   slm history --json
   ```

7. Verify explicit repository selection from outside the root:

   ```bash
   slm -C ../example-repository specs
   ```

## Expected Results

- `slm --help` shows `specs`, `tasks`, `next`, `requirements`, `history`, and
  `install`.
- Bare `slm` and `slm specs` show the same active-spec records.
- `slm spec` defaults to open inventory, and `slm spec 039` defaults to tasks;
  singular routes match their compatible plural command output.
- Specs with task-backed phases show completed/total phase progress and the
  current phase's task-derived normalized state; unphased specs show `-`.
- Human mode uses concise plain text; `--json` emits one valid versioned JSON
  document.
- `--pending` shows literal pending tasks, while `--open` includes all defined
  non-terminal task states.
- Both next-task command forms select the same dependency-aware result.
- Requirements show canonical priority or `unspecified`.
- History includes removed specs without requiring their package directories.
- None of the inspection commands modify the repository.

## Validation Evidence

| Step Or Scenario | Evidence | Result | Residual Risk |
|------------------|----------|--------|---------------|
| Help and install routing | Isolated tarball smoke | passed | Sole `slm` shim present; legacy shims absent. |
| Active spec human/JSON views | Focused CLI test and terminal command pass | passed | Table width differs by terminal. |
| Task filters and next equivalence | Table-driven tests and core comparison | passed | Future markers require test updates. |
| Requirement priorities | Canonical/missing/invalid priority fixtures | passed | Traceability may be absent. |
| Removed history | Archive fixture with absent package directory | passed | Malformed records fail closed. |
| Explicit/nested root selection | Temporary repository fixture | passed locally | Windows/macOS/Linux workflow run remains a release gate. |
| Read-only guarantee | Before/after worktree fingerprint | passed | `install` is excluded by design. |
| Singular route equivalence | Seven live JSON comparisons plus focused source and installed-package tests | passed | Existing plural commands remain supported compatibility surfaces. |
| Phase progress/state | Mixed-state, precedence, all-complete, no-phase, human/JSON, and installed-package tests | passed | Future normalized task states require explicit precedence review. |

## Cleanup

- Remove isolated npm prefixes, caches, and unpacked tarballs created by smoke
  tests.
- Do not remove or reset user repository files as part of CLI validation.
- Do not install a development checkout into user-wide Codex or Claude state.

## Promotion Or Discard Decision

- **Disposition:** promote
- **Durable destination:** `README.md` for the concise path and
  `docs/reference/spec-lifecycle-runtime.md` for complete command semantics
- **Reason:** The commands are the primary public onboarding path for the new
  executable.
- **Owner or follow-up:** platform, T008

## Related Artifacts

- Requirements: `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
