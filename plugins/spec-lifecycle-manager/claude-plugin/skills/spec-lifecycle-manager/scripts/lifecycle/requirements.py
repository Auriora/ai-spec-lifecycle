"""Shared requirement parsing helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


REQ_HEADING_RE = re.compile(r"^###\s+(Requirement\s+[^:]+):?\s*(.*?)\s*$")
AC_HEADING_RE = re.compile(r"^#{4}\s+Acceptance Criteria\b", re.IGNORECASE)
SUBHEADING_RE = re.compile(r"^#{4}\s+")
PRIORITY_RE = re.compile(r"^\s*\*\*Priority:\*\*\s*(.+?)\s*$", re.IGNORECASE)
CANONICAL_PRIORITIES = {"must-have", "should-have", "could-have"}
SHORTHAND_PRIORITIES = {
    "must": "must-have",
    "must have": "must-have",
    "musthave": "must-have",
    "should": "should-have",
    "should have": "should-have",
    "shouldhave": "should-have",
    "could": "could-have",
    "could have": "could-have",
    "couldhave": "could-have",
}
EXCLUSION_PRIORITIES = {"wont-have", "won't-have", "wont have", "won't have", "will-not-have", "will not have"}


def strip_priority_value(value: str) -> str:
    return value.strip().strip("`").strip().rstrip(".").strip()


def normalize_priority_value(value: str) -> str:
    return re.sub(r"\s+", " ", strip_priority_value(value).lower())


def parse_priority_lines(block_lines: list[str], requirement_id: str, start_line: int) -> tuple[str | None, list[dict[str, Any]]]:
    priority: str | None = None
    diagnostics: list[dict[str, Any]] = []
    seen_line: int | None = None
    for offset, line in enumerate(block_lines, start=0):
        match = PRIORITY_RE.match(line)
        if not match:
            continue
        line_number = start_line + offset
        raw_value = strip_priority_value(match.group(1))
        normalized = normalize_priority_value(raw_value)
        if seen_line is not None:
            diagnostics.append(
                {
                    "severity": "warn",
                    "code": "REQUIREMENT_PRIORITY_DUPLICATE",
                    "line": line_number,
                    "message": f"{requirement_id} has multiple priority lines; keep exactly one requirement-level priority.",
                    "requirement_id": requirement_id,
                    "priority": raw_value,
                }
            )
            continue
        seen_line = line_number
        if normalized in CANONICAL_PRIORITIES:
            priority = normalized
        elif normalized in SHORTHAND_PRIORITIES:
            canonical = SHORTHAND_PRIORITIES[normalized]
            diagnostics.append(
                {
                    "severity": "warn",
                    "code": "REQUIREMENT_PRIORITY_SHORTHAND",
                    "line": line_number,
                    "message": f"{requirement_id} priority `{raw_value}` must be persisted as `{canonical}`.",
                    "requirement_id": requirement_id,
                    "priority": raw_value,
                    "canonical_priority": canonical,
                }
            )
        elif normalized in EXCLUSION_PRIORITIES:
            diagnostics.append(
                {
                    "severity": "warn",
                    "code": "REQUIREMENT_PRIORITY_EXCLUSION_VALUE",
                    "line": line_number,
                    "message": (
                        f"{requirement_id} uses `{raw_value}` as accepted priority; excluded scope belongs in "
                        "non-goals, out-of-scope text, rejected decisions, or routed residuals."
                    ),
                    "requirement_id": requirement_id,
                    "priority": raw_value,
                }
            )
        else:
            diagnostics.append(
                {
                    "severity": "warn",
                    "code": "REQUIREMENT_PRIORITY_UNKNOWN",
                    "line": line_number,
                    "message": (
                        f"{requirement_id} priority `{raw_value}` is not recognized; use `must-have`, "
                        "`should-have`, or `could-have`."
                    ),
                    "requirement_id": requirement_id,
                    "priority": raw_value,
                }
            )
    return priority, diagnostics


def extract_acceptance_criteria(block_lines: list[str], requirement_id: str) -> list[dict[str, str]]:
    criteria: list[dict[str, str]] = []
    in_acceptance = False
    current_number: str | None = None
    current_text: list[str] = []
    for line in block_lines:
        if AC_HEADING_RE.match(line):
            in_acceptance = True
            continue
        if in_acceptance and SUBHEADING_RE.match(line):
            break
        if not in_acceptance:
            continue
        item = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
        if item:
            if current_number:
                text = " ".join(current_text).strip()
                criteria.append(
                    {
                        "id": f"{requirement_id} AC{current_number}",
                        "number": current_number,
                        "text": text,
                        "source": f"{current_number}. {text}",
                    }
                )
            current_number = item.group(1)
            current_text = [item.group(2).strip()]
        elif current_number and line.strip():
            current_text.append(line.strip())
    if current_number:
        text = " ".join(current_text).strip()
        criteria.append(
            {
                "id": f"{requirement_id} AC{current_number}",
                "number": current_number,
                "text": text,
                "source": f"{current_number}. {text}",
            }
        )
    return criteria


def requirement_blocks_from_text(text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        match = REQ_HEADING_RE.match(line)
        if match:
            starts.append((idx, match.group(1).strip()))
    blocks: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for pos, (start, req_id) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        for idx in range(start + 1, end):
            if lines[idx].startswith("## ") and not lines[idx].startswith("### "):
                end = idx
                break
        block_lines = lines[start:end]
        priority, priority_diagnostics = parse_priority_lines(block_lines, req_id, start + 1)
        diagnostics.extend(priority_diagnostics)
        block = {
            "id": req_id,
            "text": "\n".join(block_lines),
            "acceptance_criteria": extract_acceptance_criteria(block_lines, req_id),
        }
        if priority:
            block["priority"] = priority
        blocks.append(block)
    return blocks, diagnostics


def requirement_blocks(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not path.exists():
        return [], []
    return requirement_blocks_from_text(path.read_text(encoding="utf-8"))
