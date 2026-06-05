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

        self.assertEqual("T010", payload["selected"]["task_id"])
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

    def test_prompt_definitions_are_discoverable_and_valid(self):
        payload = spec_runtime.load_prompt_definitions(ROOT)

        names = {prompt["name"] for prompt in payload["prompts"]}
        self.assertTrue({"reconcile-spec", "choose-next-task", "task-context", "lint-spec"} <= names)
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_hook_spec_file_changed_lints_affected_package(self):
        payload = spec_runtime.run_hook(
            ROOT,
            "spec-file-changed",
            changed_files=["docs/specs/004-spec-management-mcp/tasks.md"],
            severity_profile="advisory",
        )

        self.assertTrue(payload["advisory"])
        self.assertFalse(payload["blocked"])
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])
        self.assertEqual(1, len(payload["affected_specs"]))

    def test_hook_task_checkbox_changed_blocks_missing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = repo / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "tasks.md").write_text(
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

            payload = spec_runtime.run_hook(
                repo,
                "task-checkbox-changed",
                changed_files=["docs/specs/001-example/tasks.md"],
                severity_profile="blocking",
            )

        self.assertTrue(payload["blocked"])
        self.assertIn("TASK_EVIDENCE_MISSING", {item["code"] for item in payload["blocking"]})

    def test_hook_implementation_task_complete_blocks_missing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = repo / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "tasks.md").write_text(
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

            payload = spec_runtime.run_hook(
                repo,
                "implementation-task-complete",
                spec_path=spec,
                task_id="T001",
                severity_profile="blocking",
            )

        self.assertTrue(payload["blocked"])
        self.assertIn("TASK_EVIDENCE_MISSING", {item["code"] for item in payload["blocking"]})

    def test_hook_verification_updated_checks_requirement_and_task_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = repo / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "verification.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: Verification",
                        "doc_type: spec",
                        "artifact_type: verification",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Verification",
                        "",
                        "## Quality Gates",
                        "",
                        "## Evidence Log",
                        "",
                        "- T001 covers Requirement 1.",
                        "",
                        "## Residual Risks",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.run_hook(
                repo,
                "verification-updated",
                spec_path=spec,
                severity_profile="blocking",
            )

        self.assertFalse(payload["blocked"])
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_hook_spec_resumed_flags_old_format(self):
        spec = ROOT / "docs/specs/001-spec-lifecycle-manager-skill"

        payload = spec_runtime.run_hook(ROOT, "spec-resumed", spec_path=spec, severity_profile="advisory")

        self.assertFalse(payload["blocked"])
        self.assertIn("OLD_FORMAT_MIGRATION_DECISION_NEEDED", {item["code"] for item in payload["diagnostics"]})

    def test_hook_spec_close_check_blocks_active_spec(self):
        payload = spec_runtime.run_hook(ROOT, "spec-close-check", spec_path=SPEC, severity_profile="blocking")

        self.assertTrue(payload["blocked"])
        self.assertIn("TASK_NOT_VERIFIED", {item["code"] for item in payload["blocking"]})

    def test_cli_prompts_outputs_json(self):
        completed = subprocess.run(
            [str(SCRIPT), "prompts", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(4, len(payload["prompts"]))

    def test_cli_spec_close_hook_exits_nonzero_when_blocking(self):
        completed = subprocess.run(
            [
                str(SCRIPT),
                "hook",
                "spec-close-check",
                "--spec-path",
                str(SPEC),
                "--severity-profile",
                "blocking",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(1, completed.returncode)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["blocked"])


if __name__ == "__main__":
    unittest.main()
