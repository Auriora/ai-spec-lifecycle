import os
import sys
import tempfile
import unittest
from unittest import mock
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

    def test_compact_is_deterministic_bounded_and_prioritizes_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            context = core.phase_gate_context(spec)
            context["sources"] = [
                {
                    "source": "lint_spec_package",
                    "status": "findings",
                    "finding_count": 26,
                    "findings": [
                        {
                            "severity": "error" if index >= 5 else "warn",
                            "code": f"CODE_{index:02d}",
                            "path": str(spec / "requirements.md"),
                            "reference": f"R{index:02d}",
                            "waivable": index < 5,
                        }
                        for index in range(26)
                    ],
                }
            ]
            with mock.patch.object(core, "phase_gate_context", return_value=context):
                first = core.phase_gate_check(spec)
                second = core.phase_gate_check(spec)

        self.assertEqual(first, second)
        self.assertEqual(20, len(first["findings"]))
        self.assertLessEqual(len(first["next_actions"]), 10)
        self.assertTrue(first["limits"]["findings"]["truncated"])
        self.assertTrue(first["limits"]["limit_exceeded"])
        self.assertTrue(all(item["severity"] == "error" for item in first["findings"]))
        self.assertNotIn(str(spec.parent.parent.parent), str(first))

    def test_explicit_warning_blocker_is_preserved_and_precedes_source_advice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            context = core.phase_gate_context(spec)
            advice = [
                {
                    "severity": "warn",
                    "code": f"ADVISORY_{index:02d}",
                    "advisory": True,
                    "waivable": True,
                }
                for index in range(21)
            ]
            warning_blocker = {
                "severity": "warn",
                "code": "AUTHORITATIVE_WARNING_BLOCKER",
                "source": "governance-policy",
                "authority": "canonical",
                "proof": "recorded",
                "blocking": True,
                "advisory": False,
                "waivable": False,
            }
            context["sources"] = [
                core._phase_gate_source(
                    "lint_spec_package",
                    status="findings",
                    findings=[*advice, warning_blocker],
                )
            ]
            with mock.patch.object(core, "phase_gate_context", return_value=context):
                compact = core.phase_gate_check(spec)
                section = core.phase_gate_check(
                    spec, detail="section", section="source_signals"
                )

        surfaced = compact["findings"][0]
        self.assertEqual("AUTHORITATIVE_WARNING_BLOCKER", surfaced["code"])
        self.assertTrue(surfaced["blocking"])
        self.assertEqual("canonical", surfaced["authority"])
        self.assertEqual("recorded", surfaced["proof"])
        self.assertFalse(compact["decision"]["ready_to_advance"])
        source = section["content"]["sources"][0]
        self.assertEqual("AUTHORITATIVE_WARNING_BLOCKER", source["findings"][0]["code"])
        self.assertEqual(
            {"returned": 20, "total": 22, "limit": 20, "truncated": True},
            source["finding_limits"],
        )

    def test_render_modes_share_fingerprint_and_sections_are_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            self.add_design(spec)
            compact = core.phase_gate_check(spec)
            full = core.phase_gate_check(spec, detail="full")
            sections = {
                section: core.phase_gate_check(spec, detail="section", section=section)
                for section in core.PHASE_GATE_SECTIONS
            }

        self.assertEqual(compact["evidence_fingerprint"], full["evidence_fingerprint"])
        self.assertTrue(
            all(
                payload["evidence_fingerprint"] == compact["evidence_fingerprint"]
                for payload in sections.values()
            )
        )
        self.assertLessEqual(len(full["context"]["sources"]), 7)
        self.assertEqual(set(core.PHASE_GATE_SECTIONS), set(sections))

    def test_invalid_detail_section_combinations_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            with self.assertRaises(ValueError):
                core.phase_gate_check(spec, detail="verbose")
            with self.assertRaises(ValueError):
                core.phase_gate_check(spec, section="coverage")
            with self.assertRaises(ValueError):
                core.phase_gate_check(spec, detail="section")
            with self.assertRaises(ValueError):
                core.phase_gate_check(spec, detail="section", section="everything")

    def test_wording_only_content_change_and_mtime_do_not_change_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            before = core.phase_gate_check(spec)["evidence_fingerprint"]
            requirements = spec / "requirements.md"
            stat = requirements.stat()
            os.utime(requirements, (stat.st_atime + 10, stat.st_mtime + 10))
            self.assertEqual(before, core.phase_gate_check(spec)["evidence_fingerprint"])
            requirements.write_text(
                requirements.read_text(encoding="utf-8") + "\nAdditional explanatory wording.\n",
                encoding="utf-8",
            )
            after = core.phase_gate_check(spec)["evidence_fingerprint"]
        self.assertEqual(before, after)

    def test_stale_expansion_returns_refreshed_same_tool_follow_up(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            self.add_design(spec)
            self.record_fingerprints(spec, "design.md", ["requirements.md"])
            original = core.phase_gate_check(spec)
            (spec / "requirements.md").write_text(
                (spec / "requirements.md").read_text(encoding="utf-8") + "\nChanged.\n",
                encoding="utf-8",
            )
            stale = core.phase_gate_check(
                spec,
                detail="section",
                section="coverage",
                expected_fingerprint=original["evidence_fingerprint"],
            )

        self.assertEqual("stale", stale["status"])
        self.assertEqual(original["evidence_fingerprint"], stale["requested_fingerprint"])
        self.assertNotEqual(
            stale["requested_fingerprint"], stale["current_evidence_fingerprint"]
        )
        self.assertEqual("phase_gate_check", stale["expansion"]["tool"])
        self.assertEqual(
            stale["current_evidence_fingerprint"],
            stale["expansion"]["arguments"]["expected_fingerprint"],
        )
        self.assertEqual("coverage", stale["expansion"]["arguments"]["section"])

    def test_outputs_exclude_metadata_absolute_paths_commands_and_verbose_messages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            payloads = [
                core.phase_gate_check(spec),
                core.phase_gate_check(spec, detail="full"),
                core.phase_gate_check(spec, detail="section", section="source_signals"),
            ]
            host_prefix = str(Path(tmp))

        for payload in payloads:
            rendered = str(payload)
            self.assertNotIn("lifecycle_metadata", payload)
            self.assertNotIn(host_prefix, rendered)
            self.assertNotIn("host_command", rendered)
            self.assertNotIn("message", rendered)

    def test_ready_to_advance_is_conservative_for_stale_and_open_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.base_spec(Path(tmp))
            ready = core.phase_gate_check(spec)
            self.assertTrue(ready["decision"]["ready_to_advance"])
            self.add_design(spec)
            self.record_fingerprints(spec, "design.md", ["requirements.md"])
            (spec / "requirements.md").write_text(
                (spec / "requirements.md").read_text(encoding="utf-8") + "\nChanged.\n",
                encoding="utf-8",
            )
            stale = core.phase_gate_check(spec)
            self.assertFalse(stale["decision"]["ready_to_advance"])
            (spec / "open-decisions.md").write_text(
                "| D001 | Choose policy | owner |\n", encoding="utf-8"
            )
            blocked = core.phase_gate_check(spec)
        self.assertFalse(blocked["decision"]["ready_to_advance"])
        self.assertIn(
            "OPEN_DECISION_UNRESOLVED",
            {item["code"] for item in blocked["findings"]},
        )


if __name__ == "__main__":
    unittest.main()
