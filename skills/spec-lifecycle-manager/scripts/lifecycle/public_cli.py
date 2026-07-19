"""Standard-library command line interface for public lifecycle inspection."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence, TextIO

from lifecycle import core
from lifecycle import public_views


EXIT_SUCCESS = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")


class PublicArgumentParser(argparse.ArgumentParser):
    """Argument parser that reports expected input failures without exiting."""

    def error(self, message: str) -> None:
        raise public_views.PublicViewError(message, code="usage")


def _add_common_options(parser: argparse.ArgumentParser, *, suppress_defaults: bool = False) -> None:
    default = argparse.SUPPRESS if suppress_defaults else None
    parser.add_argument("-C", "--repo", dest="repo", default=default, help="Repository root (defaults to discovery from cwd).")
    parser.add_argument("--json", action="store_true", default=default, help="Emit the stable JSON view envelope.")


def build_parser() -> PublicArgumentParser:
    parser = PublicArgumentParser(
        prog="slm",
        description="Inspect Spec Lifecycle Manager state.",
        epilog="Inspection commands are read-only. The package dispatcher owns 'slm install'.",
    )
    _add_common_options(parser)
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    specs = subparsers.add_parser("specs", help="List active specs and their lifecycle state.")
    _add_common_options(specs, suppress_defaults=True)
    specs.add_argument("--all", action="store_true", help="Include historic specs.")

    tasks = subparsers.add_parser("tasks", help="List tasks and normalized state for a selected spec.")
    _add_common_options(tasks, suppress_defaults=True)
    tasks.add_argument("spec", nargs="?", help="Spec ID, number, slug, or package path.")
    tasks.add_argument("--complete", action="store_true", help="Include complete tasks.")
    tasks.add_argument("--pending", action="store_true", help="Include literal pending tasks.")
    tasks.add_argument("--open", action="store_true", help="Include all non-terminal open states.")
    tasks.add_argument("--state", action="append", default=[], help="Include a normalized task state; repeatable.")
    tasks.add_argument("--next", action="store_true", dest="next_only", help="Show only the dependency-aware next task.")

    next_parser = subparsers.add_parser("next", help="Show the dependency-aware next task for a selected spec.")
    _add_common_options(next_parser, suppress_defaults=True)
    next_parser.add_argument("spec", nargs="?", help="Spec ID, number, slug, or package path.")

    requirements = subparsers.add_parser("requirements", help="List requirements, priorities, and linked tasks.")
    _add_common_options(requirements, suppress_defaults=True)
    requirements.add_argument("spec", nargs="?", help="Spec ID, number, slug, or package path.")
    requirements.add_argument(
        "--priority",
        action="append",
        default=[],
        help="Filter by canonical priority; repeatable.",
    )
    requirements.add_argument(
        "--missing-priority",
        action="store_true",
        help="Show requirements without an accepted canonical priority.",
    )

    history = subparsers.add_parser("history", help="List closed and historic specs.")
    _add_common_options(history, suppress_defaults=True)
    history.add_argument("--archived", action="store_true", help="Include retained archived specs.")
    history.add_argument("--removed", action="store_true", help="Include removed specs.")
    history.add_argument("--limit", type=int, help="Return at most the most recent N records.")

    install = subparsers.add_parser("install", help="Install the packaged Codex plugin.")
    install.add_argument("install_args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    return parser


def normalize_argv(argv: Sequence[str]) -> list[str]:
    values = list(argv)
    if not values:
        return ["specs"]
    if any(value in public_views.PUBLIC_COMMANDS for value in values):
        return values
    if "-h" in values or "--help" in values:
        return values
    return ["specs", *values]


def resolve_repo_root(repo: str | None, cwd: Path) -> Path:
    if repo:
        requested = Path(repo).expanduser()
        candidate = requested if requested.is_absolute() else cwd / requested
        if not candidate.exists():
            raise public_views.PublicViewError(f"Repository path does not exist: {repo}", code="repo_missing")
        if not candidate.is_dir():
            raise public_views.PublicViewError(f"Repository path is not a directory: {repo}", code="repo_invalid")
        return candidate.resolve()
    return core.repo_root_for(cwd.resolve())


def build_view(args: argparse.Namespace, repo_root: Path) -> dict[str, Any]:
    command = args.command or "specs"
    if command == "specs":
        return public_views.build_specs_view(repo_root, include_history=bool(getattr(args, "all", False)))
    if command in {"tasks", "next"}:
        spec_path = public_views.select_active_spec(repo_root, getattr(args, "spec", None))
        next_only = command == "next" or bool(getattr(args, "next_only", False))
        filters = public_views.TaskFilters(
            complete=bool(getattr(args, "complete", False)),
            pending=bool(getattr(args, "pending", False)),
            open=bool(getattr(args, "open", False)),
            states=tuple(getattr(args, "state", [])),
            next_only=next_only,
        )
        return public_views.build_tasks_view(repo_root, spec_path, filters=filters, command=command)
    if command == "requirements":
        spec_path = public_views.select_active_spec(repo_root, getattr(args, "spec", None))
        filters = public_views.RequirementFilters(
            priorities=tuple(getattr(args, "priority", [])),
            missing_priority=bool(getattr(args, "missing_priority", False)),
        )
        return public_views.build_requirements_view(repo_root, spec_path, filters=filters)
    if command == "history":
        filters = public_views.HistoryFilters(
            archived=bool(getattr(args, "archived", False)),
            removed=bool(getattr(args, "removed", False)),
            limit=getattr(args, "limit", None),
        )
        return public_views.build_history_view(repo_root, filters=filters)
    if command == "install":
        raise public_views.PublicViewError(
            "The package dispatcher owns 'slm install'; invoke the packaged slm executable.",
            code="install_dispatch_required",
        )
    raise public_views.PublicViewError(f"Unknown command: {command}", code="usage")


def safe_text(value: Any) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (list, tuple)):
        value = ", ".join(safe_text(item) for item in value) or "-"
    text = ANSI_ESCAPE_RE.sub("", str(value))
    return re.sub(r"\s+", " ", CONTROL_RE.sub(" ", text)).strip() or "-"


def _spec_rows(records: list[dict[str, Any]]) -> tuple[list[str], list[list[str]]]:
    headers = ["SPEC", "STATUS", "LIFECYCLE", "DISPOSITION", "HEALTH", "TASKS", "NEXT", "PATH"]
    rows = []
    for record in records:
        total = record.get("tasks_total")
        complete = record.get("tasks_complete")
        progress = f"{complete}/{total}" if total is not None and complete is not None else "-"
        rows.append(
            [
                record.get("spec_id"),
                record.get("status"),
                record.get("lifecycle"),
                record.get("disposition"),
                record.get("health"),
                progress,
                record.get("next_task"),
                record.get("path") or record.get("package_path"),
            ]
        )
    return headers, [[safe_text(value) for value in row] for row in rows]


def _task_rows(records: list[dict[str, Any]]) -> tuple[list[str], list[list[str]]]:
    headers = ["TASK", "MARKER", "STATE", "DEPENDS", "REQUIREMENTS", "SUMMARY"]
    rows = [
        [
            record.get("task_id"),
            f"[{record.get('marker', ' ')}]",
            record.get("state"),
            record.get("dependencies"),
            record.get("requirements"),
            record.get("summary"),
        ]
        for record in records
    ]
    return headers, [[safe_text(value) for value in row] for row in rows]


def _requirement_rows(records: list[dict[str, Any]]) -> tuple[list[str], list[list[str]]]:
    headers = ["REQUIREMENT", "PRIORITY", "TASKS", "TITLE", "DIAGNOSTICS"]
    rows = [
        [
            record.get("requirement_id"),
            record.get("priority"),
            record.get("tasks"),
            record.get("title"),
            [item.get("code") for item in record.get("diagnostics", [])],
        ]
        for record in records
    ]
    return headers, [[safe_text(value) for value in row] for row in rows]


def _history_rows(records: list[dict[str, Any]]) -> tuple[list[str], list[list[str]]]:
    headers = ["SPEC", "TITLE", "DISPOSITION", "FINAL COMMIT", "CLEANUP COMMIT", "PACKAGE"]
    rows = [
        [
            record.get("spec_id"),
            record.get("title"),
            record.get("disposition"),
            record.get("final_spec_commit"),
            record.get("cleanup_commit"),
            record.get("package_path"),
        ]
        for record in records
    ]
    return headers, [[safe_text(value) for value in row] for row in rows]


def table_data(view: dict[str, Any]) -> tuple[list[str], list[list[str]]]:
    command = str(view.get("command"))
    records = view.get("records", [])
    if command == "specs":
        return _spec_rows(records)
    if command in {"tasks", "next"}:
        return _task_rows(records)
    if command == "requirements":
        return _requirement_rows(records)
    if command == "history":
        return _history_rows(records)
    raise public_views.PublicViewError(f"No table renderer for command: {command}", code="render_invalid")


def empty_message(command: str) -> str:
    return {
        "specs": "No specs found.",
        "tasks": "No tasks matched.",
        "next": "No runnable task found.",
        "requirements": "No requirements matched.",
        "history": "No historic specs found.",
    }.get(command, "No records found.")


def render_table(view: dict[str, Any], stream: TextIO) -> None:
    headers, rows = table_data(view)
    if not rows:
        stream.write(empty_message(str(view.get("command"))) + "\n")
        return
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    stream.write("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)).rstrip() + "\n")
    stream.write("  ".join("-" * width for width in widths).rstrip() + "\n")
    for row in rows:
        stream.write("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)).rstrip() + "\n")


def render_json(view: dict[str, Any], stream: TextIO) -> None:
    json.dump(view, stream, indent=2, ensure_ascii=True)
    stream.write("\n")


def error_exit_code(error: public_views.PublicViewError) -> int:
    return EXIT_RUNTIME if error.code in {"history_invalid", "render_invalid"} else EXIT_USAGE


def format_error(error: public_views.PublicViewError) -> str:
    lines = [safe_text(str(error))]
    if error.candidates:
        lines.append("Candidates: " + ", ".join(safe_text(candidate) for candidate in error.candidates))
    for diagnostic in error.diagnostics:
        code = safe_text(diagnostic.get("code", "UNKNOWN"))
        message = safe_text(diagnostic.get("message", ""))
        lines.append(f"{code}: {message}".rstrip())
    return "\n".join(lines)


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    cwd: Path | None = None,
) -> int:
    output = stdout or sys.stdout
    errors = stderr or sys.stderr
    parser = build_parser()
    try:
        args = parser.parse_args(normalize_argv(sys.argv[1:] if argv is None else argv))
        repo_root = resolve_repo_root(getattr(args, "repo", None), cwd or Path.cwd())
        view = build_view(args, repo_root)
        if bool(getattr(args, "json", False)):
            render_json(view, output)
        else:
            render_table(view, output)
        return EXIT_SUCCESS
    except public_views.PublicViewError as error:
        errors.write(f"slm: {format_error(error)}\n")
        return error_exit_code(error)
    except OSError as error:
        errors.write(f"slm: {error}\n")
        return EXIT_RUNTIME
    except Exception as error:  # pragma: no cover - final CLI containment boundary
        errors.write(f"slm: unexpected error: {error}\n")
        return EXIT_RUNTIME
