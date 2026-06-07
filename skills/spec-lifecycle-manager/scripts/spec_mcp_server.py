#!/usr/bin/env python3
"""Minimal stdio MCP adapter for the spec lifecycle runtime.

The adapter is dependency-free and intentionally read-only. It exposes the
tested spec runtime helpers as MCP resources, tools, and prompts without
duplicating lifecycle policy or parsing logic.
"""

from __future__ import annotations

import json
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
SPEC_PATH_PROPERTIES = {
    "repo_root": REPO_ROOT_PROPERTY,
    "spec_path": "Spec package path or ID.",
}


def find_repo_root(path: Path | None = None) -> Path:
    start = (path or Path.cwd()).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start


def json_text(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def text_content(payload: Any) -> list[dict[str, str]]:
    return [{"type": "text", "text": json_text(payload)}]


def tool_result(payload: Any) -> dict[str, Any]:
    return {
        "content": text_content(payload),
        "structuredContent": payload if isinstance(payload, dict) else {"result": payload},
        "isError": False,
    }


def error_response(request_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


def response(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def repo_root_arg(arguments: dict[str, Any]) -> Path:
    return Path(arguments.get("repo_root") or Path.cwd()).resolve()


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


def spec_path_arg(arguments: dict[str, Any]) -> Path:
    value = arguments.get("spec_path") or arguments.get("spec_id")
    if not value:
        raise ValueError("spec_path or spec_id is required")
    return resolve_spec_path(repo_root_arg(arguments), str(value))


def path_arg(arguments: dict[str, Any], name: str) -> Path:
    value = arguments.get(name)
    if not value:
        raise ValueError(f"{name} is required")
    path = Path(value)
    if path.exists():
        return path.resolve()
    return (repo_root_arg(arguments) / str(value)).resolve()


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
                "tool_name": "Agent-backed tool name.",
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
        tool_schema("closure_check", "Check closure readiness and blockers.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema("archive_index", "Validate spec archive index and closure-log consistency.", {"repo_root": REPO_ROOT_PROPERTY}),
        tool_schema("reconcile_spec", "Generate a classified reconciliation report.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema("promotion_plan", "Generate durable documentation promotion targets.", SPEC_PATH_PROPERTIES, ["spec_path"]),
        tool_schema(
            "review_packet",
            "Generate a bounded read-only review packet.",
            {**SPEC_PATH_PROPERTIES, "review_type": "Review packet type.", "model_class": "Optional model class."},
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


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "scan_specs":
        return spec_runtime.scan_specs(
            repo_root_arg(arguments),
            arguments.get("docs_root"),
            include_archived_lint=bool_arg(arguments, "include_archived_lint"),
        )
    if name == "active_spec_preflight":
        spec_path = spec_path_arg(arguments) if arguments.get("spec_path") or arguments.get("spec_id") else None
        return spec_runtime.active_spec_preflight(repo_root_arg(arguments), spec_path, arguments.get("task_id"), arguments.get("docs_root"))
    if name == "agent_readiness_packet":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return spec_runtime.agent_readiness_packet(spec_path_arg(arguments), str(task_id))
    if name == "agent_backed_tool":
        tool_name = arguments.get("tool_name")
        if not tool_name:
            raise ValueError("tool_name is required")
        return spec_runtime.agent_backed_tool(spec_path_arg(arguments), str(tool_name), arguments.get("model_class"))
    if name == "no_active_spec_context":
        return spec_runtime.no_active_spec_context(repo_root_arg(arguments))
    if name == "spec_summary":
        return spec_runtime.spec_summary(spec_path_arg(arguments))
    if name == "lint_spec_package":
        payload = spec_runtime.lint_spec_package(spec_path_arg(arguments))
        assert isinstance(payload, dict)
        return payload
    if name == "lint_doc":
        path = path_arg(arguments, "path")
        diagnostics = spec_runtime.lint_doc(path, arguments.get("artifact_type"))
        return {"path": str(path), "diagnostics": diagnostics, "summary": spec_runtime.diagnostic_summary(diagnostics)}
    if name == "next_task":
        return spec_runtime.next_task(spec_path_arg(arguments))
    if name == "closure_check":
        return spec_runtime.closure_check(spec_path_arg(arguments))
    if name == "archive_index":
        return spec_runtime.archive_index(repo_root_arg(arguments))
    if name == "reconcile_spec":
        return spec_runtime.reconcile_spec(spec_path_arg(arguments))
    if name == "promotion_plan":
        return spec_runtime.promotion_plan(spec_path_arg(arguments))
    if name == "review_packet":
        return spec_runtime.generate_review_packet(
            spec_path_arg(arguments),
            arguments.get("review_type") or "design_requirements_trace",
            arguments.get("model_class"),
        )
    if name == "task_context":
        task_id = arguments.get("task_id")
        if not task_id:
            raise ValueError("task_id is required")
        return traceability_lookup.task_lookup(spec_path_arg(arguments), str(task_id))
    if name == "traceability_lookup":
        spec_path = spec_path_arg(arguments)
        if arguments.get("task_id"):
            return traceability_lookup.task_lookup(spec_path, str(arguments["task_id"]))
        if arguments.get("requirement"):
            return traceability_lookup.reverse_lookup(spec_path, "requirement", str(arguments["requirement"]))
        if arguments.get("design"):
            return traceability_lookup.reverse_lookup(spec_path, "design", str(arguments["design"]))
        raise ValueError("task_id, requirement, or design is required")
    if name == "prompts_validate":
        return spec_runtime.load_prompt_definitions(repo_root_arg(arguments))
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
        return resource_payload(uri, "application/json", json_text(payload))
    if uri == "governance://constitution":
        path = repo_root / "docs" / "governance" / "constitution.md"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        return resource_payload(uri, "text/markdown", text)
    if uri == "history://spec-archive-index":
        payload = spec_runtime.archive_index(repo_root)
        return resource_payload(uri, "application/json", json_text(payload))
    if uri == "templates://spec-package":
        template_dir = repo_root / "skills" / "spec-lifecycle-manager" / "references" / "spec-package"
        payload = {"path": str(template_dir), "templates": sorted(path.name for path in template_dir.glob("*.md")) if template_dir.exists() else []}
        return resource_payload(uri, "application/json", json_text(payload))

    spec_match = uri.removeprefix("specs://")
    if "/" in spec_match:
        spec_id, suffix = spec_match.split("/", 1)
        spec_path = resolve_spec_path(repo_root, spec_id)
        if suffix == "summary":
            return resource_payload(uri, "application/json", json_text(spec_runtime.spec_summary(spec_path)))
        if suffix == "health":
            payload = spec_runtime.lint_spec_package(spec_path)
            assert isinstance(payload, dict)
            return resource_payload(uri, "application/json", json_text(payload))
    raise ValueError(f"Unknown resource URI: {uri}")


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
            payload = call_tool(params.get("name", ""), params.get("arguments") or {})
            return response(request_id, tool_result(payload))
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
    root = find_repo_root(repo_root)
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
