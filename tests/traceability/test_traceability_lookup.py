import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle import traceability


def write_traceability_spec(repo: Path) -> Path:
    (repo / ".git").mkdir()
    skill = repo / "skills/spec-lifecycle-manager"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
    spec = repo / "docs/specs/001-traceability"
    spec.mkdir(parents=True)
    (spec / "requirements.md").write_text(
        "\n".join(
            [
                "# Requirements",
                "",
                "### Requirement 6A: MCP Context",
                "",
                "The runtime exposes MCP context.",
            ]
        ),
        encoding="utf-8",
    )
    (spec / "design.md").write_text(
        "\n".join(
            [
                "# Design",
                "",
                "## MCP Resources",
                "",
                "Expose spec resources.",
                "",
                "## MCP Tools",
                "",
                "Expose spec tools.",
            ]
        ),
        encoding="utf-8",
    )
    (spec / "traceability.md").write_text(
        "\n".join(
            [
                "# Traceability",
                "",
                "## Task To Context Matrix",
                "",
                "| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |",
                "|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|",
                "| T012 | Requirement 6A | AC1 | `design.md#mcp-resources`, `design.md#mcp-tools` | none | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/SKILL.md` | none |",
                "",
                "## Requirement To Delivery Matrix",
                "",
                "| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |",
                "|-------------|---------------------|-----------------|-------|--------------|-----------------|",
                "| Requirement 6A | AC1 | `design.md#mcp-resources`, `design.md#mcp-tools` | T012 | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/SKILL.md` |",
                "",
                "## Design To Implementation Matrix",
                "",
                "| Design Section | Requirements | Tasks | Implementation Targets | Verification |",
                "|----------------|--------------|-------|------------------------|--------------|",
                "| `design.md#mcp-tools` | Requirement 6A | T012 | `skills/spec-lifecycle-manager/SKILL.md` | `verification.md#quality-gates` |",
            ]
        ),
        encoding="utf-8",
    )
    (spec / "tasks.md").write_text("# Tasks\n\n- [x] T012 Add MCP context.\n  - Evidence: Done.\n", encoding="utf-8")
    (spec / "verification.md").write_text("# Verification\n\n## Quality Gates\n", encoding="utf-8")
    return spec


class TraceabilityLookupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.spec = write_traceability_spec(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_task_lookup_returns_full_context(self):
        payload = traceability.task_lookup(self.spec, "T012")

        self.assertEqual(payload["lookup"], {"type": "task", "value": "T012"})
        self.assertEqual(payload["traceability_row"]["Requirements"], "Requirement 6A")
        self.assertIn("Requirement 6A", [item["id"] for item in payload["requirements"]])
        self.assertIn("design.md#mcp-tools", payload["design_sections"])
        self.assertIn("skills/spec-lifecycle-manager/SKILL.md", payload["durable_targets"])
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_task_lookup_accepts_extended_task_status_markers(self):
        (self.spec / "tasks.md").write_text(
            "# Tasks\n\n- [?] T012 Add MCP context.\n  - Evidence: Review pending.\n",
            encoding="utf-8",
        )

        payload = traceability.task_lookup(self.spec, "T012")

        self.assertIn("- [?] T012 Add MCP context.", payload["task"]["source"])
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_task_lookup_accepts_compact_task_column_context_matrix(self):
        (self.spec / "traceability.md").write_text(
            "\n".join(
                [
                    "# Traceability",
                    "",
                    "## Task To Delivery Matrix",
                    "",
                    "| Task | Requirements | Context Required Before Execution | Verification | Durable Targets |",
                    "| --- | --- | --- | --- | --- |",
                    "| T010 | Requirement 6A | Analytics API/data-health surfaces and no-fallback route checks. | API/data-health tests. | Data-health and production-reporting docs. |",
                    "",
                    "## Task To Context Matrix",
                    "",
                    "| Task | Required Context |",
                    "| --- | --- |",
                    "| T010 | `verification.md`, Analytics API/data-health surfaces, production-reporting marts, and no-fallback assertions. |",
                ]
            ),
            encoding="utf-8",
        )
        (self.spec / "tasks.md").write_text("# Tasks\n\n- [ ] T010 Verify no-fallback serving.\n", encoding="utf-8")

        payload = traceability.task_lookup(self.spec, "T010")

        self.assertEqual("Requirement 6A", payload["traceability_row"]["Requirements"])
        self.assertEqual("T010", payload["traceability_row"]["Task"])
        self.assertIn("Analytics API/data-health surfaces", payload["traceability_row"]["Required Context"])
        self.assertIn("Data-health and production-reporting docs.", payload["durable_targets"])
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_task_lookup_expands_all_requirements(self):
        (self.spec / "traceability.md").write_text(
            "\n".join(
                [
                    "# Traceability",
                    "",
                    "## Task To Context Matrix",
                    "",
                    "| Task | Requirements | Required Context |",
                    "| --- | --- | --- |",
                    "| T011 | All requirements | Closure guidance. |",
                ]
            ),
            encoding="utf-8",
        )
        (self.spec / "tasks.md").write_text("# Tasks\n\n- [ ] T011 Close spec.\n", encoding="utf-8")

        payload = traceability.task_lookup(self.spec, "T011")

        self.assertEqual(["Requirement 6A"], [item["id"] for item in payload["requirements"]])
        codes = {gap["code"] for gap in payload["gaps"]}
        self.assertNotIn("REQUIREMENT_CONTEXT_NOT_FOUND", codes)

    def test_reverse_requirement_lookup(self):
        payload = traceability.reverse_lookup(self.spec, "requirement", "Requirement 6A")

        self.assertEqual(payload["traceability_row"]["Tasks"], "T012")
        self.assertIn("design.md#mcp-resources", payload["traceability_row"]["Design Sections"])
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_reverse_design_lookup(self):
        payload = traceability.reverse_lookup(self.spec, "design", "design.md#mcp-tools")

        self.assertEqual(payload["traceability_row"]["Requirements"], "Requirement 6A")
        self.assertEqual(payload["traceability_row"]["Tasks"], "T012")
        self.assertEqual([], [gap for gap in payload["gaps"] if gap["severity"] == "error"])

    def test_missing_task_reports_gap(self):
        payload = traceability.task_lookup(self.spec, "T999")

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

            payload = traceability.task_lookup(spec, "T001")

        codes = {gap["code"] for gap in payload["gaps"]}
        self.assertIn("TRACEABILITY_REFERENCE_MISSING", codes)
        self.assertIn("TRACEABILITY_UNRESOLVED_VALUE", codes)

    def test_payload_is_json_serializable_for_mcp_structured_content(self):
        payload = traceability.task_lookup(self.spec, "T012")

        payload = json.loads(json.dumps(payload))
        self.assertEqual(payload["lookup"]["value"], "T012")


if __name__ == "__main__":
    unittest.main()
