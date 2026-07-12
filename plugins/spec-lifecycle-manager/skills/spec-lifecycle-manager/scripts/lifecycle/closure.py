"""Shared preview-first closure helper internals.

This module intentionally has no CLI or MCP transport code. Public entrypoints
can import these functions, but closure planning, rendering, write guards, and
validation command selection live here.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PENDING_CLEANUP_COMMIT = "pending-cleanup-commit"
VALID_STATUSES = {"retained", "removed", "superseded"}
ACTION_TO_STATUS = {
    "archived": "retained",
    "retained-as-history": "retained",
    "removed": "removed",
    "removed-after-index": "removed",
    "superseded": "superseded",
}
STATUS_ACTIONS = {
    "retained": {"archived", "retained-as-history"},
    "removed": {"removed", "removed-after-index"},
    "superseded": {"superseded"},
}
WRITE_ACTION_TYPES = {"cleanup_package", "resolve_cleanup_hash", "render_records", "update_active_reference"}
HISTORICAL_REFERENCE_PATHS = {
    "docs/history/spec-closure-log.md",
    "docs/history/spec-archive-index.md",
}
KNOWN_ACTIVE_REFERENCE_PATHS = {
    "docs/backlog/README.md",
    "docs/roadmap/README.md",
}
DEFAULT_ARCHIVED_SPEC_ROOT = "docs/history/archived-specs"
ROOT_IGNORE_FILE_NAMES = (".gitignore", ".aiignore")
DEFAULT_REFERENCE_EXCLUDED_DIRS = {".cache", ".git", "__pycache__"}
DEFAULT_REFERENCE_EXCLUDED_SUFFIXES = {
    ".db",
    ".db-shm",
    ".db-wal",
    ".sqlite",
    ".sqlite-shm",
    ".sqlite-wal",
    ".sqlite3",
}
CLOSURE_PLAN_FINDING_LIMIT = 20
CLOSURE_PLAN_ACTION_LIMIT = 10
CLOSURE_PLAN_REFERENCE_SAMPLE_LIMIT = 20
CLOSURE_PLAN_PREVIEW_LIMIT = 500
CLOSURE_PLAN_PAYLOAD_TARGET_BYTES = 32768
CLOSURE_PLAN_SECTIONS = {"references", "edits", "validation"}


@dataclass(frozen=True)
class IgnoreRule:
    pattern: str
    negated: bool
    directory_only: bool
    anchored: bool
    has_slash: bool


def _parse_ignore_rules(content: str) -> list[IgnoreRule]:
    rules: list[IgnoreRule] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        negated = line.startswith("!")
        if negated:
            line = line[1:]
        anchored = line.startswith("/")
        if anchored:
            line = line[1:]
        directory_only = line.endswith("/")
        if directory_only:
            line = line[:-1]
        if not line:
            continue
        rules.append(
            IgnoreRule(
                pattern=line,
                negated=negated,
                directory_only=directory_only,
                anchored=anchored,
                has_slash="/" in line,
            )
        )
    return rules


def _read_root_ignore_rules(repo_root: Path) -> list[IgnoreRule]:
    rules: list[IgnoreRule] = []
    for name in ROOT_IGNORE_FILE_NAMES:
        path = repo_root / name
        try:
            rules.extend(_parse_ignore_rules(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeError):
            continue
    return rules


def _ignore_pattern_matches(pattern: str, value: str) -> bool:
    escaped = re.escape(pattern).replace(r"\*", "[^/]*")
    return re.fullmatch(escaped, value) is not None


def _ignore_rule_matches(rule: IgnoreRule, relative_path: str, is_directory: bool) -> bool:
    if (
        rule.directory_only
        and not is_directory
        and relative_path != rule.pattern
        and not relative_path.startswith(f"{rule.pattern}/")
    ):
        return False
    if rule.anchored or rule.has_slash:
        return _ignore_pattern_matches(rule.pattern, relative_path) or relative_path.startswith(
            f"{rule.pattern}/"
        )
    return any(_ignore_pattern_matches(rule.pattern, segment) for segment in relative_path.split("/"))


def _is_ignored_path(relative_path: str, is_directory: bool, rules: list[IgnoreRule]) -> bool:
    ignored = False
    for rule in rules:
        if _ignore_rule_matches(rule, relative_path, is_directory):
            ignored = not rule.negated
    return ignored


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FollowUp:
    text: str
    destination: str = "none"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ClosureMetadata:
    spec_id: str
    title: str
    package_path: str
    status: str = "removed"
    closure_action: str = "removed"
    final_spec_commit: str = "pending"
    cleanup_commit: str = PENDING_CLEANUP_COMMIT
    durable_destinations: list[str] = field(default_factory=list)
    verification_summary: str = ""
    residual_risks: list[str] = field(default_factory=list)
    follow_ups: list[FollowUp] = field(default_factory=list)
    closed_by: str = "agent"
    closed_date: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["follow_ups"] = [item.to_dict() for item in self.follow_ups]
        return data


@dataclass(frozen=True)
class FilePrecondition:
    path: str
    exists: bool
    content_hash: str | None = None
    required_snippet: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlannedEdit:
    edit_id: str
    path: str
    action: str
    reason: str
    preview: str
    precondition: FilePrecondition
    content: str | None = None
    destination_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["precondition"] = self.precondition.to_dict()
        return data


@dataclass(frozen=True)
class ClosureAction:
    action_id: str
    action_type: str
    mode: str = "preview"
    requires_write_intent: bool = False
    planned_edit_ids: list[str] = field(default_factory=list)
    manual_decision: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ValidationCommand:
    command: str
    reason: str
    runnable_by_helper: bool
    required: bool
    phase: str = "final"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CandidateCommit:
    commit: str
    subject: str
    date: str
    evidence: list[str]
    confidence: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ClosureStep:
    step_id: str
    label: str
    status: str
    action_kind: str
    blockers: list[Diagnostic] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["id"] = data.pop("step_id")
        data["blockers"] = [item.to_dict() for item in self.blockers]
        return data


@dataclass(frozen=True)
class ClosurePlan:
    plan_id: str
    generated_at: str
    repo_root: str
    spec_path: str
    metadata: ClosureMetadata
    steps: list[ClosureStep]
    actions: list[ClosureAction]
    planned_edits: list[PlannedEdit]
    validation_commands: list[ValidationCommand]
    preconditions: list[FilePrecondition]
    diagnostics: list[Diagnostic] = field(default_factory=list)
    final_spec_commit_candidates: list[CandidateCommit] = field(default_factory=list)
    references: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "generated_at": self.generated_at,
            "repo_root": self.repo_root,
            "spec_path": self.spec_path,
            "metadata": self.metadata.to_dict(),
            "steps": [item.to_dict() for item in self.steps],
            "actions": [item.to_dict() for item in self.actions],
            "planned_edits": [item.to_dict() for item in self.planned_edits],
            "validation_commands": [item.to_dict() for item in self.validation_commands],
            "preconditions": [item.to_dict() for item in self.preconditions],
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "final_spec_commit_candidates": [item.to_dict() for item in self.final_spec_commit_candidates],
            "references": self.references,
            "ready": not any(item.severity == "error" for item in self.diagnostics),
            "mutates_files": False,
        }


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "closure"


def _repo_relative(repo_root: Path, path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    resolved = candidate.resolve()
    root = repo_root.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"path escapes repo root: {path}") from exc


def _path_hash(path: Path) -> str | None:
    if not path.exists() or path.is_dir():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_hash(path: Path) -> str | None:
    if not path.exists() or not path.is_dir():
        return None
    digest = hashlib.sha256()
    for child in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(child.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _precondition(repo_root: Path, relative_path: str, required_snippet: str | None = None) -> FilePrecondition:
    path = repo_root / relative_path
    return FilePrecondition(
        path=relative_path,
        exists=path.exists(),
        content_hash=_path_hash(path),
        required_snippet=required_snippet,
    )


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _title_from_requirements(spec_path: Path) -> str:
    requirements = spec_path / "requirements.md"
    text = _read(requirements)
    match = re.search(r"^title:\s*(.+?)\s*$", text, re.MULTILINE)
    if match:
        return match.group(1).strip().strip("\"'")
    return spec_path.name


def _markdown_list(items: list[str]) -> str:
    return "\n".join(f"  - `{item}`" for item in items) if items else "  - none"


def _coerce_follow_ups(value: Any) -> list[FollowUp]:
    if not value:
        return []
    result: list[FollowUp] = []
    for item in value:
        if isinstance(item, FollowUp):
            result.append(item)
        elif isinstance(item, dict):
            result.append(FollowUp(text=str(item.get("text") or ""), destination=str(item.get("destination") or "none")))
        else:
            result.append(FollowUp(text=str(item), destination="none"))
    return result


def _normalize_metadata(data: ClosureMetadata | dict[str, Any]) -> tuple[ClosureMetadata | None, list[Diagnostic]]:
    if isinstance(data, ClosureMetadata):
        metadata = data
    elif isinstance(data, dict):
        status_provided = bool(str(data.get("status") or "").strip())
        raw_status = str(data.get("status") or "").replace("_", "-")
        action = str(data.get("closure_action") or "")
        if not action and raw_status == "archived":
            action = "archived"
        if not action and raw_status == "retained-as-history":
            action = "retained-as-history"
        if not action:
            action = raw_status or "removed"
        if raw_status in {"archived", "retained-as-history"}:
            status = "retained"
        elif status_provided:
            status = raw_status
        else:
            status = ACTION_TO_STATUS.get(action, "removed")
        metadata = ClosureMetadata(
            spec_id=str(data.get("spec_id") or ""),
            title=str(data.get("title") or ""),
            package_path=str(data.get("package_path") or ""),
            status=status,
            closure_action=action,
            final_spec_commit=str(data.get("final_spec_commit") or "pending"),
            cleanup_commit=str(data.get("cleanup_commit") or PENDING_CLEANUP_COMMIT),
            durable_destinations=[str(item) for item in data.get("durable_destinations") or []],
            verification_summary=str(data.get("verification_summary") or ""),
            residual_risks=[str(item) for item in data.get("residual_risks") or []],
            follow_ups=_coerce_follow_ups(data.get("follow_ups")),
            closed_by=str(data.get("closed_by") or "agent"),
            closed_date=str(data.get("closed_date") or ""),
        )
    else:
        return None, [Diagnostic("error", "CLOSURE_METADATA_INVALID", "Closure metadata must be an object.")]
    return metadata, validate_closure_metadata(metadata)


def validate_closure_metadata(metadata: ClosureMetadata, *, final: bool = False) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    required = {
        "spec_id": metadata.spec_id,
        "title": metadata.title,
        "package_path": metadata.package_path,
        "closure_action": metadata.closure_action,
        "final_spec_commit": metadata.final_spec_commit,
        "cleanup_commit": metadata.cleanup_commit,
        "verification_summary": metadata.verification_summary,
    }
    for field_name, value in required.items():
        if not str(value).strip():
            diagnostics.append(Diagnostic("error", "CLOSURE_METADATA_FIELD_MISSING", f"Closure metadata missing field: {field_name}."))
    if metadata.status not in VALID_STATUSES:
        diagnostics.append(Diagnostic("error", "CLOSURE_STATUS_INVALID", f"Invalid closure status: {metadata.status}."))
    allowed_actions = STATUS_ACTIONS.get(metadata.status, set())
    if allowed_actions and metadata.closure_action not in allowed_actions:
        diagnostics.append(
            Diagnostic(
                "error",
                "CLOSURE_STATUS_ACTION_MISMATCH",
                f"status={metadata.status} requires closure_action in {sorted(allowed_actions)}, got {metadata.closure_action}.",
            )
        )
    if final and metadata.cleanup_commit == PENDING_CLEANUP_COMMIT:
        diagnostics.append(Diagnostic("error", "CLOSURE_CLEANUP_COMMIT_PENDING", "Cleanup commit remains unresolved."))
    return diagnostics


def parse_closure_metadata(value: ClosureMetadata | dict[str, Any] | str) -> ClosureMetadata:
    if isinstance(value, str):
        value = json.loads(value)
    metadata, diagnostics = _normalize_metadata(value)
    if metadata is None:
        raise ValueError("; ".join(item.message for item in diagnostics))
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        raise ValueError("; ".join(item.message for item in errors))
    return metadata


def parse_closure_plan(value: ClosurePlan | dict[str, Any] | str) -> ClosurePlan:
    if isinstance(value, ClosurePlan):
        return value
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise ValueError("Closure plan must be an object.")
    metadata = parse_closure_metadata(value.get("metadata") or {})
    planned_edits = []
    for item in value.get("planned_edits") or []:
        pre = item.get("precondition") or {}
        planned_edits.append(
            PlannedEdit(
                edit_id=str(item.get("edit_id") or ""),
                path=str(item.get("path") or ""),
                action=str(item.get("action") or ""),
                reason=str(item.get("reason") or ""),
                preview=str(item.get("preview") or ""),
                precondition=FilePrecondition(
                    path=str(pre.get("path") or item.get("path") or ""),
                    exists=bool(pre.get("exists")),
                    content_hash=pre.get("content_hash"),
                    required_snippet=pre.get("required_snippet"),
                ),
                content=item.get("content"),
                destination_path=item.get("destination_path"),
            )
        )
    actions = [
        ClosureAction(
            action_id=str(item.get("action_id") or ""),
            action_type=str(item.get("action_type") or ""),
            mode=str(item.get("mode") or "preview"),
            requires_write_intent=bool(item.get("requires_write_intent")),
            planned_edit_ids=[str(edit_id) for edit_id in item.get("planned_edit_ids") or []],
            manual_decision=item.get("manual_decision"),
        )
        for item in value.get("actions") or []
    ]
    commands = [
        ValidationCommand(
            command=str(item.get("command") or ""),
            reason=str(item.get("reason") or ""),
            runnable_by_helper=bool(item.get("runnable_by_helper")),
            required=bool(item.get("required")),
            phase=str(item.get("phase") or "final"),
        )
        for item in value.get("validation_commands") or []
    ]
    preconditions = [edit.precondition for edit in planned_edits]
    return ClosurePlan(
        plan_id=str(value.get("plan_id") or ""),
        generated_at=str(value.get("generated_at") or ""),
        repo_root=str(value.get("repo_root") or "."),
        spec_path=str(value.get("spec_path") or metadata.package_path),
        metadata=metadata,
        steps=[],
        actions=actions,
        planned_edits=planned_edits,
        validation_commands=commands,
        preconditions=preconditions,
        diagnostics=[Diagnostic(**item) for item in value.get("diagnostics") or [] if isinstance(item, dict)],
        references=value.get("references") or {},
    )


def _core_module() -> Any:
    from lifecycle import core

    return core


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo_root, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def discover_final_spec_commits(repo_root: Path, spec_path: Path | str, limit: int = 10) -> list[CandidateCommit]:
    root = repo_root.resolve()
    rel = _repo_relative(root, spec_path)
    result = _git(root, "log", f"-n{limit}", "--format=%H%x09%cs%x09%s", "--", rel)
    if result.returncode != 0:
        return []
    candidates: list[CandidateCommit] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        commit, commit_date, subject = parts
        tree = _git(root, "ls-tree", "-r", "--name-only", commit, rel)
        files = set(tree.stdout.splitlines()) if tree.returncode == 0 else set()
        expected = {f"{rel}/requirements.md", f"{rel}/design.md", f"{rel}/tasks.md", f"{rel}/verification.md"}
        present = sorted(expected & files)
        evidence = [f"contains {path}" for path in present]
        if f"{rel}/tasks.md" in files and f"{rel}/verification.md" in files:
            confidence = "high" if len(present) >= 3 else "medium"
        elif files:
            confidence = "low"
        else:
            continue
        candidates.append(CandidateCommit(commit=commit, subject=subject, date=commit_date, evidence=evidence, confidence=confidence))
    return candidates


def classify_spec_references(repo_root: Path, spec_id: str, package_path: str) -> dict[str, list[dict[str, Any]]]:
    root = repo_root.resolve()
    needles = [spec_id, package_path.rstrip("/")]
    results: dict[str, list[dict[str, Any]]] = {"active_stale": [], "historical": [], "historical_or_validation": [], "review": []}
    ignore_rules = _read_root_ignore_rules(root)
    for path in sorted(root.rglob("*")):
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if _is_ignored_path(rel, path.is_dir(), ignore_rules):
            continue
        if any(part in DEFAULT_REFERENCE_EXCLUDED_DIRS for part in path.parts):
            continue
        if not path.is_file() or any(rel.endswith(suffix) for suffix in DEFAULT_REFERENCE_EXCLUDED_SUFFIXES):
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if b"\x00" in raw[:8192]:
            continue
        text = raw.decode("utf-8", errors="ignore")
        for needle in needles:
            if not needle or needle not in text:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if needle not in line:
                    continue
                item = {"path": rel, "line": line_no, "text": line.strip()[:240], "needle": needle}
                lower = line.lower()
                if rel in HISTORICAL_REFERENCE_PATHS:
                    results["historical"].append(item)
                elif rel.startswith("tests/"):
                    results["historical_or_validation"].append(item)
                elif rel in KNOWN_ACTIVE_REFERENCE_PATHS or " active " in f" {lower} " or package_path in line:
                    results["active_stale"].append(item)
                else:
                    results["review"].append(item)
    for key, items in results.items():
        deduped = []
        seen = set()
        for item in items:
            marker = (item["path"], item["line"], item["needle"])
            if marker not in seen:
                deduped.append(item)
                seen.add(marker)
        results[key] = deduped
    return results


def _bounded_text(value: str, limit: int = CLOSURE_PLAN_PREVIEW_LIMIT) -> str:
    return value if len(value) <= limit else value[: limit - 3] + "..."


def _edit_summary(edit: dict[str, Any]) -> dict[str, Any]:
    content = edit.get("content")
    precondition = edit.get("precondition") or {}
    return {
        "edit_id": edit.get("edit_id"),
        "path": edit.get("path"),
        "action": edit.get("action"),
        "reason": edit.get("reason"),
        "preview": _bounded_text(str(edit.get("preview") or "")),
        "content_hash": hashlib.sha256(str(content or "").encode("utf-8")).hexdigest() if content is not None else None,
        "content_bytes": len(str(content).encode("utf-8")) if content is not None else 0,
        "precondition": {
            "exists": precondition.get("exists"),
            "content_hash": precondition.get("content_hash"),
        },
        "destination_path": edit.get("destination_path"),
    }


def closure_plan_manifest(
    plan: dict[str, Any],
    *,
    detail: str = "summary",
    section: str | None = None,
) -> dict[str, Any]:
    """Return only agent-usable closure decisions, summaries, and action handles."""
    if detail not in {"summary", "section"}:
        raise ValueError("detail must be one of: summary, section")
    if detail == "section" and section not in CLOSURE_PLAN_SECTIONS:
        raise ValueError("section must be one of: references, edits, validation")
    if detail != "section" and section is not None:
        raise ValueError("section is only valid when detail='section'")

    references = plan.get("references", {})
    reference_counts = {key: len(value) for key, value in references.items() if isinstance(value, list)}
    reference_samples: list[dict[str, Any]] = []
    for category in ("active_stale", "review", "historical_or_validation", "historical"):
        for item in references.get(category, []):
            if len(reference_samples) >= CLOSURE_PLAN_REFERENCE_SAMPLE_LIMIT:
                break
            reference_samples.append({"category": category, **item})
    edit_summaries = [_edit_summary(item) for item in plan.get("planned_edits", [])]
    validation = plan.get("validation_commands", [])
    if detail == "section":
        content = {
            "references": {"counts": reference_counts, "samples": reference_samples},
            "edits": {"items": edit_summaries},
            "validation": {"commands": validation[:CLOSURE_PLAN_ACTION_LIMIT]},
        }[str(section)]
        return {
            "detail": "section",
            "schema_version": "1",
            "plan_id": plan["plan_id"],
            "section": section,
            "content": content,
        }

    diagnostics = list(plan.get("diagnostics", []))
    active_references = [
        {"severity": "warn", "code": "CLOSURE_ACTIVE_REFERENCE", **item}
        for item in references.get("active_stale", [])
    ]
    findings = (diagnostics + active_references)[:CLOSURE_PLAN_FINDING_LIMIT]
    action_dependencies = {"cleanup_package": ["render_records"]}
    edit_paths = {item.get("edit_id"): item.get("path") for item in edit_summaries}
    actions = [
        {
            **item,
            "depends_on": action_dependencies.get(str(item.get("action_id")), []),
            "affected_paths": [
                edit_paths[edit_id]
                for edit_id in item.get("planned_edit_ids", [])
                if edit_id in edit_paths
            ],
        }
        for item in plan.get("actions", [])[:CLOSURE_PLAN_ACTION_LIMIT]
    ]
    result = {
        "detail": "summary",
        "schema_version": "1",
        "plan_id": plan["plan_id"],
        "decision": {
            "ready": bool(plan.get("ready")),
            "spec_path": plan.get("spec_path"),
            "spec_id": plan.get("metadata", {}).get("spec_id"),
            "closure_action": plan.get("metadata", {}).get("closure_action"),
            "final_spec_commit": plan.get("metadata", {}).get("final_spec_commit"),
        },
        "findings": findings,
        "next_actions": actions,
        "limits": {
            "findings": {"returned": len(findings), "total": len(diagnostics) + len(active_references), "limit": CLOSURE_PLAN_FINDING_LIMIT, "truncated": len(findings) < len(diagnostics) + len(active_references)},
            "next_actions": {"returned": len(actions), "total": len(plan.get("actions", [])), "limit": CLOSURE_PLAN_ACTION_LIMIT, "truncated": len(actions) < len(plan.get("actions", []))},
            "payload_target_bytes": CLOSURE_PLAN_PAYLOAD_TARGET_BYTES,
            "limit_exceeded": False,
        },
        "reference_summary": {"counts": reference_counts, "sample_count": len(reference_samples)},
        "edit_summaries": edit_summaries,
        "expansion": {
            "tool": "closure_plan",
            "sections": sorted(CLOSURE_PLAN_SECTIONS),
            "arguments": {
                "spec_path": plan.get("spec_path"),
                "final_spec_commit": plan.get("metadata", {}).get("final_spec_commit"),
                "closure_action": plan.get("metadata", {}).get("closure_action"),
                "detail": "section",
                "plan_id": plan["plan_id"],
            },
        },
    }
    if len(json.dumps(result, sort_keys=True).encode("utf-8")) > CLOSURE_PLAN_PAYLOAD_TARGET_BYTES:
        result["limits"]["limit_exceeded"] = True
    return result


def render_closure_log_entry(metadata: ClosureMetadata) -> str:
    return "\n".join(
        [
            f"### {metadata.closed_date or datetime.now(timezone.utc).date().isoformat()} - {metadata.spec_id}",
            "",
            f"- **Spec:** `{metadata.package_path}/`",
            f"- **Title:** {metadata.title}",
            f"- **Final spec commit:** `{metadata.final_spec_commit}`",
            f"- **Closure cleanup commit:** `{metadata.cleanup_commit}`",
            f"- **Closure action:** {metadata.closure_action}",
            "- **Durable docs updated:**",
            _markdown_list(metadata.durable_destinations),
            f"- **Verification summary:** {metadata.verification_summary or 'TBD'}",
            "- **Residual risks:**",
            _markdown_list(metadata.residual_risks),
            "- **Follow-up:** "
            + ("; ".join(f"{item.text} -> {item.destination}" for item in metadata.follow_ups) if metadata.follow_ups else "none"),
            "",
        ]
    )


def render_archive_index_row(metadata: ClosureMetadata) -> str:
    durable = "; ".join(f"`{item}`" for item in metadata.durable_destinations) if metadata.durable_destinations else "none"
    return (
        f"| {metadata.spec_id} | {metadata.title} | `{metadata.package_path}/` | {metadata.status} | "
        f"{metadata.final_spec_commit} | {metadata.cleanup_commit} | {metadata.closure_action} | {durable} | "
        "`docs/history/spec-closure-log.md` |"
    )


def _insert_closure_log(existing: str, entry: str) -> str:
    if not existing.strip():
        return "# Spec Closure Log\n\n## Entries\n\n" + entry
    heading = entry.splitlines()[0]
    spec_id = heading.rsplit(" - ", 1)[-1]
    existing_match = re.search(
        rf"(?ms)^### [^\n]+ - {re.escape(spec_id)}\n.*?(?=^### |\Z)",
        existing,
    )
    if existing_match:
        return existing[: existing_match.start()] + entry.rstrip() + "\n\n" + existing[existing_match.end():].lstrip("\n")
    marker = "## Entries"
    if marker not in existing:
        return existing.rstrip() + "\n\n" + marker + "\n\n" + entry
    before, after = existing.split(marker, 1)
    return before + marker + "\n\n" + entry + after.lstrip("\n")


def _insert_archive_row(existing: str, row: str) -> str:
    if not existing.strip():
        return "\n".join(
            [
                "# Spec Archive Index",
                "",
                "## Entries",
                "",
                "| Spec ID | Title | Package path | Status | Final spec commit | Cleanup commit | Closure action | Durable destinations | Verification |",
                "|---------|-------|--------------|--------|-------------------|----------------|----------------|----------------------|--------------|",
                row,
                "",
            ]
        )
    lines = existing.splitlines()
    spec_id = row.split("|", 2)[1].strip()
    for idx, line in enumerate(lines):
        cells = line.split("|")
        if len(cells) > 2 and cells[1].strip() == spec_id:
            lines[idx] = row
            return "\n".join(lines) + "\n"
    for idx, line in enumerate(lines):
        if line.strip().startswith("|---------"):
            lines.insert(idx + 1, row)
            return "\n".join(lines) + "\n"
    return existing.rstrip() + "\n" + row + "\n"


def _planned_record_edits(repo_root: Path, metadata: ClosureMetadata) -> list[PlannedEdit]:
    log_rel = "docs/history/spec-closure-log.md"
    index_rel = "docs/history/spec-archive-index.md"
    log_content = _insert_closure_log(_read(repo_root / log_rel), render_closure_log_entry(metadata))
    index_content = _insert_archive_row(_read(repo_root / index_rel), render_archive_index_row(metadata))
    return [
        PlannedEdit(
            edit_id="render_closure_log",
            path=log_rel,
            action="update" if (repo_root / log_rel).exists() else "add",
            reason="Render closure-log entry from canonical closure metadata.",
            preview=render_closure_log_entry(metadata),
            precondition=_precondition(repo_root, log_rel),
            content=log_content,
        ),
        PlannedEdit(
            edit_id="render_archive_index",
            path=index_rel,
            action="update" if (repo_root / index_rel).exists() else "add",
            reason="Render archive-index row from canonical closure metadata.",
            preview=render_archive_index_row(metadata),
            precondition=_precondition(repo_root, index_rel),
            content=index_content,
        ),
    ]


def _cleanup_edit(repo_root: Path, metadata: ClosureMetadata, source_package_path: str) -> PlannedEdit:
    action = "move" if metadata.closure_action == "archived" else "delete"
    destination_path = metadata.package_path if action == "move" else None
    return PlannedEdit(
        edit_id="cleanup_package",
        path=source_package_path,
        action=action,
        reason="Remove or archive the temporary spec package after durable closure metadata is recorded.",
        preview=f"{metadata.closure_action} {source_package_path}" + (f" -> {destination_path}" if destination_path else ""),
        precondition=_precondition(repo_root, source_package_path),
        content=None,
        destination_path=destination_path,
    )


def _resolve_record_edits(repo_root: Path, spec_id: str, cleanup_commit: str) -> list[PlannedEdit]:
    edits = []
    for rel in ["docs/history/spec-closure-log.md", "docs/history/spec-archive-index.md"]:
        text = _read(repo_root / rel)
        replaced = text.replace(PENDING_CLEANUP_COMMIT, cleanup_commit)
        edits.append(
            PlannedEdit(
                edit_id=f"resolve_{Path(rel).stem.replace('-', '_')}",
                path=rel,
                action="update",
                reason=f"Resolve cleanup commit placeholder for {spec_id}.",
                preview=f"{PENDING_CLEANUP_COMMIT} -> {cleanup_commit}",
                precondition=_precondition(repo_root, rel, PENDING_CLEANUP_COMMIT),
                content=replaced,
            )
        )
    return edits


def validate_owned_closure_records(repo_root: Path, metadata: ClosureMetadata) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    log_text = _read(repo_root / "docs/history/spec-closure-log.md")
    index_text = _read(repo_root / "docs/history/spec-archive-index.md")
    owned_values = {
        "spec_id": metadata.spec_id,
        "title": metadata.title,
        "package_path": metadata.package_path,
        "final_spec_commit": metadata.final_spec_commit,
        "cleanup_commit": metadata.cleanup_commit,
        "closure_action": metadata.closure_action,
    }
    for field_name, value in owned_values.items():
        if value and value not in log_text:
            diagnostics.append(Diagnostic("warn", "CLOSURE_LOG_OWNED_FIELD_MISSING", f"Closure log missing {field_name}: {value}.", "docs/history/spec-closure-log.md"))
        if value and value not in index_text:
            diagnostics.append(Diagnostic("warn", "ARCHIVE_INDEX_OWNED_FIELD_MISSING", f"Archive index missing {field_name}: {value}.", "docs/history/spec-archive-index.md"))
    if metadata.cleanup_commit == PENDING_CLEANUP_COMMIT:
        diagnostics.append(Diagnostic("warn", "CLOSURE_RECORD_CLEANUP_COMMIT_PENDING", "Cleanup commit placeholder remains in owned closure records."))
    return diagnostics


def build_validation_plan(repo_root: Path, changed_files: list[str] | None = None, phase: str = "final") -> list[ValidationCommand]:
    changed = changed_files or []
    commands = [
        ValidationCommand("mcp__spec_lifecycle_manager.scan_specs", "Preferred MCP active-spec inventory check.", False, True, phase),
        ValidationCommand("PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .", "No-MCP recovery active-spec inventory check.", True, True, phase),
        ValidationCommand("PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .", "Validate closure-log and archive-index consistency.", True, True, phase),
        ValidationCommand("git diff --check", "Verify whitespace before commit.", True, True, phase),
    ]
    if phase in {"plan", "cleanup"}:
        commands.append(ValidationCommand("mcp__spec_lifecycle_manager.closure_check", "Preferred MCP closure readiness check while the package exists.", False, True, phase))
    if any(path.startswith("skills/spec-lifecycle-manager/scripts/") for path in changed):
        commands.append(ValidationCommand("PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime", "Focused runtime tests for lifecycle script changes.", True, True, phase))
    if any(path.startswith("skills/spec-lifecycle-manager/scripts/spec_mcp_server.py") for path in changed):
        commands.append(ValidationCommand("PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server", "Focused MCP tests for MCP server changes.", True, True, phase))
    if any(path.startswith("plugins/spec-lifecycle-manager/") or path.startswith("packaging/spec-lifecycle-manager/") for path in changed):
        commands.append(ValidationCommand("PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .", "Validate package contract for package or plugin changes.", True, True, phase))
        commands.append(ValidationCommand("PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5", "Validate source, bundle, and install-cache parity.", True, True, phase))
    if any(path.startswith("docs/history/") for path in changed):
        commands.append(ValidationCommand("PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime.SpecRuntimeTests.test_spec_030_closure_fixture_separates_pending_and_resolved_cleanup_metadata", "Focused closure metadata fixture test.", True, False, phase))
    if (repo_root / "package.json").exists():
        commands.append(ValidationCommand("npm run validate", "Repository validation bundle.", True, False, phase))
    return commands


def _step(step_id: str, label: str, ok: bool, *, action_kind: str = "preview_only", blockers: list[Diagnostic] | None = None, evidence: list[str] | None = None) -> ClosureStep:
    return ClosureStep(
        step_id=step_id,
        label=label,
        status="ready" if ok else "blocked",
        action_kind=action_kind,
        blockers=blockers or [],
        evidence=evidence or [],
    )


def closure_plan(
    spec_path: Path,
    *,
    repo_root: Path | None = None,
    final_spec_commit: str | None = None,
    closure_action: str = "removed",
    include_reference_scan: bool = True,
) -> dict[str, Any]:
    root = (repo_root or spec_path.parents[2]).resolve()
    spec = spec_path.resolve()
    rel_spec = _repo_relative(root, spec)
    core = _core_module()

    diagnostics: list[Diagnostic] = []
    candidates = discover_final_spec_commits(root, spec)
    selected_commit = final_spec_commit or (candidates[0].commit if len([item for item in candidates if item.confidence == "high"]) == 1 else "pending")
    if selected_commit == "pending":
        diagnostics.append(Diagnostic("warn", "CLOSURE_FINAL_SPEC_COMMIT_SELECTION_REQUIRED", "Final spec commit must be selected explicitly when candidate evidence is absent or ambiguous."))
    status = ACTION_TO_STATUS.get(closure_action, closure_action)
    package_path = rel_spec
    if closure_action == "archived":
        package_path = f"{DEFAULT_ARCHIVED_SPEC_ROOT}/{spec.name}"
    metadata = ClosureMetadata(
        spec_id=spec.name,
        title=_title_from_requirements(spec),
        package_path=package_path,
        status=status,
        closure_action=closure_action,
        final_spec_commit=selected_commit,
        cleanup_commit=PENDING_CLEANUP_COMMIT,
        durable_destinations=[
            item.get("target")
            for item in core.promotion_plan(spec).get("targets", [])
            if isinstance(item, dict) and item.get("target") and item.get("target") != "TBD"
        ],
        verification_summary="Closure validation not yet executed.",
        residual_risks=[],
        follow_ups=[],
        closed_date=datetime.now(timezone.utc).date().isoformat(),
    )
    metadata_diagnostics = validate_closure_metadata(metadata)
    diagnostics.extend(metadata_diagnostics)
    closure_payload = core.closure_check(spec) if spec.exists() else {"ready": False, "blockers": [{"code": "SPEC_MISSING", "message": "Spec package is missing."}]}
    promotion_payload = core.promotion_plan(spec) if spec.exists() else {"missing_targets": [{"target": "TBD"}]}
    if closure_payload.get("blockers"):
        diagnostics.append(Diagnostic("warn", "CLOSURE_CHECK_BLOCKERS_PRESENT", "Closure check has blockers; cleanup remains manual/blocked until resolved."))
    if promotion_payload.get("missing_targets"):
        diagnostics.append(Diagnostic("error", "CLOSURE_PROMOTION_TARGET_MISSING", "Durable promotion target is missing."))
    references = classify_spec_references(root, spec.name, rel_spec) if include_reference_scan else {}
    if references.get("active_stale"):
        diagnostics.append(Diagnostic("warn", "CLOSURE_ACTIVE_REFERENCES_PRESENT", "Active references require review or explicit planned edits before cleanup."))
    edits = _planned_record_edits(root, metadata) + [_cleanup_edit(root, metadata, rel_spec)]
    actions = [
        ClosureAction("render_records", "render_records", "preview", True, ["render_closure_log", "render_archive_index"]),
        ClosureAction("cleanup_package", "cleanup_package", "preview", True, ["cleanup_package"]),
        ClosureAction("run_validation", "run_validation", "preview", False, [], None),
    ]
    steps = [
        _step("durable_promotion", "Durable promotion review", not promotion_payload.get("missing_targets"), blockers=[Diagnostic("error", "CLOSURE_PROMOTION_TARGET_MISSING", "Durable promotion target is missing.")] if promotion_payload.get("missing_targets") else [], evidence=[str(item.get("target")) for item in promotion_payload.get("targets", []) if isinstance(item, dict)]),
        _step("final_spec_commit", "Final spec commit capture", selected_commit != "pending", action_kind="manual_judgment" if selected_commit == "pending" else "preview_only", blockers=[Diagnostic("warn", "CLOSURE_FINAL_SPEC_COMMIT_SELECTION_REQUIRED", "Select final spec commit.")] if selected_commit == "pending" else [], evidence=[item.commit for item in candidates]),
        _step("records", "Closure-log and archive-index preview", True, action_kind="scriptable"),
        _step("cleanup", "Package cleanup preview", not closure_payload.get("blockers"), action_kind="scriptable", blockers=[Diagnostic("warn", str(item.get("code") or "CLOSURE_BLOCKER"), str(item.get("message") or item)) for item in closure_payload.get("blockers", [])]),
        _step("references", "Active-state reference review", not references.get("active_stale"), action_kind="preview_only"),
        _step("validation", "Validation command planning", True, action_kind="scriptable"),
    ]
    plan_fingerprint = {
        "metadata": metadata.to_dict(),
        "spec_package_hash": _tree_hash(spec),
    }
    plan_id = hashlib.sha256(json.dumps(plan_fingerprint, sort_keys=True).encode("utf-8")).hexdigest()[:12]
    commands = build_validation_plan(root, [edit.path for edit in edits], "cleanup")
    plan = ClosurePlan(
        plan_id=plan_id,
        generated_at=_now(),
        repo_root=".",
        spec_path=rel_spec,
        metadata=metadata,
        steps=steps,
        actions=actions,
        planned_edits=edits,
        validation_commands=commands,
        preconditions=[edit.precondition for edit in edits],
        diagnostics=diagnostics,
        final_spec_commit_candidates=candidates,
        references=references,
    )
    return plan.to_dict()


def _verify_precondition(repo_root: Path, precondition: FilePrecondition) -> Diagnostic | None:
    path = repo_root / precondition.path
    if path.exists() != precondition.exists:
        return Diagnostic("error", "CLOSURE_PRECONDITION_EXISTS_MISMATCH", f"Precondition failed for {precondition.path}: existence changed.", precondition.path)
    current_hash = _path_hash(path)
    if precondition.content_hash != current_hash:
        return Diagnostic("error", "CLOSURE_PRECONDITION_HASH_MISMATCH", f"Precondition failed for {precondition.path}: content changed.", precondition.path)
    if precondition.required_snippet and precondition.required_snippet not in _read(path):
        return Diagnostic("error", "CLOSURE_PRECONDITION_SNIPPET_MISSING", f"Precondition failed for {precondition.path}: required snippet missing.", precondition.path)
    return None


def _select_edits(plan: ClosurePlan, action_id: str) -> tuple[ClosureAction | None, list[PlannedEdit]]:
    action = next((item for item in plan.actions if item.action_id == action_id), None)
    if action is None:
        return None, []
    wanted = set(action.planned_edit_ids)
    return action, [edit for edit in plan.planned_edits if edit.edit_id in wanted]


def _closure_records_match(repo_root: Path, metadata: ClosureMetadata) -> bool:
    log = _read(repo_root / "docs/history/spec-closure-log.md")
    index = _read(repo_root / "docs/history/spec-archive-index.md")
    log_match = re.search(
        rf"(?ms)^### [^\n]+ - {re.escape(metadata.spec_id)}\n.*?(?=^### |\Z)",
        log,
    )
    index_match = re.search(
        rf"(?m)^\|\s*{re.escape(metadata.spec_id)}\s*\|.*$",
        index,
    )
    if not log_match or not index_match:
        return False
    required = (
        metadata.final_spec_commit,
        metadata.cleanup_commit,
        metadata.closure_action,
    )
    return all(value in log_match.group(0) and value in index_match.group(0) for value in required)


def _edit_already_applied(repo_root: Path, edit: PlannedEdit) -> bool:
    target = repo_root / _repo_relative(repo_root, edit.path)
    if edit.action in {"add", "update"}:
        return target.is_file() and _read(target) == (edit.content or "")
    if edit.action == "delete":
        return not target.exists()
    if edit.action == "move" and edit.destination_path:
        return not target.exists() and (repo_root / edit.destination_path).exists()
    return False


def _write_edit(repo_root: Path, edit: PlannedEdit) -> None:
    target = repo_root / _repo_relative(repo_root, edit.path)
    if edit.action in {"add", "update"}:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(edit.content or "", encoding="utf-8")
    elif edit.action == "delete":
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    elif edit.action == "move":
        if not edit.destination_path:
            raise ValueError("Move planned edit missing destination_path.")
        destination = repo_root / _repo_relative(repo_root, edit.destination_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(destination))
    else:
        raise ValueError(f"Unsupported planned edit action: {edit.action}")


def closure_apply(
    spec_path: Path,
    *,
    repo_root: Path | None = None,
    plan: ClosurePlan | dict[str, Any],
    action_id: str,
    dry_run: bool = True,
    write_intent: bool = False,
) -> dict[str, Any]:
    root = (repo_root or spec_path.parents[2]).resolve()
    parsed = parse_closure_plan(plan)
    action, edits = _select_edits(parsed, action_id)
    diagnostics: list[Diagnostic] = []
    if action is None:
        diagnostics.append(Diagnostic("error", "CLOSURE_ACTION_UNKNOWN", f"Unknown action_id: {action_id}."))
    elif action.requires_write_intent and not write_intent and not dry_run:
        diagnostics.append(Diagnostic("error", "CLOSURE_WRITE_INTENT_MISSING", f"{action_id} requires write_intent."))
    if action_id == "cleanup_package" and not _closure_records_match(root, parsed.metadata):
        diagnostics.append(
            Diagnostic(
                "error",
                "CLOSURE_RECORDS_NOT_APPLIED",
                "Matching closure-log and archive-index records must exist before package cleanup.",
            )
        )
    for edit in edits:
        try:
            _repo_relative(root, edit.path)
            if edit.destination_path:
                _repo_relative(root, edit.destination_path)
        except ValueError as exc:
            diagnostics.append(Diagnostic("error", "CLOSURE_EDIT_PATH_INVALID", str(exc), edit.path))
        stale = _verify_precondition(root, edit.precondition)
        if stale:
            diagnostics.append(stale)
    if diagnostics or dry_run:
        return {
            "status": "preview" if not diagnostics else "rejected",
            "dry_run": dry_run,
            "action_id": action_id,
            "changed_files": [],
            "planned_files": [edit.path for edit in edits],
            "diagnostics": [item.to_dict() for item in diagnostics],
            "validation_commands": [item.to_dict() for item in parsed.validation_commands],
            "mutates_files": False,
        }
    if edits and all(_edit_already_applied(root, edit) for edit in edits):
        return {
            "status": "already_applied",
            "dry_run": dry_run,
            "action_id": action_id,
            "changed_files": [],
            "planned_files": [edit.path for edit in edits],
            "diagnostics": [],
            "validation_commands": [item.to_dict() for item in parsed.validation_commands],
            "mutates_files": False,
        }
    changed: list[str] = []
    intended = [edit.path for edit in edits]
    try:
        for edit in edits:
            _write_edit(root, edit)
            changed.append(edit.path)
    except OSError as exc:
        diagnostics.append(Diagnostic("error", "CLOSURE_PARTIAL_WRITE_FAILURE", str(exc)))
        return {
            "status": "partial_failure",
            "dry_run": dry_run,
            "action_id": action_id,
            "changed_files": changed,
            "intended_files": intended,
            "diagnostics": [item.to_dict() for item in diagnostics],
            "validation_commands": [item.to_dict() for item in parsed.validation_commands],
            "mutates_files": True,
        }
    return {
        "status": "updated",
        "dry_run": dry_run,
        "action_id": action_id,
        "changed_files": changed,
        "intended_files": intended,
        "diagnostics": [],
        "validation_commands": [item.to_dict() for item in parsed.validation_commands],
        "mutates_files": True,
    }


def _head_commit(repo_root: Path) -> str:
    result = _git(repo_root, "rev-parse", "--short=12", "HEAD")
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def closure_resolve(
    repo_root: Path,
    *,
    spec_id: str,
    cleanup_commit: str | None = None,
    dry_run: bool = True,
    write_intent: bool = False,
) -> dict[str, Any]:
    root = repo_root.resolve()
    resolved = cleanup_commit or _head_commit(root)
    metadata = ClosureMetadata(
        spec_id=spec_id,
        title=spec_id,
        package_path=f"docs/specs/{spec_id}",
        cleanup_commit=resolved,
        final_spec_commit="provided",
        verification_summary="Cleanup commit resolved.",
    )
    edits = _resolve_record_edits(root, spec_id, resolved)
    plan = ClosurePlan(
        plan_id=_slug(f"resolve-{spec_id}-{resolved}"),
        generated_at=_now(),
        repo_root=".",
        spec_path=f"docs/specs/{spec_id}",
        metadata=metadata,
        steps=[],
        actions=[ClosureAction("resolve_cleanup_hash", "resolve_cleanup_hash", "preview", True, [edit.edit_id for edit in edits])],
        planned_edits=edits,
        validation_commands=build_validation_plan(root, [edit.path for edit in edits], "resolve"),
        preconditions=[edit.precondition for edit in edits],
    )
    return closure_apply(root / metadata.package_path, repo_root=root, plan=plan, action_id="resolve_cleanup_hash", dry_run=dry_run, write_intent=write_intent)
