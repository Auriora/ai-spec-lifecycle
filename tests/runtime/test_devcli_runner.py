from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEVCLI_SRC = REPO_ROOT / "tools" / "devcli" / "src"
if str(DEVCLI_SRC) not in sys.path:
    sys.path.insert(0, str(DEVCLI_SRC))

from auriora_dev.repo import discover_repo_root, repo_relative
from auriora_dev.runner import CommandSpec, render_plan, run_plan, shell_quote


class DevCliRepoTests(unittest.TestCase):
    def test_discovers_repo_root_from_nested_path(self) -> None:
        nested = REPO_ROOT / "tools" / "devcli" / "src" / "auriora_dev"

        self.assertEqual(discover_repo_root(nested), REPO_ROOT)

    def test_repo_relative_uses_absolute_path_outside_repo(self) -> None:
        inside = REPO_ROOT / "tools" / "devcli" / "pyproject.toml"

        self.assertEqual(
            repo_relative(inside, REPO_ROOT),
            "tools/devcli/pyproject.toml",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            outside = Path(tmpdir) / "outside.txt"
            outside.write_text("x", encoding="utf-8")
            self.assertEqual(repo_relative(outside, REPO_ROOT), str(outside))


class DevCliRunnerTests(unittest.TestCase):
    def test_render_plan_includes_order_mutation_cwd_and_quoted_command(self) -> None:
        command = CommandSpec.from_argv(
            "example",
            ["python3", "-m", "unittest", "name with space"],
            cwd=REPO_ROOT / "tools" / "devcli",
            mutates=False,
        )

        self.assertEqual(
            render_plan([command], repo_root=REPO_ROOT),
            [
                "1. example [read-only] (cwd: tools/devcli): "
                "python3 -m unittest 'name with space'"
            ],
        )

    def test_run_plan_stops_after_first_failure(self) -> None:
        calls: list[list[str]] = []

        def fake_runner(argv: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            calls.append(argv)
            return subprocess.CompletedProcess(
                argv,
                returncode=1 if argv[0] == "fail" else 0,
                stdout="out",
                stderr="err",
            )

        commands = [
            CommandSpec.from_argv("ok", ["ok"]),
            CommandSpec.from_argv("fail", ["fail"]),
            CommandSpec.from_argv("skipped", ["skipped"]),
        ]

        results = run_plan(commands, repo_root=REPO_ROOT, runner=fake_runner)

        self.assertEqual([result.exit_code for result in results], [0, 1])
        self.assertEqual(calls, [["ok"], ["fail"]])
        self.assertEqual(results[1].stdout, "out")
        self.assertEqual(results[1].stderr, "err")

    def test_dry_run_does_not_call_runner(self) -> None:
        def fake_runner(*_: object, **__: object) -> subprocess.CompletedProcess[str]:
            raise AssertionError("runner should not be called in dry-run mode")

        command = CommandSpec.from_argv("would run", ["python3", "--version"])

        results = run_plan(
            [command],
            repo_root=REPO_ROOT,
            dry_run=True,
            runner=fake_runner,
        )

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].ok)
        self.assertEqual(results[0].elapsed_seconds, 0.0)

    def test_shell_quote_handles_single_quotes(self) -> None:
        self.assertEqual(shell_quote(["echo", "Bob's file"]), "echo 'Bob'\"'\"'s file'")


if __name__ == "__main__":
    unittest.main()
