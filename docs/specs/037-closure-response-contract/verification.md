---
title: Closure Response Contract Verification
doc_type: spec
artifact_type: verification
status: active
owner: maintainers
last_reviewed: 2026-07-12
---

# Verification

## Quality Gates

- Focused MCP runtime tests cover response shape, response size, ignored WAL
  input, targeted edit expansion, action order, idempotent record rendering,
  package-only cleanup, and stale fingerprints.
- Full Python and Node validation must pass after source-to-bundle sync.
- `package-contract`, `sync-guard`, and `git diff --check` must pass.

## Evidence Log

| Date | Scope | Evidence | Result |
|---|---|---|---|
| 2026-07-12 | Focused MCP runtime | `python3 -m unittest tests.runtime.test_spec_mcp_server` | Pass: 45 tests |
| 2026-07-12 | Full repository | `npm run validate` | Pass: 306 Python, 25 Node, runtime/package/sync/pack/diff gates |

## Residual Risks

The retained CLI plan-file format still carries full generated content for
explicit no-MCP recovery. It is not returned through the agent-facing MCP
contract and is outside this response-size defect.

The checked-in Codex and Claude bundles match source. The currently installed
Codex cache still reflects the prior build and requires the normal reinstall
and client reload before live MCP calls use this implementation.
