"""Normalized, read-only records for the public ``slm`` command surface.

This module composes the lifecycle core and shared Markdown parsers. Rendering,
argument parsing, process exits, and package dispatch remain separate concerns.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from lifecycle import core
from lifecycle import requirements as requirements_parser
from lifecycle import traceability


SCHEMA_VERSION = "1"
PUBLIC_COMMANDS = ("spec", "specs", "tasks", "next", "requirements", "history", "install")
QUERY_COMMANDS = PUBLIC_COMMANDS[:-1]
ENVELOPE_FIELDS = ("schema_version", "command", "repo_root", "records", "summary")
OPEN_TASK_STATES = frozenset({"pending", "in_progress", "partial", "review_needed", "attention"})
CANONICAL_PRIORITIES = frozenset(requirements_parser.CANONICAL_PRIORITIES)
PHASE_STATE_PRECEDENCE = (
    "attention",
    "review_needed",
    "in_progress",
    "partial",
    "pending",
    "follow_up",
    "no_op",
    "complete",
)


class PublicViewError(ValueError):
    """Expected public-query error with stable details for a future CLI layer."""

    def __init__(
        self,
        message: str,
        *,
        code: str,
        candidates: Iterable[str] = (),
        diagnostics: Iterable[dict[str, Any]] = (),
    ) -> None:
        super().__init__(message)
        self.code = code
        self.candidates = list(candidates)
        self.diagnostics = list(diagnostics)


@dataclass(frozen=True)
class TaskFilters:
    complete: bool = False
    pending: bool = False
    open: bool = False
    states: tuple[str, ...] = ()
    next_only: bool = False


@dataclass(frozen=True)
class RequirementFilters:
    priorities: tuple[str, ...] = ()
    missing_priority: bool = False


@dataclass(frozen=True)
class HistoryFilters:
    archived: bool = False
    removed: bool = False
    limit: int | None = None


def command_view(command: str, repo_root: Path, records: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, Any]:
    """Return the stable record envelope consumed by all presentation modes."""
    return {
        "schema_version": SCHEMA_VERSION,
        "command": command,
        "repo_root": ".",
        "records": records,
        "summary": summary,
    }


def repo_relative_path(repo_root: Path, value: str | Path | None) -> str | None:
    if value in {None, ""}:
        return None
    root = repo_root.resolve()
    path = Path(value)
    resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        return str(value)


def select_active_spec(repo_root: Path, reference: str | None = None, docs_root: str | None = None) -> Path:
    """Resolve an explicit active spec or apply the exactly-one-active rule."""
    root = repo_root.resolve()
    if reference:
        result = core.resolve_spec_reference(root, reference, docs_root)
        status = result.get("status")
        if status == "active" and result.get("lifecycle") == "active":
            return Path(result["path"])
        if status == "archived" or (status == "active" and result.get("lifecycle") != "active"):
            matches = result.get("archive_matches") or [result]
            raise PublicViewError(
                f"Spec reference is historic, not active: {reference}",
                code="spec_historic",
                candidates=(str(item.get("spec_id", "")) for item in matches),
            )
        if status == "ambiguous":
            raise PublicViewError(
                f"Spec reference is ambiguous: {reference}",
                code="spec_ambiguous",
                candidates=sorted(str(item.get("spec_id", "")) for item in result.get("matches", [])),
            )
        raise PublicViewError(f"No active spec matched: {reference}", code="spec_missing")

    scan = core.scan_specs(root, docs_root)
    active = sorted(
        (item for item in scan.get("specs", []) if item.get("lifecycle") == "active"),
        key=lambda item: str(item.get("spec_id", "")),
    )
    if len(active) == 1:
        return Path(active[0]["path"])
    if not active:
        raise PublicViewError("No active specs found.", code="spec_none")
    candidates = [str(item.get("spec_id", "")) for item in active]
    raise PublicViewError("Multiple active specs found; select one explicitly.", code="spec_ambiguous", candidates=candidates)


def _active_spec_record(repo_root: Path, item: dict[str, Any]) -> dict[str, Any]:
    spec_path = Path(item["path"])
    tasks_path = spec_path / "tasks.md"
    tasks = core.parse_tasks(tasks_path)
    phase_fields = _phase_progress(tasks_path, tasks)
    next_payload = core.next_task(spec_path)
    selected = next_payload.get("selected")
    health = item.get("health", {})
    return {
        "spec_id": item.get("spec_id", spec_path.name),
        "path": repo_relative_path(repo_root, spec_path),
        "status": item.get("status"),
        "lifecycle": item.get("lifecycle"),
        "disposition": None,
        "health": health.get("severity", "unknown"),
        "tasks_total": len(tasks),
        "tasks_complete": sum(1 for task in tasks if task.complete),
        "next_task": selected.get("task_id") if isinstance(selected, dict) else None,
        **phase_fields,
    }


def _phase_progress(tasks_path: Path, tasks: list[core.Task]) -> dict[str, Any]:
    phase_by_task = core.task_phase_map(tasks_path)
    phases: dict[str, list[core.Task]] = {}
    for task in tasks:
        phase = phase_by_task.get(task.task_id, "Unphased")
        if phase == "Unphased":
            continue
        phases.setdefault(phase, []).append(task)

    if not phases:
        return {
            "phases_total": None,
            "phases_complete": None,
            "current_phase": None,
            "phase_state": None,
        }

    phase_items = list(phases.items())
    complete_count = sum(1 for _name, phase_tasks in phase_items if all(task.complete for task in phase_tasks))
    current_name, current_tasks = next(
        ((name, phase_tasks) for name, phase_tasks in phase_items if not all(task.complete for task in phase_tasks)),
        phase_items[-1],
    )
    current_states = {task.status for task in current_tasks}
    phase_state = next(state for state in PHASE_STATE_PRECEDENCE if state in current_states)
    return {
        "phases_total": len(phase_items),
        "phases_complete": complete_count,
        "current_phase": current_name,
        "phase_state": phase_state,
    }


def build_specs_view(repo_root: Path, *, include_history: bool = False, docs_root: str | None = None) -> dict[str, Any]:
    root = repo_root.resolve()
    scan = core.scan_specs(root, docs_root)
    active_items = sorted(
        (item for item in scan.get("specs", []) if item.get("lifecycle") == "active"),
        key=lambda item: str(item.get("spec_id", "")),
    )
    records = [_active_spec_record(root, item) for item in active_items]
    active_count = len(records)
    if include_history:
        records.extend(build_history_view(root)["records"])
    return command_view(
        "specs",
        root,
        records,
        {
            "total": len(records),
            "active": active_count,
            "historic": len(records) - active_count,
            "empty": not records,
        },
    )


def _selected_task_states(filters: TaskFilters) -> frozenset[str] | None:
    has_state_filter = filters.complete or filters.pending or filters.open or bool(filters.states)
    if filters.next_only and has_state_filter:
        raise PublicViewError("--next is exclusive with task-state filters.", code="filter_conflict")
    unknown = sorted(set(filters.states) - set(core.TASK_STATE_MARKERS))
    if unknown:
        raise PublicViewError(f"Unknown task state: {', '.join(unknown)}", code="filter_invalid")
    if not has_state_filter:
        return None
    selected = set(filters.states)
    if filters.complete:
        selected.add("complete")
    if filters.pending:
        selected.add("pending")
    if filters.open:
        selected.update(OPEN_TASK_STATES)
    return frozenset(selected)


def _task_requirement_map(spec_path: Path) -> dict[str, list[str]]:
    _docs, _gaps, tables = traceability.load_spec(spec_path)
    rows = tables.get("Task To Context Matrix", [])
    mapping: dict[str, list[str]] = {}
    for row in rows:
        task_value = row.get("Task ID", "") or row.get("Task", "")
        task_ids = core.TASK_RE.findall(task_value)
        requirements = core.REQ_RE.findall(row.get("Requirements", ""))
        for task_id in task_ids:
            mapping[task_id] = list(dict.fromkeys(requirements))
    return mapping


def build_tasks_view(
    repo_root: Path,
    spec_path: Path,
    *,
    filters: TaskFilters | None = None,
    include_subtasks: bool = True,
    command: str = "tasks",
) -> dict[str, Any]:
    root = repo_root.resolve()
    selected_filters = filters or TaskFilters()
    states = _selected_task_states(selected_filters)
    payload = core.task_list(spec_path, include_subtasks=include_subtasks)
    requirement_map = _task_requirement_map(spec_path)
    source_tasks = [task for phase in payload.get("phases", []) for task in phase.get("tasks", [])]
    records = [
        {
            "task_id": task.get("task_id"),
            "marker": task.get("marker"),
            "state": task.get("status"),
            "summary": task.get("title", ""),
            "dependencies": list(task.get("depends_on", [])),
            "requirements": requirement_map.get(str(task.get("task_id")), []),
            "is_subtask": bool(task.get("parent_id")),
        }
        for task in source_tasks
    ]
    if selected_filters.next_only:
        selected = core.next_task(spec_path).get("selected")
        selected_id = selected.get("task_id") if isinstance(selected, dict) else None
        records = [record for record in records if record["task_id"] == selected_id]
    elif states is not None:
        records = [record for record in records if record["state"] in states]
    return command_view(
        command,
        root,
        records,
        {
            "total": len(records),
            "source_total": len(source_tasks),
            "next_only": selected_filters.next_only,
            "states": sorted(states) if states is not None else [],
            "spec_id": spec_path.name,
            "spec_path": repo_relative_path(root, spec_path),
        },
    )


def _requirement_title(block: dict[str, Any]) -> str:
    first_line = str(block.get("text", "")).splitlines()[0] if block.get("text") else ""
    match = requirements_parser.REQ_HEADING_RE.match(first_line)
    return match.group(2).strip() if match else ""


def _requirement_task_map(spec_path: Path) -> dict[str, list[str]]:
    _docs, _gaps, tables = traceability.load_spec(spec_path)
    rows = tables.get("Requirement To Delivery Matrix", [])
    available_task_ids = [task.task_id for task in core.parse_tasks(spec_path / "tasks.md")]
    mapping: dict[str, list[str]] = {}
    for row in rows:
        requirement_value = row.get("Requirement", "") or row.get("Requirements", "")
        for requirement_id in core.REQ_RE.findall(requirement_value):
            task_value = row.get("Tasks", "") or row.get("Covered by tasks", "")
            mapping[requirement_id.lower()] = core.task_ids_from_value(task_value, available_task_ids)
    return mapping


def build_requirements_view(
    repo_root: Path,
    spec_path: Path,
    *,
    filters: RequirementFilters | None = None,
) -> dict[str, Any]:
    root = repo_root.resolve()
    selected_filters = filters or RequirementFilters()
    if selected_filters.missing_priority and selected_filters.priorities:
        raise PublicViewError("--missing-priority is exclusive with --priority.", code="filter_conflict")
    unknown = sorted(set(selected_filters.priorities) - CANONICAL_PRIORITIES)
    if unknown:
        raise PublicViewError(f"Unknown requirement priority: {', '.join(unknown)}", code="filter_invalid")
    blocks, diagnostics = requirements_parser.requirement_blocks(spec_path / "requirements.md")
    diagnostics_by_requirement: dict[str, list[dict[str, Any]]] = {}
    for item in diagnostics:
        diagnostics_by_requirement.setdefault(str(item.get("requirement_id", "")).lower(), []).append(item)
    task_map = _requirement_task_map(spec_path)
    records = []
    for block in blocks:
        requirement_id = str(block["id"])
        priority = block.get("priority", "unspecified")
        records.append(
            {
                "requirement_id": requirement_id,
                "title": _requirement_title(block),
                "priority": priority,
                "tasks": task_map.get(requirement_id.lower(), []),
                "diagnostics": diagnostics_by_requirement.get(requirement_id.lower(), []),
            }
        )
    if selected_filters.missing_priority:
        records = [record for record in records if record["priority"] == "unspecified"]
    elif selected_filters.priorities:
        priorities = set(selected_filters.priorities)
        records = [record for record in records if record["priority"] in priorities]
    return command_view(
        "requirements",
        root,
        records,
        {
            "total": len(records),
            "source_total": len(blocks),
            "diagnostic_count": len(diagnostics),
            "spec_id": spec_path.name,
            "spec_path": repo_relative_path(root, spec_path),
        },
    )


def _history_disposition(entry: dict[str, Any]) -> str:
    return "removed" if entry.get("status") == "removed" or entry.get("closure_action") == "remove" else "archived"


def build_history_view(
    repo_root: Path,
    *,
    filters: HistoryFilters | None = None,
) -> dict[str, Any]:
    root = repo_root.resolve()
    selected_filters = filters or HistoryFilters()
    if selected_filters.limit is not None and selected_filters.limit < 0:
        raise PublicViewError("History limit must be zero or greater.", code="filter_invalid")
    payload = core.archive_index(root)
    errors = [item for item in payload.get("diagnostics", []) if item.get("severity") == "error"]
    if errors:
        raise PublicViewError("Historic spec metadata is invalid.", code="history_invalid", diagnostics=errors)
    records = [
        {
            "spec_id": entry.get("spec_id"),
            "title": entry.get("title"),
            "disposition": _history_disposition(entry),
            "lifecycle": "historic",
            "final_spec_commit": entry.get("final_spec_commit"),
            "cleanup_commit": entry.get("cleanup_commit"),
            "package_path": repo_relative_path(root, entry.get("package_path")),
        }
        for entry in payload.get("entries", [])
    ]
    dispositions = set()
    if selected_filters.archived:
        dispositions.add("archived")
    if selected_filters.removed:
        dispositions.add("removed")
    if dispositions:
        records = [record for record in records if record["disposition"] in dispositions]
    source_total = len(records)
    if selected_filters.limit is not None:
        records = records[: selected_filters.limit]
    return command_view(
        "history",
        root,
        records,
        {"total": len(records), "filtered_total": source_total, "diagnostic_count": len(payload.get("diagnostics", []))},
    )
