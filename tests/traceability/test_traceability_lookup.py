import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
SPEC = ROOT / "docs/specs/004-spec-management-mcp"
sys.path.insert(0, str(SCRIPT.parent))

import traceability_lookup


class TraceabilityLookupTests(unittest.TestCase):
    def test_task_lookup_returns_full_context(self):
        payload = traceability_lookup.task_lookup(SPEC, "T012")

        self.assertEqual(payload["lookup"], {"type": "task", "value": "T012"})
        self.assertEqual(payload["traceability_row"]["Requirements"], "Requirement 6A")
        self.assertIn("Requirement 6A", [item["id"] for item in payload["requirements"]])
        self.assertIn("design.md#mcp-tools", payload["design_sections"])
        self.assertIn("skills/spec-lifecycle-manager/SKILL.md", payload["durable_targets"])
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_reverse_requirement_lookup(self):
        payload = traceability_lookup.reverse_lookup(SPEC, "requirement", "Requirement 6A")

        self.assertEqual(payload["traceability_row"]["Tasks"], "T012")
        self.assertIn("design.md#mcp-resources", payload["traceability_row"]["Design Sections"])
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_reverse_design_lookup(self):
        payload = traceability_lookup.reverse_lookup(SPEC, "design", "design.md#mcp-tools")

        self.assertEqual(payload["traceability_row"]["Requirements"], "Requirement 6A")
        self.assertEqual(payload["traceability_row"]["Tasks"], "T012")
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_missing_task_reports_gap(self):
        payload = traceability_lookup.task_lookup(SPEC, "T999")

        codes = {gap["code"] for gap in payload["gaps"]}
        self.assertIn("TRACEABILITY_TASK_ROW_MISSING", codes)

    def test_missing_artifact_reference_reports_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp)
            (spec / "traceability.md").write_text(
                "\n".join(
                    [
                        "# Traceability Matrix",
                        "",
                        "## Task To Context Matrix",
                        "",
                        "| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |",
                        "|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|",
                        "| T001 | Requirement 1 | AC1 | `missing.md#x` | none | TBD | none | none |",
                    ]
                ),
                encoding="utf-8",
            )

            payload = traceability_lookup.task_lookup(spec, "T001")

        codes = {gap["code"] for gap in payload["gaps"]}
        self.assertIn("TRACEABILITY_REFERENCE_MISSING", codes)
        self.assertIn("TRACEABILITY_UNRESOLVED_VALUE", codes)

    def test_cli_json_output(self):
        completed = subprocess.run(
            [str(SCRIPT), str(SPEC), "--task", "T012"],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["lookup"]["value"], "T012")


if __name__ == "__main__":
    unittest.main()
