#!/usr/bin/env python3
"""Minimal stdio MCP adapter for the spec lifecycle runtime.

The adapter is dependency-free. It exposes the tested spec runtime helpers as
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

import spec_runtime
import traceability_lookup


PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "spec-lifecycle-manager"
SERVER_VERSION = "0.1.0"
REPO_ROOT_PROPERTY = "Repository root. Defaults to current working directory."
WORKSPACE_ROOT_ENV_VARS = (
    "SPEC_LIFECYCLE_REPO_ROOT",
    "CODEX_REPO_ROOT",
    "CODEX_WORKSPACE_ROOT",
    "CODEX_WORKSPACE",
    "WORKSPACE_ROOT",
)
SPEC_PATH_PROPERTIES = {
    "repo_root": REPO_ROOT_PROPERTY,
    "spec_path": "Spec package path or ID.",
}
REVIEW_PACKET_TYPE_CONTRACT = spec_runtime.review_packet_type_contract()
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

    matches = [spec for spec in spec_runtime.discover_spec_paths(root) if spec.name == value]
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
            "Summarize spec lifecycle MCP mentions and explicit errors in Codex session logs.",
            {
                "repo_root": REPO_ROOT_PROPERTY,
                "sessions_root": "Directory containing Codex session JSONL files.",
                "since": "Optional lexicographic relative-path cutoff, such as 2026/06/07.",
                "limit": {"type": ["integer", "string"], "description": "Maximum matched session files and per-file items to return."},
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
        ),
        tool_schema("prompts_validate", "List and validate prompt definitions.", {"repo_root": REPO_ROOT_PROPERTY}),
    ]


def tool_schema(name: str, description: str, properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    schema_properties = {
        key: value if isinstance(value, dict) else {"type": "string", "description": value}
        for key, value in properties.items()
    }
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": schema_properties,
            "required": required or [],
            "additionalProperties": False,
        },
    }


def call_tool(name: str, arguments: dict[str, Any], default_root: Path) -> tuple[dict[str, Any], Path]:
    root = repo_root_arg(arguments, default_root)
    if name == "scan_specs":
        return spec_runtime.scan_specs(
            root,
            arguments.get("docs_root"),
            include_archived_lint=bool_arg(arguments, "include_archived_lint"),
        ), root
    if name == "active_spec_preflight":
        spec_path = spec_path_arg(arguments, default_root) if arguments.get("spec_path") or arguments.get("spec_id") else None
        return spec_runtime.active_spec_preflight(root, spec_path, arguments.get("task_id"), arguments.get("docs_root")), root
    if name == "validation_plan":
        spec_path = spec_path_arg(arguments, default_root) if arguments.get("spec_path") or arguments.get("spec_id") else None
        changed_files = arguments.get("changed_files") or []
        if not isinstance(changed_files, list):
            raise ValueError("changed_files must be an array")
        return spec_runtime.validation_plan(
            root,
            [str(item) for item in changed_files],
            spec_path,
            arguments.get("task_id"),
            arguments.get("risk_level"),
        ), root
    if name == "evidence_quality_check":
        return spec_runtime.evidence_quality_check(spec_path_arg(arguments, default_root)), root
    if name == "agent_readiness_packet":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return spec_runtime.agent_readiness_packet(spec_path_arg(arguments, default_root), str(task_id)), root
    if name == "agent_backed_tool":
        tool_name = arguments.get("tool_name")
        if not tool_name:
            raise ValueError("tool_name is required")
        return spec_runtime.agent_backed_tool(spec_path_arg(arguments, default_root), str(tool_name), arguments.get("model_class")), root
    if name == "no_active_spec_context":
        return spec_runtime.no_active_spec_context(root), root
    if name == "spec_summary":
        return spec_runtime.spec_summary(spec_path_arg(arguments, default_root)), root
    if name == "lint_spec_package":
        payload = spec_runtime.lint_spec_package(spec_path_arg(arguments, default_root))
        assert isinstance(payload, dict)
        return payload, root
    if name == "lint_doc":
        path = path_arg(arguments, "path", default_root)
        diagnostics = spec_runtime.lint_doc(path, arguments.get("artifact_type"))
        return {"path": str(path), "diagnostics": diagnostics, "summary": spec_runtime.diagnostic_summary(diagnostics)}, root
    if name == "next_task":
        return spec_runtime.next_task(spec_path_arg(arguments, default_root)), root
    if name == "list_tasks":
        include_subtasks = arguments.get("include_subtasks")
        include = True if include_subtasks is None else bool_arg(arguments, "include_subtasks")
        return spec_runtime.task_list(spec_path_arg(arguments, default_root), include_subtasks=include, status=arguments.get("status")), root
    if name == "task_details":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return spec_runtime.task_details(spec_path_arg(arguments, default_root), str(task_id)), root
    if name == "task_state_audit":
        task_id = arguments.get("task_id")
        return spec_runtime.task_state_audit(spec_path_arg(arguments, default_root), str(task_id) if task_id else None), root
    if name == "set_task_state":
        task_id = arguments.get("task_id")
        state = arguments.get("state")
        evidence = arguments.get("evidence")
        if not task_id or not state or evidence is None:
            raise ValueError("task_id, state, and evidence are required")
        dry_run_value = arguments.get("dry_run")
        dry_run = True if dry_run_value is None else bool_arg(arguments, "dry_run")
        return spec_runtime.set_task_state(
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
        return spec_runtime.closure_check(spec_path_arg(arguments, default_root)), root
    if name == "archive_index":
        return spec_runtime.archive_index(root), root
    if name == "resolve_spec_reference":
        reference = arguments.get("reference")
        if not reference:
            raise ValueError("reference is required")
        return spec_runtime.resolve_spec_reference(root, str(reference), arguments.get("docs_root")), root
    if name == "mcp_audit":
        sessions_root = arguments.get("sessions_root")
        if not sessions_root:
            raise ValueError("sessions_root is required")
        limit_value = arguments.get("limit", 200)
        try:
            limit = int(limit_value)
        except (TypeError, ValueError):
            raise ValueError("limit must be an integer")
        return spec_runtime.mcp_audit(root, Path(str(sessions_root)), arguments.get("since"), limit), root
    if name == "reconcile_spec":
        return spec_runtime.reconcile_spec(spec_path_arg(arguments, default_root)), root
    if name == "promotion_plan":
        return spec_runtime.promotion_plan(spec_path_arg(arguments, default_root)), root
    if name == "review_packet":
        return spec_runtime.generate_review_packet(
            spec_path_arg(arguments, default_root),
            arguments.get("review_type") or "design_requirements_trace",
            arguments.get("model_class"),
        ), root
    if name == "task_context":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return traceability_lookup.task_lookup(spec_path_arg(arguments, default_root), str(task_id)), root
    if name == "traceability_lookup":
        spec_path = spec_path_arg(arguments, default_root)
        if arguments.get("task_id"):
            return traceability_lookup.task_lookup(spec_path, str(arguments["task_id"])), root
        if arguments.get("requirement"):
            return traceability_lookup.reverse_lookup(spec_path, "requirement", str(arguments["requirement"])), root
        if arguments.get("design"):
            return traceability_lookup.reverse_lookup(spec_path, "design", str(arguments["design"])), root
        raise ValueError("task_id, requirement, or design is required")
    if name == "prompts_validate":
        return spec_runtime.load_prompt_definitions(root), root
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
    for spec in spec_runtime.discover_spec_paths(repo_root):
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
        payload = spec_runtime.scan_specs(repo_root)
        payload["resource_binding"] = resource_binding(uri, repo_root)
        return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))
    if uri == "governance://constitution":
        path = repo_root / "docs" / "governance" / "constitution.md"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        return resource_payload(uri, "text/markdown", text)
    if uri == "history://spec-archive-index":
        payload = spec_runtime.archive_index(repo_root)
        payload["resource_binding"] = resource_binding(uri, repo_root)
        return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))
    if uri == "templates://spec-package":
        template_dir = spec_runtime.spec_package_template_dir(repo_root)
        payload = {
            "path": str(template_dir) if template_dir else None,
            "template_authority": spec_runtime.template_authority(repo_root),
            "templates": sorted(path.name for path in template_dir.glob("*.md")) if template_dir and template_dir.exists() else [],
        }
        payload["resource_binding"] = resource_binding(uri, repo_root)
        return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))

    spec_match = uri.removeprefix("specs://")
    if "/" in spec_match:
        spec_id, suffix = spec_match.split("/", 1)
        spec_path = resolve_spec_path(repo_root, spec_id)
        if suffix == "summary":
            payload = spec_runtime.spec_summary(spec_path)
            payload["resource_binding"] = resource_binding(uri, repo_root)
            return resource_payload(uri, "application/json", json_text(normalize_mcp_payload(payload, repo_root)))
        if suffix == "health":
            payload = spec_runtime.lint_spec_package(spec_path)
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
    payload = spec_runtime.load_prompt_definitions(repo_root)
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
    payload = spec_runtime.load_prompt_definitions(repo_root)
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
