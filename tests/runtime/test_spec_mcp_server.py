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


def write_current_spec(repo: Path, relative: str = "docs/specs/001-current") -> Path:
    spec = repo / relative
    spec.mkdir(parents=True)
    frontmatter = "\n".join(
        [
            "---",
            "title: Current",
            "doc_type: spec",
            "status: draft",
            "owner: platform",
            "last_reviewed: 2026-06-06",
            "---",
            "",
        ]
    )
    artifact_frontmatter = lambda artifact: frontmatter.replace("status: draft", f"artifact_type: {artifact}\nstatus: draft")
    (spec / "requirements.md").write_text(
        artifact_frontmatter("requirements")
        + "# Requirements\n\n## Durable Source Baseline\n\n## Goals\n\n## Non-Goals\n\n## Requirements\n\n### Requirement 1: Current\n\n#### Acceptance Criteria\n\n1. GIVEN context, WHEN action, THEN result.\n\n## Correctness Properties\n\n- CP-001: Holds.\n\n## Success Criteria\n",
        encoding="utf-8",
    )
    (spec / "design.md").write_text(
        artifact_frontmatter("design")
        + "# Design\n\n## Overview\n\n## High-Level Design\n\n## Low-Level Design\n\n## Operational Considerations\n\n## Open Questions\n",
        encoding="utf-8",
    )
    (spec / "tasks.md").write_text(
        artifact_frontmatter("tasks")
        + "# Tasks\n\n- [ ] T001 Do work.\n  - Depends on: none\n  - Files: `docs/reference/current.md`\n  - Acceptance: Done.\n  - Evidence: Pending.\n",
        encoding="utf-8",
    )
    (spec / "traceability.md").write_text(
        artifact_frontmatter("traceability")
        + "\n".join(
            [
                "# Traceability Matrix",
                "",
                "## Task To Context Matrix",
                "",
                "| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |",
                "|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|",
                "| T001 | Requirement 1 | AC1 | `design.md#low-level-design` | none | `verification.md#quality-gates` | `docs/reference/current.md` | none |",
                "",
                "## Requirement To Delivery Matrix",
                "",
                "| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |",
                "|-------------|---------------------|-----------------|-------|--------------|-----------------|",
                "| Requirement 1 | AC1 | `design.md#low-level-design` | T001 | `verification.md#quality-gates` | `docs/reference/current.md` |",
                "",
                "## Design To Implementation Matrix",
                "",
                "| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |",
                "|----------------|--------------|-------|---------------------|--------------|",
                "| `design.md#low-level-design` | Requirement 1 | T001 | `docs/reference/current.md` | `verification.md#quality-gates` |",
                "",
                "## Open Decision Impact",
                "",
                "| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |",
                "|-------------|--------|-----------------------|----------------|-------------------|",
                "| none | none | Requirement 1 | T001 | none |",
            ]
        ),
        encoding="utf-8",
    )
    return spec


def rpc(request_id, method, params=None):
    message = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        message["params"] = params
    return message


class SpecMcpServerTests(unittest.TestCase):
    def send(self, *messages, root: Path = ROOT):
        completed = subprocess.run(
            [sys.executable, str(SERVER), str(root)],
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
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            responses = self.send(
                rpc(1, "tools/list"),
                rpc(2, "tools/call", {"name": "scan_specs", "arguments": {"repo_root": str(repo)}}),
                root=repo,
            )

        tools = {tool["name"] for tool in responses[0]["result"]["tools"]}
        self.assertIn("scan_specs", tools)
        self.assertIn("active_spec_preflight", tools)
        self.assertIn("agent_readiness_packet", tools)
        self.assertIn("agent_backed_tool", tools)
        self.assertIn("no_active_spec_context", tools)
        self.assertIn("closure_check", tools)
        self.assertIn("archive_index", tools)
        structured = responses[1]["result"]["structuredContent"]
        self.assertIn("specs", structured)
        self.assertEqual(0, structured["summary"]["total"])
        scan_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "scan_specs")
        self.assertIn("include_archived_lint", scan_schema["inputSchema"]["properties"])
        self.assertIn("boolean", scan_schema["inputSchema"]["properties"]["include_archived_lint"]["type"])

    def test_spec_path_tools_advertise_repo_root(self):
        [response] = self.send(rpc(1, "tools/list"))

        tools = {tool["name"]: tool for tool in response["result"]["tools"]}
        for name in [
            "agent_readiness_packet",
            "agent_backed_tool",
            "spec_summary",
            "lint_spec_package",
            "next_task",
            "closure_check",
            "reconcile_spec",
            "promotion_plan",
            "review_packet",
            "task_context",
            "traceability_lookup",
        ]:
            with self.subTest(tool=name):
                schema = tools[name]["inputSchema"]
                self.assertIn("repo_root", schema["properties"])
                self.assertIn("spec_path", schema["properties"])
                self.assertIn("spec_path", schema["required"])

    def test_agent_backed_tool_returns_unavailable_through_mcp(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            write_current_spec(repo)
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "agent_backed_tool",
                        "arguments": {
                            "repo_root": str(repo),
                            "spec_path": "001-current",
                            "tool_name": "closure_risk_review",
                            "model_class": "cheap",
                        },
                    },
                ),
                root=repo,
            )

        payload = response["result"]["structuredContent"]
        self.assertEqual("unavailable", payload["status"])
        self.assertEqual("disabled", payload["model_class"])
        self.assertTrue(payload["advisory"])

    def test_active_spec_preflight_and_readiness_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            write_current_spec(repo)
            responses = self.send(
                rpc(1, "tools/call", {"name": "active_spec_preflight", "arguments": {"repo_root": str(repo)}}),
                rpc(2, "tools/call", {"name": "agent_readiness_packet", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "task_id": "T001"}}),
                root=repo,
            )

        preflight = responses[0]["result"]["structuredContent"]
        readiness = responses[1]["result"]["structuredContent"]
        self.assertEqual("ready", preflight["status"])
        self.assertEqual("001-current", preflight["selected_spec"]["spec_id"])
        self.assertEqual("T001", readiness["task_id"])
        self.assertIn("Requirement 1", {item["id"] for item in readiness["required_review"]["requirements"]})

    def test_no_active_spec_context_tool(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            [response] = self.send(
                rpc(1, "tools/call", {"name": "no_active_spec_context", "arguments": {"repo_root": str(repo)}}),
                root=repo,
            )

        payload = response["result"]["structuredContent"]
        self.assertEqual("no_active_spec", payload["status"])
        self.assertIn("archive_index_summary", payload)

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

    def test_resource_read_returns_error_for_removed_or_missing_spec(self):
        [response] = self.send(rpc(1, "resources/read", {"uri": "specs://004-spec-management-mcp/summary"}))

        self.assertEqual(-32602, response["error"]["code"])
        self.assertIn("Active spec not found", response["error"]["message"])

    def test_nested_partition_spec_resolves_for_tools_and_resources(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_current_spec(repo, "docs/platform/specs/001-nested")
            responses = self.send(
                rpc(1, "tools/call", {"name": "scan_specs", "arguments": {"repo_root": str(repo)}}),
                rpc(2, "tools/call", {"name": "spec_summary", "arguments": {"repo_root": str(repo), "spec_path": "001-nested"}}),
                rpc(3, "resources/list"),
                rpc(4, "resources/read", {"uri": "specs://001-nested/summary"}),
                root=repo,
            )

        scan_payload = responses[0]["result"]["structuredContent"]
        self.assertEqual(str(spec), scan_payload["specs"][0]["path"])
        self.assertEqual("001-nested", responses[1]["result"]["structuredContent"]["spec_id"])
        uris = {resource["uri"] for resource in responses[2]["result"]["resources"]}
        self.assertIn("specs://001-nested/summary", uris)
        resource_payload = json.loads(responses[3]["result"]["contents"][0]["text"])
        self.assertEqual("001-nested", resource_payload["spec_id"])

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

    def test_prompt_resource_references_are_implemented(self):
        allowed_resources = {
            "specs://active",
            "specs://{spec_id}/summary",
            "specs://{spec_id}/health",
            "templates://spec-package",
            "governance://constitution",
            "history://spec-archive-index",
        }
        [response] = self.send(rpc(1, "tools/call", {"name": "prompts_validate", "arguments": {"repo_root": str(ROOT)}}))

        prompts = response["result"]["structuredContent"]["prompts"]
        used_resources = {resource for prompt in prompts for resource in prompt["resources"]}
        self.assertLessEqual(used_resources, allowed_resources)

    def test_unknown_tool_returns_json_rpc_error(self):
        [payload] = self.send(rpc(1, "tools/call", {"name": "missing_tool", "arguments": {}}))

        self.assertEqual(-32602, payload["error"]["code"])
        self.assertIn("Unknown tool", payload["error"]["message"])


if __name__ == "__main__":
    unittest.main()
