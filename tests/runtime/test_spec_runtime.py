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
        self.assertEqual("archived", specs["001-spec-lifecycle-manager-skill"]["lifecycle"])
        self.assertEqual("archived", specs["001-spec-lifecycle-manager-skill"]["health"]["severity"])
        self.assertTrue(specs["001-spec-lifecycle-manager-skill"]["health"]["skipped"])
        self.assertGreaterEqual(payload["summary"]["archived"], 1)
        self.assertEqual("skill-fallback", payload["template_authority"]["authority"])

    def test_scan_can_opt_into_archived_lint_audit(self):
        payload = spec_runtime.scan_specs(ROOT, include_archived_lint=True)
        specs = {item["spec_id"]: item for item in payload["specs"]}
        archived = specs["001-spec-lifecycle-manager-skill"]

        self.assertEqual("archived", archived["lifecycle"])
        self.assertEqual("error", archived["health"]["severity"])
        self.assertFalse(archived["health"]["skipped"])
        self.assertGreater(archived["health"]["diagnostic_count"], 0)

    def test_archive_index_validates_current_index(self):
        payload = spec_runtime.archive_index(ROOT)

        self.assertEqual(0, payload["summary"]["error"])
        self.assertGreaterEqual(payload["summary"]["retained"], 1)
        self.assertEqual(1, payload["summary"]["legacy_gaps"])
        self.assertIn("003-coding-agent-operating-model", {entry["spec_id"] for entry in payload["entries"]})

    def test_archive_index_reports_missing_commits_and_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            history = repo / "docs/history"
            spec = repo / "docs/specs/001-example"
            durable = repo / "docs/design"
            history.mkdir(parents=True)
            spec.mkdir(parents=True)
            durable.mkdir(parents=True)
            (durable / "example.md").write_text("# Example\n", encoding="utf-8")
            (history / "spec-closure-log.md").write_text(
                "\n".join(
                    [
                        "# Spec Closure Log",
                        "",
                        "## Entries",
                        "",
                        "### 2026-06-06 - 001-example",
                        "",
                        "- **Spec:** `docs/specs/001-example/`",
                        "- **Title:** Example",
                        "- **Final spec commit:** `abc1234`",
                        "- **Closure cleanup commit:** `def5678`",
                        "- **Closure action:** retained-as-history",
                        "- **Durable docs updated:**",
                        "  - `docs/design/example.md`",
                    ]
                ),
                encoding="utf-8",
            )
            (history / "spec-archive-index.md").write_text(
                "\n".join(
                    [
                        "# Spec Archive Index",
                        "",
                        "## Entries",
                        "",
                        "| Spec ID | Title | Package path | Status | Final spec commit | Cleanup commit | Closure action | Durable destinations | Verification |",
                        "|---------|-------|--------------|--------|-------------------|----------------|----------------|----------------------|--------------|",
                        "| 001-example | Different title | `docs/specs/001-example/` | retained | pending | zzzzzzz | retained-as-history | `docs/design/missing.md` | `docs/history/spec-closure-log.md` |",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.archive_index(repo)

        codes = {item["code"] for item in payload["diagnostics"]}
        self.assertIn("ARCHIVE_INDEX_FINAL_COMMIT_MISSING", codes)
        self.assertIn("ARCHIVE_INDEX_CLEANUP_COMMIT_INVALID", codes)
        self.assertIn("ARCHIVE_INDEX_DURABLE_DESTINATION_MISSING", codes)
        self.assertIn("ARCHIVE_INDEX_CLOSURE_LOG_DRIFT", codes)
        self.assertGreater(payload["summary"]["error"], 0)

    def test_summary_reports_tasks_and_resources(self):
        payload = spec_runtime.spec_summary(SPEC)

        self.assertEqual("004-spec-management-mcp", payload["spec_id"])
        self.assertEqual("archived", payload["lifecycle"])
        self.assertGreater(payload["tasks"]["total"], 0)
        self.assertEqual("current", payload["format"])
        self.assertEqual("present", payload["artifacts"]["traceability.md"])

    def test_cli_scan_can_opt_into_archived_lint_audit(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "scan", str(ROOT), "--include-archived-lint"],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        specs = {item["spec_id"]: item for item in payload["specs"]}

        self.assertEqual("error", specs["001-spec-lifecycle-manager-skill"]["health"]["severity"])

    def test_cli_archive_index_outputs_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "archive-index", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(0, payload["summary"]["error"])
        self.assertIn("entries", payload)

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

        self.assertIsNone(payload["selected"])
        self.assertEqual("No runnable incomplete task found.", payload["message"])

    def test_closure_check_reports_completed_spec_ready(self):
        payload = spec_runtime.closure_check(SPEC)

        self.assertTrue(payload["ready"])
        self.assertEqual([], payload["blockers"])

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

    def test_hook_spec_close_check_blocks_incomplete_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.write_incomplete_spec(Path(tmp))
            payload = spec_runtime.run_hook(Path(tmp), "spec-close-check", spec_path=spec, severity_profile="blocking")

        self.assertTrue(payload["blocked"])
        self.assertIn("TASK_NOT_VERIFIED", {item["code"] for item in payload["blocking"]})

    def test_reconcile_spec_reports_incomplete_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.write_incomplete_spec(Path(tmp))
            payload = spec_runtime.reconcile_spec(spec)

        self.assertIn("code incomplete", payload["summary"])

    def test_promotion_plan_returns_durable_targets(self):
        payload = spec_runtime.promotion_plan(SPEC)

        targets = {item["target"] for item in payload["targets"]}
        self.assertIn("skills/spec-lifecycle-manager/SKILL.md", targets)

    def test_generate_review_packet_is_read_only_and_bounded(self):
        payload = spec_runtime.generate_review_packet(SPEC, "design_requirements_trace", "cheap")

        self.assertEqual("read-only", payload["scope"])
        self.assertEqual("cheap", payload["model_class"])
        self.assertIn("expected_output_schema", payload)
        self.assertIn("requirements.md", payload["input_artifacts"])

    def test_validate_review_result_disposition(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review-result.json"
            path.write_text(
                json.dumps(spec_runtime.review_result_disposition_template("design_requirements_trace")),
                encoding="utf-8",
            )

            payload = spec_runtime.validate_review_result(path)

        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_agent_slice_start_uses_traceability(self):
        payload = spec_runtime.run_hook(
            ROOT,
            "agent-slice-start",
            spec_path=SPEC,
            task_id="T010",
            severity_profile="blocking",
        )

        self.assertFalse(payload["blocked"])
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_agent_response_check_warns_without_changed_files(self):
        payload = spec_runtime.run_hook(
            ROOT,
            "agent-response-check",
            spec_path=SPEC,
            task_id="T010",
            severity_profile="advisory",
        )

        self.assertFalse(payload["blocked"])
        self.assertIn("AGENT_CHANGED_FILES_MISSING", {item["code"] for item in payload["diagnostics"]})

    def test_review_result_recorded_blocks_invalid_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review-result.json"
            path.write_text("{}", encoding="utf-8")

            payload = spec_runtime.run_hook(
                ROOT,
                "review-result-recorded",
                result_path=path,
                severity_profile="blocking",
            )

        self.assertTrue(payload["blocked"])
        self.assertIn("REVIEW_RESULT_FIELD_MISSING", {item["code"] for item in payload["blocking"]})

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
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.write_incomplete_spec(Path(tmp))
            completed = subprocess.run(
                [
                    str(SCRIPT),
                    "hook",
                    "spec-close-check",
                    "--repo-root",
                    tmp,
                    "--spec-path",
                    str(spec),
                    "--severity-profile",
                    "blocking",
                ],
                capture_output=True,
                text=True,
            )

        self.assertEqual(1, completed.returncode)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["blocked"])

    def test_cli_review_packet_outputs_json(self):
        completed = subprocess.run(
            [str(SCRIPT), "review-packet", str(SPEC), "--review-type", "design_requirements_trace"],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual("design_requirements_trace", payload["review_type"])

    def write_incomplete_spec(self, repo: Path) -> Path:
        spec = repo / "docs/specs/001-example"
        spec.mkdir(parents=True)
        frontmatter = [
            "---",
            "title: Example",
            "doc_type: spec",
            "status: draft",
            "owner: platform",
            "last_reviewed: 2026-06-05",
            "---",
            "",
        ]
        (spec / "requirements.md").write_text(
            "\n".join(
                frontmatter
                + [
                    "# Requirements",
                    "",
                    "## Durable Source Baseline",
                    "- No durable source exists yet.",
                    "",
                    "## Goals",
                    "## Non-Goals",
                    "## Requirements",
                    "### Requirement 1: Example",
                    "#### Acceptance Criteria",
                    "1. GIVEN context, WHEN action, THEN outcome.",
                    "## Correctness Properties",
                    "## Success Criteria",
                ]
            ),
            encoding="utf-8",
        )
        (spec / "design.md").write_text(
            "\n".join(
                frontmatter
                + [
                    "# Design",
                    "",
                    "## Overview",
                    "## High-Level Design",
                    "## Low-Level Design",
                    "## Operational Considerations",
                    "## Open Questions",
                ]
            ),
            encoding="utf-8",
        )
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
                    "- [ ] T001 Do thing.",
                    "  - Depends on: none",
                    "  - Files: `src/x`",
                    "  - Acceptance: Done.",
                    "  - Evidence: Pending.",
                ]
            ),
            encoding="utf-8",
        )
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
                    "## Evidence Log",
                    "- T001 covers Requirement 1.",
                    "## Residual Risks",
                ]
            ),
            encoding="utf-8",
        )
        (spec / "traceability.md").write_text(
            "\n".join(
                [
                    "---",
                    "title: Traceability",
                    "doc_type: spec",
                    "artifact_type: traceability",
                    "status: draft",
                    "owner: platform",
                    "last_reviewed: 2026-06-05",
                    "---",
                    "",
                    "# Traceability Matrix",
                    "",
                    "## Task To Context Matrix",
                    "## Requirement To Delivery Matrix",
                    "## Design To Implementation Matrix",
                    "## Open Decision Impact",
                ]
            ),
            encoding="utf-8",
        )
        return spec


if __name__ == "__main__":
    unittest.main()
