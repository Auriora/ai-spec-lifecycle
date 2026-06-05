#!/usr/bin/env python3
"""Deterministic spec lifecycle runtime helpers.

The helpers in this module are dependency-free and CLI-first. They provide the
payloads that a future MCP server can expose as resources and tools.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import traceability_lookup


CORE_ARTIFACTS = ["requirements.md", "design.md", "tasks.md"]
OPTIONAL_ARTIFACTS = [
    "change-impact.md",
    "verification.md",
    "research.md",
    "quickstart.md",
    "open-decisions.md",
    "traceability.md",
]
SPEC_ARTIFACTS = CORE_ARTIFACTS + OPTIONAL_ARTIFACTS
REQUIRED_PROMPTS = ["reconcile-spec", "choose-next-task", "task-context", "lint-spec"]
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
TASK_RE = re.compile(r"\bT\d{3}(?:\.\d+)?\b")
REQ_RE = re.compile(r"\bRequirement\s+\d+[A-Z]?\b", re.IGNORECASE)
TASK_LINE_RE = re.compile(r"^\s*-\s+\[([ xX])\]\s+(T\d{3}(?:\.\d+)?)\b(.*)$")


@dataclass
class Task:
    task_id: str
    title: str
    complete: bool
    block: str
    depends_on: list[str]
    files: list[str]
    acceptance: str
    evidence: str
    line: int

    @property
    def verified(self) -> bool:
        evidence = self.evidence.strip().lower()
        return self.complete and bool(evidence) and evidence not in {"pending", "pending."}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def headings(text: str) -> set[str]:
    return {match.group(2).strip().lower() for match in HEADING_RE.finditer(text)}


def diagnostic(
    severity: str,
    code: str,
    path: Path,
    message: str,
    line: int | None = None,
    lifecycle_gate: str = "authoring",
    artifact_type: str | None = None,
    waivable: bool = True,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "severity": severity,
        "code": code,
        "path": str(path),
        "message": message,
        "lifecycle_gate": lifecycle_gate,
        "waivable": waivable,
    }
    if line is not None:
        item["line"] = line
    if artifact_type:
        item["artifact_type"] = artifact_type
    return item


def repo_root_for(path: Path) -> Path:
    for candidate in [path, *path.parents]:
        if (candidate / ".git").exists():
            return candidate
    return path.resolve()


def artifact_inventory(spec_path: Path) -> dict[str, str]:
    inventory: dict[str, str] = {}
    for name in SPEC_ARTIFACTS + ["spec.md", "plan.md", "validation-evidence.md"]:
        inventory[name] = "present" if (spec_path / name).exists() else "missing"
    return inventory


def spec_format(inventory: dict[str, str]) -> str:
    has_current = all(inventory.get(name) == "present" for name in CORE_ARTIFACTS)
    has_old = inventory.get("spec.md") == "present" or inventory.get("plan.md") == "present"
    if has_current:
        return "current"
    if has_old:
        return "old-format"
    return "partial"


def spec_status(spec_path: Path) -> str:
    for name in ["requirements.md", "tasks.md", "spec.md", "plan.md"]:
        path = spec_path / name
        if path.exists():
            return parse_frontmatter(read_text(path)).get("status", "unknown")
    return "unknown"


def docs_roots(repo_root: Path, docs_root: str | None = None) -> list[Path]:
    if docs_root:
        return [(repo_root / docs_root).resolve()]
    roots = []
    direct = repo_root / "docs"
    if direct.exists():
        roots.append(direct.resolve())
    return roots


def discover_spec_paths(repo_root: Path, docs_root: str | None = None) -> list[Path]:
    paths: set[Path] = set()
    for root in docs_roots(repo_root, docs_root):
        if (root / "specs").exists():
            for child in (root / "specs").iterdir():
                if child.is_dir():
                    paths.add(child.resolve())
        for specs_dir in root.glob("*/specs"):
            if specs_dir.is_dir():
                for child in specs_dir.iterdir():
                    if child.is_dir():
                        paths.add(child.resolve())
    return sorted(paths)


def template_authority(repo_root: Path) -> dict[str, Any]:
    repo_templates = repo_root / "docs" / "templates"
    skill_templates = repo_root / "skills" / "spec-lifecycle-manager" / "references" / "spec-package"
    if repo_templates.exists():
        return {
            "authority": "repository",
            "path": str(repo_templates),
            "decision": "Use repository templates as authoritative.",
        }
    if skill_templates.exists():
        return {
            "authority": "skill-fallback",
            "path": str(skill_templates),
            "decision": "Use skill fallback templates because no repository templates were found.",
        }
    return {
        "authority": "missing",
        "path": None,
        "decision": "No repository or skill fallback templates were found.",
    }


def scan_specs(repo_root: Path, docs_root: str | None = None) -> dict[str, Any]:
    root = repo_root.resolve()
    specs = []
    for spec_path in discover_spec_paths(root, docs_root):
        inventory = artifact_inventory(spec_path)
        specs.append(
            {
                "spec_id": spec_path.name,
                "path": str(spec_path),
                "status": spec_status(spec_path),
                "format": spec_format(inventory),
                "artifacts": inventory,
                "health": health_summary(spec_path),
            }
        )
    return {
        "repo_root": str(root),
        "docs_root": docs_root or "docs",
        "resources": {
            "active": "specs://active",
            "summary_pattern": "specs://{spec_id}/summary",
            "templates": "templates://spec-package/{artifact_type}",
        },
        "template_authority": template_authority(root),
        "specs": specs,
    }


def health_summary(spec_path: Path) -> dict[str, Any]:
    diagnostics = lint_spec_package(spec_path, include_summary=False)
    severity_rank = {"error": 3, "warn": 2, "info": 1}
    max_severity = "pass"
    for item in diagnostics:
        if severity_rank.get(item["severity"], 0) > severity_rank.get(max_severity, 0):
            max_severity = item["severity"]
    return {"severity": max_severity, "diagnostic_count": len(diagnostics)}


def spec_summary(spec_path: Path) -> dict[str, Any]:
    inventory = artifact_inventory(spec_path)
    tasks = parse_tasks(spec_path / "tasks.md") if (spec_path / "tasks.md").exists() else []
    by_id = {task.task_id: task for task in tasks}
    open_decisions = parse_open_decisions(spec_path / "open-decisions.md")
    durable_refs = durable_source_refs(spec_path / "requirements.md")
    return {
        "spec_id": spec_path.name,
        "path": str(spec_path.resolve()),
        "status": spec_status(spec_path),
        "format": spec_format(inventory),
        "artifacts": inventory,
        "tasks": {
            "total": len(tasks),
            "complete": len([task for task in tasks if task.complete]),
            "verified": len([task for task in tasks if task_verified(task, by_id)]),
            "incomplete": len([task for task in tasks if not task.complete]),
        },
        "open_decisions": open_decisions,
        "durable_source_references": durable_refs,
        "health": health_summary(spec_path),
    }


def durable_source_refs(requirements_path: Path) -> list[str]:
    if not requirements_path.exists():
        return []
    text = read_text(requirements_path)
    match = re.search(r"^## Durable Source Baseline\s*(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    refs = []
    for line in match.group(1).splitlines():
        if line.strip().startswith("- "):
            refs.append(line.strip()[2:])
    return refs


def parse_open_decisions(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    decisions = []
    for line in read_text(path).splitlines():
        if line.strip().startswith("| D"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells:
                decisions.append({"id": cells[0], "raw": line.strip()})
    return decisions


def lint_frontmatter(path: Path, text: str, artifact_type: str) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    data = parse_frontmatter(text)
    required = ["title", "doc_type", "status", "owner", "last_reviewed"]
    if artifact_type in {"requirements", "design", "tasks", "traceability", "verification", "change-impact"}:
        required.append("artifact_type")
    for key in required:
        if not data.get(key):
            diagnostics.append(
                diagnostic(
                    "error",
                    "FRONTMATTER_FIELD_MISSING",
                    path,
                    f"Missing frontmatter field: {key}",
                    artifact_type=artifact_type,
                )
            )
    return diagnostics


def lint_doc(path: Path, artifact_type: str | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return [diagnostic("error", "DOC_MISSING", path, "Document does not exist.", waivable=False)]
    text = read_text(path)
    artifact = artifact_type or path.stem
    diagnostics = lint_frontmatter(path, text, artifact)
    doc_headings = headings(text)

    def require_heading(title: str, code: str) -> None:
        if title.lower() not in doc_headings:
            diagnostics.append(diagnostic("warn", code, path, f"Missing section: {title}", artifact_type=artifact))

    if artifact == "requirements":
        for title, code in [
            ("Durable Source Baseline", "REQUIREMENTS_DURABLE_BASELINE_MISSING"),
            ("Goals", "REQUIREMENTS_GOALS_MISSING"),
            ("Non-Goals", "REQUIREMENTS_NON_GOALS_MISSING"),
            ("Requirements", "REQUIREMENTS_SECTION_MISSING"),
            ("Correctness Properties", "REQUIREMENTS_PROPERTIES_MISSING"),
            ("Success Criteria", "REQUIREMENTS_SUCCESS_MISSING"),
        ]:
            require_heading(title, code)
        if not re.search(r"^###\s+Requirement\s+\d+", text, re.MULTILINE):
            diagnostics.append(
                diagnostic("error", "REQUIREMENT_ID_MISSING", path, "No Requirement N sections found.", artifact_type=artifact)
            )
        if "GIVEN" not in text and "WHERE" not in text and "IF" not in text:
            diagnostics.append(
                diagnostic("warn", "REQUIREMENTS_EARS_MISSING", path, "No EARS-style acceptance criteria found.", artifact_type=artifact)
            )
    elif artifact == "design":
        for title, code in [
            ("Overview", "DESIGN_OVERVIEW_MISSING"),
            ("High-Level Design", "DESIGN_HIGH_LEVEL_MISSING"),
            ("Low-Level Design", "DESIGN_LOW_LEVEL_MISSING"),
            ("Operational Considerations", "DESIGN_OPERATIONAL_MISSING"),
            ("Open Questions", "DESIGN_OPEN_QUESTIONS_MISSING"),
        ]:
            require_heading(title, code)
    elif artifact == "tasks":
        diagnostics.extend(lint_tasks_doc(path, text))
    elif artifact == "traceability":
        for title, code in [
            ("Task To Context Matrix", "TRACEABILITY_TASK_MATRIX_MISSING"),
            ("Requirement To Delivery Matrix", "TRACEABILITY_REQUIREMENT_MATRIX_MISSING"),
            ("Design To Implementation Matrix", "TRACEABILITY_DESIGN_MATRIX_MISSING"),
            ("Open Decision Impact", "TRACEABILITY_DECISION_MATRIX_MISSING"),
        ]:
            require_heading(title, code)
    elif artifact == "verification":
        for title, code in [
            ("Quality Gates", "VERIFICATION_GATES_MISSING"),
            ("Evidence Log", "VERIFICATION_EVIDENCE_LOG_MISSING"),
            ("Residual Risks", "VERIFICATION_RISKS_MISSING"),
        ]:
            require_heading(title, code)
    elif artifact == "change-impact":
        for title, code in [
            ("Durable Source Mapping", "CHANGE_IMPACT_SOURCE_MAPPING_MISSING"),
            ("Proposed Changes", "CHANGE_IMPACT_PROPOSED_CHANGES_MISSING"),
            ("Promotion Targets", "CHANGE_IMPACT_PROMOTION_TARGETS_MISSING"),
        ]:
            require_heading(title, code)
    return apply_waivers(text, diagnostics)


def apply_waivers(text: str, diagnostics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    waivers = parse_waivers(text)
    if not waivers:
        return diagnostics
    results: list[dict[str, Any]] = []
    for item in diagnostics:
        waiver = waivers.get(item["code"])
        if waiver and item.get("waivable", True):
            waived = dict(item)
            waived["severity"] = "info"
            waived["waived"] = True
            waived["waiver_reason"] = waiver
            results.append(waived)
        else:
            results.append(item)
    return results


def parse_waivers(text: str) -> dict[str, str]:
    waivers: dict[str, str] = {}
    for line in text.splitlines():
        match = re.search(r"spec-lint-waive:\s*([A-Z0-9_]+)\s*(?:-\s*)?(.*)$", line)
        if match:
            waivers[match.group(1)] = match.group(2).strip() or "No reason recorded."
    return waivers


def lint_tasks_doc(path: Path, text: str) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    tasks = parse_tasks_from_text(text)
    if not tasks:
        diagnostics.append(diagnostic("error", "TASKS_MISSING", path, "No task checklist items found.", artifact_type="tasks"))
        return diagnostics
    ids = [task.task_id for task in tasks]
    by_id = {task.task_id: task for task in tasks}
    seen: set[str] = set()
    for task in tasks:
        if task.task_id in seen:
            diagnostics.append(
                diagnostic("error", "TASK_ID_DUPLICATE", path, f"Duplicate task ID: {task.task_id}", task.line, "planning", "tasks")
            )
        seen.add(task.task_id)
        if not task.acceptance and "." not in task.task_id:
            diagnostics.append(
                diagnostic("warn", "TASK_ACCEPTANCE_MISSING", path, f"{task.task_id} has no Acceptance field.", task.line, "planning", "tasks")
            )
        if task.complete and not task_verified(task, by_id):
            diagnostics.append(
                diagnostic("error", "TASK_EVIDENCE_MISSING", path, f"Completed task {task.task_id} has no evidence.", task.line, "completion", "tasks")
            )
        for dep in task.depends_on:
            if dep not in ids:
                diagnostics.append(
                    diagnostic("error", "TASK_DEPENDENCY_UNKNOWN", path, f"{task.task_id} depends on unknown task {dep}.", task.line, "planning", "tasks")
                )
    return diagnostics


def lint_spec_package(spec_path: Path, include_summary: bool = True) -> list[dict[str, Any]] | dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    inventory = artifact_inventory(spec_path)
    for artifact in CORE_ARTIFACTS:
        path = spec_path / artifact
        if not path.exists():
            diagnostics.append(
                diagnostic("error", "CORE_ARTIFACT_MISSING", path, f"Missing core artifact: {artifact}", waivable=False)
            )
        else:
            diagnostics.extend(lint_doc(path, artifact.removesuffix(".md")))
    for artifact in OPTIONAL_ARTIFACTS:
        if inventory[artifact] == "present":
            diagnostics.extend(lint_doc(spec_path / artifact, artifact.removesuffix(".md")))
    if include_summary:
        return {
            "spec_path": str(spec_path.resolve()),
            "diagnostics": diagnostics,
            "summary": diagnostic_summary(diagnostics),
        }
    return diagnostics


def diagnostic_summary(diagnostics: list[dict[str, Any]]) -> dict[str, int]:
    summary = {"error": 0, "warn": 0, "info": 0}
    for item in diagnostics:
        summary[item["severity"]] = summary.get(item["severity"], 0) + 1
    return summary


def parse_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []
    return parse_tasks_from_text(read_text(path))


def parse_tasks_from_text(text: str) -> list[Task]:
    lines = text.splitlines()
    starts: list[tuple[int, re.Match[str]]] = []
    for idx, line in enumerate(lines):
        match = TASK_LINE_RE.match(line)
        if match:
            starts.append((idx, match))
    tasks: list[Task] = []
    for pos, (start, match) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        for idx in range(start + 1, end):
            if lines[idx].startswith("## "):
                end = idx
                break
        block_lines = lines[start:end]
        block = "\n".join(block_lines).strip()
        tasks.append(
            Task(
                task_id=match.group(2),
                title=match.group(3).strip(),
                complete=match.group(1).lower() == "x",
                block=block,
                depends_on=field_task_ids(block, "Depends on"),
                files=field_refs(block, "Files"),
                acceptance=field_value(block, "Acceptance"),
                evidence=field_value(block, "Evidence"),
                line=start + 1,
            )
        )
    return tasks


def field_value(block: str, field: str) -> str:
    pattern = re.compile(rf"^\s+-\s+{re.escape(field)}:\s*(.*)$", re.MULTILINE)
    match = pattern.search(block)
    if not match:
        return ""
    value_lines = [match.group(1).strip()]
    for line in block[match.end() :].splitlines()[1:]:
        if re.match(r"^\s+-\s+\w[\w -]+:", line) or TASK_LINE_RE.match(line):
            break
        if line.startswith("    ") or line.startswith("  "):
            value_lines.append(line.strip())
        else:
            break
    return " ".join(part for part in value_lines if part).strip()


def field_task_ids(block: str, field: str) -> list[str]:
    value = field_value(block, field)
    if value.lower() in {"", "none"}:
        return []
    return TASK_RE.findall(value)


def field_refs(block: str, field: str) -> list[str]:
    value = field_value(block, field)
    refs = re.findall(r"`([^`]+)`", value)
    return refs if refs else [item.strip() for item in value.split(",") if item.strip()]


def next_task(spec_path: Path) -> dict[str, Any]:
    tasks = parse_tasks(spec_path / "tasks.md")
    by_id = {task.task_id: task for task in tasks}
    blocked: list[dict[str, Any]] = []
    for task in tasks:
        if task.complete:
            continue
        blockers = []
        for dep_id in task.depends_on:
            dep = by_id.get(dep_id)
            if dep is None:
                blockers.append({"task_id": dep_id, "reason": "unknown dependency"})
            elif not task_verified(dep, by_id):
                blockers.append({"task_id": dep_id, "reason": "dependency not complete with evidence"})
        if blockers:
            blocked.append({"task_id": task.task_id, "blockers": blockers})
            continue
        context = traceability_context(spec_path, task.task_id)
        return {
            "spec_path": str(spec_path.resolve()),
            "selected": task_payload(task),
            "traceability_context": context,
            "blocked": blocked,
        }
    return {
        "spec_path": str(spec_path.resolve()),
        "selected": None,
        "traceability_context": None,
        "blocked": blocked,
        "message": "No runnable incomplete task found.",
    }


def traceability_context(spec_path: Path, task_id: str) -> dict[str, Any]:
    if not (spec_path / "traceability.md").exists():
        return {
            "gaps": [
                {
                    "severity": "warn",
                    "code": "TRACEABILITY_MISSING",
                    "message": "No traceability.md found; infer context from full package before implementing.",
                }
            ]
        }
    return traceability_lookup.task_lookup(spec_path.resolve(), task_id)


def task_payload(task: Task) -> dict[str, Any]:
    return {
        "task_id": task.task_id,
        "title": task.title,
        "line": task.line,
        "complete": task.complete,
        "verified": task.verified,
        "depends_on": task.depends_on,
        "files": task.files,
        "acceptance": task.acceptance,
        "evidence": task.evidence,
        "source": task.block,
    }


def task_verified(task: Task, by_id: dict[str, Task] | None = None) -> bool:
    if task.verified:
        return True
    if "." not in task.task_id or not task.complete or by_id is None:
        return False
    parent_id = task.task_id.split(".", 1)[0]
    parent = by_id.get(parent_id)
    return bool(parent and parent.verified)


def closure_check(spec_path: Path) -> dict[str, Any]:
    lint_result = lint_spec_package(spec_path)
    assert isinstance(lint_result, dict)
    tasks = parse_tasks(spec_path / "tasks.md")
    by_id = {task.task_id: task for task in tasks}
    blockers: list[dict[str, Any]] = []
    for task in tasks:
        if not task_verified(task, by_id):
            blockers.append(
                {
                    "code": "TASK_NOT_VERIFIED",
                    "task_id": task.task_id,
                    "message": f"{task.task_id} is not complete with evidence.",
                }
            )
    if not (spec_path / "verification.md").exists():
        blockers.append(
            {
                "code": "VERIFICATION_ARTIFACT_MISSING",
                "message": "verification.md is missing.",
            }
        )
    if not (spec_path / "traceability.md").exists():
        blockers.append(
            {
                "code": "TRACEABILITY_ARTIFACT_MISSING",
                "message": "traceability.md is missing.",
            }
        )
    for item in lint_result["diagnostics"]:
        if item["severity"] == "error":
            blockers.append({"code": item["code"], "message": item["message"], "path": item["path"]})
    return {
        "spec_path": str(spec_path.resolve()),
        "ready": not blockers,
        "blockers": blockers,
        "lint_summary": lint_result["summary"],
        "promotion_required": True,
    }


def prompts_dir(repo_root: Path) -> Path:
    return repo_root / "skills" / "spec-lifecycle-manager" / "prompts"


def load_prompt_definitions(repo_root: Path) -> dict[str, Any]:
    root = repo_root.resolve()
    directory = prompts_dir(root)
    prompts: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    if not directory.exists():
        diagnostics.append(
            diagnostic("error", "PROMPTS_DIR_MISSING", directory, "Prompt directory is missing.", waivable=False)
        )
        return {"repo_root": str(root), "prompts": prompts, "diagnostics": diagnostics, "summary": diagnostic_summary(diagnostics)}
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            diagnostics.append(
                diagnostic("error", "PROMPT_JSON_INVALID", path, f"Invalid prompt JSON: {exc}", waivable=False)
            )
            continue
        prompts.append(data)
        diagnostics.extend(validate_prompt_definition(path, data))
    names = {prompt.get("name") for prompt in prompts}
    for required in REQUIRED_PROMPTS:
        if required not in names:
            diagnostics.append(
                diagnostic("error", "PROMPT_REQUIRED_MISSING", directory, f"Required prompt missing: {required}", waivable=False)
            )
    return {
        "repo_root": str(root),
        "prompts_dir": str(directory),
        "prompts": prompts,
        "diagnostics": diagnostics,
        "summary": diagnostic_summary(diagnostics),
    }


def validate_prompt_definition(path: Path, data: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    required_fields = ["name", "description", "arguments", "resources", "tools", "instructions", "return_format"]
    for field in required_fields:
        if not data.get(field):
            diagnostics.append(
                diagnostic("error", "PROMPT_FIELD_MISSING", path, f"Prompt missing field: {field}", waivable=False)
            )
    if data.get("name") != path.stem:
        diagnostics.append(
            diagnostic("error", "PROMPT_NAME_MISMATCH", path, "Prompt name must match the JSON filename.", waivable=False)
        )
    args = data.get("arguments", [])
    if not isinstance(args, list):
        diagnostics.append(diagnostic("error", "PROMPT_ARGUMENTS_INVALID", path, "arguments must be a list.", waivable=False))
    else:
        for arg in args:
            if not isinstance(arg, dict) or not arg.get("name") or "required" not in arg or not arg.get("description"):
                diagnostics.append(
                    diagnostic("error", "PROMPT_ARGUMENT_INVALID", path, "Each argument needs name, required, and description.", waivable=False)
                )
    if not data.get("client_support_fallback"):
        diagnostics.append(
            diagnostic("warn", "PROMPT_FALLBACK_MISSING", path, "Prompt should document client-support fallback.")
        )
    return diagnostics


def spec_path_for_changed_file(repo_root: Path, changed_file: str) -> Path | None:
    path = (repo_root / changed_file).resolve()
    parts = path.parts
    for idx, part in enumerate(parts):
        if part == "specs" and idx + 1 < len(parts):
            return Path(*parts[: idx + 2])
    return None


def run_hook(
    repo_root: Path,
    hook_name: str,
    changed_files: list[str] | None = None,
    spec_path: Path | None = None,
    task_id: str | None = None,
    severity_profile: str = "advisory",
    advisory: bool = False,
) -> dict[str, Any]:
    root = repo_root.resolve()
    changed_files = changed_files or []
    effective_advisory = advisory or severity_profile == "advisory"
    diagnostics: list[dict[str, Any]] = []
    affected_specs: list[str] = []

    if spec_path:
        affected = [spec_path.resolve()]
    else:
        affected_set = {
            found
            for changed in changed_files
            if (found := spec_path_for_changed_file(root, changed)) is not None
        }
        affected = sorted(affected_set)

    if hook_name == "spec-file-changed":
        for spec in affected:
            affected_specs.append(str(spec))
            result = lint_spec_package(spec)
            assert isinstance(result, dict)
            diagnostics.extend(result["diagnostics"])
    elif hook_name == "task-checkbox-changed":
        for spec in affected:
            tasks_path = spec / "tasks.md"
            if tasks_path.exists():
                affected_specs.append(str(spec))
                diagnostics.extend(lint_doc(tasks_path, "tasks"))
    elif hook_name == "template-changed":
        for changed in changed_files:
            path = (root / changed).resolve()
            if path.exists() and path.suffix == ".md":
                diagnostics.extend(lint_doc(path, path.stem))
    elif hook_name == "implementation-task-complete":
        for spec in affected:
            affected_specs.append(str(spec))
            diagnostics.extend(check_implementation_task_complete(spec, task_id, changed_files, root))
    elif hook_name == "verification-updated":
        for spec in affected:
            affected_specs.append(str(spec))
            diagnostics.extend(check_verification_updated(spec))
    elif hook_name == "spec-resumed":
        for spec in affected:
            affected_specs.append(str(spec))
            diagnostics.extend(check_spec_resumed(spec))
    elif hook_name == "spec-close-check":
        for spec in affected:
            affected_specs.append(str(spec))
            diagnostics.extend(check_spec_close_hook(spec))
    else:
        diagnostics.append(
            diagnostic("error", "HOOK_UNKNOWN", root, f"Unknown hook: {hook_name}", waivable=False)
        )

    blocking = hook_blockers(diagnostics, effective_advisory)
    return {
        "hook": hook_name,
        "repo_root": str(root),
        "severity_profile": severity_profile,
        "advisory": effective_advisory,
        "changed_files": changed_files,
        "affected_specs": affected_specs,
        "diagnostics": diagnostics,
        "summary": diagnostic_summary(diagnostics),
        "blocking": blocking,
        "blocked": bool(blocking),
    }


def check_implementation_task_complete(
    spec_path: Path,
    task_id: str | None,
    changed_files: list[str],
    repo_root: Path,
) -> list[dict[str, Any]]:
    tasks_path = spec_path / "tasks.md"
    diagnostics: list[dict[str, Any]] = []
    tasks = parse_tasks(tasks_path)
    by_id = {task.task_id: task for task in tasks}
    selected = [by_id[task_id]] if task_id and task_id in by_id else [task for task in tasks if task.complete]
    if task_id and task_id not in by_id:
        return [
            diagnostic(
                "error",
                "TASK_NOT_FOUND",
                tasks_path,
                f"Task {task_id} was not found.",
                lifecycle_gate="completion",
                artifact_type="tasks",
                waivable=False,
            )
        ]
    for task in selected:
        if not task.complete:
            diagnostics.append(
                diagnostic(
                    "warn",
                    "TASK_NOT_MARKED_COMPLETE",
                    tasks_path,
                    f"{task.task_id} is not marked complete.",
                    task.line,
                    "completion",
                    "tasks",
                )
            )
        if task.complete and not task_verified(task, by_id):
            diagnostics.append(
                diagnostic(
                    "error",
                    "TASK_EVIDENCE_MISSING",
                    tasks_path,
                    f"Completed task {task.task_id} has no evidence.",
                    task.line,
                    "completion",
                    "tasks",
                )
            )
        if task.complete and not task.files:
            diagnostics.append(
                diagnostic(
                    "warn",
                    "TASK_FILES_MISSING",
                    tasks_path,
                    f"Completed task {task.task_id} has no Files field.",
                    task.line,
                    "completion",
                    "tasks",
                )
            )
        if task.complete and task.files and changed_files:
            changed = {(repo_root / item).resolve() for item in changed_files}
            expected = {(repo_root / item).resolve() for item in task.files if item != "implementation path TBD"}
            if expected and not any(path in changed for path in expected):
                diagnostics.append(
                    diagnostic(
                        "warn",
                        "TASK_CHANGED_FILES_UNMATCHED",
                        tasks_path,
                        f"Changed files do not include Files entries for {task.task_id}.",
                        task.line,
                        "completion",
                        "tasks",
                    )
                )
    return diagnostics


def check_verification_updated(spec_path: Path) -> list[dict[str, Any]]:
    path = spec_path / "verification.md"
    if not path.exists():
        return [
            diagnostic(
                "error",
                "VERIFICATION_ARTIFACT_MISSING",
                path,
                "verification.md is missing.",
                lifecycle_gate="verification",
                artifact_type="verification",
                waivable=False,
            )
        ]
    text = read_text(path)
    diagnostics = lint_doc(path, "verification")
    if not TASK_RE.search(text):
        diagnostics.append(
            diagnostic(
                "warn",
                "VERIFICATION_TASK_REF_MISSING",
                path,
                "Verification evidence does not reference task IDs.",
                lifecycle_gate="verification",
                artifact_type="verification",
            )
        )
    if not REQ_RE.search(text):
        diagnostics.append(
            diagnostic(
                "warn",
                "VERIFICATION_REQUIREMENT_REF_MISSING",
                path,
                "Verification evidence does not reference requirement IDs.",
                lifecycle_gate="verification",
                artifact_type="verification",
            )
        )
    return diagnostics


def check_spec_resumed(spec_path: Path) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    inventory = artifact_inventory(spec_path)
    if spec_format(inventory) == "old-format":
        diagnostics.append(
            diagnostic(
                "warn",
                "OLD_FORMAT_MIGRATION_DECISION_NEEDED",
                spec_path,
                "Old-format package found; make migration decision visible before implementation.",
                lifecycle_gate="resume",
            )
        )
    result = lint_spec_package(spec_path)
    assert isinstance(result, dict)
    diagnostics.extend(result["diagnostics"])
    status = spec_status(spec_path)
    if status in {"archived", "closed"}:
        diagnostics.append(
            diagnostic(
                "warn",
                "RESUMING_CLOSED_SPEC",
                spec_path,
                f"Spec status is {status}; confirm this package should be resumed.",
                lifecycle_gate="resume",
            )
        )
    review_date = last_reviewed(spec_path)
    if review_date and (date.today() - review_date).days > 30:
        diagnostics.append(
            diagnostic(
                "warn",
                "SPEC_REVIEW_STALE",
                spec_path,
                f"Spec last_reviewed is {review_date.isoformat()}; reconcile stale context.",
                lifecycle_gate="resume",
            )
        )
    return diagnostics


def last_reviewed(spec_path: Path) -> date | None:
    for name in ["requirements.md", "tasks.md", "spec.md", "plan.md"]:
        path = spec_path / name
        if not path.exists():
            continue
        value = parse_frontmatter(read_text(path)).get("last_reviewed")
        if not value:
            continue
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def check_spec_close_hook(spec_path: Path) -> list[dict[str, Any]]:
    result = closure_check(spec_path)
    diagnostics: list[dict[str, Any]] = []
    for blocker in result["blockers"]:
        diagnostics.append(
            diagnostic(
                "error",
                blocker["code"],
                Path(blocker.get("path", spec_path)),
                blocker["message"],
                lifecycle_gate="closure",
                waivable=False,
            )
        )
    return diagnostics


def hook_blockers(diagnostics: list[dict[str, Any]], advisory: bool) -> list[dict[str, Any]]:
    if advisory:
        return []
    blockers: list[dict[str, Any]] = []
    for item in diagnostics:
        if item["severity"] == "error":
            blockers.append(item)
        elif item["code"] == "TASK_EVIDENCE_MISSING":
            blockers.append(item)
    return blockers


def print_payload(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Spec lifecycle runtime helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Scan active spec packages.")
    scan.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    scan.add_argument("--docs-root")

    summary = sub.add_parser("summary", help="Return specs://{id}/summary style payload.")
    summary.add_argument("spec_path", type=Path)

    lint = sub.add_parser("lint", help="Lint a spec package or document.")
    lint.add_argument("path", type=Path)
    lint.add_argument("--artifact-type")

    next_cmd = sub.add_parser("next-task", help="Return the next runnable task with context.")
    next_cmd.add_argument("spec_path", type=Path)

    closure = sub.add_parser("closure-check", help="Check spec closure readiness.")
    closure.add_argument("spec_path", type=Path)

    prompts = sub.add_parser("prompts", help="List and validate prompt definitions.")
    prompts.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())

    hook = sub.add_parser("hook", help="Run a spec lifecycle hook.")
    hook.add_argument(
        "hook_name",
        choices=[
            "spec-file-changed",
            "task-checkbox-changed",
            "template-changed",
            "implementation-task-complete",
            "verification-updated",
            "spec-resumed",
            "spec-close-check",
        ],
    )
    hook.add_argument("--repo-root", type=Path, default=Path.cwd())
    hook.add_argument("--changed-files", nargs="*", default=[])
    hook.add_argument("--spec-path", type=Path)
    hook.add_argument("--task-id")
    hook.add_argument("--severity-profile", choices=["advisory", "blocking"], default="advisory")
    hook.add_argument("--advisory", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.command == "scan":
        payload = scan_specs(args.repo_root, args.docs_root)
    elif args.command == "summary":
        payload = spec_summary(args.spec_path.resolve())
    elif args.command == "lint":
        if args.path.is_dir():
            payload = lint_spec_package(args.path.resolve())
        else:
            diagnostics = lint_doc(args.path.resolve(), args.artifact_type)
            payload = {"path": str(args.path.resolve()), "diagnostics": diagnostics, "summary": diagnostic_summary(diagnostics)}
    elif args.command == "next-task":
        payload = next_task(args.spec_path.resolve())
    elif args.command == "closure-check":
        payload = closure_check(args.spec_path.resolve())
    elif args.command == "prompts":
        payload = load_prompt_definitions(args.repo_root)
    elif args.command == "hook":
        payload = run_hook(
            args.repo_root,
            args.hook_name,
            changed_files=args.changed_files,
            spec_path=args.spec_path,
            task_id=args.task_id,
            severity_profile=args.severity_profile,
            advisory=args.advisory,
        )
    else:
        raise ValueError(args.command)
    print_payload(payload)
    if args.command == "hook":
        return 1 if payload["blocked"] else 0
    if "summary" in payload and payload["summary"].get("error", 0):
        return 1
    if args.command == "closure-check" and not payload["ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
