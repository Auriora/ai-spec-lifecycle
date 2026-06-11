---
title: MCP ergonomics and observability hardening design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Design

## Overview

Add a small read-only hardening layer to the existing runtime. The runtime
stays dependency-free and deterministic; the MCP server delegates to it and
normalizes paths for client display.

## High-Level Design

- `resolve_spec_reference(repo_root, value)` classifies a spec reference as
  active, archived, ambiguous, or missing.
- `mcp_audit(repo_root, sessions_root, since)` scans Codex session JSONL files
  for lifecycle tool/resource mentions and explicit errors without needing to
  parse every prompt echo as a tool call.
- `sync_guard` and `package_contract` compare the source skill against both
  Codex and Claude bundled skill copies.
- MCP tools expose `resolve_spec_reference` and `mcp_audit`; resource payloads
  include root binding metadata.

## Low-Level Design

- Active resolution uses `discover_spec_paths` and repo-relative display paths.
- Archived resolution reuses `archive_index` entries and matches package path
  basename, full package path, or numeric slug prefix.
- Ambiguity returns all matching active candidates and does not choose one.
- Missing resolution returns guidance and available active IDs.
- Audit scans only supplied/local session files and records line numbers,
  explicit `Unknown review packet type` and `Active spec not found` errors,
  and lifecycle resource/tool mentions.
- MCP schema metadata uses existing `review_packet_type_contract()`.

## Operational Considerations

- All new commands are read-only.
- Audit output can be noisy when session files include copied prompts, so it is
  a triage signal, not proof that a tool executed.
- Installed sessions may still need reload after package install; sync guard
  reports this without touching processes.

## Open Questions

- A future slice can decide whether audit summaries should also parse hook log
  JSONL files as a first-class input.
