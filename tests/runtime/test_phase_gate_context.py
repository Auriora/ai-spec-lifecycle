import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle import core


FRONTMATTER = """---
title: {title}
doc_type: spec
artifact_type: {artifact}
status: {status}
owner: platform
last_reviewed: 2026-07-12
---
"""


class PhaseGateContextTests(unittest.TestCase):
    def write(self, spec: Path, name: str, body: str, status: str = "active") -> None:
        (spec / name).write_text(
            FRONTMATTER.format(title=name, artifact=name.removesuffix(".md"), status=status) + body,
            encoding="utf-8",
        )

    def base_spec(self, root: Path, status: str = "active") -> Path:
        (root / ".git").mkdir(exist_ok=True)
        spec = root / "docs/specs/001-example"
        spec.mkdir(parents=True)
        self.write(
            spec,
            "requirements.md",
            """# Requirements

## Requirements

### Requirement 1: Example

1. GIVEN input WHEN checked THEN THE SYSTEM SHALL report output.

## Correctness Properties

- CP-001: Output is deterministic.
""",
            status,
        )
        return spec

    def fingerprint(self, spec: Path, artifact: str) -> str:
        return core._artifact_evidence_fingerprint(spec, artifact)

    def record_fingerprints(self, spec: Path, artifact: str, upstreams: list[str]) -> None:
        path = spec / artifact
        rows = "\n".join(
            f"| `{core._repo_relative_artifact_identity(spec, upstream)}` | "
            f"`{self.fingerprint(spec, upstream)}` |"
            for upstream in upstreams
        )
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n## Upstream Fingerprints\n\n"
            + "| Upstream Artifact | Fingerprint |\n|---|---|\n"
            + rows
            + "\n",
            encoding="utf-8",
        )

    def add_design(self, spec: Path) -> None:
        self.write(
            spec,
            "design.md",
            """# Design
## Overview
Example.
## High-Level Design
Example.
## Low-Level Design
Example.
## Operational Considerations
Example.
## Open Questions
None.
""",
        )

    def add_tasks(self, spec: Path, marker: str = " ", evidence: str = "pending") -> None:
        self.write(
            spec,
            "tasks.md",
            f"""# Tasks
- [{marker}] T001 Implement example
  - Acceptance: output is deterministic.
  - Evidence: {evidence}
""",
        )

    def add_traceability(self, spec: Path) -> None:
        self.write(
            spec,
            "traceability.md",
            """# Traceability
## Task To Context Matrix
| Task | Requirements |
|---|---|
| T001 | Requirement 1 |
## Requirement To Delivery Matrix
| Requirement | Tasks |
|---|---|
| Requirement 1 | T001 |
## Design To Implementation Matrix
| Design | Task |
|---|---|
| Low-Level Design | T001 |
## Open Decision Impact
None.
""",
        )

    def add_verification(self, spec: Path, promoted: bool = False) -> None:
        evidence = "`python3 -m unittest`: 1 test passed"
        if promoted:
            evidence += "; durable documentation promoted in `docs/reference/runtime.md`"
        self.write(
            spec,
            "verification.md",
            f"""# Verification
## Quality Gates
- Unit tests pass.
## Evidence Log
- {evidence}
## Residual Risks
None.
""",
        )

    def test_infers_all_public_phases_and_lazy_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing = core.phase_gate_context(root / "missing")
            self.assertEqual(("missing", "unknown"), (missing["applicability"], missing["phase"]))

            unknown = root / "docs/specs/000-unknown"
            unknown.mkdir(parents=True)
            self.assertEqual("unknown", core.phase_gate_context(unknown)["phase"])

            spec = self.base_spec(root)
            self.assertEqual("requirements", core.phase_gate_context(spec)["phase"])
            self.add_design(spec)
            self.assertEqual("design", core.phase_gate_context(spec)["phase"])
            self.add_tasks(spec)
            self.assertEqual("tasks", core.phase_gate_context(spec)["phase"])
            self.add_traceability(spec)
            implementation = core.phase_gate_context(spec)
            self.assertEqual("implementation", implementation["phase"])
            self.assertNotIn("validation_plan", [item["source"] for item in implementation["sources"]])

            self.add_tasks(spec, "x", "`tests/test_example.py`: 1 test passed")
            verification = core.phase_gate_context(spec)
            self.assertEqual("verification", verification["phase"])
            self.assertIn("validation_plan", [item["source"] for item in verification["sources"]])

            self.add_verification(spec)
            promotion = core.phase_gate_context(spec)
            self.assertEqual("promotion", promotion["phase"])
            self.assertIn("promotion_plan", [item["source"] for item in promotion["sources"]])

            self.add_verification(spec, promoted=True)
            closure = core.phase_gate_context(spec)
            self.assertEqual("closure", closure["phase"])
            self.assertEqual("closure_check", closure["sources"][-1]["source"])
            self.assertLessEqual(len(closure["sources"]), 7)

    def test_archived_is_not_applicable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp), status="archived")
            payload = core.phase_gate_context(spec)
        self.assertEqual("not_applicable", payload["applicability"])
        self.assertEqual("unknown", payload["phase"])
        self.assertEqual([], payload["sources"])

    def test_unresolved_decision_and_lint_meaning_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            (spec / "open-decisions.md").write_text(
                "| D001 | Select policy | owner |\n", encoding="utf-8"
            )
            payload = core.phase_gate_context(spec)

        stage = payload["sources"][0]
        decision = stage["findings"][0]
        self.assertEqual("error", decision["severity"])
        self.assertEqual("OPEN_DECISION_UNRESOLVED", decision["code"])
        self.assertEqual("D001", decision["reference"])
        lint = payload["sources"][1]
        for finding in lint["findings"]:
            self.assertIn("severity", finding)
            self.assertIn("code", finding)
            self.assertIn("path", finding)

    def test_source_order_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            first = core.phase_gate_context(spec)
            second = core.phase_gate_context(spec)
        self.assertEqual(
            [item["source"] for item in first["sources"]],
            [item["source"] for item in second["sources"]],
        )

    def test_matching_and_changed_upstream_fingerprints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            self.add_design(spec)
            self.record_fingerprints(spec, "design.md", ["requirements.md"])
            current = core.phase_gate_context(spec)["artifact_freshness"][0]
            self.assertEqual("current", current["status"])

            requirements = spec / "requirements.md"
            requirements.write_text(
                requirements.read_text(encoding="utf-8") + "\nChanged decision.\n",
                encoding="utf-8",
            )
            stale = core.phase_gate_context(spec)["artifact_freshness"][0]
            self.assertEqual("stale", stale["status"])
            self.assertIn("reconciliation_action", stale)
            self.assertNotEqual(
                stale["upstreams"][0]["recorded_fingerprint"],
                stale["upstreams"][0]["current_fingerprint"],
            )

    def test_missing_record_is_review_required_and_mtime_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            self.add_design(spec)
            missing = core.phase_gate_context(spec)["artifact_freshness"][0]
            self.assertEqual("review_required", missing["status"])

            self.record_fingerprints(spec, "design.md", ["requirements.md"])
            before = core.phase_gate_context(spec)["artifact_freshness"]
            requirements = spec / "requirements.md"
            stat = requirements.stat()
            os.utime(requirements, (stat.st_atime + 20, stat.st_mtime + 20))
            after = core.phase_gate_context(spec)["artifact_freshness"]
            self.assertEqual(before, after)
            self.assertEqual("current", after[0]["status"])

    def test_multiple_upstreams_are_ordered_and_gate_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            self.add_design(spec)
            self.add_tasks(spec)
            self.add_traceability(spec)
            self.add_verification(spec)
            for artifact in ("tasks.md", "traceability.md", "verification.md"):
                self.record_fingerprints(
                    spec, artifact, ["requirements.md", "design.md"]
                )
            before = {
                path.name: (path.read_bytes(), path.stat().st_mtime_ns)
                for path in spec.iterdir()
            }
            first = core.phase_gate_context(spec)["artifact_freshness"]
            second = core.phase_gate_context(spec)["artifact_freshness"]
            after = {
                path.name: (path.read_bytes(), path.stat().st_mtime_ns)
                for path in spec.iterdir()
            }

            self.assertEqual(first, second)
            self.assertEqual(before, after)
            self.assertEqual(
                ["design.md", "tasks.md", "traceability.md", "verification.md"],
                [item["artifact"] for item in first],
            )
            for item in first[1:]:
                self.assertEqual("current", item["status"])
                self.assertEqual(
                    [
                        core._repo_relative_artifact_identity(spec, "requirements.md"),
                        core._repo_relative_artifact_identity(spec, "design.md"),
                    ],
                    [upstream["artifact"] for upstream in item["upstreams"]],
                )


if __name__ == "__main__":
    unittest.main()
