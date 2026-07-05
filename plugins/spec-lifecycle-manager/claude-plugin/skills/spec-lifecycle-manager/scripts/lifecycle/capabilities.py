"""Capability report construction for lifecycle MCP adapters."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .actions import lifecycle_next_actions


UNKNOWN = "unknown"


def lifecycle_capabilities(
    repo_root: Path,
    session_state: dict[str, Any] | None = None,
    *,
    server_name: str = "spec-lifecycle-manager",
    server_version: str = "0.1.0",
    protocol_version: str = "2025-06-18",
) -> dict[str, Any]:
    """Build an advisory MCP capability report.

    Missing client/session fields are reported as ``unknown`` instead of being
    inferred from client names or private runtime details.
    """
    state = session_state or {}
    client = state.get("client") if isinstance(state.get("client"), dict) else {}
    client_capabilities = client.get("capabilities", UNKNOWN) if client else UNKNOWN
    status = "known" if client else "partial"
    return {
        "status": status,
        "server": {
            "name": server_name,
            "version": server_version,
            "protocol_version": state.get("protocol_version") or protocol_version,
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"listChanged": False},
                "prompts": {"listChanged": False},
            },
        },
        "client": {
            "name": client.get("name", UNKNOWN) if client else UNKNOWN,
            "version": client.get("version", UNKNOWN) if client else UNKNOWN,
            "protocol_version": client.get("protocol_version", UNKNOWN) if client else UNKNOWN,
            "capabilities": client_capabilities,
        },
        "dynamic_tools": {
            "server_support": False,
            "client_refresh_observed": state.get("client_refresh_observed", UNKNOWN),
            "decision": "stable_tool_surface",
        },
        "available_next_actions": lifecycle_next_actions(repo_root),
    }
