---
title: MCP-first runtime migration
doc_type: spec
artifact_type: requirements
status: draft
owner: platform
last_reviewed: 2026-07-05
---

# Requirements

## Problem Context

The lifecycle MCP tools should call shared lifecycle logic directly instead of
routing through `spec_runtime.py`.

## Requirements

### Requirement 1: MCP Runtime Boundary

**User Story:** As an agent, I want MCP tools to use shared lifecycle internals,
so that runtime entry points do not duplicate behavior.

#### Acceptance Criteria

1. GIVEN an MCP tool handles lifecycle context, WHEN it needs lifecycle logic,
   THEN THE SYSTEM SHALL call shared lifecycle internals directly.
