import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
SCRIPT = SCRIPT_DIR / "spec_runtime.py"
SPEC = ROOT / "docs/specs/004-spec-management-mcp"
sys.path.insert(0, str(SCRIPT_DIR))

import spec_runtime


class SpecRuntimeTests(unittest.TestCase):
    def test_scan_discovers_current_and_old_format_specs(self):
        payload = spec_runtime.scan_specs(ROOT)
        specs = {item["spec_id"]: item for item in payload["specs"]}

        self.assertEqual("current", specs["004-spec-management-mcp"]["format"])
        self.assertEqual("old-format", specs["001-spec-lifecycle-manager-skill"]["format"])
        self.assertEqual("skill-fallback", payload["template_authority"]["authority"])

    def test_summary_reports_tasks_and_resources(self):
        payload = spec_runtime.spec_summary(SPEC)

        self.assertEqual("004-spec-management-mcp", payload["spec_id"])
        self.assertGreater(payload["tasks"]["total"], 0)
        self.assertEqual("current", payload["format"])
        self.assertEqual("present", payload["artifacts"]["traceability.md"])

    def test_lint_doc_reports_completed_task_without_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.md"
            path.write_text(
                "\n".join(
                    [
                        "---",
                        "title: Tasks",
                        "doc_type: spec",
                        "artifact_type: tasks",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Tasks",
                        "",
                        "- [x] T001 Do thing.",
                        "  - Depends on: none",
                        "  - Files: `src/x`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Pending.",
                    ]
                ),
                encoding="utf-8",
            )

            diagnostics = spec_runtime.lint_doc(path, "tasks")

        codes = {item["code"] for item in diagnostics}
        self.assertIn("TASK_EVIDENCE_MISSING", codes)

    def test_lint_doc_reports_explicit_waiver(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.md"
            path.write_text(
                "\n".join(
                    [
                        "---",
                        "title: Requirements",
                        "doc_type: spec",
                        "artifact_type: requirements",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Requirements",
                        "",
                        "<!-- spec-lint-waive: REQUIREMENTS_PROPERTIES_MISSING - low-risk docs-only change -->",
                        "",
                        "## Durable Source Baseline",
                        "## Goals",
                        "## Non-Goals",
                        "## Requirements",
                        "### Requirement 1: Example",
                        "#### Acceptance Criteria",
                        "1. GIVEN context, WHEN action, THEN outcome.",
                        "## Success Criteria",
                    ]
                ),
                encoding="utf-8",
            )

            diagnostics = spec_runtime.lint_doc(path, "requirements")

        waived = [item for item in diagnostics if item["code"] == "REQUIREMENTS_PROPERTIES_MISSING"]
        self.assertTrue(waived)
        self.assertTrue(waived[0]["waived"])

    def test_lint_spec_package_returns_summary(self):
        payload = spec_runtime.lint_spec_package(SPEC)

        self.assertIn("summary", payload)
        self.assertIsInstance(payload["diagnostics"], list)

    def test_next_task_selects_first_unblocked_task_with_context(self):
        payload = spec_runtime.next_task(SPEC)

        self.assertEqual("T007", payload["selected"]["task_id"])
        self.assertIn("traceability_context", payload)
        self.assertEqual([], [gap for gap in payload["traceability_context"]["gaps"] if gap["severity"] == "error"])

    def test_closure_check_blocks_incomplete_spec(self):
        payload = spec_runtime.closure_check(SPEC)

        self.assertFalse(payload["ready"])
        codes = {item["code"] for item in payload["blockers"]}
        self.assertIn("TASK_NOT_VERIFIED", codes)

    def test_cli_scan_outputs_json(self):
        completed = subprocess.run(
            [str(SCRIPT), "scan", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertIn("specs", payload)


if __name__ == "__main__":
    unittest.main()
