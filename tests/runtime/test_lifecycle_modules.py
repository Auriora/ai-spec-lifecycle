import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle.actions import lifecycle_next_actions
from lifecycle.capabilities import lifecycle_capabilities
from lifecycle.migration import (
    TRACEABILITY_CLAUDE_BUNDLE,
    TRACEABILITY_CODEX_BUNDLE,
    TRACEABILITY_SOURCE,
    migrated_script_closure_check,
    script_migration_inventory,
)
from lifecycle.traceability import task_lookup


class LifecycleModuleTests(unittest.TestCase):
    def test_capability_report_uses_unknown_client_fields_without_guessing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(
                '{"name": "target-application", "version": "99.0.0"}\n',
                encoding="utf-8",
            )
            report = lifecycle_capabilities(repo)

        self.assertEqual("ready", report["status"])
        self.assertEqual("not_observed", report["client_metadata_status"])
        self.assertEqual("spec-lifecycle-manager", report["server"]["name"])
        self.assertEqual("0.4.0", report["server"]["version"])
        self.assertFalse(report["server"]["capabilities"]["tools"]["listChanged"])
        self.assertEqual("unknown", report["client"]["name"])
        self.assertEqual("stable_tool_surface", report["dynamic_tools"]["decision"])
        self.assertEqual("CLIENT_METADATA_NOT_OBSERVED", report["limitations"][0]["code"])
        self.assertEqual("none", report["limitations"][0]["impact"])
        self.assertIn("available_next_actions", report)

    def test_capability_report_preserves_documented_session_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            report = lifecycle_capabilities(
                repo,
                {
                    "protocol_version": "2025-06-18",
                    "client": {
                        "name": "ExampleClient",
                        "version": "1.2.3",
                        "protocol_version": "2025-06-18",
                        "capabilities": {"roots": {"listChanged": True}},
                    },
                    "client_refresh_observed": "unknown",
                },
            )

        self.assertEqual("ready", report["status"])
        self.assertEqual("observed", report["client_metadata_status"])
        self.assertEqual("ExampleClient", report["client"]["name"])
        self.assertEqual({"roots": {"listChanged": True}}, report["client"]["capabilities"])
        self.assertEqual("unknown", report["dynamic_tools"]["client_refresh_observed"])
        self.assertEqual([], report["limitations"])

    def test_capability_report_allows_an_explicit_server_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = lifecycle_capabilities(Path(tmp), server_version="9.8.7-test")

        self.assertEqual("9.8.7-test", report["server"]["version"])

    def test_next_actions_are_state_based_not_client_based(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = repo / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "requirements.md").write_text("# Requirements\n", encoding="utf-8")

            actions = lifecycle_next_actions(repo, spec)

        self.assertEqual(["advance_to_design"], [action["id"] for action in actions])
        self.assertEqual("design.md", actions[0]["artifact"])

    def test_migration_inventory_reports_selected_script_blockers(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for relative in (TRACEABILITY_SOURCE, TRACEABILITY_CODEX_BUNDLE, TRACEABILITY_CLAUDE_BUNDLE):
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("print('legacy traceability')\n", encoding="utf-8")

            inventory = script_migration_inventory(repo)

        self.assertEqual("ok", inventory["status"])
        migrated = inventory["migrated_scripts"]
        self.assertEqual(["traceability_lookup.py"], [row["script"] for row in migrated])
        self.assertEqual("traceability_lookup", migrated[0]["replacement_contract"]["replacement_mcp_tool"])
        blocker_paths = {blocker["path"] for blocker in inventory["closure_blockers"]}
        self.assertEqual({TRACEABILITY_SOURCE, TRACEABILITY_CODEX_BUNDLE, TRACEABILITY_CLAUDE_BUNDLE}, blocker_paths)

    def test_closure_check_passes_when_selected_script_paths_are_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            blockers = migrated_script_closure_check(Path(tmp))

        self.assertEqual([], blockers)

    def test_traceability_module_delegates_lookup_without_mcp_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "requirements.md").write_text(
                "# Requirements\n\n### Requirement 1: Context\n\n#### Acceptance Criteria\n\n1. GIVEN context, WHEN used, THEN THE SYSTEM SHALL respond.\n",
                encoding="utf-8",
            )
            (spec / "design.md").write_text("# Design\n\n## Context Flow\n", encoding="utf-8")
            (spec / "tasks.md").write_text("# Tasks\n\n- [ ] T001 Do work.\n", encoding="utf-8")
            (spec / "traceability.md").write_text(
                "\n".join(
                    [
                        "# Traceability",
                        "",
                        "## Task To Context Matrix",
                        "",
                        "| Task ID | Requirements | Design Sections |",
                        "| --- | --- | --- |",
                        "| T001 | Requirement 1 | `design.md#context-flow` |",
                    ]
                ),
                encoding="utf-8",
            )

            payload = task_lookup(spec, "T001")

        self.assertEqual({"type": "task", "value": "T001"}, payload["lookup"])
        self.assertEqual("Requirement 1", payload["traceability_row"]["Requirements"])
        self.assertIn("design.md#context-flow", payload["design_sections"])


if __name__ == "__main__":
    unittest.main()
