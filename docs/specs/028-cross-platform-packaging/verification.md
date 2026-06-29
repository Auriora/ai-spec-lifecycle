---
title: Cross-platform packaging verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-29
---

# Verification

## Validation Strategy

Portability claims must be backed by **executed runs on each OS**, not static
review from a Linux host. The bar is a real platform matrix: CI jobs on
windows-latest, macos-latest, and ubuntu-latest, or — where a runner is
unavailable — a recorded manual run with the gap noted.

## Quality Gates

| Gate | Method |
| --- | --- |
| Interpreter resolution (P2) | Unit test `resolvePython` for `win32` (`py -3`) and POSIX (`python3`) with injected env/platform; assert override honored |
| Install on Windows (R1) | Run `bin` installer on windows-latest with Node + Python 3, no shell; assert files copied, configs pinned |
| MCP launch (R2) | Start server from the installed `.mcp.json` on all three OSes; assert stdio handshake |
| Hook execution (R3) | Fire PostToolUse with a Claude-shaped payload (`tool_name:"Write"`, `tool_input.file_path`) on all three OSes; assert advisory output, no shell error, no silent no-op |
| Hook parity (R3) | Existing `tests/runtime/test_codex_spec_lifecycle_hook.py` Claude-payload tests stay green |
| Package parity (P3) | `tests/runtime/test_spec_plugin_package.py` byte-identical bundled-skill guard stays green |
| Single source (P3) | Assert no independently-maintained `.sh` install logic remains |
| Fail-loud (P4) | Remove Python from PATH; assert actionable error, not a silent partial install or MCP no-op |

## Evidence Log

Each entry: OS, Python, interpreter resolved, command/outcome, link.

- **Linux (local), Python 3.12.4, interpreter `python3`.** Full suite green:
  `npm run validate` → 147 Python tests + 17 Node tests, package-contract pass,
  `npm pack --dry-run`. Cross-platform smoke (`smoke_cross_platform.mjs`):
  SMOKE PASS — shell-free install, MCP `initialize` handshake (protocolVersion
  2025-06-18, serverInfo `spec-lifecycle-manager`), PostToolUse hook with a
  Claude-shaped payload (`tool_name:"Write"`) exit 0.
- **Installer oracle parity (Linux).** `installer.mjs` proven byte-identical to
  the legacy `.sh` before interpreter-pinning: dry-run output, real-install
  `diff -r` of both copied trees, and the `config.toml` / `hooks.json` /
  `marketplace.json` edit paths.
- **Interpreter resolution (P2).** `resolve-python.test.mjs` 11/11: win32
  `py -3`→`python`→`python3`, POSIX `python3`→`python`, `SPEC_LIFECYCLE_PYTHON`
  honored verbatim, P4 actionable throw when none resolve.
- **Pinning (R2/R3).** `installer.test.mjs` with `SPEC_LIFECYCLE_PYTHON="py -3"`:
  installed Codex/Claude `.mcp.json` → `command:"py", args:["-3", …server.py]`;
  Claude hook exec form `py`/`["-3", …hook.py]`; Codex hook shell-string
  `py -3 "${PLUGIN_ROOT}/…hook.py"`.
- **Fail-loud (P4).** Installer with no Python on PATH and no override → exits 1
  with the actionable "Python 3.10 or newer is required …" message.
- **Windows test-harness hardening (R4.2).** The package-contract test launched
  `subprocess.run(["npm", …])` and set a hardcoded `/tmp/…` npm cache — both fail
  on `windows-latest` for harness reasons (CreateProcess ignores PATHEXT so a bare
  `npm` cannot find `npm.cmd`; `/tmp` is not a valid Windows path). Hardened to
  resolve `npm` via `shutil.which` (PATHEXT-aware) and use
  `tempfile.gettempdir()`, so the CI matrix can actually go green on Windows
  rather than reding before exercising the implementation. Re-run green on Linux.
- **First CI matrix run (run 28386954873, commit 2ca0a21) — RED, two real
  defects surfaced; fixed in follow-up.** The matrix did its job: it exposed
  cross-OS/version problems a Linux-only run never could. Results were
  ubuntu-3.12 ✅, macos-3.12 ✅, and red on every 3.9 lane plus windows-3.12.
  Two distinct causes:
  1. **Python 3.10+ floor (all OSes at 3.9, including ubuntu).** Not a
     cross-platform issue — pre-existing product code already required 3.10
     (`spec_runtime.py` uses `zip(strict=)` and PEP 604 `X | None` runtime
     unions). The "3.9+" claim was never accurate. Resolution: raise the
     documented/probed floor to **3.10** (CI matrix `3.10`/`3.12`, installer
     probe `minor >= 10`, install doc, `package-manifest.json` `>=3.10`); the
     product needs no change. 3.9 is also EOL as of 2025-10.
  2. **Windows test-harness subprocess (`WinError 193`, windows-3.12).** Nine
     test call-sites invoked `spec_runtime.py`/`traceability_lookup.py` *by
     path*, relying on the `#!/usr/bin/env python3` shebang — works on POSIX,
     impossible on Windows. The shipped product is unaffected (MCP via
     `command: python`, hook exec form, internal `sys.executable`); only the
     tests were wrong. Fixed by prefixing every site with `sys.executable`.
     A path-separator assertion (`endswith("references/spec-package")`) was also
     made OS-agnostic via `os.path.join`. The `npm pack` test fix from the prior
     commit passed on Windows (not in the failure list), confirming the
     `shutil.which` approach.
  All fixes are test/config/doc only — no product logic changed.
- **Green CI matrix (run 28396955459, commit 1f30465) — all 6 jobs pass; the
  verification gap is now CLOSED.**
  <https://github.com/Auriora/ai-spec-lifecycle/actions/runs/28396955459>.
  Every job ran all six steps (Node unit tests, Python runtime+hook tests,
  package contract, **cross-platform smoke**, npm pack dry-run) to success on
  `ubuntu-latest`, `macos-latest`, and `windows-latest` × Python 3.10 and 3.12.
  The smoke step — the actual proof of R1/R2/R3 — executed and passed per OS:
  - **windows-latest, Python 3.12, interpreter `py`.** `install completed
    shell-free`; `MCP initialize handshake (protocolVersion=2025-06-18,
    interpreter=py)`; `hook executed (exit 0)`; `SMOKE PASS`. The resolver
    selected the PEP 397 `py` launcher first, exactly as designed (R2), and the
    install/launch/hook path used no POSIX shell (R1/P1) — the core Windows
    blocker the spec set out to remove.
  - **macos-latest, Python 3.12, interpreter `python3`.** `install completed
    shell-free`; MCP handshake (interpreter `python3`); hook exit 0; `SMOKE
    PASS`.
  - **ubuntu-latest** continues to pass (interpreter `python3`).
  R1 (shell-free install), R2 (interpreter resolution + MCP launch), and R3
  (hook execution with a Claude-shaped payload) are now evidenced on all three
  OSes via executed CI, satisfying R4.2.

## Residual Risks

- Marketplace static-config path relies on the chosen `python`-on-PATH
  prerequisite (design.md Resolved Decisions §1) rather than guaranteed
  resolution; confirm the trade-off still holds at closure and note any host
  where `python` is absent.
- ~~Windows CI runner availability may force manual verification for some
  gates.~~ Resolved: the GitHub-hosted `windows-latest`/`macos-latest` runners
  executed the full gate set (run 28396955459); no manual substitution was
  needed.
- Codex exec-form hook support is unconfirmed in-repo (design.md Resolved
  Decisions §4): the Codex hook ships shell-form with the resolved interpreter
  pinned in. T009 must confirm exec-form support against the live Codex runtime;
  upgrade to exec form if it passes, otherwise the shell-form-with-resolved-
  interpreter fallback stands.

## Closure Readiness

`ready_to_close` requires: all gates evidenced on all three OSes (or gaps
recorded), durable platform/interpreter matrix promoted, and the marketplace
static-config decision resolved.
