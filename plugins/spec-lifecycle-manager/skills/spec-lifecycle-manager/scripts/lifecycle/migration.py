"""Script migration inventory and closure checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any


TRACEABILITY_SOURCE = "skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
TRACEABILITY_CODEX_BUNDLE = "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
TRACEABILITY_CLAUDE_BUNDLE = (
    "plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
)
TRACEABILITY_CODEX_CACHE = "skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
TRACEABILITY_CLAUDE_CACHE = "claude-plugin/skills/spec-lifecycle-manager/scripts/traceability_lookup.py"


def default_script_inventory() -> list[dict[str, Any]]:
    """Return the accepted v1 script migration inventory."""
    return [
        {
            "script": "spec_mcp_server.py",
            "classification": "retain_internal",
            "public_owner": "MCP server entrypoint",
            "rationale": "Required adapter for the public MCP tool surface.",
        },
        {
            "script": "spec_runtime.py",
            "classification": "retain_recovery",
            "public_owner": "retained validation/recovery/admin surface",
            "rationale": (
                "Required for CI, package validation, install checks, hooks, and emergency no-MCP recovery. "
                "It must not expose duplicate agent-facing lifecycle tools for migrated behavior."
            ),
        },
        {
            "script": "codex_spec_lifecycle_hook.py",
            "classification": "retain_internal",
            "public_owner": "hook adapter",
            "rationale": "Required advisory hook entrypoint.",
        },
        {
            "script": "spec_agent_schemas.py",
            "classification": "retain_internal",
            "public_owner": "internal schema helper",
            "rationale": "Supports MCP structured output schemas and is not an agent-facing runtime tool.",
        },
        {
            "script": "traceability_lookup.py",
            "classification": "migrate_to_mcp",
            "public_owner": "MCP traceability_lookup tool",
            "rationale": (
                "Agent-facing lookup behavior already has an MCP replacement and should not remain as "
                "a parallel executable script after migration."
            ),
            "replacement_contract": traceability_replacement_contract(),
        },
    ]


def traceability_replacement_contract() -> dict[str, Any]:
    return {
        "old_entrypoint": f"python3 {TRACEABILITY_SOURCE}",
        "replacement_mcp_tool": "traceability_lookup",
        "retained_ci_debug_command": "none",
        "replacement_cli_command": None,
        "shared_logic_destination": "skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py",
        "docs_to_update": ["docs/reference/spec-lifecycle-runtime.md"],
        "tests_to_port": ["tests/traceability/test_traceability_lookup.py", "tests/runtime/test_spec_mcp_server.py"],
        "source_removal_paths": [TRACEABILITY_SOURCE],
        "bundle_removal_paths": [TRACEABILITY_CODEX_BUNDLE, TRACEABILITY_CLAUDE_BUNDLE],
        "installed_cache_removal_paths": [TRACEABILITY_CODEX_CACHE, TRACEABILITY_CLAUDE_CACHE],
        "installed_cache_validation": "install refresh followed by sync-guard .",
    }


def script_migration_inventory(repo_root: Path) -> dict[str, Any]:
    rows = default_script_inventory()
    return {
        "status": "ok",
        "repo_root": ".",
        "scripts": rows,
        "migrated_scripts": [row for row in rows if row["classification"] == "migrate_to_mcp"],
        "retained_scripts": [row for row in rows if row["classification"].startswith("retain_")],
        "closure_blockers": migrated_script_closure_check(repo_root, {"scripts": rows}),
    }


def migrated_script_closure_check(
    repo_root: Path,
    inventory: dict[str, Any] | None = None,
    installed_cache_roots: list[Path] | None = None,
) -> list[dict[str, str]]:
    root = repo_root.resolve()
    rows = (inventory or {"scripts": default_script_inventory()}).get("scripts", [])
    blockers: list[dict[str, str]] = []
    for row in rows:
        if row.get("classification") != "migrate_to_mcp":
            continue
        contract = row.get("replacement_contract") or {}
        if not contract.get("replacement_mcp_tool"):
            blockers.append(
                {
                    "severity": "error",
                    "code": "MIGRATED_SCRIPT_REPLACEMENT_MISSING",
                    "script": str(row.get("script", "")),
                    "message": "Migrated script has no replacement MCP tool.",
                }
            )
        for field in ("source_removal_paths", "bundle_removal_paths"):
            for relative in contract.get(field, []):
                if (root / relative).exists():
                    blockers.append(
                        {
                            "severity": "error",
                            "code": "MIGRATED_SCRIPT_STILL_PRESENT",
                            "script": str(row.get("script", "")),
                            "path": relative,
                            "message": f"Migrated script path still exists: {relative}",
                        }
                    )
        for cache_root in installed_cache_roots or []:
            for relative in contract.get("installed_cache_removal_paths", []):
                if (cache_root / relative).exists():
                    blockers.append(
                        {
                            "severity": "error",
                            "code": "MIGRATED_SCRIPT_STILL_PRESENT",
                            "script": str(row.get("script", "")),
                            "path": str(cache_root / relative),
                            "message": f"Migrated script path still exists in installed cache: {cache_root / relative}",
                        }
                    )
    return blockers
