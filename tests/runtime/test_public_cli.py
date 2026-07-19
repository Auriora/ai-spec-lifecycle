import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
SCRIPT = SCRIPT_DIR / "slm_cli.py"
sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle import public_cli
from lifecycle import public_views


def view(command: str, records: list[dict]) -> dict:
    return public_views.command_view(command, Path("/repo"), records, {"total": len(records)})


def tree_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def write_query_repo(root: Path) -> Path:
    (root / ".git").mkdir()
    spec = root / "docs/specs/001-example"
    spec.mkdir(parents=True)
    frontmatter = "---\ntitle: Example\ndoc_type: spec\nartifact_type: {artifact}\nstatus: draft\nowner: platform\nlast_reviewed: 2026-07-19\n---\n"
    (spec / "requirements.md").write_text(
        frontmatter.format(artifact="requirements")
        + "# Requirements\n\n### Requirement 1: Example\n\n**Priority:** must-have\n\n#### Acceptance Criteria\n\n1. It works.\n",
        encoding="utf-8",
    )
    (spec / "tasks.md").write_text(
        frontmatter.format(artifact="tasks")
        + "# Tasks\n\n## Phase 1\n\n- [ ] T001 Do work.\n  - Depends on: none\n  - Evidence: Pending.\n",
        encoding="utf-8",
    )
    (spec / "traceability.md").write_text(
        frontmatter.format(artifact="traceability")
        + "# Traceability Matrix\n\n## Task To Context Matrix\n\n| Task ID | Requirements |\n|---------|--------------|\n| T001 | Requirement 1 |\n\n"
        + "## Requirement To Delivery Matrix\n\n| Requirement | Tasks |\n|-------------|-------|\n| Requirement 1 | T001 |\n",
        encoding="utf-8",
    )
    return spec


class PublicCliParsingTests(unittest.TestCase):
    def run_main(self, argv, *, cwd=Path("/repo")):
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = public_cli.main(argv, stdout=stdout, stderr=stderr, cwd=cwd)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_help_lists_public_queries_and_install(self):
        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as caught:
            public_cli.build_parser().parse_args(["--help"])
        self.assertEqual(0, caught.exception.code)
        help_text = public_cli.build_parser().format_help()
        for command in public_views.PUBLIC_COMMANDS:
            self.assertIn(command, help_text)

    def test_bare_invocation_and_explicit_specs_use_the_same_view(self):
        payload = view(
            "specs",
            [{"spec_id": "001-a", "status": "draft", "lifecycle": "active", "health": "pass", "tasks_complete": 1, "tasks_total": 2, "next_task": "T002", "path": "docs/specs/001-a"}],
        )
        with mock.patch.object(public_cli.public_views, "build_specs_view", return_value=payload) as build:
            bare = self.run_main([])
            explicit = self.run_main(["specs"])
        self.assertEqual(0, bare[0])
        self.assertEqual(bare[1], explicit[1])
        self.assertIn("001-a", bare[1])
        self.assertEqual(2, build.call_count)

    def test_json_and_table_render_from_the_same_normalized_records(self):
        payload = view(
            "requirements",
            [{"requirement_id": "Requirement 1", "priority": "must-have", "tasks": ["T001"], "title": "Safe output", "diagnostics": []}],
        )
        with (
            mock.patch.object(public_cli.public_views, "select_active_spec", return_value=Path("/repo/docs/specs/001-a")),
            mock.patch.object(public_cli.public_views, "build_requirements_view", return_value=payload),
        ):
            table_result = self.run_main(["requirements", "001-a"])
            json_result = self.run_main(["requirements", "001-a", "--json"])
        self.assertEqual(0, table_result[0])
        self.assertIn("Requirement 1", table_result[1])
        self.assertEqual(payload, json.loads(json_result[1]))

    def test_global_options_are_accepted_before_the_command(self):
        payload = view("specs", [])
        with mock.patch.object(public_cli.public_views, "build_specs_view", return_value=payload):
            code, stdout, stderr = self.run_main(["--json", "-C", ".", "specs"], cwd=ROOT)
        self.assertEqual(0, code)
        self.assertEqual(payload, json.loads(stdout))
        self.assertEqual("", stderr)

    def test_task_filters_and_next_command_reach_the_shared_view_contract(self):
        payload = view("tasks", [])
        with (
            mock.patch.object(public_cli.public_views, "select_active_spec", return_value=Path("/repo/docs/specs/001-a")),
            mock.patch.object(public_cli.public_views, "build_tasks_view", return_value=payload) as build,
        ):
            result = self.run_main(["tasks", "001-a", "--complete", "--open", "--state", "attention"])
            next_result = self.run_main(["next", "001-a"])
        self.assertEqual(0, result[0])
        filters = build.call_args_list[0].kwargs["filters"]
        self.assertTrue(filters.complete)
        self.assertTrue(filters.open)
        self.assertEqual(("attention",), filters.states)
        self.assertTrue(build.call_args_list[1].kwargs["filters"].next_only)
        self.assertEqual("next", build.call_args_list[1].kwargs["command"])
        self.assertEqual(0, next_result[0])

    def test_invalid_and_conflicting_filters_return_usage_exit(self):
        with mock.patch.object(public_cli.public_views, "select_active_spec", return_value=Path("/repo/docs/specs/001-a")):
            conflict = self.run_main(["tasks", "001-a", "--next", "--pending"])
            invalid_priority = self.run_main(["requirements", "001-a", "--priority", "urgent"])
            invalid_limit = self.run_main(["history", "--limit", "-1"])
        for code, stdout, stderr in (conflict, invalid_priority, invalid_limit):
            self.assertEqual(2, code)
            self.assertEqual("", stdout)
            self.assertTrue(stderr.startswith("slm: "))

    def test_ambiguous_selection_is_exit_two_with_candidates_and_no_stdout(self):
        error = public_views.PublicViewError(
            "Multiple active specs found; select one explicitly.",
            code="spec_ambiguous",
            candidates=["001-a", "002-b"],
        )
        with mock.patch.object(public_cli.public_views, "select_active_spec", side_effect=error):
            code, stdout, stderr = self.run_main(["tasks", "--json"])
        self.assertEqual(2, code)
        self.assertEqual("", stdout)
        self.assertIn("001-a, 002-b", stderr)

    def test_malformed_history_is_exit_one_with_shared_diagnostics(self):
        error = public_views.PublicViewError(
            "Historic spec metadata is invalid.",
            code="history_invalid",
            diagnostics=[{"code": "ARCHIVE_BAD", "message": "bad row"}],
        )
        with mock.patch.object(public_cli.public_views, "build_history_view", side_effect=error):
            code, stdout, stderr = self.run_main(["history", "--json"])
        self.assertEqual(1, code)
        self.assertEqual("", stdout)
        self.assertIn("ARCHIVE_BAD: bad row", stderr)

    def test_table_rendering_removes_repository_control_sequences(self):
        payload = view(
            "requirements",
            [{"requirement_id": "Requirement 1", "priority": "must-have", "tasks": [], "title": "\x1b[31mUnsafe\x07", "diagnostics": []}],
        )
        output = io.StringIO()
        public_cli.render_table(payload, output)
        self.assertNotIn("\x1b", output.getvalue())
        self.assertNotIn("\x07", output.getvalue())
        self.assertIn("Unsafe", output.getvalue())

    def test_error_rendering_removes_repository_control_sequences(self):
        error = public_views.PublicViewError(
            "Unsafe\x1b[31m message",
            code="spec_ambiguous",
            candidates=["001-safe\x07"],
        )
        rendered = public_cli.format_error(error)
        self.assertNotIn("\x1b", rendered)
        self.assertNotIn("\x07", rendered)


class PublicCliRepositoryTests(unittest.TestCase):
    def test_valid_empty_repository_is_a_successful_empty_result(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".git").mkdir()
            stdout = io.StringIO()
            stderr = io.StringIO()
            code = public_cli.main(["specs", "--json", "-C", str(root)], stdout=stdout, stderr=stderr)
        self.assertEqual(0, code, stderr.getvalue())
        self.assertEqual([], json.loads(stdout.getvalue())["records"])
        self.assertEqual("", stderr.getvalue())

    def test_nested_working_directory_discovers_repository_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_query_repo(root)
            nested = root / "src/nested"
            nested.mkdir(parents=True)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(public_cli.public_views, "build_specs_view", return_value=view("specs", [])) as build:
                code = public_cli.main(["specs", "--json"], stdout=stdout, stderr=stderr, cwd=nested)
        self.assertEqual(0, code)
        self.assertEqual(root, build.call_args.args[0])

    def test_missing_explicit_repository_is_usage_error(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = public_cli.main(["specs", "-C", "/definitely/missing/slm-repo"], stdout=stdout, stderr=stderr)
        self.assertEqual(2, code)
        self.assertEqual("", stdout.getvalue())
        self.assertIn("does not exist", stderr.getvalue())

    def test_successful_query_is_read_only_and_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_query_repo(root)
            before = tree_snapshot(root)
            environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
            first = subprocess.run(
                [sys.executable, str(SCRIPT), "specs", "--json", "-C", str(root)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
            )
            second = subprocess.run(
                [sys.executable, str(SCRIPT), "specs", "--json", "-C", str(root)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
            )
            after = tree_snapshot(root)
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, after)
        payload = json.loads(first.stdout)
        self.assertEqual(".", payload["repo_root"])
        self.assertNotIn(str(root), first.stdout)


if __name__ == "__main__":
    unittest.main()
