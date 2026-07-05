---
title: MCP-first runtime migration tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-07-05
---

# Tasks

- [x] T013 Complete MCP tool registration.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/runtime/test_spec_mcp_server.py` passed.
- [x] T014 Remove migrated runtime scripts.
  - Evidence: `rg traceability_lookup.py skills plugins` returned no migrated runtime script.
