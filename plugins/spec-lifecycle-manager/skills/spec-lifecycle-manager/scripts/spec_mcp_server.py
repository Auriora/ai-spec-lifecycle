#!/usr/bin/env python3
"""Minimal stdio MCP adapter for shared lifecycle internals.

The adapter is dependency-free. It exposes shared lifecycle internals as
MCP resources, tools, and prompts without duplicating lifecycle policy or
parsing logic. Write-capable tools are preview-first and scoped by the runtime.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle import core as lifecycle_core
import spec_agent_schemas
from lifecycle import traceability
from lifecycle.actions import lifecycle_next_actions
from lifecycle.capabilities import lifecycle_capabilities
from lifecycle.migration import script_migration_inventory


PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "spec-lifecycle-manager"
SERVER_VERSION = "0.1.0"
SERVER_INSTRUCTIONS = (
    "Use spec-lifecycle-manager tools for lifecycle context, validation, "
    "traceability, task state, promotion, and closure. Prefer MCP tools over "
    "direct runtime-script commands; retained runtime scripts are for CI, "
    "explicit recovery when MCP is unavailable, and MCP debugging."
)
REPO_ROOT_PROPERTY = "Repository root. Defaults to current working directory."
WORKSPACE_ROOT_ENV_VARS = (
    "SPEC_LIFECYCLE_REPO_ROOT",
    "CODEX_REPO_ROOT",
    "CODEX_WORKSPACE_ROOT",
    "CODEX_WORKSPACE",
    "WORKSPACE_ROOT",
    "PWD",
)
SPEC_PATH_PROPERTIES = {
    "repo_root": REPO_ROOT_PROPERTY,
    "spec_path": "Spec package path or ID.",
}
REVIEW_PACKET_TYPE_CONTRACT = lifecycle_core.review_packet_type_contract()
REVIEW_TYPE_PROPERTY = {
    "type": "string",
    "description": (
        "Optional review packet template ID. Defaults to design_requirements_trace. "
        "Implementation-style aliases such as implementation and implementation-readiness "
        "map to implementation_review. Unknown values map to generic_review and are "
        "preserved as requested_review_type."
    ),
    "default": REVIEW_PACKET_TYPE_CONTRACT["default"],
    "x-canonical-review-types": REVIEW_PACKET_TYPE_CONTRACT["canonical_types"],
    "x-review-type-aliases": REVIEW_PACKET_TYPE_CONTRACT["aliases"],
    "x-unknown-type-behavior": REVIEW_PACKET_TYPE_CONTRACT["unknown_type_behavior"],
}


def find_repo_root(path: Path | None = None) -> Path:
    start = (path or Path.cwd()).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start


def workspace_repo_root() -> Path | None:
    for name in WORKSPACE_ROOT_ENV_VARS:
        value = os.environ.get(name)
        if value:
            return find_repo_root(Path(value))
    return None


def default_repo_root(path: Path | None = None) -> Path:
    return find_repo_root(path) if path is not None else workspace_repo_root() or find_repo_root()


def json_text(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def text_content(payload: Any) -> list[dict[str, str]]:
    return [{"type": "text", "text": json_text(payload)}]


def relative_path_for_mcp(path: Path, repo_root: Path) -> str | None:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(repo_root.resolve())
    except ValueError:
        return None
    return relative.as_posix() or "."


def normalize_mcp_string(value: str, repo_root: Path) -> str | None:
    path = Path(value)
    if path.is_absolute():
        return relative_path_for_mcp(path, repo_root)
    root_text = repo_root.resolve().as_posix()
    if root_text in value:
        return value.replace(root_text, ".")
    return value


def normalize_mcp_payload(payload: Any, repo_root: Path) -> Any:
    if isinstance(payload, dict):
        normalized = {}
        for key, value in payload.items():
            normalized_value = normalize_mcp_payload(value, repo_root)
            if normalized_value is not None:
                normalized[key] = normalized_value
        return normalized
    if isinstance(payload, list):
        return [item for item in (normalize_mcp_payload(value, repo_root) for value in payload) if item is not None]
    if isinstance(payload, str):
        return normalize_mcp_string(payload, repo_root)
    return payload


def tool_result(payload: Any, repo_root: Path) -> dict[str, Any]:
    normalized = normalize_mcp_payload(payload, repo_root)
    return {
        "content": text_content(normalized),
        "structuredContent": normalized if isinstance(normalized, dict) else {"result": normalized},
        "isError": False,
    }


def error_response(request_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


def response(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def repo_root_arg(arguments: dict[str, Any], default_root: Path) -> Path:
    return Path(arguments.get("repo_root") or default_root).resolve()


def bool_arg(arguments: dict[str, Any], name: str) -> bool:
    value = arguments.get(name)
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def resolve_spec_path(repo_root: Path, value: str) -> Path:
    """Resolve a live spec path using the same discovery rules as scan_specs."""
    root = repo_root.resolve()
    path = Path(value)
    candidates = []
    if path.is_absolute():
        candidates.append(path)
    else:
        candidates.extend([Path(value), root / value])
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    matches = [spec for spec in lifecycle_core.discover_spec_paths(root) if spec.name == value]
    if len(matches) == 1:
        return matches[0].resolve()
    if len(matches) > 1:
        raise ValueError(f"Spec ID is ambiguous across docs partitions: {value}; use a package path.")
    raise ValueError(f"Active spec not found: {value}. Use scan_specs for live packages or history://spec-archive-index for removed specs.")


def spec_path_arg(arguments: dict[str, Any], default_root: Path) -> Path:
    value = arguments.get("spec_path") or arguments.get("spec_id")
    if not value:
        raise ValueError("spec_path or spec_id is required")
    return resolve_spec_path(repo_root_arg(arguments, default_root), str(value))


def path_arg(arguments: dict[str, Any], name: str, default_root: Path) -> Path:
    value = arguments.get(name)
    if not value:
        raise ValueError(f"{name} is required")
    path = Path(value)
    if path.is_absolute() and path.exists():
        return path.resolve()
    return (repo_root_arg(arguments, default_root) / str(value)).resolve()


def tool_definitions() -> list[dict[str, Any]]:
    return [
        tool_schema(
            "lifecycle_capabilities",
            "Report MCP server/client capability visibility and the dynamic-tool decision.",
            {"repo_root": REPO_ROOT_PROPERTY},
            output_schema=spec_agent_schemas.lifecycle_capabilities_output_schema(),
        ),
        tool_schema(
            "scan_specs",
            "Discover spec packages, artifact inventory, health, and template authority.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "docs_root": "Optional docs root.",
                "include_archived_lint": {
                    "type": ["boolean", "string"],
                    "description": "Set true to run authoring lint against archived specs during scan.",
                },
            },
        ),
        tool_schema(
            "active_spec_preflight",
            "Return active spec, next task, required context, open decisions, and validation commands.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "spec_path": "Optional spec package path or ID when multiple active specs exist.",
                "task_id": "Optional task ID such as T004.",
                "docs_root": "Optional docs root.",
            },
        ),
        tool_schema(
            "lifecycle_guide",
            "Return first-run lifecycle readiness, bootstrap guidance, and next actions.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "docs_root": "Optional docs root.",
                "mode": "Optional guide mode. Defaults to auto.",
            },
        ),
        tool_schema(
            "bootstrap_plan",
            "Preview minimal lifecycle bootstrap writes without mutating files.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "docs_root": "Optional docs root. Defaults to docs.",
                "project_summary": "Optional user-confirmed project purpose statement.",
                "create_spec": {"type": ["boolean", "string"], "description": "Preview an optional first spec package.", "default": False},
                "spec_slug": "Optional slug for the first spec package when create_spec is true.",
            },
        ),
        tool_schema(
            "stage_readiness",
            "Return staged artifact, coverage, downstream review, and agent-readiness status.",
            SPEC_PATH_PROPERTIES,
            ["spec_path"],
        ),
        tool_schema(
            "validation_plan",
            "Plan validation checks from changed files and optional task context.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "changed_files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Repo-relative or absolute changed file paths.",
                    "default": [],
                },
                "spec_path": "Optional spec package path or ID.",
                "task_id": "Optional task ID such as T004.",
                "risk_level": "Optional caller-supplied risk level.",
            },
        ),
        tool_schema(
            "evidence_quality_check",
            "Review task and verification evidence quality without mutating files.",
            SPEC_PATH_PROPERTIES,
            ["spec_path"],
        ),
        tool_schema(
            "closure_risk_review",
            "Review closure risk signals without mutating files.",
            SPEC_PATH_PROPERTIES,
            ["spec_path"],
        ),
        tool_schema(
            "agent_readiness_packet",
            "Return bounded implementation context for a task before coding.",
            {**SPEC_PATH_PROPERTIES, "task_id": "Task ID such as T004."},
            ["spec_path", "task_id"],
        ),
        tool_schema(
            "agent_backed_tool",
            "Run an advisory agent-backed tool; returns unavailable when no runner is configured.",
            {
                **SPEC_PATH_PROPERTIES,
                "tool_name": {
                    **REVIEW_TYPE_PROPERTY,
                    "description": (
                        "Agent-backed review tool selector. Uses the same canonical values, "
                        "aliases, default, and generic fallback as review_packet review_type."
                    ),
                },
                "model_class": "Optional model class.",
            },
            ["spec_path", "tool_name"],
        ),
        tool_schema(
            "no_active_spec_context",
            "Return durable docs, backlog, roadmap, closure-log, and archive-index context when no active spec exists.",
            {"repo_root": REPO_ROOT_PROPERTY},
        ),
        tool_schema(
            "script_migration_inventory",
            "Return script migration classifications, replacement contracts, and closure blockers.",
            {"repo_root": REPO_ROOT_PROPERTY},
            output_schema=spec_agent_schemas.script_migration_inventory_output_schema(),
        ),
        tool_schema("spec_summary", "Return a specs://{spec_id}/summary style payload.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema("lint_spec_package", "Lint a spec package.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema(
            "lint_doc",
            "Lint a single spec or template document.",
            {"path": "Document path.", "artifact_type": "Optional artifact type override.", "repo_root": "Repository root for relative paths."},
            ["path"],
        ),
        tool_schema("next_task", "Select the next runnable task with traceability context.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema(
            "list_tasks",
            "Return grouped tasks, dependency readiness, evidence summaries, and advisory findings.",
            {
                **SPEC_PATH_PROPERTIES,
                "include_subtasks": {
                    "type": ["boolean", "string"],
                    "description": "Include subtasks in grouped output. Defaults to true.",
                    "default": True,
                },
                "status": "Optional normalized task status filter.",
            },
            ["spec_path"],
        ),
        tool_schema(
            "task_details",
            "Return parsed task detail with parent/subtask, dependency, traceability, and advisory context.",
            {**SPEC_PATH_PROPERTIES, "task_id": "Task ID such as T004."},
            ["spec_path", "task_id"],
        ),
        tool_schema(
            "task_state_audit",
            "Audit task state, evidence, metadata, broad tasks, and dependency trust.",
            {**SPEC_PATH_PROPERTIES, "task_id": "Optional task ID filter."},
            ["spec_path"],
        ),
        tool_schema(
            "set_task_state",
            "Preview or write a guarded task-state update. Defaults to dry-run and requires write_intent for writes.",
            {
                **SPEC_PATH_PROPERTIES,
                "task_id": "Task ID such as T004.",
                "state": "Target normalized task state.",
                "evidence": "Evidence text to write.",
                "status_note": "Optional Status metadata.",
                "evidence_mode": "Optional Evidence mode metadata.",
                "destination": "Optional Destination metadata.",
                "decision_owner": "Optional Decision owner metadata.",
                "dry_run": {"type": ["boolean", "string"], "description": "Preview without writing. Defaults to true.", "default": True},
                "write_intent": {"type": ["boolean", "string"], "description": "Required true when dry_run is false.", "default": False},
            },
            ["spec_path", "task_id", "state", "evidence"],
        ),
        tool_schema("closure_check", "Check closure readiness and blockers.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema(
            "closure_plan",
            "Preview closure metadata, blockers, planned edits, scriptable actions, and validation commands.",
            {
                **SPEC_PATH_PROPERTIES,
                "final_spec_commit": "Optional final spec commit hash.",
                "closure_action": "Closure action. Defaults to removed.",
                "include_reference_scan": {
                    "type": ["boolean", "string"],
                    "description": "Set false to skip active-reference scanning. Defaults to true.",
                    "default": True,
                },
            },
            ["spec_path"],
        ),
        tool_schema(
            "closure_apply",
            "Preview or apply one closure planned action. Defaults to dry-run and requires write_intent for writes.",
            {
                **SPEC_PATH_PROPERTIES,
                "plan": {"type": "object", "description": "Closure plan payload returned by closure_plan."},
                "action_id": "Planned action ID to apply.",
                "dry_run": {"type": ["boolean", "string"], "description": "Preview without writing. Defaults to true.", "default": True},
                "write_intent": {"type": ["boolean", "string"], "description": "Required true when dry_run is false.", "default": False},
            },
            ["spec_path", "plan", "action_id"],
        ),
        tool_schema(
            "closure_resolve",
            "Preview or apply cleanup-hash resolution in closure records.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "spec_id": "Spec ID whose pending cleanup metadata should be resolved.",
                "cleanup_commit": "Optional cleanup commit hash. Defaults to repository HEAD when omitted.",
                "dry_run": {"type": ["boolean", "string"], "description": "Preview without writing. Defaults to true.", "default": True},
                "write_intent": {"type": ["boolean", "string"], "description": "Required true when dry_run is false.", "default": False},
            },
            ["spec_id"],
        ),
        tool_schema("archive_index", "Validate spec archive index and closure-log consistency.", {"repo_root": REPO_ROOT_PROPERTY}),
        tool_schema(
            "resolve_spec_reference",
            "Resolve an active, archived, missing, or ambiguous spec reference without throwing path-lookup errors.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "reference": "Spec package path, spec ID, numeric prefix, or archive package reference.",
                "docs_root": "Optional docs root.",
            },
            ["reference"],
        ),
        tool_schema(
            "mcp_audit",
            "Summarize spec lifecycle MCP mentions, explicit errors, and interaction comments in Codex session logs.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "sessions_root": "Directory containing Codex session JSONL files.",
                "since": "Optional lexicographic relative-path cutoff, such as 2026/06/07.",
                "limit": {"type": ["integer", "string"], "description": "Maximum matched session files and per-file items to return."},
                "include_sessions": {
                    "type": ["boolean", "string"],
                    "description": "Set true to include per-session matched items. Defaults to compact aggregate output.",
                    "default": False,
                },
            },
            ["sessions_root"],
        ),
        tool_schema("reconcile_spec", "Generate a classified reconciliation report.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema("promotion_plan", "Generate durable documentation promotion targets.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema(
            "review_packet",
            "Generate a bounded read-only review packet. review_type is optional; omit it for design_requirements_trace.",
            {**SPEC_PATH_PROPERTIES, "review_type": REVIEW_TYPE_PROPERTY, "model_class": "Optional model class."},
            ["spec_path"],
        ),
        tool_schema(
            "task_context",
            "Return task traceability context.",
            {**SPEC_PATH_PROPERTIES, "task_id": "Task ID such as T004."},
            ["spec_path", "task_id"],
        ),
        tool_schema(
            "traceability_lookup",
            "Lookup task, requirement, or design traceability.",
            {**SPEC_PATH_PROPERTIES, "task_id": "Task ID.", "requirement": "Requirement ID.", "design": "Design section reference."},
            ["spec_path"],
            output_schema=spec_agent_schemas.traceability_lookup_output_schema(),
        ),
        tool_schema("prompts_validate", "List and validate prompt definitions.", {"repo_root": REPO_ROOT_PROPERTY}),
    ]


def tool_schema(
    name: str,
    description: str,
    properties: dict[str, Any],
    required: list[str] | None = None,
    *,
    output_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema_properties = {
        key: value if isinstance(value, dict) else {"type": "string", "description": value}
        for key, value in properties.items()
    }
    schema = {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": schema_properties,
            "required": required or [],
            "additionalProperties": False,
        },
    }
    if output_schema is not None:
        schema["outputSchema"] = output_schema
    return schema


def with_available_next_actions(payload: dict[str, Any], repo_root: Path, spec_path: Path | None = None) -> dict[str, Any]:
    enriched = dict(payload)
    enriched["available_next_actions"] = lifecycle_next_actions(repo_root, spec_path)
    return enriched


def call_tool(name: str, arguments: dict[str, Any], default_root: Path) -> tuple[dict[str, Any], Path]:
    root = repo_root_arg(arguments, default_root)
    if name == "lifecycle_capabilities":
        return lifecycle_capabilities(root, server_name=SERVER_NAME, server_version=SERVER_VERSION, protocol_version=PROTOCOL_VERSION), root
    if name == "scan_specs":
        return lifecycle_core.scan_specs(
            root,
            arguments.get("docs_root"),
            include_archived_lint=bool_arg(arguments, "include_archived_lint"),
        ), root
    if name == "active_spec_preflight":
        spec_path = spec_path_arg(arguments, default_root) if arguments.get("spec_path") or arguments.get("spec_id") else None
        payload = lifecycle_core.active_spec_preflight(root, spec_path, arguments.get("task_id"), arguments.get("docs_root"))
        selected = payload.get("selected_spec") if isinstance(payload, dict) else None
        selected_path = root / selected["path"] if isinstance(selected, dict) and selected.get("path") else spec_path
        return with_available_next_actions(payload, root, selected_path), root
    if name == "lifecycle_guide":
        return with_available_next_actions(lifecycle_core.lifecycle_guide(root, arguments.get("docs_root"), arguments.get("mode") or "auto"), root), root
    if name == "bootstrap_plan":
        return lifecycle_core.bootstrap_plan(
            root,
            arguments.get("docs_root") or "docs",
            arguments.get("project_summary"),
            bool_arg(arguments, "create_spec"),
            arguments.get("spec_slug"),
        ), root
    if name == "stage_readiness":
        spec_path = spec_path_arg(arguments, default_root)
        return with_available_next_actions(lifecycle_core.stage_readiness(spec_path), root, spec_path), root
    if name == "validation_plan":
        spec_path = spec_path_arg(arguments, default_root) if arguments.get("spec_path") or arguments.get("spec_id") else None
        changed_files = arguments.get("changed_files") or []
        if not isinstance(changed_files, list):
            raise ValueError("changed_files must be an array")
        return lifecycle_core.validation_plan(
            root,
            [str(item) for item in changed_files],
            spec_path,
            arguments.get("task_id"),
            arguments.get("risk_level"),
        ), root
    if name == "evidence_quality_check":
        return lifecycle_core.evidence_quality_check(spec_path_arg(arguments, default_root)), root
    if name == "closure_risk_review":
        return lifecycle_core.closure_risk_review(spec_path_arg(arguments, default_root)), root
    if name == "agent_readiness_packet":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return lifecycle_core.agent_readiness_packet(spec_path_arg(arguments, default_root), str(task_id)), root
    if name == "agent_backed_tool":
        tool_name = arguments.get("tool_name")
        if not tool_name:
            raise ValueError("tool_name is required")
        return lifecycle_core.agent_backed_tool(spec_path_arg(arguments, default_root), str(tool_name), arguments.get("model_class")), root
    if name == "no_active_spec_context":
        return with_available_next_actions(lifecycle_core.no_active_spec_context(root), root), root
    if name == "script_migration_inventory":
        return script_migration_inventory(root), root
    if name == "spec_summary":
        return lifecycle_core.spec_summary(spec_path_arg(arguments, default_root)), root
    if name == "lint_spec_package":
        payload = lifecycle_core.lint_spec_package(spec_path_arg(arguments, default_root))
        assert isinstance(payload, dict)
        return payload, root
    if name == "lint_doc":
        path = path_arg(arguments, "path", default_root)
        diagnostics = lifecycle_core.lint_doc(path, arguments.get("artifact_type"))
        return {"path": str(path), "diagnostics": diagnostics, "summary": lifecycle_core.diagnostic_summary(diagnostics)}, root
    if name == "next_task":
        return lifecycle_core.next_task(spec_path_arg(arguments, default_root)), root
    if name == "list_tasks":
        include_subtasks = arguments.get("include_subtasks")
        include = True if include_subtasks is None else bool_arg(arguments, "include_subtasks")
        return lifecycle_core.task_list(spec_path_arg(arguments, default_root), include_subtasks=include, status=arguments.get("status")), root
    if name == "task_details":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return lifecycle_core.task_details(spec_path_arg(arguments, default_root), str(task_id)), root
    if name == "task_state_audit":
        task_id = arguments.get("task_id")
        return lifecycle_core.task_state_audit(spec_path_arg(arguments, default_root), str(task_id) if task_id else None), root
    if name == "set_task_state":
        task_id = arguments.get("task_id")
        state = arguments.get("state")
        evidence = arguments.get("evidence")
        if not task_id or not state or evidence is None:
            raise ValueError("task_id, state, and evidence are required")
        dry_run_value = arguments.get("dry_run")
        dry_run = True if dry_run_value is None else bool_arg(arguments, "dry_run")
        return lifecycle_core.set_task_state(
            spec_path_arg(arguments, default_root),
            str(task_id),
            str(state),
            str(evidence),
            status_note=arguments.get("status_note"),
            dry_run=dry_run,
            write_intent=bool_arg(arguments, "write_intent"),
            evidence_mode=arguments.get("evidence_mode"),
            destination=arguments.get("destination"),
            decision_owner=arguments.get("decision_owner"),
        ), root
    if name == "closure_check":
        return lifecycle_core.closure_check(spec_path_arg(arguments, default_root)), root
    if name == "closure_plan":
        include_reference_scan = True
        if "include_reference_scan" in arguments:
            include_reference_scan = bool_arg(arguments, "include_reference_scan")
        return lifecycle_core.closure_plan(
            spec_path_arg(arguments, default_root),
            repo_root=root,
            final_spec_commit=arguments.get("final_spec_commit"),
            closure_action=arguments.get("closure_action") or "removed",
            include_reference_scan=include_reference_scan,
        ), root
    if name == "closure_apply":
        plan = arguments.get("plan")
        action_id = arguments.get("action_id")
        if not isinstance(plan, dict):
            raise ValueError("plan must be an object")
        if not action_id:
            raise ValueError("action_id is required")
        dry_run_value = arguments.get("dry_run")
        dry_run = True if dry_run_value is None else bool_arg(arguments, "dry_run")
        return lifecycle_core.closure_apply(
            spec_path_arg(arguments, default_root),
            repo_root=root,
            plan=plan,
            action_id=str(action_id),
            dry_run=dry_run,
            write_intent=bool_arg(arguments, "write_intent"),
        ), root
    if name == "closure_resolve":
        spec_id = arguments.get("spec_id")
        if not spec_id:
            raise ValueError("spec_id is required")
        dry_run_value = arguments.get("dry_run")
        dry_run = True if dry_run_value is None else bool_arg(arguments, "dry_run")
        return lifecycle_core.closure_resolve(
            root,
            spec_id=str(spec_id),
            cleanup_commit=arguments.get("cleanup_commit"),
            dry_run=dry_run,
            write_intent=bool_arg(arguments, "write_intent"),
        ), root
    if name == "archive_index":
        return lifecycle_core.archive_index(root), root
    if name == "resolve_spec_reference":
        reference = arguments.get("reference")
        if not reference:
            raise ValueError("reference is required")
        return lifecycle_core.resolve_spec_reference(root, str(reference), arguments.get("docs_root")), root
    if name == "mcp_audit":
        sessions_root = arguments.get("sessions_root")
        if not sessions_root:
            raise ValueError("sessions_root is required")
        limit_value = arguments.get("limit", 200)
        try:
            limit = int(limit_value)
        except (TypeError, ValueError):
            raise ValueError("limit must be an integer")
        return lifecycle_core.mcp_audit(
            root,
            Path(str(sessions_root)),
            arguments.get("since"),
            limit,
            bool_arg(arguments, "include_sessions"),
        ), root
    if name == "reconcile_spec":
        return lifecycle_core.reconcile_spec(spec_path_arg(arguments, default_root)), root
    if name == "promotion_plan":
        return lifecycle_core.promotion_plan(spec_path_arg(arguments, default_root)), root
    if name == "review_packet":
        return lifecycle_core.generate_review_packet(
            spec_path_arg(arguments, default_root),
            arguments.get("review_type") or "design_requirements_trace",
            arguments.get("model_class"),
        ), root
    if name == "task_context":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return traceability.task_lookup(spec_path_arg(arguments, default_root), str(task_id)), root
    if name == "traceability_lookup":
        spec_path = spec_path_arg(arguments, default_root)
        if arguments.get("task_id"):
            return traceability.task_lookup(spec_path, str(arguments["task_id"])), root
        if arguments.get("requirement"):
            return traceability.reverse_lookup(spec_path, "requirement", str(arguments["requirement"])), root
        if arguments.get("design"):
            return traceability.reverse_lookup(spec_path, "design", str(arguments["design"])), root
        raise ValueError("task_id, requirement, or design is required")
    if name == "prompts_validate":
        return lifecycle_core.load_prompt_definitions(root), root
    raise ValueError(f"Unknown tool: {name}")


def list_resources(repo_root: Path) -> list[dict[str, str]]:
    resources = [
        {
            "uri": "specs://active",
            "name": "Active spec inventory",
            "description": "Spec package inventory, health, and template authority.",
            "mimeType": "application/json",
        },
        {
            "uri": "governance://constitution",
            "name": "Governance constitution",
            "description": "Repository governance principles when present.",
            "mimeType": "text/markdown",
        },
        {
            "uri": "history://spec-archive-index",
            "name": "Spec archive index",
            "description": "Closed spec package archive index validation payload.",
            "mimeType": "application/json",
        },
        {
            "uri": "templates://spec-package",
            "name": "Spec package templates",
            "description": "Fallback spec package template inventory.",
            "mimeType": "application/json",
        },
    ]
    for spec in lifecycle_core.discover_spec_paths(repo_root):
        spec_id = spec.name
        resources.extend(
            [
                {
                    "uri": f"specs://{spec_id}/summary",
                    "name": f"{spec_id} summary",
                    "description": "Spec summary, task counts, artifact inventory, and health.",
                    "mimeType": "application/json",
                },
                {
                    "uri": f"specs://{spec_id}/health",
                    "name": f"{spec_id} health",
                    "description": "Spec lint health summary and diagnostics.",
                    "mimeType": "application/json",
                },
            ]
        )
    return resources


def read_resource(uri: str, repo_root: Path) -> dict[str, Any]:
    if uri == "specs://active":
        payload = lifecycle_core.scan_specs(repo_root)
        payload["resource_binding"] = resource_binding(uri, repo_root)
        return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))
    if uri == "governance://constitution":
        path = repo_root / "docs" / "governance" / "constitution.md"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        return resource_payload(uri, "text/markdown", text)
    if uri == "history://spec-archive-index":
        payload = lifecycle_core.archive_index(repo_root)
        payload["resource_binding"] = resource_binding(uri, repo_root)
        return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))
    if uri == "templates://spec-package":
        template_dir = lifecycle_core.spec_package_template_dir(repo_root)
        payload = {
            "path": str(template_dir) if template_dir else None,
            "template_authority": lifecycle_core.template_authority(repo_root),
            "templates": sorted(path.name for path in template_dir.glob("*.md")) if template_dir and template_dir.exists() else [],
        }
        payload["resource_binding"] = resource_binding(uri, repo_root)
        return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))

    spec_match = uri.removeprefix("specs://")
    if "/" in spec_match:
        spec_id, suffix = spec_match.split("/", 1)
        spec_path = resolve_spec_path(repo_root, spec_id)
        if suffix == "summary":
            payload = lifecycle_core.spec_summary(spec_path)
            payload["resource_binding"] = resource_binding(uri, repo_root)
            return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))
        if suffix == "health":
            payload = lifecycle_core.lint_spec_package(spec_path)
            assert isinstance(payload, dict)
            payload["resource_binding"] = resource_binding(uri, repo_root)
            return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))
    raise ValueError(f"Unknown resource URI: {uri}")


def resource_binding(uri: str, repo_root: Path) -> dict[str, str]:
    return {
        "uri": uri,
        "repo_root": str(repo_root.resolve()),
        "path_policy": "repo-relative",
    }


def resource_payload(uri: str, mime_type: str, text: str) -> dict[str, Any]:
    return {"contents": [{"uri": uri, "mimeType": mime_type, "text": text}]}


def list_prompts(repo_root: Path) -> list[dict[str, Any]]:
    payload = lifecycle_core.load_prompt_definitions(repo_root)
    prompts = []
    for prompt in payload.get("prompts", []):
        prompts.append(
            {
                "name": prompt["name"],
                "description": prompt.get("description", ""),
                "arguments": [
                    {
                        "name": arg["name"],
                        "description": arg.get("description", ""),
                        "required": bool(arg.get("required")),
                    }
                    for arg in prompt.get("arguments", [])
                ],
            }
        )
    return prompts


def get_prompt(name: str, arguments: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    payload = lifecycle_core.load_prompt_definitions(repo_root)
    prompts = {prompt["name"]: prompt for prompt in payload.get("prompts", [])}
    prompt = prompts.get(name)
    if not prompt:
        raise ValueError(f"Unknown prompt: {name}")
    text = "\n".join(
        [
            f"Use the spec-lifecycle-manager skill for `{name}`.",
            "",
            "Arguments:",
            json_text(arguments or {}),
            "",
            "Resources:",
            *[f"- {item}" for item in prompt.get("resources", [])],
            "",
            "Tools:",
            *[f"- {item}" for item in prompt.get("tools", [])],
            "",
            "Instructions:",
            *[f"- {item}" for item in prompt.get("instructions", [])],
            "",
            "Return format:",
            *[f"- {item}" for item in prompt.get("return_format", [])],
            "",
            f"Recovery: {prompt.get('client_support_recovery') or prompt.get('client_support_fallback', '')}",
        ]
    )
    return {
        "description": prompt.get("description", ""),
        "messages": [{"role": "user", "content": {"type": "text", "text": text}}],
    }


def handle_request(message: dict[str, Any], repo_root: Path) -> dict[str, Any] | None:
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}
    if request_id is None:
        return None
    try:
        if method == "initialize":
            return response(
                request_id,
                {
                    "protocolVersion": params.get("protocolVersion") or PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"listChanged": False},
                        "prompts": {"listChanged": False},
                    },
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                    "instructions": SERVER_INSTRUCTIONS,
                },
            )
        if method == "ping":
            return response(request_id, {})
        if method == "tools/list":
            return response(request_id, {"tools": tool_definitions()})
        if method == "tools/call":
            payload, target_root = call_tool(params.get("name", ""), params.get("arguments") or {}, repo_root)
            return response(request_id, tool_result(payload, target_root))
        if method == "resources/list":
            return response(request_id, {"resources": list_resources(repo_root)})
        if method == "resources/read":
            return response(request_id, read_resource(params.get("uri", ""), repo_root))
        if method == "prompts/list":
            return response(request_id, {"prompts": list_prompts(repo_root)})
        if method == "prompts/get":
            return response(request_id, get_prompt(params.get("name", ""), params.get("arguments") or {}, repo_root))
        return error_response(request_id, -32601, f"Method not found: {method}")
    except Exception as exc:
        return error_response(request_id, -32602, str(exc))


def serve(repo_root: Path | None = None) -> int:
    root = default_repo_root(repo_root)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            print(json.dumps(error_response(None, -32700, f"Parse error: {exc}")), flush=True)
            continue
        result = handle_request(message, root)
        if result is not None:
            print(json.dumps(result, separators=(",", ":")), flush=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    repo_root = Path(args[0]).resolve() if args else None
    return serve(repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
