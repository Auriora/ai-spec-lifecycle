#!/usr/bin/env python3
"""Advisory Codex PostToolUse hook for spec lifecycle checks."""

from __future__ import annotations

import json
import os
import re
import hashlib
import subprocess
import sys
import time
from json import JSONDecodeError
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SPEC_RUNTIME = SCRIPT_DIR / "spec_runtime.py"
DEFAULT_LOG_PATH = Path.home() / ".codex" / "hooks" / "spec_lifecycle_hook.log.jsonl"
# Codex emits write_file/create_file (and apply_patch, handled separately); Claude Code
# emits Write/Edit/MultiEdit/NotebookEdit. Both runtimes share this hook, so recognize
# every write-style tool name or the hook silently skips one runtime's edits.
WRITE_STYLE_TOOL_NAMES = {
    "write_file",
    "create_file",
    "Write",
    "Edit",
    "MultiEdit",
    "NotebookEdit",
}
WRITE_STYLE_PATH_KEYS = ("path", "file_path", "filepath", "filename", "target_file", "notebook_path")
HOOK_TIMEOUT_SECONDS = 5
MAX_DIAGNOSTICS = 6
DEFAULT_DEBOUNCE_SECONDS = 45


def read_payload() -> dict[str, Any] | None:
    raw = sys.stdin.read()
    if not raw.strip():
        return None
    try:
        payload = json.loads(raw)
    except JSONDecodeError:
        append_log({"status": "skipped_invalid_json", "raw_stdin_preview": raw[:500]})
        return None
    if not isinstance(payload, dict):
        append_log({"status": "skipped_non_object_payload", "payload_type": type(payload).__name__})
        return None
    return payload


def append_log(record: dict[str, Any]) -> None:
    configured = os.environ.get("SPEC_LIFECYCLE_HOOK_LOG")
    path = Path(configured).expanduser() if configured else DEFAULT_LOG_PATH
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    except OSError:
        return


def debounce_cache_path() -> Path:
    configured = os.environ.get("SPEC_LIFECYCLE_HOOK_DEBOUNCE_PATH")
    if configured:
        return Path(configured).expanduser()
    log_path = Path(os.environ.get("SPEC_LIFECYCLE_HOOK_LOG", str(DEFAULT_LOG_PATH))).expanduser()
    return log_path.with_name(f"{log_path.name}.debounce.json")


def debounce_seconds() -> float:
    raw = os.environ.get("SPEC_LIFECYCLE_HOOK_DEBOUNCE_SECONDS", str(DEFAULT_DEBOUNCE_SECONDS))
    try:
        return max(0.0, float(raw))
    except ValueError:
        return float(DEFAULT_DEBOUNCE_SECONDS)


def read_debounce_cache() -> dict[str, float]:
    try:
        data = json.loads(debounce_cache_path().read_text(encoding="utf-8"))
    except (JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    cache: dict[str, float] = {}
    for key, value in data.items():
        if isinstance(key, str) and isinstance(value, (int, float)):
            cache[key] = float(value)
    return cache


def write_debounce_cache(cache: dict[str, float], now: float, window_seconds: float) -> None:
    prune_before = now - max(window_seconds * 8, 300)
    pruned = {key: timestamp for key, timestamp in cache.items() if timestamp >= prune_before}
    path = debounce_cache_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(pruned, sort_keys=True), encoding="utf-8")
    except OSError:
        return


def find_repo_root(cwd: str) -> Path | None:
    if not cwd:
        return None
    start = Path(cwd).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start if start.exists() else None


def decoded_tool_response_output(tool_response: Any) -> str:
    if isinstance(tool_response, dict):
        output = tool_response.get("output", "")
        return output if isinstance(output, str) else ""
    if not isinstance(tool_response, str):
        return ""
    text = tool_response.strip()
    if not text:
        return ""
    try:
        decoded = json.loads(text)
    except JSONDecodeError:
        return tool_response
    if isinstance(decoded, dict) and isinstance(decoded.get("output"), str):
        return decoded["output"]
    return tool_response


def extract_apply_patch_paths(output: str) -> list[str]:
    paths: list[str] = []
    capture = False
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if "Updated the following files:" in line or "Created the following files:" in line:
            capture = True
            continue
        if not capture or not line:
            continue
        match = re.match(r"^[AMDR]\s+(.+)$", line)
        if match:
            paths.append(match.group(1).strip())
    return paths


def extract_apply_patch_input_paths(payload: dict[str, Any]) -> list[str]:
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    if tool_name != "apply_patch" or not isinstance(tool_input, dict):
        return []
    patch = tool_input.get("patch")
    if not isinstance(patch, str):
        return []
    paths: list[str] = []
    for line in patch.splitlines():
        match = re.match(r"^\*\*\* (?:Add|Update|Delete) File:\s+(.+)$", line.strip())
        if match:
            paths.append(match.group(1).strip())
    return paths


def extract_write_tool_paths(payload: dict[str, Any]) -> list[str]:
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    if tool_name not in WRITE_STYLE_TOOL_NAMES or not isinstance(tool_input, dict):
        return []
    paths: list[str] = []
    for key in WRITE_STYLE_PATH_KEYS:
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            paths.append(value.strip())
    return paths


def extract_changed_files(payload: dict[str, Any], repo_root: Path) -> list[str]:
    paths = extract_apply_patch_paths(decoded_tool_response_output(payload.get("tool_response")))
    paths.extend(extract_apply_patch_input_paths(payload))
    paths.extend(extract_write_tool_paths(payload))
    normalized: list[str] = []
    for value in paths:
        path = Path(value)
        if path.is_absolute():
            try:
                relative = path.resolve().relative_to(repo_root)
            except ValueError:
                continue
        else:
            relative = path
        text = relative.as_posix()
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def is_spec_file(path: str) -> bool:
    relative = Path(path)
    parts = relative.parts
    return relative.suffix == ".md" and parts and parts[0] == "docs" and "specs" in parts and parts.index("specs") + 1 < len(parts)


def spec_scope_for_file(path: str) -> str | None:
    relative = Path(path)
    parts = relative.parts
    if not parts or "specs" not in parts:
        return None
    index = parts.index("specs")
    if index + 1 >= len(parts):
        return None
    return Path(*parts[: index + 2]).as_posix()


def file_state_fingerprint(repo_root: Path, changed_files: list[str]) -> str:
    digest = hashlib.sha256()
    for changed in sorted(dict.fromkeys(changed_files)):
        digest.update(changed.encode("utf-8"))
        path = (repo_root / changed).resolve()
        try:
            data = path.read_bytes()
        except OSError:
            digest.update(b"\0missing")
        else:
            digest.update(b"\0")
            digest.update(hashlib.sha256(data).hexdigest().encode("ascii"))
    return digest.hexdigest()


def debounce_keys(repo_root: Path, hook_name: str, changed_files: list[str]) -> list[str]:
    fingerprint = file_state_fingerprint(repo_root, changed_files)
    keys: list[str] = []
    for changed in changed_files:
        scope = spec_scope_for_file(changed) if is_spec_file(changed) else None
        if scope is None:
            continue
        key = f"{repo_root}|{hook_name}|{scope}|{fingerprint}"
        if key not in keys:
            keys.append(key)
    return keys


def recently_checked(keys: list[str], cache: dict[str, float], now: float, window_seconds: float) -> bool:
    if not keys or window_seconds <= 0:
        return False
    return all(now - cache.get(key, 0.0) < window_seconds for key in keys)


def is_task_file(path: str) -> bool:
    return is_spec_file(path) and Path(path).name == "tasks.md"


def is_template_file(path: str) -> bool:
    if Path(path).suffix != ".md":
        return False
    return path.startswith("docs/templates/") or path.startswith("skills/spec-lifecycle-manager/references/")


def hook_commands(changed_files: list[str]) -> list[tuple[str, list[str]]]:
    commands: list[tuple[str, list[str]]] = []
    spec_files = [path for path in changed_files if is_spec_file(path)]
    task_files = [path for path in changed_files if is_task_file(path)]
    verification_files = [path for path in spec_files if Path(path).name == "verification.md"]
    template_files = [path for path in changed_files if is_template_file(path)]
    if spec_files:
        commands.append(("spec-file-changed", spec_files))
    if task_files:
        commands.append(("task-checkbox-changed", task_files))
    if verification_files:
        commands.append(("verification-updated", verification_files))
    if template_files:
        commands.append(("template-changed", template_files))
    return commands


def run_runtime_hook(repo_root: Path, hook_name: str, changed_files: list[str]) -> dict[str, Any]:
    command = [
        sys.executable,
        str(SPEC_RUNTIME),
        "hook",
        hook_name,
        "--repo-root",
        str(repo_root),
        "--changed-files",
        *changed_files,
        "--severity-profile",
        "advisory",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=HOOK_TIMEOUT_SECONDS)
    if completed.stdout.strip():
        try:
            return json.loads(completed.stdout)
        except JSONDecodeError:
            pass
    return {
        "hook": hook_name,
        "blocked": False,
        "diagnostics": [
            {
                "severity": "warn",
                "code": "CODEX_SPEC_HOOK_RUNTIME_OUTPUT",
                "message": (completed.stderr or completed.stdout or "Spec lifecycle hook produced invalid output.").strip()[:500],
            }
        ],
        "summary": {"error": 0, "warn": 1, "info": 0},
    }


def diagnostic_line(item: dict[str, Any]) -> str:
    severity = str(item.get("severity", "info")).upper()
    code = str(item.get("code", "SPEC_LIFECYCLE_DIAGNOSTIC"))
    message = str(item.get("message", "")).strip()
    path = str(item.get("path", "")).strip()
    location = f" in {path}" if path else ""
    return f"{severity} {code}{location}: {message}".strip()


def authoring_context_lines(result: dict[str, Any]) -> list[str]:
    payload = result.get("authoring_context")
    if not isinstance(payload, dict):
        return []
    contexts = payload.get("contexts")
    if not isinstance(contexts, list):
        return []
    lines: list[str] = []
    for context in contexts:
        if not isinstance(context, dict):
            continue
        spec_path = str(context.get("spec_path", "")).strip()
        mode = str(context.get("mode", "authoring")).strip()
        prefix = f"{spec_path}: " if spec_path else ""
        next_step = context.get("next_authoring_step")
        if isinstance(next_step, dict) and next_step.get("artifact"):
            tools = next_step.get("recommended_tools")
            tool_text = ""
            if isinstance(tools, list) and tools:
                tool_text = f" Use: {', '.join(str(tool) for tool in tools[:3])}."
            lines.append(f"{prefix}{mode}. Next spec artifact: {next_step['artifact']}.{tool_text}")
        downstream = context.get("downstream_review")
        if isinstance(downstream, list) and downstream:
            artifacts = [
                str(item.get("artifact"))
                for item in downstream
                if isinstance(item, dict) and item.get("artifact")
            ]
            if artifacts:
                lines.append(f"{prefix}{mode}. Review existing downstream artifact(s): {', '.join(artifacts)}.")
        missing = context.get("missing_prerequisites")
        if isinstance(missing, list) and missing:
            artifacts = [
                f"{item.get('artifact')} before {item.get('for_artifact')}"
                for item in missing
                if isinstance(item, dict) and item.get("artifact") and item.get("for_artifact")
            ]
            if artifacts:
                lines.append(f"{prefix}{mode}. Missing prerequisite: {', '.join(artifacts)}.")
    return lines


def build_context(results: list[dict[str, Any]]) -> str:
    guidance: list[str] = []
    diagnostics: list[dict[str, Any]] = []
    for result in results:
        guidance.extend(authoring_context_lines(result))
        diagnostics.extend(item for item in result.get("diagnostics", []) if isinstance(item, dict))
    if guidance:
        diagnostics = [
            item
            for item in diagnostics
            if not str(item.get("code", "")).startswith("SPEC_AUTHORING_")
        ]
    if not diagnostics and not guidance:
        return ""
    lines = guidance[:MAX_DIAGNOSTICS]
    remaining_guidance = len(guidance) - len(lines)
    remaining_slots = max(0, MAX_DIAGNOSTICS - len(lines))
    diagnostic_lines = [diagnostic_line(item) for item in diagnostics[:remaining_slots]]
    lines.extend(diagnostic_lines)
    remaining = remaining_guidance + max(0, len(diagnostics) - len(diagnostic_lines))
    suffix = f" {remaining} more finding(s) omitted." if remaining > 0 else ""
    return "Spec lifecycle advisory guidance. " + " ".join(lines) + suffix


def emit_context(context: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": context,
                }
            }
        )
    )


def main() -> int:
    payload = read_payload()
    if payload is None:
        return 0
    repo_root = find_repo_root(str(payload.get("cwd") or ""))
    if repo_root is None:
        append_log({"status": "skipped_missing_repo_root", "payload_keys": sorted(payload.keys())})
        return 0
    changed_files = extract_changed_files(payload, repo_root)
    commands = hook_commands(changed_files)
    if not commands:
        append_log({"status": "skipped_no_spec_lifecycle_targets", "repo_root": str(repo_root), "changed_files": changed_files})
        return 0
    results: list[dict[str, Any]] = []
    now = time.time()
    window_seconds = debounce_seconds()
    cache = read_debounce_cache() if window_seconds > 0 else {}
    skipped_debounced: list[dict[str, Any]] = []
    for hook_name, files in commands:
        keys = debounce_keys(repo_root, hook_name, files)
        if recently_checked(keys, cache, now, window_seconds):
            skipped_debounced.append({"hook": hook_name, "changed_files": files})
            continue
        try:
            results.append(run_runtime_hook(repo_root, hook_name, files))
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append(
                {
                    "hook": hook_name,
                    "blocked": False,
                    "diagnostics": [
                        {
                            "severity": "warn",
                            "code": "CODEX_SPEC_HOOK_RUNTIME_UNAVAILABLE",
                            "message": f"Spec lifecycle hook could not run: {exc}",
                        }
                    ],
                    "summary": {"error": 0, "warn": 1, "info": 0},
                }
            )
        for key in keys:
            cache[key] = now
    if window_seconds > 0:
        write_debounce_cache(cache, now, window_seconds)
    context = build_context(results)
    status = "skipped_debounced" if skipped_debounced and not results else "checked"
    append_log(
        {
            "status": status,
            "repo_root": str(repo_root),
            "changed_files": changed_files,
            "results": results,
            "skipped_debounced": skipped_debounced,
            "debounce_seconds": window_seconds,
        }
    )
    if context:
        emit_context(context)
    return 0


def run_advisory_hook(main_func=main) -> int:
    try:
        return main_func()
    except Exception as exc:  # noqa: BLE001 - Codex advisory hooks must never break tool flow.
        append_log(
            {
                "status": "hook_failed",
                "error_type": type(exc).__name__,
                "message": str(exc)[:500],
            }
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(run_advisory_hook())
