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

- Pending. Record per-OS CI run URLs or manual-run transcripts here as tasks
  complete. Each entry: OS, Python version, interpreter resolved, command,
  outcome, link.

## Residual Risks

- Marketplace static-config path relies on the chosen `python`-on-PATH
  prerequisite (design.md Resolved Decisions §1) rather than guaranteed
  resolution; confirm the trade-off still holds at closure and note any host
  where `python` is absent.
- Windows CI runner availability may force manual verification for some gates;
  any such gap must be recorded, not silently skipped.
- Codex exec-form hook support is unconfirmed in-repo (design.md Resolved
  Decisions §4): the Codex hook ships shell-form with the resolved interpreter
  pinned in. T009 must confirm exec-form support against the live Codex runtime;
  upgrade to exec form if it passes, otherwise the shell-form-with-resolved-
  interpreter fallback stands.

## Closure Readiness

`ready_to_close` requires: all gates evidenced on all three OSes (or gaps
recorded), durable platform/interpreter matrix promoted, and the marketplace
static-config decision resolved.
