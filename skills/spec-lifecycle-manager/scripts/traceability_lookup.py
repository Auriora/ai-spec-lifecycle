#!/usr/bin/env python3
"""Lookup spec context from a traceability matrix.

This script is intentionally dependency-free so it can run from a checked-out
skill, from hooks, or behind a future MCP tool.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TASK_RE = re.compile(r"\bT\d{3}(?:\.\d+)?\b")
REQ_RE = re.compile(r"\bRequirement\s+\d+[A-Z]?\b", re.IGNORECASE)
MD_PATH_RE = re.compile(r"`([^`]+\.md(?:#[^`]+)?)`|\[([^\]]+)\]\(([^)]+\.md(?:#[^)]+)?)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TASK_LINE_RE = re.compile(r"^\s*-\s+\[[ xX~Yy*eE]\]\s+(T\d{3}(?:\.\d+)?)\b.*$")


@dataclass
class MarkdownDoc:
    path: Path
    text: str
    headings: dict[str, str]


def slugify(title: str) -> str:
    title = re.sub(r"`([^`]+)`", r"\1", title.strip().lower())
    title = re.sub(r"[^a-z0-9\s-]", "", title)
    title = re.sub(r"\s+", "-", title)
    title = re.sub(r"-+", "-", title)
    return title.strip("-")


def read_doc(path: Path) -> MarkdownDoc | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    headings: dict[str, str] = {}
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        title = match.group(2).strip()
        headings[slugify(title)] = title
    return MarkdownDoc(path=path, text=text, headings=headings)


def split_table_row(line: str) -> list[str]:
    return [cell.strip().replace("<br>", "\n") for cell in line.strip().strip("|").split("|")]


def parse_tables(text: str) -> dict[str, list[dict[str, str]]]:
    tables: dict[str, list[dict[str, str]]] = {}
    current_heading = "Untitled"
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        heading = HEADING_RE.match(lines[i])
        if heading:
            current_heading = heading.group(2).strip()
            i += 1
            continue
        if (
            lines[i].lstrip().startswith("|")
            and i + 1 < len(lines)
            and re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1])
        ):
            headers = split_table_row(lines[i])
            rows: list[dict[str, str]] = []
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                values = split_table_row(lines[i])
                row = {headers[idx]: values[idx] if idx < len(values) else "" for idx in range(len(headers))}
                rows.append(row)
                i += 1
            tables[current_heading] = rows
            continue
        i += 1
    return tables


def normalize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"`|\[|\]|\([^)]*\)", "", value)).strip().lower()


def split_refs(value: str) -> list[str]:
    if not value:
        return []
    parts = re.split(r",|\n|;", value)
    refs: list[str] = []
    for part in parts:
        clean = part.strip().strip("`")
        if clean and clean.lower() not in {"none", "n/a", "na"}:
            refs.append(clean)
    return refs


def extract_task_blocks(text: str) -> dict[str, str]:
    lines = text.splitlines()
    starts: list[tuple[str, int]] = []
    for idx, line in enumerate(lines):
        match = TASK_LINE_RE.match(line)
        if match:
            starts.append((match.group(1), idx))
    blocks: dict[str, str] = {}
    for pos, (task_id, start) in enumerate(starts):
        end = starts[pos + 1][1] if pos + 1 < len(starts) else len(lines)
        for idx in range(start + 1, end):
            if lines[idx].startswith("## "):
                end = idx
                break
        blocks[task_id] = "\n".join(lines[start:end]).strip()
    return blocks


def extract_requirement_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^###\s+(Requirement\s+\d+[A-Z]?:?.*)$", text, re.MULTILINE))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = match.group(1).strip()
        req_id = REQ_RE.search(title)
        if req_id:
            sections[req_id.group(0).lower()] = text[start:end].strip()
    return sections


def extract_acceptance_criteria(requirement_block: str) -> list[str]:
    criteria: list[str] = []
    in_ac = False
    current: list[str] = []
    for line in requirement_block.splitlines():
        if re.match(r"^#{4}\s+Acceptance Criteria\b", line):
            in_ac = True
            continue
        if in_ac and line.startswith("#### "):
            break
        if not in_ac:
            continue
        if re.match(r"^\d+\.\s+", line):
            if current:
                criteria.append(" ".join(current))
            current = [line.strip()]
        elif current and (line.startswith("   ") or line.startswith("      ")):
            current.append(line.strip())
    if current:
        criteria.append(" ".join(current))
    return criteria


def referenced_markdown_paths(row: dict[str, str]) -> list[str]:
    refs: list[str] = []
    for value in row.values():
        for match in MD_PATH_RE.finditer(value):
            refs.append(next(group for group in match.groups() if group))
    return refs


def find_table_row(rows: list[dict[str, str]], column: str, lookup: str) -> dict[str, str] | None:
    target = normalize_cell(lookup)
    for row in rows:
        cell = normalize_cell(row.get(column, ""))
        refs = [normalize_cell(ref) for ref in split_refs(row.get(column, ""))]
        if cell == target or target in refs or target in cell:
            return row
    return None


def load_spec(spec_path: Path) -> tuple[dict[str, MarkdownDoc], list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    docs: dict[str, MarkdownDoc] = {}
    gaps: list[dict[str, str]] = []
    for name in [
        "requirements.md",
        "design.md",
        "tasks.md",
        "change-impact.md",
        "verification.md",
        "open-decisions.md",
        "traceability.md",
    ]:
        doc = read_doc(spec_path / name)
        if doc:
            docs[name] = doc
    traceability = docs.get("traceability.md")
    if not traceability:
        gaps.append(
            {
                "severity": "error",
                "code": "TRACEABILITY_MISSING",
                "message": f"No traceability.md found under {spec_path}",
            }
        )
        return docs, gaps, {}
    return docs, gaps, parse_tables(traceability.text)


def find_repo_root(path: Path) -> Path:
    for candidate in [path, *path.parents]:
        if (candidate / ".git").exists():
            return candidate
    return Path.cwd()


def resolve_reference(spec_path: Path, ref: str) -> Path:
    path_part = ref.partition("#")[0]
    spec_relative = (spec_path / path_part).resolve()
    if spec_relative.exists():
        return spec_relative
    return (find_repo_root(spec_path) / path_part).resolve()


def add_reference_gaps(spec_path: Path, docs: dict[str, MarkdownDoc], row: dict[str, str], gaps: list[dict[str, str]]) -> None:
    for key, value in row.items():
        if re.search(r"\bTBD\b|\bunknown\b", value, re.IGNORECASE):
            gaps.append(
                {
                    "severity": "warn",
                    "code": "TRACEABILITY_UNRESOLVED_VALUE",
                    "field": key,
                    "message": f"{key} contains unresolved value: {value}",
                }
            )
    for ref in referenced_markdown_paths(row):
        path_part, _, anchor = ref.partition("#")
        target = resolve_reference(spec_path, ref)
        if not target.exists():
            gaps.append(
                {
                    "severity": "error",
                    "code": "TRACEABILITY_REFERENCE_MISSING",
                    "reference": ref,
                    "message": f"Referenced artifact does not exist: {ref}",
                }
            )
            continue
        if anchor:
            doc = docs.get(path_part) or read_doc(target)
            if doc and anchor not in doc.headings:
                gaps.append(
                    {
                        "severity": "warn",
                        "code": "TRACEABILITY_ANCHOR_NOT_FOUND",
                        "reference": ref,
                        "message": f"Referenced heading anchor was not found: {ref}",
                    }
                )


def task_lookup(spec_path: Path, task_id: str) -> dict[str, Any]:
    docs, gaps, tables = load_spec(spec_path)
    row = find_table_row(tables.get("Task To Context Matrix", []), "Task ID", task_id)
    if not row:
        gaps.append(
            {
                "severity": "error",
                "code": "TRACEABILITY_TASK_ROW_MISSING",
                "task_id": task_id,
                "message": f"No Task To Context Matrix row found for {task_id}",
            }
        )
        return base_payload(spec_path, "task", task_id, None, gaps)

    add_reference_gaps(spec_path, docs, row, gaps)
    tasks_doc = docs.get("tasks.md")
    task_block = extract_task_blocks(tasks_doc.text).get(task_id) if tasks_doc else None
    if not task_block:
        gaps.append(
            {
                "severity": "error",
                "code": "TASK_SOURCE_NOT_FOUND",
                "task_id": task_id,
                "message": f"{task_id} was not found in tasks.md",
            }
        )

    requirements = collect_requirements(docs.get("requirements.md"), row.get("Requirements", ""))
    if not requirements:
        gaps.append(
            {
                "severity": "warn",
                "code": "REQUIREMENT_CONTEXT_NOT_FOUND",
                "message": f"No matching requirement section found for {row.get('Requirements', '')}",
            }
        )

    payload = base_payload(spec_path, "task", task_id, row, gaps)
    payload["task"] = {"id": task_id, "source": task_block}
    payload["requirements"] = requirements
    payload["acceptance_criteria"] = row.get("Acceptance Criteria", "")
    payload["design_sections"] = split_refs(row.get("Design Sections", ""))
    payload["change_impact"] = row.get("Change Impact", "")
    payload["verification"] = row.get("Verification", "")
    payload["durable_targets"] = split_refs(row.get("Durable Targets", ""))
    payload["open_decisions"] = split_refs(row.get("Open Decisions", ""))
    return payload


def collect_requirements(doc: MarkdownDoc | None, value: str) -> list[dict[str, Any]]:
    if not doc:
        return []
    sections = extract_requirement_sections(doc.text)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for match in REQ_RE.finditer(value):
        req_id = match.group(0).lower()
        if req_id in sections and req_id not in seen:
            seen.add(req_id)
            results.append(
                {
                    "id": match.group(0),
                    "source": sections[req_id],
                    "acceptance_criteria": extract_acceptance_criteria(sections[req_id]),
                }
            )
    return results


def reverse_lookup(spec_path: Path, kind: str, value: str) -> dict[str, Any]:
    docs, gaps, tables = load_spec(spec_path)
    if kind == "requirement":
        table = "Requirement To Delivery Matrix"
        column = "Requirement"
    elif kind == "design":
        table = "Design To Implementation Matrix"
        column = "Design Section"
    else:
        raise ValueError(f"Unsupported reverse lookup kind: {kind}")

    row = find_table_row(tables.get(table, []), column, value)
    if not row:
        gaps.append(
            {
                "severity": "error",
                "code": "TRACEABILITY_ROW_MISSING",
                "lookup": value,
                "message": f"No {table} row found for {value}",
            }
        )
        return base_payload(spec_path, kind, value, None, gaps)
    add_reference_gaps(spec_path, docs, row, gaps)
    return base_payload(spec_path, kind, value, row, gaps)


def base_payload(
    spec_path: Path,
    lookup_type: str,
    lookup_value: str,
    row: dict[str, str] | None,
    gaps: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "spec_path": str(spec_path),
        "lookup": {"type": lookup_type, "value": lookup_value},
        "traceability_row": row,
        "gaps": gaps,
    }


def format_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Spec: {payload['spec_path']}",
        f"Lookup: {payload['lookup']['type']} {payload['lookup']['value']}",
    ]
    row = payload.get("traceability_row")
    if row:
        lines.append("")
        lines.append("Traceability:")
        for key, value in row.items():
            lines.append(f"- {key}: {value}")
    if payload.get("task", {}).get("source"):
        lines.append("")
        lines.append("Task Source:")
        lines.append(payload["task"]["source"])
    if payload.get("requirements"):
        lines.append("")
        lines.append("Requirements:")
        for req in payload["requirements"]:
            lines.append(f"- {req['id']}")
            for ac in req["acceptance_criteria"]:
                lines.append(f"  {ac}")
    if payload.get("gaps"):
        lines.append("")
        lines.append("Gaps:")
        for gap in payload["gaps"]:
            lines.append(f"- {gap['severity']} {gap['code']}: {gap['message']}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lookup task/spec context from traceability.md.")
    parser.add_argument("spec_path", type=Path, help="Path to a spec package.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task", help="Task ID to look up, for example T012.")
    group.add_argument("--requirement", help="Requirement ID/title to reverse look up.")
    group.add_argument("--design", help="Design section reference to reverse look up.")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    spec_path = args.spec_path.resolve()
    if args.task:
        payload = task_lookup(spec_path, args.task)
    elif args.requirement:
        payload = reverse_lookup(spec_path, "requirement", args.requirement)
    else:
        payload = reverse_lookup(spec_path, "design", args.design)

    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_text(payload))
    return 1 if any(gap["severity"] == "error" for gap in payload["gaps"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
