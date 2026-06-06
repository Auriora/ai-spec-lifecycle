import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVER = ROOT / "skills/spec-lifecycle-manager/scripts/spec_mcp_server.py"


def write_archived_old_format_spec(repo: Path) -> None:
    spec = repo / "docs/specs/001-old-format"
    spec.mkdir(parents=True)
    frontmatter = "\n".join(
        [
            "---",
            "title: Old format",
            "doc_type: spec",
            "status: archived",
            "owner: platform",
            "last_reviewed: 2026-06-06",
            "---",
            "",
        ]
    )
    (spec / "spec.md").write_text(frontmatter + "# Spec\n", encoding="utf-8")
    (spec / "tasks.md").write_text(frontmatter + "# Tasks\n\n- [ ] T001 Do work.\n", encoding="utf-8")


def rpc(request_id, method, params=None):
    message = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        message["params"] = params
    return message


class SpecMcpServerTests(unittest.TestCase):
    def send(self, *messages):
        completed = subprocess.run(
            [sys.executable, str(SERVER), str(ROOT)],
            input="\n".join(json.dumps(message) for message in messages) + "\n",
            check=True,
            capture_output=True,
            text=True,
        )
        return [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]

    def test_initialize_reports_read_only_capabilities(self):
        [payload] = self.send(rpc(1, "initialize", {"protocolVersion": "2025-06-18"}))

        result = payload["result"]
        self.assertEqual("2025-06-18", result["protocolVersion"])
        self.assertEqual("spec-lifecycle-manager", result["serverInfo"]["name"])
        self.assertIn("tools", result["capabilities"])
        self.assertIn("resources", result["capabilities"])
        self.assertIn("prompts", result["capabilities"])

    def test_tools_list_and_call_scan_specs(self):
        responses = self.send(
            rpc(1, "tools/list"),
            rpc(2, "tools/call", {"name": "scan_specs", "arguments": {"repo_root": str(ROOT)}}),
        )

        tools = {tool["name"] for tool in responses[0]["result"]["tools"]}
        self.assertIn("scan_specs", tools)
        self.assertIn("closure_check", tools)
        self.assertIn("archive_index", tools)
        structured = responses[1]["result"]["structuredContent"]
        self.assertIn("specs", structured)
        self.assertEqual(0, structured["summary"]["total"])
        scan_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "scan_specs")
        self.assertIn("include_archived_lint", scan_schema["inputSchema"]["properties"])
        self.assertIn("boolean", scan_schema["inputSchema"]["properties"]["include_archived_lint"]["type"])

    def test_scan_specs_can_include_archived_lint_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_archived_old_format_spec(repo)
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {"name": "scan_specs", "arguments": {"repo_root": str(repo), "include_archived_lint": True}},
                )
            )

        structured = response["result"]["structuredContent"]
        specs = {item["spec_id"]: item for item in structured["specs"]}
        self.assertEqual("error", specs["001-old-format"]["health"]["severity"])

    def test_resources_list_and_read_active_specs(self):
        responses = self.send(rpc(1, "resources/list"), rpc(2, "resources/read", {"uri": "specs://active"}))

        uris = {resource["uri"] for resource in responses[0]["result"]["resources"]}
        self.assertIn("specs://active", uris)
        content = responses[1]["result"]["contents"][0]
        payload = json.loads(content["text"])
        self.assertIn("specs", payload)

    def test_archive_index_tool_and_resource(self):
        responses = self.send(
            rpc(1, "tools/call", {"name": "archive_index", "arguments": {"repo_root": str(ROOT)}}),
            rpc(2, "resources/list"),
            rpc(3, "resources/read", {"uri": "history://spec-archive-index"}),
        )

        tool_payload = responses[0]["result"]["structuredContent"]
        self.assertEqual(0, tool_payload["summary"]["error"])
        self.assertIn("entries", tool_payload)
        uris = {resource["uri"] for resource in responses[1]["result"]["resources"]}
        self.assertIn("history://spec-archive-index", uris)
        resource_payload = json.loads(responses[2]["result"]["contents"][0]["text"])
        self.assertEqual(0, resource_payload["summary"]["error"])

    def test_prompts_list_and_get(self):
        responses = self.send(
            rpc(1, "prompts/list"),
            rpc(2, "prompts/get", {"name": "task-context", "arguments": {"spec_id": "004-spec-management-mcp", "task_id": "T010"}}),
        )

        prompts = {prompt["name"] for prompt in responses[0]["result"]["prompts"]}
        self.assertIn("task-context", prompts)
        message = responses[1]["result"]["messages"][0]
        self.assertEqual("user", message["role"])
        self.assertIn("Use the spec-lifecycle-manager skill", message["content"]["text"])

    def test_unknown_tool_returns_json_rpc_error(self):
        [payload] = self.send(rpc(1, "tools/call", {"name": "missing_tool", "arguments": {}}))

        self.assertEqual(-32602, payload["error"]["code"])
        self.assertIn("Unknown tool", payload["error"]["message"])


if __name__ == "__main__":
    unittest.main()
