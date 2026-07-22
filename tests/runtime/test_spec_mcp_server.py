import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVER = ROOT / "skills/spec-lifecycle-manager/scripts/spec_mcp_server.py"
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
RUNTIME_SCRIPT = SCRIPT_DIR / "spec_runtime.py"
sys.path.insert(0, str(SCRIPT_DIR))

import spec_mcp_server
import spec_runtime


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


def append_requirements_text(spec: Path, text: str) -> None:
    requirements = spec / "requirements.md"
    requirements.write_text(requirements.read_text(encoding="utf-8") + text, encoding="utf-8")


def rpc(request_id, method, params=None):
    message = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        message["params"] = params
    return message


class SpecMcpServerTests(unittest.TestCase):
    def test_mcp_server_uses_shared_core_not_runtime_adapter(self):
        source = SERVER.read_text(encoding="utf-8")
        self.assertIn("from lifecycle import core as lifecycle_core", source)
        self.assertNotIn("import spec_runtime", source)
        self.assertNotIn("spec_runtime.", source)

    def send(
        self,
        *messages,
        root: Path | None = ROOT,
        env: dict[str, str] | None = None,
        process_cwd: Path | None = None,
    ):
        process_env = None
        if env is not None:
            process_env = {**os.environ, **env}
        command = [sys.executable, str(SERVER)]
        if root is not None:
            command.append(str(root))
        completed = subprocess.run(
            command,
            input="\n".join(json.dumps(message) for message in messages) + "\n",
            check=True,
            capture_output=True,
            text=True,
            env=process_env,
            cwd=process_cwd,
        )
        return [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]

    def test_initialize_reports_read_only_capabilities(self):
        [payload] = self.send(rpc(1, "initialize", {"protocolVersion": "2025-06-18"}))

        result = payload["result"]
        self.assertEqual("2025-06-18", result["protocolVersion"])
        self.assertEqual("spec-lifecycle-manager", result["serverInfo"]["name"])
        self.assertEqual("0.6.0", result["serverInfo"]["version"])
        self.assertIn("tools", result["capabilities"])
        self.assertIn("resources", result["capabilities"])
        self.assertIn("prompts", result["capabilities"])
        self.assertIn("Prefer MCP tools", result["instructions"])
        self.assertIn("runtime scripts are for CI", result["instructions"])

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
        tools_with_output_schemas = [
            tool for tool in responses[0]["result"]["tools"] if "outputSchema" in tool
        ]
        self.assertGreater(len(tools_with_output_schemas), 0)
        for tool in tools_with_output_schemas:
            with self.subTest(tool=tool["name"]):
                self.assertEqual("object", tool["outputSchema"].get("type"))
        self.assertIn("scan_specs", tools)
        self.assertIn("spec_id_inventory", tools)
        self.assertIn("spec_creation_plan", tools)
        self.assertIn("active_spec_preflight", tools)
        self.assertIn("lifecycle_guide", tools)
        self.assertIn("bootstrap_plan", tools)
        self.assertIn("stage_readiness", tools)
        self.assertIn("validation_plan", tools)
        self.assertIn("agent_readiness_packet", tools)
        self.assertIn("agent_backed_tool", tools)
        self.assertIn("no_active_spec_context", tools)
        self.assertIn("closure_check", tools)
        self.assertIn("closure_plan", tools)
        self.assertIn("closure_apply", tools)
        self.assertIn("closure_resolve", tools)
        self.assertIn("archive_index", tools)
        self.assertIn("resolve_spec_reference", tools)
        self.assertIn("mcp_audit", tools)
        self.assertIn("list_tasks", tools)
        self.assertIn("task_details", tools)
        self.assertIn("task_state_audit", tools)
        self.assertIn("set_task_state", tools)
        self.assertIn("evidence_quality_check", tools)
        self.assertIn("closure_risk_review", tools)
        structured = responses[1]["result"]["structuredContent"]
        self.assertIn("specs", structured)
        self.assertEqual(".", structured["repo_root"])
        self.assertEqual(0, structured["summary"]["total"])
        scan_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "scan_specs")
        self.assertIn("include_archived_lint", scan_schema["inputSchema"]["properties"])
        self.assertIn("boolean", scan_schema["inputSchema"]["properties"]["include_archived_lint"]["type"])
        validation_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "validation_plan")
        self.assertEqual("array", validation_schema["inputSchema"]["properties"]["changed_files"]["type"])
        bootstrap_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "bootstrap_plan")
        self.assertIn("boolean", bootstrap_schema["inputSchema"]["properties"]["create_spec"]["type"])
        spec_id_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "spec_id_inventory")
        creation_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "spec_creation_plan")
        self.assertFalse(spec_id_schema["inputSchema"]["additionalProperties"])
        self.assertFalse(spec_id_schema["outputSchema"]["additionalProperties"])
        self.assertEqual(["slug"], creation_schema["inputSchema"]["required"])
        self.assertFalse(creation_schema["inputSchema"]["additionalProperties"])
        self.assertEqual(4, len(creation_schema["outputSchema"]["oneOf"]))
        self.assertEqual(
            ["numbering", "template", "validation"],
            creation_schema["inputSchema"]["properties"]["section"]["enum"],
        )
        self.assertTrue(all(not item["additionalProperties"] for item in creation_schema["outputSchema"]["oneOf"]))
        capabilities_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "lifecycle_capabilities")
        inventory_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "script_migration_inventory")
        traceability_schema = next(tool for tool in responses[0]["result"]["tools"] if tool["name"] == "traceability_lookup")
        self.assertIn("outputSchema", capabilities_schema)
        self.assertIn("outputSchema", inventory_schema)
        self.assertIn("outputSchema", traceability_schema)
        self.assertIn("available_next_actions", capabilities_schema["outputSchema"]["required"])
        self.assertIn("lifecycle_metadata", capabilities_schema["outputSchema"]["required"])
        metadata_schema = capabilities_schema["outputSchema"]["properties"]["lifecycle_metadata"]
        self.assertFalse(metadata_schema["additionalProperties"])
        self.assertEqual(
            ["mcp", "cli", "hook", "prompt", "unknown"],
            metadata_schema["properties"]["invocation_surface"]["enum"],
        )
        requirement_schema = traceability_schema["outputSchema"]["properties"]["requirements"]["items"]
        self.assertIn("priority", requirement_schema["properties"])

    def test_spec_allocation_mcp_tools_match_cli_decisions_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/specs/004-current").mkdir(parents=True)
            inventory_cli = subprocess.run(
                [sys.executable, str(RUNTIME_SCRIPT), "spec-id-inventory", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )
            creation_cli = subprocess.run(
                [
                    sys.executable,
                    str(RUNTIME_SCRIPT),
                    "spec-creation-plan",
                    "next-feature",
                    "--repo-root",
                    str(repo),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            inventory_mcp, _ = spec_mcp_server.call_tool(
                "spec_id_inventory", {"repo_root": str(repo)}, repo, "cwd"
            )
            creation_mcp, _ = spec_mcp_server.call_tool(
                "spec_creation_plan",
                {"repo_root": str(repo), "slug": "next-feature"},
                repo,
                "cwd",
            )

        inventory_cli_payload = json.loads(inventory_cli.stdout)
        creation_cli_payload = json.loads(creation_cli.stdout)
        inventory_cli_metadata = inventory_cli_payload.pop("lifecycle_metadata")
        creation_cli_metadata = creation_cli_payload.pop("lifecycle_metadata")
        inventory_mcp_metadata = inventory_mcp.pop("lifecycle_metadata")
        creation_mcp_metadata = creation_mcp.pop("lifecycle_metadata")
        self.assertEqual(inventory_cli_payload, inventory_mcp)
        self.assertEqual(creation_cli_payload, creation_mcp)
        self.assertEqual("cli", inventory_cli_metadata["invocation_surface"])
        self.assertEqual("cli", creation_cli_metadata["invocation_surface"])
        self.assertEqual("mcp", inventory_mcp_metadata["invocation_surface"])
        self.assertEqual("mcp", creation_mcp_metadata["invocation_surface"])

    def test_spec_creation_plan_mcp_reports_stale_invalid_and_missing_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            first, _ = spec_mcp_server.call_tool(
                "spec_creation_plan", {"repo_root": str(repo), "slug": "feature"}, repo, "cwd"
            )
            fingerprint = first["evidence_fingerprint"]
            (repo / "docs/specs/000-claimed").mkdir(parents=True)
            responses = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "spec_creation_plan",
                        "arguments": {
                            "repo_root": str(repo),
                            "slug": "feature",
                            "expected_fingerprint": fingerprint,
                        },
                    },
                ),
                rpc(
                    2,
                    "tools/call",
                    {"name": "spec_creation_plan", "arguments": {"repo_root": str(repo), "slug": "../bad"}},
                ),
                rpc(3, "tools/call", {"name": "spec_creation_plan", "arguments": {"repo_root": str(repo)}}),
                root=repo,
            )

        stale = responses[0]["result"]["structuredContent"]
        invalid = responses[1]["result"]["structuredContent"]
        self.assertEqual("stale", stale["status"])
        self.assertEqual("feature", stale["expansion"]["arguments"]["slug"])
        self.assertEqual("compact", stale["expansion"]["arguments"]["detail"])
        self.assertEqual("mcp", stale["lifecycle_metadata"]["invocation_surface"])
        self.assertEqual("invalid", invalid["decision"]["status"])
        self.assertIsNone(invalid["decision"]["proposed_path"])
        self.assertEqual(-32602, responses[2]["error"]["code"])
        self.assertNotIn(str(repo), json.dumps(responses))

    def test_spec_creation_plan_mcp_modes_and_cli_decision_parity(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            compact_response, full_response, section_response = self.send(
                rpc(1, "tools/call", {"name": "spec_creation_plan", "arguments": {"repo_root": str(repo), "slug": "feature"}}),
                rpc(2, "tools/call", {"name": "spec_creation_plan", "arguments": {"repo_root": str(repo), "slug": "feature", "detail": "full"}}),
                rpc(3, "tools/call", {"name": "spec_creation_plan", "arguments": {"repo_root": str(repo), "slug": "feature", "detail": "section", "section": "numbering"}}),
                root=repo,
            )
            compact = compact_response["result"]["structuredContent"]
            cli = subprocess.run(
                [sys.executable, str(RUNTIME_SCRIPT), "spec-creation-plan", "feature", "--repo-root", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )

        cli_payload = json.loads(cli.stdout)
        self.assertEqual("compact", compact["detail"])
        self.assertEqual("full", full_response["result"]["structuredContent"]["detail"])
        self.assertEqual("numbering", section_response["result"]["structuredContent"]["section"])
        self.assertEqual("mcp", compact["lifecycle_metadata"]["invocation_surface"])
        self.assertEqual("cli", cli_payload["lifecycle_metadata"]["invocation_surface"])
        compact.pop("lifecycle_metadata")
        cli_payload.pop("lifecycle_metadata")
        self.assertEqual(compact, cli_payload)

    def test_lifecycle_capabilities_tool_returns_stable_surface_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            [response] = self.send(
                rpc(1, "tools/call", {"name": "lifecycle_capabilities", "arguments": {"repo_root": str(repo)}}),
                root=repo,
            )

        payload = response["result"]["structuredContent"]
        self.assertEqual("ready", payload["status"])
        self.assertEqual("not_observed", payload["client_metadata_status"])
        self.assertEqual("spec-lifecycle-manager", payload["server"]["name"])
        self.assertEqual("0.6.0", payload["server"]["version"])
        self.assertFalse(payload["server"]["capabilities"]["tools"]["listChanged"])
        self.assertEqual("unknown", payload["client"]["name"])
        self.assertEqual("stable_tool_surface", payload["dynamic_tools"]["decision"])
        self.assertIn("available_next_actions", payload)
        metadata = payload["lifecycle_metadata"]
        self.assertEqual("mcp", metadata["invocation_surface"])
        self.assertEqual("argument", metadata["root_source"])
        self.assertEqual(".", metadata["repo_root"])
        self.assertNotIn(str(repo), json.dumps(metadata))

    def test_lifecycle_capabilities_retains_standard_initialize_client_metadata_in_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            responses = self.send(
                rpc(
                    1,
                    "initialize",
                    {
                        "protocolVersion": "2025-06-18",
                        "clientInfo": {"name": "ExampleClient", "version": "1.2.3"},
                        "capabilities": {"roots": {"listChanged": True}},
                    },
                ),
                rpc(2, "tools/call", {"name": "lifecycle_capabilities", "arguments": {"repo_root": str(repo)}}),
                root=repo,
            )

        payload = responses[1]["result"]["structuredContent"]
        self.assertEqual("ready", payload["status"])
        self.assertEqual("observed", payload["client_metadata_status"])
        self.assertEqual("ExampleClient", payload["client"]["name"])
        self.assertEqual("1.2.3", payload["client"]["version"])
        self.assertEqual("2025-06-18", payload["client"]["protocol_version"])
        self.assertEqual({"roots": {"listChanged": True}}, payload["client"]["capabilities"])
        self.assertEqual([], payload["limitations"])

    def test_lifecycle_capabilities_retains_mcp_default_root_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            argument_repo = base / "argument"
            environment_repo = base / "environment"
            cwd_repo = base / "cwd"
            for repo in (argument_repo, environment_repo, cwd_repo):
                repo.mkdir()
                (repo / ".git").mkdir()

            env = {
                "SPEC_LIFECYCLE_DEFAULT_REPO_ROOT": str(environment_repo),
                "SPEC_LIFECYCLE_REPO_ROOT": "",
                "CODEX_REPO_ROOT": "",
                "CODEX_WORKSPACE_ROOT": "",
                "CODEX_WORKSPACE": "",
                "WORKSPACE_ROOT": "",
            }
            [environment_response] = self.send(
                rpc(1, "tools/call", {"name": "lifecycle_capabilities", "arguments": {}}),
                root=None,
                env=env,
                process_cwd=cwd_repo,
            )
            [argument_response] = self.send(
                rpc(
                    2,
                    "tools/call",
                    {"name": "lifecycle_capabilities", "arguments": {"repo_root": str(argument_repo)}},
                ),
                root=None,
                env=env,
                process_cwd=cwd_repo,
            )
            env["SPEC_LIFECYCLE_DEFAULT_REPO_ROOT"] = ""
            [cwd_response] = self.send(
                rpc(3, "tools/call", {"name": "lifecycle_capabilities", "arguments": {}}),
                root=None,
                env=env,
                process_cwd=cwd_repo,
            )

        self.assertEqual("environment", environment_response["result"]["structuredContent"]["lifecycle_metadata"]["root_source"])
        self.assertEqual("argument", argument_response["result"]["structuredContent"]["lifecycle_metadata"]["root_source"])
        self.assertEqual("cwd", cwd_response["result"]["structuredContent"]["lifecycle_metadata"]["root_source"])

    def test_script_migration_inventory_tool_returns_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            for relative in [
                "skills/spec-lifecycle-manager/scripts/traceability_lookup.py",
                "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/traceability_lookup.py",
                "plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/traceability_lookup.py",
            ]:
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("print('legacy')\n", encoding="utf-8")
            [response] = self.send(
                rpc(1, "tools/call", {"name": "script_migration_inventory", "arguments": {"repo_root": str(repo)}}),
                root=repo,
            )

        payload = response["result"]["structuredContent"]
        self.assertEqual("ok", payload["status"])
        migrated = payload["migrated_scripts"]
        self.assertEqual(["traceability_lookup.py"], [item["script"] for item in migrated])
        self.assertEqual("traceability_lookup", migrated[0]["replacement_contract"]["replacement_mcp_tool"])
        self.assertEqual(3, len(payload["closure_blockers"]))
        self.assertTrue(all(item["code"] == "MIGRATED_SCRIPT_STILL_PRESENT" for item in payload["closure_blockers"]))

    def test_lifecycle_guide_and_bootstrap_plan_tools_are_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            responses = self.send(
                rpc(1, "tools/call", {"name": "lifecycle_guide", "arguments": {"repo_root": str(repo)}}),
                rpc(
                    2,
                    "tools/call",
                    {
                        "name": "bootstrap_plan",
                        "arguments": {
                            "repo_root": str(repo),
                            "project_summary": "Example project.",
                            "create_spec": True,
                            "spec_slug": "first-feature",
                        },
                    },
                ),
                root=repo,
            )

        guide = responses[0]["result"]["structuredContent"]
        bootstrap = responses[1]["result"]["structuredContent"]
        self.assertEqual("blank", guide["repo_classification"])
        self.assertEqual("preview", bootstrap["mode"])
        self.assertEqual(".", bootstrap["repo_root"])
        self.assertFalse((repo / "docs").exists())
        self.assertTrue(any(item["path"] == "docs/specs/000-first-feature/" for item in bootstrap["writes"]))

    def test_spec_path_tools_advertise_repo_root(self):
        [response] = self.send(rpc(1, "tools/list"))

        tools = {tool["name"]: tool for tool in response["result"]["tools"]}
        for name in [
            "agent_readiness_packet",
            "agent_backed_tool",
            "stage_readiness",
            "spec_summary",
            "lint_spec_package",
            "next_task",
            "list_tasks",
            "task_details",
            "task_state_audit",
            "set_task_state",
            "evidence_quality_check",
            "closure_risk_review",
            "closure_check",
            "closure_plan",
            "closure_apply",
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

    def test_closure_mcp_tools_preview_and_reject_missing_write_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            source = ROOT / "tests/fixtures/spec-closure-helper/spec-030-closure-scenario/before-cleanup"
            shutil.copytree(source, repo, dirs_exist_ok=True)
            responses = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "closure_plan",
                        "arguments": {
                            "repo_root": str(repo),
                            "spec_path": "030-mcp-first-runtime-migration",
                            "final_spec_commit": "de3aa4f",
                        },
                    },
                ),
                root=repo,
            )
            plan = responses[0]["result"]["structuredContent"]
            [apply_response] = self.send(
                rpc(
                    2,
                    "tools/call",
                    {
                        "name": "closure_apply",
                        "arguments": {
                            "repo_root": str(repo),
                            "spec_path": "030-mcp-first-runtime-migration",
                            "plan_id": plan["plan_id"],
                            "final_spec_commit": "de3aa4f",
                            "action_id": "render_records",
                            "dry_run": False,
                        },
                    },
                ),
                root=repo,
            )

        apply_payload = apply_response["result"]["structuredContent"]
        self.assertEqual("030-mcp-first-runtime-migration", plan["decision"]["spec_id"])
        self.assertEqual("summary", plan["detail"])
        self.assertLessEqual(len(json.dumps(plan).encode("utf-8")), 32768)
        self.assertEqual("rejected", apply_payload["status"])
        self.assertIn("CLOSURE_WRITE_INTENT_MISSING", {item["code"] for item in apply_payload["diagnostics"]})

    def test_tool_result_text_summarizes_without_duplicating_structured_payload(self):
        payload = {
            "status": "ready",
            "plan_id": "abc123",
            "edit_summaries": [{"preview": "x" * 5000}],
        }

        result = spec_mcp_server.tool_result(payload, ROOT)
        text = result["content"][0]["text"]

        self.assertEqual(payload, result["structuredContent"])
        self.assertLess(len(text.encode("utf-8")), 512)
        self.assertIn("status=ready", text)
        self.assertIn("plan_id=abc123", text)
        self.assertIn("structuredContent", text)
        self.assertNotIn("edit_summaries", text)
        self.assertNotIn("x" * 100, text)

    def test_closure_mcp_plan_is_bounded_and_actions_are_sequential_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            (repo / ".gitignore").write_text(".cache/\n", encoding="utf-8")
            (repo / ".cache").mkdir()
            (repo / ".cache/graph.sqlite-wal").write_text("030-mcp-first-runtime-migration" * 5000, encoding="utf-8")
            source = ROOT / "tests/fixtures/spec-closure-helper/spec-030-closure-scenario/before-cleanup"
            shutil.copytree(source, repo, dirs_exist_ok=True)
            history = repo / "docs/history/spec-closure-log.md"
            history.write_text(history.read_text(encoding="utf-8") + ("historical noise\n" * 10000), encoding="utf-8")
            spec = repo / "docs/specs/030-mcp-first-runtime-migration"
            compact, _ = spec_mcp_server.call_tool(
                "closure_plan",
                {"repo_root": str(repo), "spec_path": str(spec), "final_spec_commit": "de3aa4f"},
                repo,
                "cwd",
            )
            plan_id = compact["plan_id"]
            edits, _ = spec_mcp_server.call_tool(
                "closure_plan",
                {"repo_root": str(repo), "spec_path": str(spec), "final_spec_commit": "de3aa4f", "plan_id": plan_id, "detail": "section", "section": "edits"},
                repo,
                "cwd",
            )
            premature, _ = spec_mcp_server.call_tool(
                "closure_apply",
                {"repo_root": str(repo), "spec_path": str(spec), "plan_id": plan_id, "final_spec_commit": "de3aa4f", "action_id": "cleanup_package", "dry_run": False, "write_intent": True},
                repo,
                "cwd",
            )
            rendered, _ = spec_mcp_server.call_tool(
                "closure_apply",
                {"repo_root": str(repo), "spec_path": str(spec), "plan_id": plan_id, "final_spec_commit": "de3aa4f", "action_id": "render_records", "dry_run": False, "write_intent": True},
                repo,
                "cwd",
            )
            repeated, _ = spec_mcp_server.call_tool(
                "closure_apply",
                {"repo_root": str(repo), "spec_path": str(spec), "plan_id": plan_id, "final_spec_commit": "de3aa4f", "action_id": "render_records", "dry_run": False, "write_intent": True},
                repo,
                "cwd",
            )
            cleaned, _ = spec_mcp_server.call_tool(
                "closure_apply",
                {"repo_root": str(repo), "spec_path": str(spec), "plan_id": plan_id, "final_spec_commit": "de3aa4f", "action_id": "cleanup_package", "dry_run": False, "write_intent": True},
                repo,
                "cwd",
            )
            package_exists = spec.exists()
            log = (repo / "docs/history/spec-closure-log.md").read_text(encoding="utf-8")

        self.assertLessEqual(len(json.dumps(compact).encode("utf-8")), 32768)
        self.assertTrue(all("content" not in item for item in compact["edit_summaries"]))
        self.assertTrue(all(item["content_bytes"] >= 0 for item in edits["content"]["items"]))
        self.assertEqual("rejected", premature["status"])
        self.assertEqual("updated", rendered["status"])
        self.assertEqual("already_applied", repeated["status"])
        self.assertEqual("updated", cleaned["status"])
        self.assertFalse(package_exists)
        self.assertEqual(1, log.count(" - 030-mcp-first-runtime-migration"))

    def test_closure_mcp_rejects_stale_manifest_after_spec_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            source = ROOT / "tests/fixtures/spec-closure-helper/spec-030-closure-scenario/before-cleanup"
            shutil.copytree(source, repo, dirs_exist_ok=True)
            spec = repo / "docs/specs/030-mcp-first-runtime-migration"
            manifest, _ = spec_mcp_server.call_tool(
                "closure_plan",
                {"repo_root": str(repo), "spec_path": str(spec), "final_spec_commit": "de3aa4f"},
                repo,
                "cwd",
            )
            requirements = spec / "requirements.md"
            requirements.write_text(requirements.read_text(encoding="utf-8") + "\nChanged after planning.\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "CLOSURE_PLAN_STALE"):
                spec_mcp_server.call_tool(
                    "closure_apply",
                    {
                        "repo_root": str(repo),
                        "spec_path": str(spec),
                        "plan_id": manifest["plan_id"],
                        "final_spec_commit": "de3aa4f",
                        "action_id": "render_records",
                    },
                    repo,
                    "cwd",
                )

    def test_closure_mcp_resolve_previews_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            source = ROOT / "tests/fixtures/spec-closure-helper/spec-030-closure-scenario/after-cleanup-pending"
            shutil.copytree(source, repo, dirs_exist_ok=True)
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "closure_resolve",
                        "arguments": {
                            "repo_root": str(repo),
                            "spec_id": "030-mcp-first-runtime-migration",
                            "cleanup_commit": "520d37d",
                        },
                    },
                ),
                root=repo,
            )
            log_text = (repo / "docs/history/spec-closure-log.md").read_text(encoding="utf-8")

        payload = response["result"]["structuredContent"]
        self.assertEqual("preview", payload["status"])
        self.assertIn("docs/history/spec-closure-log.md", payload["planned_files"])
        self.assertIn("pending-cleanup-commit", log_text)

    def test_mcp_closure_handlers_do_not_call_runtime_script(self):
        source = (ROOT / "skills/spec-lifecycle-manager/scripts/spec_mcp_server.py").read_text(encoding="utf-8")
        closure_handler = source[source.index('if name == "closure_plan"'):source.index('if name == "archive_index"')]

        self.assertIn("lifecycle_core.closure_plan", closure_handler)
        self.assertIn("lifecycle_core.closure_apply", closure_handler)
        self.assertIn("lifecycle_core.closure_resolve", closure_handler)
        self.assertNotIn("spec_runtime.py", closure_handler)
        self.assertNotIn("subprocess", closure_handler)

    def test_review_packet_schema_publishes_type_mapping(self):
        [response] = self.send(rpc(1, "tools/list"))

        tools = {tool["name"]: tool for tool in response["result"]["tools"]}
        review_type = tools["review_packet"]["inputSchema"]["properties"]["review_type"]
        tool_name = tools["agent_backed_tool"]["inputSchema"]["properties"]["tool_name"]
        canonical = {item["value"] for item in review_type["x-canonical-review-types"]}
        aliases = {item["value"]: item["maps_to"] for item in review_type["x-review-type-aliases"]}

        self.assertEqual("design_requirements_trace", review_type["default"])
        self.assertEqual("design_requirements_trace", tool_name["default"])
        self.assertIn("implementation_review", canonical)
        self.assertIn("generic_review", canonical)
        self.assertEqual("implementation_review", aliases["implementation"])
        self.assertEqual("implementation_review", aliases["implementation-readiness"])
        self.assertIn("generic_review", review_type["x-unknown-type-behavior"])

    def test_review_packet_maps_aliases_through_mcp(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            write_current_spec(repo)
            responses = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "review_packet",
                        "arguments": {
                            "repo_root": str(repo),
                            "spec_path": "001-current",
                            "review_type": "implementation-readiness",
                            "model_class": "coding",
                        },
                    },
                ),
                rpc(
                    2,
                    "tools/call",
                    {
                        "name": "review_packet",
                        "arguments": {
                            "repo_root": str(repo),
                            "spec_path": "001-current",
                            "review_type": "release-polish",
                            "model_class": "coding",
                        },
                    },
                ),
                root=repo,
            )

        implementation = responses[0]["result"]["structuredContent"]
        generic = responses[1]["result"]["structuredContent"]
        self.assertEqual("implementation_review", implementation["review_type"])
        self.assertEqual("implementation-readiness", implementation["requested_review_type"])
        self.assertEqual("generic_review", generic["review_type"])
        self.assertEqual("release-polish", generic["requested_review_type"])

    def test_resolve_spec_reference_tool_reports_active_and_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            write_current_spec(repo)
            responses = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "resolve_spec_reference",
                        "arguments": {"repo_root": str(repo), "reference": "001-current"},
                    },
                ),
                rpc(
                    2,
                    "tools/call",
                    {
                        "name": "resolve_spec_reference",
                        "arguments": {"repo_root": str(repo), "reference": "999-missing"},
                    },
                ),
                root=repo,
            )

        active = responses[0]["result"]["structuredContent"]
        missing = responses[1]["result"]["structuredContent"]
        self.assertEqual("active", active["status"])
        self.assertEqual("docs/specs/001-current", active["path"])
        self.assertEqual("missing", missing["status"])
        self.assertIn("active_candidates", missing)

    def test_mcp_audit_tool_summarizes_session_mentions(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            sessions = Path(tmp) / "sessions"
            repo.mkdir()
            sessions.mkdir()
            (repo / ".git").mkdir()
            (sessions / "rollout.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"payload": {"role": "user", "content": "spec-lifecycle-manager.review_packet({})"}}),
                        json.dumps({"payload": {"role": "assistant", "content": "Unknown review packet type: implementation"}}),
                        json.dumps({"payload": {"role": "assistant", "content": "specs://active"}}),
                        json.dumps({"payload": {"role": "user", "content": "The specs are incomplete and missing verification."}}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "mcp_audit",
                        "arguments": {"repo_root": str(repo), "sessions_root": str(sessions)},
                    },
                ),
                root=repo,
            )

        payload = response["result"]["structuredContent"]
        self.assertEqual("ok", payload["status"])
        self.assertEqual(1, payload["matched_files"])
        self.assertEqual(1, payload["error_counts"]["unknown_review_packet_type"])
        self.assertGreaterEqual(payload["interaction_counts"]["spec_incomplete_or_stale"], 1)
        self.assertGreaterEqual(payload["interaction_counts"]["spec_missing_artifacts"], 1)
        self.assertNotIn("sessions", payload)

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
                rpc(3, "tools/call", {"name": "stage_readiness", "arguments": {"repo_root": str(repo), "spec_path": "001-current"}}),
                root=repo,
            )

        preflight = responses[0]["result"]["structuredContent"]
        readiness = responses[1]["result"]["structuredContent"]
        stage = responses[2]["result"]["structuredContent"]
        self.assertEqual("ready", preflight["status"])
        self.assertEqual("001-current", preflight["selected_spec"]["spec_id"])
        self.assertEqual("docs/specs/001-current", preflight["selected_spec"]["path"])
        self.assertIn("available_next_actions", preflight)
        self.assertTrue(any(item["id"] == "create_verification" for item in preflight["available_next_actions"]))
        self.assertEqual("T001", readiness["task_id"])
        self.assertEqual("001-current", stage["spec_id"])
        self.assertIn("coverage", stage)
        self.assertIn("available_next_actions", stage)
        self.assertIn("Requirement 1", {item["id"] for item in readiness["required_review"]["requirements"]})

    def test_active_spec_actions_are_mcp_primary_with_separate_cli_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            write_current_spec(repo)
            responses = self.send(
                rpc(1, "tools/call", {"name": "active_spec_preflight", "arguments": {"repo_root": str(repo)}}),
                rpc(2, "tools/call", {"name": "lifecycle_capabilities", "arguments": {"repo_root": str(repo)}}),
                root=repo,
            )

        payload = responses[0]["result"]["structuredContent"]
        self.assertTrue(payload["available_next_actions"])
        self.assertTrue(all(action["interface"] == "mcp" for action in payload["available_next_actions"]))
        recovery = payload["validation_or_recovery"]
        self.assertEqual("mcp_unavailable", recovery["applies_when"])
        self.assertNotIn("fallback_reason", recovery)
        self.assertTrue(all(not item["command"].startswith("/") for item in recovery["commands"]))
        capabilities = responses[1]["result"]["structuredContent"]
        self.assertEqual("mcp", capabilities["lifecycle_metadata"]["invocation_surface"])
        self.assertIn("validation_or_recovery", capabilities)
        self.assertFalse(
            any(item["command"].endswith("--spec-path ") for item in capabilities["validation_or_recovery"]["commands"])
        )

    def test_mcp_context_tools_include_source_requirement_priority(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_current_spec(repo)
            requirements = spec / "requirements.md"
            requirements.write_text(
                requirements.read_text(encoding="utf-8").replace(
                    "### Requirement 1: Current",
                    "### Requirement 1: Current\n\n**Priority:** could-have",
                ),
                encoding="utf-8",
            )
            responses = self.send(
                rpc(1, "tools/call", {"name": "task_context", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "task_id": "T001"}}),
                rpc(2, "tools/call", {"name": "traceability_lookup", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "task_id": "T001"}}),
                rpc(3, "tools/call", {"name": "traceability_lookup", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "requirement": "Requirement 1"}}),
                rpc(4, "tools/call", {"name": "agent_readiness_packet", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "task_id": "T001"}}),
                root=repo,
            )

        task_context = responses[0]["result"]["structuredContent"]
        task_lookup = responses[1]["result"]["structuredContent"]
        requirement_lookup = responses[2]["result"]["structuredContent"]
        readiness = responses[3]["result"]["structuredContent"]
        self.assertNotIn("Priority", task_context["traceability_row"])
        self.assertEqual("could-have", task_context["requirements"][0]["priority"])
        self.assertEqual("could-have", task_lookup["requirements"][0]["priority"])
        self.assertEqual("could-have", requirement_lookup["requirements"][0]["priority"])
        self.assertEqual("could-have", readiness["traceability_context"]["requirements"][0]["priority"])
        self.assertEqual("could-have", readiness["required_review"]["requirements"][0]["priority"])

    def test_lint_spec_package_returns_shared_canonical_context_diagnostic_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_current_spec(repo)
            append_requirements_text(
                spec,
                "\n\n## Stale Doc Risk\n\nLegacy docs may be non-canonical background sources.\n",
            )
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "lint_spec_package",
                        "arguments": {"repo_root": str(repo), "spec_path": "001-current"},
                    },
                ),
                root=repo,
            )

        payload = response["result"]["structuredContent"]
        diagnostic = next(item for item in payload["diagnostics"] if item["code"] == "CANONICAL_CONTEXT_MISSING")
        self.assertEqual("warn", diagnostic["severity"])
        self.assertTrue(diagnostic["advisory"])
        self.assertFalse(diagnostic["blocking"])
        self.assertIn("stale-doc-risk", diagnostic["signals"])

    def test_task_query_tools_return_structured_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            write_current_spec(repo)
            responses = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "list_tasks",
                        "arguments": {"repo_root": str(repo), "spec_path": "001-current"},
                    },
                ),
                rpc(
                    2,
                    "tools/call",
                    {
                        "name": "task_details",
                        "arguments": {"repo_root": str(repo), "spec_path": "001-current", "task_id": "T001"},
                    },
                ),
                root=repo,
            )

        listed = responses[0]["result"]["structuredContent"]
        details = responses[1]["result"]["structuredContent"]
        self.assertEqual(1, listed["summary"]["total"])
        self.assertEqual("T001", listed["phases"][0]["tasks"][0]["task_id"])
        self.assertIn("dependency_state", listed["phases"][0]["tasks"][0])
        self.assertEqual("T001", details["task_id"])
        self.assertEqual("Requirement 1", details["traceability_context"]["traceability_row"]["Requirements"])
        self.assertTrue(details["dependency_state"]["ready"])

    def test_task_state_audit_and_update_tools_return_structured_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            write_current_spec(repo)
            responses = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "task_state_audit",
                        "arguments": {"repo_root": str(repo), "spec_path": "001-current"},
                    },
                ),
                rpc(
                    2,
                    "tools/call",
                    {
                        "name": "set_task_state",
                        "arguments": {
                            "repo_root": str(repo),
                            "spec_path": "001-current",
                            "task_id": "T001",
                            "state": "complete",
                            "evidence": "Unit tests passed.",
                        },
                    },
                ),
                root=repo,
            )

        audit = responses[0]["result"]["structuredContent"]
        update = responses[1]["result"]["structuredContent"]
        self.assertIn("summary", audit)
        self.assertEqual("preview", update["status"])
        self.assertTrue(update["dry_run"])
        self.assertTrue(update["validation"]["valid"])

    def test_validation_plan_tool_matches_runtime_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_current_spec(repo)
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "validation_plan",
                        "arguments": {
                            "repo_root": str(repo),
                            "changed_files": ["docs/reference/current.md"],
                            "spec_path": "001-current",
                            "task_id": "T001",
                        },
                    },
                ),
                root=repo,
            )
            expected = spec_mcp_server.normalize_mcp_payload(
                spec_runtime.validation_plan(repo, ["docs/reference/current.md"], spec, "T001"),
                repo,
            )
        payload = response["result"]["structuredContent"]
        self.assertEqual(expected, payload)
        self.assertEqual("not_applicable", {item["id"]: item for item in payload["checks"]}["unit-tests"]["applicability"])
        self.assertEqual("planned", payload["validation_contract"]["status"])

    def test_evidence_quality_check_tool_returns_structured_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_current_spec(repo)
            (spec / "tasks.md").write_text(
                (spec / "tasks.md").read_text(encoding="utf-8").replace("- [ ] T001", "- [x] T001").replace("Evidence: Pending.", "Evidence: Done."),
                encoding="utf-8",
            )
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "evidence_quality_check",
                        "arguments": {"repo_root": str(repo), "spec_path": "001-current"},
                    },
                ),
                root=repo,
            )
            expected = spec_mcp_server.normalize_mcp_payload(spec_runtime.evidence_quality_check(spec), repo)

        payload = response["result"]["structuredContent"]
        self.assertEqual(expected, payload)
        self.assertTrue(payload["advisory"])
        self.assertFalse(payload["mutates_files"])
        self.assertEqual("vague", payload["records"][0]["classification"])
        self.assertEqual("EVIDENCE_VAGUE", payload["diagnostics"][0]["code"])

    def test_closure_risk_review_tool_returns_structured_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_current_spec(repo)
            (spec / "verification.md").write_text(
                "# Verification\n\n## Quality Gates\n\n| Gate | Required | Status | Evidence |\n|------|----------|--------|----------|\n| MCP payload | yes | pass | `python3 -m unittest tests.runtime.test_spec_mcp_server` passed. |\n",
                encoding="utf-8",
            )
            (repo / "docs/reference").mkdir(parents=True)
            (repo / "docs/reference/current.md").write_text("# Current\n", encoding="utf-8")
            (spec / "tasks.md").write_text(
                (spec / "tasks.md")
                .read_text(encoding="utf-8")
                .replace("- [ ] T001", "- [x] T001")
                .replace("Evidence: Pending.", "Evidence: `python3 -m unittest tests.runtime.test_spec_mcp_server` passed."),
                encoding="utf-8",
            )
            [response] = self.send(
                rpc(
                    1,
                    "tools/call",
                    {
                        "name": "closure_risk_review",
                        "arguments": {"repo_root": str(repo), "spec_path": "001-current"},
                    },
                ),
                root=repo,
            )
            expected = spec_mcp_server.normalize_mcp_payload(spec_runtime.closure_risk_review(spec), repo)

        payload = response["result"]["structuredContent"]
        self.assertEqual(expected, payload)
        self.assertTrue(payload["advisory"])
        self.assertFalse(payload["mutates_files"])
        self.assertIn("signals", payload)
        self.assertIn(payload["risk_level"], {"low", "medium", "high"})

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
        self.assertIn("available_next_actions", payload)
        self.assertTrue(any(item["id"] == "review_backlog" for item in payload["available_next_actions"]))

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
        self.assertEqual(".", payload["repo_root"])
        self.assertEqual(".", payload["resource_binding"]["repo_root"])
        self.assertEqual("repo-relative", payload["resource_binding"]["path_policy"])
        self.assertNotIn(str(ROOT), content["text"])

    def test_resources_use_workspace_env_when_server_has_no_root_argument(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "target"
            repo.mkdir()
            (repo / ".git").mkdir()
            write_current_spec(repo)
            [response] = self.send(
                rpc(1, "resources/read", {"uri": "specs://active"}),
                root=None,
                env={"SPEC_LIFECYCLE_REPO_ROOT": str(repo)},
            )

        content = response["result"]["contents"][0]
        payload = json.loads(content["text"])
        self.assertEqual(".", payload["repo_root"])
        self.assertEqual("docs/specs/001-current", payload["specs"][0]["path"])
        self.assertEqual(".", payload["resource_binding"]["repo_root"])
        self.assertNotIn(str(repo), content["text"])

    def test_resources_use_launcher_default_root_when_launched_from_plugin_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "target"
            plugin = base / "plugin"
            repo.mkdir()
            plugin.mkdir()
            (repo / ".git").mkdir()
            write_current_spec(repo)
            [response] = self.send(
                rpc(1, "resources/read", {"uri": "specs://active"}),
                root=None,
                env={"SPEC_LIFECYCLE_DEFAULT_REPO_ROOT": str(repo), "PWD": str(plugin)},
                process_cwd=plugin,
            )

        content = response["result"]["contents"][0]
        payload = json.loads(content["text"])
        self.assertEqual(".", payload["repo_root"])
        self.assertEqual("docs/specs/001-current", payload["specs"][0]["path"])
        self.assertEqual(".", payload["resource_binding"]["repo_root"])
        self.assertNotIn(str(repo), content["text"])

    def test_server_repo_root_flag_overrides_launcher_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            env_repo = base / "env-target"
            arg_repo = base / "arg-target"
            env_repo.mkdir()
            arg_repo.mkdir()
            (env_repo / ".git").mkdir()
            (arg_repo / ".git").mkdir()
            write_current_spec(env_repo, "docs/specs/001-env")
            write_current_spec(arg_repo, "docs/specs/002-arg")

            command = [sys.executable, str(SERVER), "--repo-root", str(arg_repo)]
            completed = subprocess.run(
                command,
                input=json.dumps(rpc(1, "resources/read", {"uri": "specs://active"})) + "\n",
                check=True,
                capture_output=True,
                text=True,
                env={**os.environ, "SPEC_LIFECYCLE_DEFAULT_REPO_ROOT": str(env_repo)},
                cwd=env_repo,
            )

        [response] = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
        content = response["result"]["contents"][0]
        payload = json.loads(content["text"])
        self.assertEqual("docs/specs/002-arg", payload["specs"][0]["path"])

    def test_archive_index_tool_and_resource(self):
        responses = self.send(
            rpc(1, "tools/call", {"name": "archive_index", "arguments": {"repo_root": str(ROOT)}}),
            rpc(2, "resources/list"),
            rpc(3, "resources/read", {"uri": "history://spec-archive-index"}),
        )

        tool_payload = responses[0]["result"]["structuredContent"]
        self.assertEqual(0, tool_payload["summary"]["error"])
        self.assertIn("entries", tool_payload)
        self.assertEqual(".", tool_payload["repo_root"])
        uris = {resource["uri"] for resource in responses[1]["result"]["resources"]}
        self.assertIn("history://spec-archive-index", uris)
        resource_payload = json.loads(responses[2]["result"]["contents"][0]["text"])
        self.assertEqual(0, resource_payload["summary"]["error"])
        self.assertEqual(".", resource_payload["repo_root"])

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
        self.assertEqual("docs/platform/specs/001-nested", scan_payload["specs"][0]["path"])
        self.assertEqual("001-nested", responses[1]["result"]["structuredContent"]["spec_id"])
        uris = {resource["uri"] for resource in responses[2]["result"]["resources"]}
        self.assertIn("specs://001-nested/summary", uris)
        resource_payload = json.loads(responses[3]["result"]["contents"][0]["text"])
        self.assertEqual("001-nested", resource_payload["spec_id"])

    def test_spec_template_resource_uses_skill_fallback_without_repo_spec_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            (repo / "docs/templates").mkdir(parents=True)
            (repo / "docs/templates/README.md").write_text("# Durable templates\n", encoding="utf-8")
            [response] = self.send(rpc(1, "resources/read", {"uri": "templates://spec-package"}), root=repo)

        payload = json.loads(response["result"]["contents"][0]["text"])
        self.assertEqual("skill-fallback", payload["template_authority"]["authority"])
        self.assertIn("requirements.md", payload["templates"])
        self.assertNotIn("path", payload)

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

    def test_phase_gate_tool_publishes_closed_selector_and_output_contract(self):
        [response] = self.send(rpc(1, "tools/list"))
        tool = {item["name"]: item for item in response["result"]["tools"]}["phase_gate_check"]

        self.assertEqual(["spec_path"], tool["inputSchema"]["required"])
        self.assertFalse(tool["inputSchema"]["additionalProperties"])
        self.assertEqual(
            ["source_signals", "coverage", "validation", "promotion", "closure"],
            tool["inputSchema"]["properties"]["section"]["enum"],
        )
        self.assertEqual(4, len(tool["outputSchema"]["oneOf"]))

    def test_phase_gate_mcp_modes_stale_metadata_and_cli_parity(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_current_spec(repo)
            compact_response, full_response, section_response, stale_response = self.send(
                rpc(1, "tools/call", {"name": "phase_gate_check", "arguments": {"repo_root": str(repo), "spec_path": "001-current"}}),
                rpc(2, "tools/call", {"name": "phase_gate_check", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "detail": "full"}}),
                rpc(3, "tools/call", {"name": "phase_gate_check", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "detail": "section", "section": "coverage"}}),
                rpc(4, "tools/call", {"name": "phase_gate_check", "arguments": {"repo_root": str(repo), "spec_path": "001-current", "expected_fingerprint": "sha256:" + "0" * 64}}),
                root=repo,
            )
            compact = compact_response["result"]["structuredContent"]
            cli = subprocess.run(
                [sys.executable, str(ROOT / "skills/spec-lifecycle-manager/scripts/spec_runtime.py"), "phase-gate-check", str(spec)],
                check=True, capture_output=True, text=True,
            )

        self.assertEqual("compact", compact["detail"])
        self.assertEqual("full", full_response["result"]["structuredContent"]["detail"])
        self.assertEqual("coverage", section_response["result"]["structuredContent"]["section"])
        self.assertEqual("stale", stale_response["result"]["structuredContent"]["status"])
        self.assertEqual("mcp", compact["lifecycle_metadata"]["invocation_surface"])
        self.assertEqual("argument", compact["lifecycle_metadata"]["root_source"])
        cli_payload = json.loads(cli.stdout)
        self.assertEqual("cli", cli_payload["lifecycle_metadata"]["invocation_surface"])
        compact.pop("lifecycle_metadata")
        cli_payload.pop("lifecycle_metadata")
        self.assertEqual(compact, cli_payload)
        self.assertNotIn(str(repo), json.dumps(compact))

    def test_phase_gate_rejects_invalid_selector_combinations(self):
        missing_section, misplaced_section = self.send(
            rpc(1, "tools/call", {"name": "phase_gate_check", "arguments": {"spec_path": "033-phase-gate-check", "detail": "section"}}),
            rpc(2, "tools/call", {"name": "phase_gate_check", "arguments": {"spec_path": "033-phase-gate-check", "detail": "compact", "section": "coverage"}}),
        )
        self.assertIn("section is required", missing_section["error"]["message"])
        self.assertIn("section is only valid", misplaced_section["error"]["message"])


if __name__ == "__main__":
    unittest.main()
