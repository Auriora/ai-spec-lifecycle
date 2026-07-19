"""Next-action derivation for lifecycle MCP results."""

from __future__ import annotations

from pathlib import Path
from typing import Any


RUNTIME_COMMAND = "skills/spec-lifecycle-manager/scripts/spec_runtime.py"
BLOCKER_LIMIT = 20


def _action(
    action_id: str,
    label: str,
    stage: str,
    reason: str,
    tool: str,
    *,
    artifact: str | None = None,
    required: bool = True,
    blockers: list[dict[str, Any]] | None = None,
    task_id: str | None = None,
) -> dict[str, Any]:
    action: dict[str, Any] = {
        "id": action_id,
        "label": label,
        "stage": stage,
        "reason": reason,
        "tool": tool,
        "interface": "mcp",
        "required": required,
    }
    if artifact:
        action["artifact"] = artifact
    if blockers:
        action["blockers"] = blockers[:BLOCKER_LIMIT]
        action["blocker_summary"] = {
            "returned": min(len(blockers), BLOCKER_LIMIT),
            "total": len(blockers),
            "truncated": len(blockers) > BLOCKER_LIMIT,
        }
        if len(blockers) > BLOCKER_LIMIT:
            action["blocker_expansion"] = {
                "tool": tool,
                "reason": "Call the authoritative source tool for the complete blocker set.",
            }
    if task_id:
        action["task_id"] = task_id
    return action


def _repo_relative_path(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.name


def _recovery_command(action: dict[str, Any], repo_root: Path, spec_path: Path | None) -> dict[str, str]:
    tool = str(action["tool"])
    spec = _repo_relative_path(repo_root, spec_path) if spec_path is not None else ""
    task_id = str(action.get("task_id") or "")
    commands = {
        "no_active_spec_context": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} no-active-spec-context .",
        "documentation-wizard": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} lifecycle-guide .",
        "active_spec_preflight": (
            f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} active-spec-preflight . --spec-path {spec}"
            if spec
            else f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} active-spec-preflight ."
        ),
        "stage_readiness": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} stage-readiness {spec}",
        "next_task": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} next-task {spec}",
        "task_context": (
            f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} task-details {spec} --task-id {task_id}"
            if task_id
            else f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} next-task {spec}"
        ),
        "lint_spec_package": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} lint {spec}",
        "validation_plan": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} validation-plan . --spec-path {spec}",
        "evidence_quality_check": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} evidence-quality {spec}",
        "promotion_plan": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} promotion-plan {spec}",
        "closure_check": f"PYTHONDONTWRITEBYTECODE=1 {RUNTIME_COMMAND} closure-check {spec}",
    }
    return {
        "action_id": str(action["id"]),
        "command": commands[tool],
        "applies_when": "mcp_unavailable",
    }


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
    from . import core as lifecycle_core

    task_result = lifecycle_core.next_task(spec)
    selected = task_result.get("selected") or {}
    if selected.get("task_id"):
        return [
            _action(
                "get_task_context",
                "Get task context",
                "implement",
                "The spec has tasks and verification context for an implementation slice.",
                "task_context",
                task_id=str(selected["task_id"]),
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

    blocked_tasks = task_result.get("blocked") or []
    if blocked_tasks:
        return [
            _action(
                "resolve_task_blockers",
                "Resolve task blockers",
                "implement",
                "No task is runnable; preserve dependency and task-context blockers before implementation.",
                "next_task",
                blockers=blocked_tasks,
            )
        ]

    actions = [
        _action(
            "plan_validation",
            "Plan validation",
            "verify",
            "Implementation tasks are complete; build the validation plan before reviewing evidence.",
            "validation_plan",
        )
    ]
    evidence = lifecycle_core.evidence_quality_check(spec)
    evidence_blockers = evidence.get("diagnostics") or []
    actions.append(
        _action(
            "review_evidence",
            "Review evidence quality",
            "verify",
            "Review completed task and verification evidence before promotion or closure.",
            "evidence_quality_check",
            blockers=evidence_blockers,
        )
    )
    if evidence_blockers:
        return actions

    promotion = lifecycle_core.promotion_plan(spec)
    promotion_blockers = promotion.get("missing_targets") or []
    actions.append(
        _action(
            "plan_promotion",
            "Plan durable promotion",
            "promote",
            "Route accepted behavior and residual work to durable destinations before closure.",
            "promotion_plan",
            blockers=promotion_blockers,
        )
    )
    if promotion_blockers:
        return actions

    closure = lifecycle_core.closure_check(spec)
    actions.append(
        _action(
            "check_closure",
            "Check closure readiness",
            "close",
            "Run the existing closure authority only after validation, evidence, and promotion routing.",
            "closure_check",
            blockers=closure.get("blockers") or [],
        )
    )
    return actions


def lifecycle_action_presentation(repo_root: Path, spec_path: Path | None = None) -> dict[str, Any]:
    """Return MCP-primary actions plus explicitly labelled CLI recovery."""

    actions = lifecycle_next_actions(repo_root, spec_path)
    return {
        "available_next_actions": actions,
        "validation_or_recovery": {
            "applies_when": "mcp_unavailable",
            "commands": [_recovery_command(action, repo_root, spec_path) for action in actions],
        },
    }
