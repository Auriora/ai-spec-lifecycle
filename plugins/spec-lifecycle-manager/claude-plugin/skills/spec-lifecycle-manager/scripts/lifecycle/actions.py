"""Next-action derivation for lifecycle MCP results."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _action(
    action_id: str,
    label: str,
    stage: str,
    reason: str,
    tool: str,
    *,
    artifact: str | None = None,
    required: bool = True,
) -> dict[str, Any]:
    action: dict[str, Any] = {
        "id": action_id,
        "label": label,
        "stage": stage,
        "reason": reason,
        "tool": tool,
        "required": required,
    }
    if artifact:
        action["artifact"] = artifact
    return action


def lifecycle_next_actions(repo_root: Path, spec_path: Path | None = None) -> list[dict[str, Any]]:
    """Return deterministic next lifecycle actions for a repo/spec state.

    This helper intentionally does not inspect client identity. It supports the
    stable-tool fallback strategy by making state-specific actions data in tool
    results rather than relying on dynamic tool-list changes.
    """
    root = repo_root.resolve()
    if spec_path is None:
        specs_root = root / "docs/specs"
        active_specs = sorted(path for path in specs_root.glob("*") if path.is_dir()) if specs_root.exists() else []
        if not active_specs:
            return [
                _action(
                    "review_backlog",
                    "Review backlog",
                    "discover",
                    "No active spec packages were found.",
                    "no_active_spec_context",
                    required=False,
                ),
                _action(
                    "create_spec_requirements",
                    "Create requirements artifact",
                    "requirements",
                    "A backlog item or user request needs a first spec artifact.",
                    "documentation-wizard",
                    artifact="requirements.md",
                ),
            ]
        return [
            _action(
                "select_active_spec",
                "Select active spec",
                "discover",
                "Active spec packages exist and need a selected context.",
                "active_spec_preflight",
            )
        ]

    spec = spec_path.resolve()
    if not (spec / "requirements.md").exists():
        return [
            _action(
                "advance_to_requirements",
                "Create requirements artifact",
                "requirements",
                "The spec package does not contain requirements.md.",
                "documentation-wizard",
                artifact="requirements.md",
            )
        ]
    if not (spec / "design.md").exists():
        return [
            _action(
                "advance_to_design",
                "Create design artifact",
                "design",
                "The spec has requirements but no design artifact.",
                "stage_readiness",
                artifact="design.md",
            )
        ]
    if not (spec / "tasks.md").exists():
        return [
            _action(
                "advance_to_tasks",
                "Create tasks and traceability artifacts",
                "tasks",
                "The spec has design context but no task plan.",
                "stage_readiness",
                artifact="tasks.md",
            )
        ]
    if not (spec / "verification.md").exists():
        return [
            _action(
                "create_verification",
                "Create verification artifact",
                "verify",
                "The spec has runnable tasks but no verification evidence artifact.",
                "stage_readiness",
                artifact="verification.md",
                required=False,
            ),
            _action(
                "get_task_context",
                "Get task context",
                "implement",
                "The spec has tasks and can provide bounded context for an implementation slice.",
                "task_context",
            ),
        ]
    return [
        _action(
            "get_task_context",
            "Get task context",
            "implement",
            "The spec has tasks and verification context for an implementation slice.",
            "task_context",
        ),
        _action(
            "validate_spec",
            "Validate spec package",
            "verify",
            "Run lifecycle validation before promotion or closure.",
            "lint_spec_package",
            required=False,
        ),
    ]
