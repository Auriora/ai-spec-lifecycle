import json
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVALID_FIXTURE_ROOT = ROOT / "tests/fixtures/codex-hook/invalid-spec"
HOOK = ROOT / "skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"

HOOK_SPEC = importlib.util.spec_from_file_location("codex_spec_lifecycle_hook", HOOK)
assert HOOK_SPEC is not None
hook_module = importlib.util.module_from_spec(HOOK_SPEC)
assert HOOK_SPEC.loader is not None
HOOK_SPEC.loader.exec_module(hook_module)


def write_valid_spec(repo: Path, relative: str = "docs/specs/001-valid") -> None:
    spec = repo / relative
    spec.mkdir(parents=True)
    frontmatter = "\n".join(
        [
            "---",
            "title: Valid",
            "doc_type: spec",
            "artifact_type: {artifact}",
            "status: draft",
            "owner: platform",
            "last_reviewed: 2026-06-06",
            "---",
            "",
        ]
    )
    (spec / "requirements.md").write_text(
        frontmatter.format(artifact="requirements")
        + "# Requirements\n\n## Durable Source Baseline\n\n## Goals\n\n## Non-Goals\n\n## Requirements\n\n### Requirement 1: Valid\n\n#### Acceptance Criteria\n\n1. GIVEN context, WHEN checked, THEN outcome.\n\n## Correctness Properties\n\n- CP-001: Holds.\n\n## Success Criteria\n",
        encoding="utf-8",
    )
    (spec / "design.md").write_text(
        frontmatter.format(artifact="design")
        + "# Design\n\n## Overview\n\n## High-Level Design\n\n## Low-Level Design\n\n## Operational Considerations\n\n## Open Questions\n",
        encoding="utf-8",
    )
    (spec / "tasks.md").write_text(
        frontmatter.format(artifact="tasks")
        + "# Tasks\n\n- [x] T001 Do work.\n  - Depends on: none\n  - Files: `docs/reference/x.md`\n  - Acceptance: Done.\n  - Evidence: Done.\n",
        encoding="utf-8",
    )
    (spec / "verification.md").write_text(
        frontmatter.format(artifact="verification") + "# Verification\n\n## Quality Gates\n\n## Evidence Log\n\n## Residual Risks\n",
        encoding="utf-8",
    )


def run_hook(
    payload: dict[str, object],
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["SPEC_LIFECYCLE_HOOK_LOG"] = str(Path(tmp) / "hook.log.jsonl")
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=True,
            env=env,
        )


def run_hook_with_log(
    payload: dict[str, object],
    log_path: Path,
    debounce_path: Path,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["SPEC_LIFECYCLE_HOOK_LOG"] = str(log_path)
    env["SPEC_LIFECYCLE_HOOK_DEBOUNCE_PATH"] = str(debounce_path)
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )


class CodexSpecLifecycleHookTests(unittest.TestCase):
    def test_hook_reports_concise_guidance_when_spec_checks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            (repo / ".git").mkdir()
            write_valid_spec(repo)
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "apply_patch",
                "tool_response": {
                    "output": "Updated the following files:\nM docs/specs/001-valid/tasks.md\n"
                },
            }

            result = run_hook(payload)
        data = json.loads(result.stdout)
        context = data["hookSpecificOutput"]["additionalContext"]

        self.assertIn("Spec lifecycle advisory guidance.", context)
        self.assertIn("docs/specs/001-valid", context)
        self.assertIn("Next spec artifact: traceability.md", context)
        self.assertNotIn(str(repo), context)
        self.assertNotRegex(context, r"\b(ERROR|WARN)\b")
        self.assertEqual("", result.stderr)

    def test_hook_matches_nested_partition_specs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            (repo / ".git").mkdir()
            write_valid_spec(repo, "docs/platform/specs/001-valid")
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "apply_patch",
                "tool_response": {
                    "output": "Updated the following files:\nM docs/platform/specs/001-valid/tasks.md\n"
                },
            }

            result = run_hook(payload)
        data = json.loads(result.stdout)
        context = data["hookSpecificOutput"]["additionalContext"]

        self.assertIn("docs/platform/specs/001-valid", context)
        self.assertIn("Next spec artifact: traceability.md", context)
        self.assertNotIn(str(repo), context)
        self.assertEqual("", result.stderr)

    def test_hook_extracts_apply_patch_input_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            (repo / ".git").mkdir()
            write_valid_spec(repo)
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "apply_patch",
                "tool_input": {
                    "patch": "*** Begin Patch\n*** Update File: docs/specs/001-valid/tasks.md\n@@\n*** End Patch\n"
                },
                "tool_response": {"output": ""},
            }

            result = run_hook(payload)
        data = json.loads(result.stdout)
        context = data["hookSpecificOutput"]["additionalContext"]

        self.assertIn("Next spec artifact: traceability.md", context)
        self.assertEqual("", result.stderr)

    def test_hook_debounces_repeated_spec_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = tmp_path / "repo"
            repo.mkdir()
            (repo / ".git").mkdir()
            write_valid_spec(repo)
            log_path = tmp_path / "hook.log.jsonl"
            debounce_path = tmp_path / "debounce.json"
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "apply_patch",
                "tool_response": {
                    "output": "Updated the following files:\nM docs/specs/001-valid/tasks.md\n"
                },
            }

            first = run_hook_with_log(payload, log_path, debounce_path)
            second = run_hook_with_log(payload, log_path, debounce_path)
            records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]

        first_data = json.loads(first.stdout)
        self.assertIn("Spec lifecycle advisory guidance.", first_data["hookSpecificOutput"]["additionalContext"])
        self.assertEqual("", second.stdout)
        self.assertEqual("", second.stderr)
        self.assertEqual("skipped_debounced", records[-1]["status"])
        self.assertEqual(
            [
                {"hook": "spec-file-changed", "changed_files": ["docs/specs/001-valid/tasks.md"]},
                {"hook": "task-checkbox-changed", "changed_files": ["docs/specs/001-valid/tasks.md"]},
            ],
            records[-1]["skipped_debounced"],
        )

    def test_hook_rechecks_when_spec_content_changes_inside_debounce_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = tmp_path / "repo"
            repo.mkdir()
            (repo / ".git").mkdir()
            write_valid_spec(repo)
            log_path = tmp_path / "hook.log.jsonl"
            debounce_path = tmp_path / "debounce.json"
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "apply_patch",
                "tool_response": {
                    "output": "Updated the following files:\nM docs/specs/001-valid/tasks.md\n"
                },
            }

            first = run_hook_with_log(payload, log_path, debounce_path)
            (repo / "docs/specs/001-valid/tasks.md").write_text(
                "# Tasks\n\n- [z] T001 Broken state.\n",
                encoding="utf-8",
            )
            second = run_hook_with_log(payload, log_path, debounce_path)
            records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]

        self.assertIn("Spec lifecycle advisory guidance.", json.loads(first.stdout)["hookSpecificOutput"]["additionalContext"])
        self.assertIn("Spec lifecycle advisory guidance.", json.loads(second.stdout)["hookSpecificOutput"]["additionalContext"])
        self.assertRegex(second.stdout, r"\b(ERROR|WARN)\b")
        self.assertEqual("checked", records[-1]["status"])

    def test_hook_debounce_can_be_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            (repo / ".git").mkdir()
            write_valid_spec(repo)
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "apply_patch",
                "tool_response": {
                    "output": "Updated the following files:\nM docs/specs/001-valid/tasks.md\n"
                },
            }

            first = run_hook(payload, {"SPEC_LIFECYCLE_HOOK_DEBOUNCE_SECONDS": "0"})
            second = run_hook(payload, {"SPEC_LIFECYCLE_HOOK_DEBOUNCE_SECONDS": "0"})

        self.assertIn("Spec lifecycle advisory guidance.", json.loads(first.stdout)["hookSpecificOutput"]["additionalContext"])
        self.assertIn("Spec lifecycle advisory guidance.", json.loads(second.stdout)["hookSpecificOutput"]["additionalContext"])

    def test_hook_reports_advisory_findings_for_invalid_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            shutil.copytree(INVALID_FIXTURE_ROOT, repo)
            (repo / ".git").mkdir()
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "write_file",
                "tool_input": {
                    "path": "docs/specs/001-invalid-spec/tasks.md"
                },
            }

            result = run_hook(payload)
        data = json.loads(result.stdout)
        context = data["hookSpecificOutput"]["additionalContext"]

        self.assertIn("Spec lifecycle advisory guidance.", context)
        self.assertRegex(context, r"\b(ERROR|WARN)\b")

    def test_hook_reports_next_authoring_step_for_clean_design_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            spec = repo / "docs/specs/001-new"
            spec.mkdir(parents=True)
            (repo / ".git").mkdir()
            (spec / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            (spec / "design.md").write_text("# Design\n", encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "write_file",
                "tool_input": {
                    "path": "docs/specs/001-new/design.md"
                },
            }

            result = run_hook(payload)
        data = json.loads(result.stdout)
        context = data["hookSpecificOutput"]["additionalContext"]

        self.assertIn("Next spec artifact: tasks.md", context)
        self.assertIn("templates://spec-package", context)
        self.assertNotIn("CORE_ARTIFACT_MISSING", context)

    def test_hook_handles_claude_write_tool_payload(self):
        # Claude Code emits tool_name "Write"/"Edit"/"MultiEdit" with a file_path,
        # not codex's write_file/apply_patch. Regression guard: the hook must extract
        # the changed file and emit guidance instead of silently skipping.
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            spec = repo / "docs/specs/001-new"
            spec.mkdir(parents=True)
            (repo / ".git").mkdir()
            (spec / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            (spec / "design.md").write_text("# Design\n", encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "docs/specs/001-new/design.md"
                },
            }

            result = run_hook(payload)
        data = json.loads(result.stdout)
        context = data["hookSpecificOutput"]["additionalContext"]

        self.assertIn("Next spec artifact: tasks.md", context)
        self.assertIn("templates://spec-package", context)
        self.assertEqual("", result.stderr)

    def test_hook_extracts_claude_edit_and_notebookedit_paths(self):
        # Edit/MultiEdit use file_path; NotebookEdit uses notebook_path.
        for tool_name, key in (("Edit", "file_path"), ("NotebookEdit", "notebook_path")):
            with self.subTest(tool_name=tool_name):
                paths = hook_module.extract_write_tool_paths(
                    {
                        "tool_name": tool_name,
                        "tool_input": {key: "docs/specs/001-new/tasks.md"},
                    }
                )
                self.assertEqual(["docs/specs/001-new/tasks.md"], paths)

    def test_hook_routes_verification_writes_to_narrow_verification_check(self):
        commands = hook_module.hook_commands(
            ["docs/specs/001-valid/verification.md"]
        )

        self.assertIn(
            ("verification-updated", ["docs/specs/001-valid/verification.md"]),
            commands,
        )

    def test_hook_is_quiet_for_non_lifecycle_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            (repo / ".git").mkdir()
            payload = {
                "hook_event_name": "PostToolUse",
                "cwd": str(repo),
                "tool_name": "write_file",
                "tool_input": {"path": "src/example.py"},
            }

            result = run_hook(payload)

        self.assertEqual("", result.stdout)
        self.assertEqual("", result.stderr)

    def test_hook_wrapper_logs_unexpected_errors_without_failing_codex(self):
        def fail() -> int:
            raise RuntimeError("forced hook failure")

        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "hook.log.jsonl"
            previous_log = os.environ.get("SPEC_LIFECYCLE_HOOK_LOG")
            os.environ["SPEC_LIFECYCLE_HOOK_LOG"] = str(log_path)
            try:
                result = hook_module.run_advisory_hook(fail)
            finally:
                if previous_log is None:
                    os.environ.pop("SPEC_LIFECYCLE_HOOK_LOG", None)
                else:
                    os.environ["SPEC_LIFECYCLE_HOOK_LOG"] = previous_log

            records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(0, result)
        self.assertEqual("hook_failed", records[0]["status"])
        self.assertEqual("RuntimeError", records[0]["error_type"])


if __name__ == "__main__":
    unittest.main()
