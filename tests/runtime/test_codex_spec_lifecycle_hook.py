import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"


def run_hook(payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["SPEC_LIFECYCLE_HOOK_LOG"] = str(Path(tmp) / "hook.log.jsonl")
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=True,
            env=env,
        )


class CodexSpecLifecycleHookTests(unittest.TestCase):
    def test_hook_stays_quiet_when_spec_checks_pass(self):
        payload = {
            "hook_event_name": "PostToolUse",
            "cwd": str(ROOT),
            "tool_name": "apply_patch",
            "tool_response": {
                "output": "Updated the following files:\nM docs/specs/009-archived-spec-scan-hygiene/tasks.md\n"
            },
        }

        result = run_hook(payload)

        self.assertEqual("", result.stdout)
        self.assertEqual("", result.stderr)

    def test_hook_reports_advisory_findings_for_invalid_spec(self):
        payload = {
            "hook_event_name": "PostToolUse",
            "cwd": str(ROOT),
            "tool_name": "write_file",
            "tool_input": {
                "path": "docs/specs/002-spec-lifecycle-validation/requirements.md"
            },
        }

        result = run_hook(payload)
        data = json.loads(result.stdout)
        context = data["hookSpecificOutput"]["additionalContext"]

        self.assertIn("Spec lifecycle advisory checks found issues.", context)
        self.assertIn("ERROR", context)


if __name__ == "__main__":
    unittest.main()
