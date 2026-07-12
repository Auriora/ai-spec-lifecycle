"""Retained runtime adapter for spec lifecycle recovery commands."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from lifecycle.core import *  # noqa: F401,F403 - runtime dispatch compatibility
from lifecycle.capabilities import lifecycle_capabilities
from lifecycle.provenance import assemble_lifecycle_metadata


WORKSPACE_ROOT_ENV_VARS = (
    "SPEC_LIFECYCLE_DEFAULT_REPO_ROOT",
    "SPEC_LIFECYCLE_REPO_ROOT",
    "CODEX_REPO_ROOT",
    "CODEX_WORKSPACE_ROOT",
    "CODEX_WORKSPACE",
    "WORKSPACE_ROOT",
)


def _find_repo_root(path: Path) -> Path:
    start = path.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def capabilities_root(argument: Path | None) -> tuple[Path, str]:
    if argument is not None:
        return _find_repo_root(argument), "argument"
    for name in WORKSPACE_ROOT_ENV_VARS:
        value = os.environ.get(name)
        if value:
            return _find_repo_root(Path(value)), "environment"
    return _find_repo_root(Path.cwd()), "cwd"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Spec lifecycle runtime helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    capabilities = sub.add_parser("lifecycle-capabilities", help="Report lifecycle runtime capability visibility.")
    capabilities.add_argument("repo_root", type=Path, nargs="?", default=None)

    scan = sub.add_parser("scan", help="Scan active spec packages.")
    scan.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    scan.add_argument("--docs-root")
    scan.add_argument("--include-archived-lint", action="store_true", help="Run authoring lint against archived specs during scan.")

    summary = sub.add_parser("summary", help="Return specs://{id}/summary style payload.")
    summary.add_argument("spec_path", type=Path)

    lint = sub.add_parser("lint", help="Lint a spec package or document.")
    lint.add_argument("path", type=Path)
    lint.add_argument("--artifact-type")
    lint.add_argument("--mode", choices=["wizard", "full"], default="wizard", help="Package lint mode. Wizard mode validates only the current staged authoring slice.")

    next_cmd = sub.add_parser("next-task", help="Return the next runnable task with context.")
    next_cmd.add_argument("spec_path", type=Path)

    list_tasks = sub.add_parser("list-tasks", help="Return grouped task records for a spec package.")
    list_tasks.add_argument("spec_path", type=Path)
    list_tasks.add_argument("--status")
    list_tasks.add_argument("--no-subtasks", action="store_true")

    details = sub.add_parser("task-details", help="Return task detail with traceability context.")
    details.add_argument("spec_path", type=Path)
    details.add_argument("--task-id", required=True)

    state_audit = sub.add_parser("task-state-audit", help="Audit task state and evidence consistency.")
    state_audit.add_argument("spec_path", type=Path)
    state_audit.add_argument("--task-id")

    set_state = sub.add_parser("set-task-state", help="Preview or write a guarded task state update.")
    set_state.add_argument("spec_path", type=Path)
    set_state.add_argument("--task-id", required=True)
    set_state.add_argument("--state", required=True)
    set_state.add_argument("--evidence", required=True)
    set_state.add_argument("--status-note")
    set_state.add_argument("--evidence-mode")
    set_state.add_argument("--destination")
    set_state.add_argument("--decision-owner")
    set_state.add_argument("--write", action="store_true")
    set_state.add_argument("--write-intent", action="store_true")

    preflight = sub.add_parser("active-spec-preflight", help="Return active spec, next task, required context, and validation commands.")
    preflight.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    preflight.add_argument("--spec-path", type=Path)
    preflight.add_argument("--task-id")
    preflight.add_argument("--docs-root")

    guide = sub.add_parser("lifecycle-guide", help="Return first-run lifecycle readiness and next actions.")
    guide.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    guide.add_argument("--docs-root")
    guide.add_argument("--mode", default="auto")

    bootstrap = sub.add_parser("bootstrap-plan", help="Preview minimal lifecycle bootstrap writes for blank or near-blank repos.")
    bootstrap.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    bootstrap.add_argument("--docs-root", default="docs")
    bootstrap.add_argument("--project-summary")
    bootstrap.add_argument("--create-spec", action="store_true")
    bootstrap.add_argument("--spec-slug")

    stage = sub.add_parser("stage-readiness", help="Return staged artifact, coverage, and agent readiness status.")
    stage.add_argument("spec_path", type=Path)

    validation = sub.add_parser("validation-plan", help="Plan validation checks from changed files and optional task context.")
    validation.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    validation.add_argument("--changed-files", nargs="*", default=[])
    validation.add_argument("--spec-path", type=Path)
    validation.add_argument("--task-id")
    validation.add_argument("--risk-level")

    evidence = sub.add_parser("evidence-quality", help="Review task and verification evidence quality.")
    evidence.add_argument("spec_path", type=Path)

    readiness = sub.add_parser("agent-readiness-packet", help="Return bounded implementation context for a task.")
    readiness.add_argument("spec_path", type=Path)
    readiness.add_argument("--task-id", required=True)

    no_active = sub.add_parser("no-active-spec-context", help="Return durable context to use when no active spec exists.")
    no_active.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())

    closure = sub.add_parser("closure-check", help="Check spec closure readiness.")
    closure.add_argument("spec_path", type=Path)

    closure_plan_cmd = sub.add_parser("closure-plan", help="Preview closure metadata, edits, blockers, and validation commands.")
    closure_plan_cmd.add_argument("spec_path", type=Path)
    closure_plan_cmd.add_argument("--repo-root", type=Path)
    closure_plan_cmd.add_argument("--final-spec-commit")
    closure_plan_cmd.add_argument("--closure-action", default="removed")
    closure_plan_cmd.add_argument("--no-reference-scan", action="store_true")

    closure_apply_cmd = sub.add_parser("closure-apply", help="Preview or apply a closure planned action from a plan file.")
    closure_apply_cmd.add_argument("spec_path", type=Path)
    closure_apply_cmd.add_argument("--repo-root", type=Path)
    closure_apply_cmd.add_argument("--plan-file", type=Path, required=True)
    closure_apply_cmd.add_argument("--action-id", required=True)
    closure_apply_cmd.add_argument("--write", action="store_true")
    closure_apply_cmd.add_argument("--write-intent", action="store_true")

    closure_resolve_cmd = sub.add_parser("closure-resolve", help="Preview or apply cleanup-hash resolution in closure records.")
    closure_resolve_cmd.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    closure_resolve_cmd.add_argument("--spec-id", required=True)
    closure_resolve_cmd.add_argument("--cleanup-commit")
    closure_resolve_cmd.add_argument("--write", action="store_true")
    closure_resolve_cmd.add_argument("--write-intent", action="store_true")

    closure_risk = sub.add_parser("closure-risk-review", help="Review closure risk signals without mutating files.")
    closure_risk.add_argument("spec_path", type=Path)

    reconcile = sub.add_parser("reconcile", help="Generate a classified reconciliation report.")
    reconcile.add_argument("spec_path", type=Path)

    promote = sub.add_parser("promotion-plan", help="Generate durable documentation promotion targets.")
    promote.add_argument("spec_path", type=Path)

    packet = sub.add_parser("review-packet", help="Generate a bounded review packet.")
    packet.add_argument("spec_path", type=Path)
    packet.add_argument("--review-type", default="design_requirements_trace")
    packet.add_argument("--model-class")

    agent_tool = sub.add_parser("agent-backed-tool", help="Run an advisory agent-backed tool.")
    agent_tool.add_argument("spec_path", type=Path)
    agent_tool.add_argument("--tool-name", required=True)
    agent_tool.add_argument("--model-class")

    disposition = sub.add_parser("review-result-template", help="Emit review result disposition template.")
    disposition.add_argument("--review-type", default="design_requirements_trace")

    validate_result = sub.add_parser("validate-review-result", help="Validate a review result disposition file.")
    validate_result.add_argument("path", type=Path)

    prompts = sub.add_parser("prompts", help="List and validate prompt definitions.")
    prompts.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())

    archive = sub.add_parser("archive-index", help="Validate spec archive index and closure-log consistency.")
    archive.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())

    resolve = sub.add_parser("resolve-spec", help="Resolve an active, archived, missing, or ambiguous spec reference.")
    resolve.add_argument("reference")
    resolve.add_argument("--repo-root", type=Path, default=Path.cwd())
    resolve.add_argument("--docs-root")

    audit = sub.add_parser("mcp-audit", help="Summarize spec lifecycle MCP mentions, explicit errors, and interaction comments in Codex session logs.")
    audit.add_argument("sessions_root", type=Path)
    audit.add_argument("--repo-root", type=Path, default=Path.cwd())
    audit.add_argument("--since")
    audit.add_argument("--limit", type=int, default=200)
    audit.add_argument("--include-sessions", action="store_true", help="Include per-session matched items instead of compact aggregates only.")

    sync = sub.add_parser("sync-guard", help="Report source, package, install, MCP reload, and commit sync state.")
    sync.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())
    sync.add_argument("--codex-home", type=Path)
    sync.add_argument("--commits", type=int, default=5)

    package = sub.add_parser("package-contract", help="Validate the Spec Lifecycle Manager package distribution contract.")
    package.add_argument("repo_root", type=Path, nargs="?", default=Path.cwd())

    hook = sub.add_parser("hook", help="Run a spec lifecycle hook.")
    hook.add_argument(
        "hook_name",
        choices=[
            "spec-file-changed",
            "task-checkbox-changed",
            "template-changed",
            "implementation-task-complete",
            "verification-updated",
            "spec-resumed",
            "spec-close-check",
            "set-task-state",
            "agent-slice-start",
            "agent-response-check",
            "review-packet-dispatch",
            "review-result-recorded",
        ],
    )
    hook.add_argument("--repo-root", type=Path, default=Path.cwd())
    hook.add_argument("--changed-files", nargs="*", default=[])
    hook.add_argument("--spec-path", type=Path)
    hook.add_argument("--task-id")
    hook.add_argument("--result-path", type=Path)
    hook.add_argument("--severity-profile", choices=["advisory", "blocking"], default="advisory")
    hook.add_argument("--advisory", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.command == "lifecycle-capabilities":
        args.repo_root, root_source = capabilities_root(args.repo_root)
        payload = lifecycle_capabilities(args.repo_root)
        payload["lifecycle_metadata"] = assemble_lifecycle_metadata(
            args.repo_root,
            invocation_surface="cli",
            root_source=root_source,
            runtime_start_path=Path(__file__),
        )
    elif args.command == "scan":
        payload = scan_specs(args.repo_root, args.docs_root, include_archived_lint=args.include_archived_lint)
    elif args.command == "summary":
        payload = spec_summary(args.spec_path.resolve())
    elif args.command == "lint":
        if args.path.is_dir():
            payload = lint_spec_package(args.path.resolve(), mode=args.mode)
        else:
            diagnostics = lint_doc(args.path.resolve(), args.artifact_type)
            payload = {"path": str(args.path.resolve()), "diagnostics": diagnostics, "summary": diagnostic_summary(diagnostics)}
    elif args.command == "next-task":
        payload = next_task(args.spec_path.resolve())
    elif args.command == "list-tasks":
        payload = task_list(args.spec_path.resolve(), include_subtasks=not args.no_subtasks, status=args.status)
    elif args.command == "task-details":
        payload = task_details(args.spec_path.resolve(), args.task_id)
    elif args.command == "task-state-audit":
        payload = task_state_audit(args.spec_path.resolve(), args.task_id)
    elif args.command == "set-task-state":
        payload = set_task_state(
            args.spec_path.resolve(),
            args.task_id,
            args.state,
            args.evidence,
            status_note=args.status_note,
            dry_run=not args.write,
            write_intent=args.write_intent,
            evidence_mode=args.evidence_mode,
            destination=args.destination,
            decision_owner=args.decision_owner,
        )
    elif args.command == "active-spec-preflight":
        payload = active_spec_preflight(args.repo_root, args.spec_path, args.task_id, args.docs_root)
    elif args.command == "lifecycle-guide":
        payload = lifecycle_guide(args.repo_root, args.docs_root, args.mode)
    elif args.command == "bootstrap-plan":
        payload = bootstrap_plan(args.repo_root, args.docs_root, args.project_summary, args.create_spec, args.spec_slug)
    elif args.command == "stage-readiness":
        payload = stage_readiness(args.spec_path.resolve())
    elif args.command == "validation-plan":
        payload = validation_plan(args.repo_root, args.changed_files, args.spec_path, args.task_id, args.risk_level)
    elif args.command == "evidence-quality":
        payload = evidence_quality_check(args.spec_path.resolve())
    elif args.command == "agent-readiness-packet":
        payload = agent_readiness_packet(args.spec_path.resolve(), args.task_id)
    elif args.command == "no-active-spec-context":
        payload = no_active_spec_context(args.repo_root)
    elif args.command == "closure-check":
        payload = closure_check(args.spec_path.resolve())
    elif args.command == "closure-plan":
        payload = closure_plan(
            args.spec_path.resolve(),
            repo_root=args.repo_root.resolve() if args.repo_root else None,
            final_spec_commit=args.final_spec_commit,
            closure_action=args.closure_action,
            include_reference_scan=not args.no_reference_scan,
        )
    elif args.command == "closure-apply":
        plan = json.loads(args.plan_file.read_text(encoding="utf-8"))
        payload = closure_apply(
            args.spec_path.resolve(),
            repo_root=args.repo_root.resolve() if args.repo_root else None,
            plan=plan,
            action_id=args.action_id,
            dry_run=not args.write,
            write_intent=args.write_intent,
        )
    elif args.command == "closure-resolve":
        payload = closure_resolve(
            args.repo_root.resolve(),
            spec_id=args.spec_id,
            cleanup_commit=args.cleanup_commit,
            dry_run=not args.write,
            write_intent=args.write_intent,
        )
    elif args.command == "closure-risk-review":
        payload = closure_risk_review(args.spec_path.resolve())
    elif args.command == "reconcile":
        payload = reconcile_spec(args.spec_path.resolve())
    elif args.command == "promotion-plan":
        payload = promotion_plan(args.spec_path.resolve())
    elif args.command == "review-packet":
        payload = generate_review_packet(args.spec_path.resolve(), args.review_type, args.model_class)
    elif args.command == "agent-backed-tool":
        payload = agent_backed_tool(args.spec_path.resolve(), args.tool_name, args.model_class)
    elif args.command == "review-result-template":
        payload = review_result_disposition_template(args.review_type)
    elif args.command == "validate-review-result":
        payload = validate_review_result(args.path.resolve())
    elif args.command == "prompts":
        payload = load_prompt_definitions(args.repo_root)
    elif args.command == "archive-index":
        payload = archive_index(args.repo_root)
    elif args.command == "resolve-spec":
        payload = resolve_spec_reference(args.repo_root, args.reference, args.docs_root)
    elif args.command == "mcp-audit":
        payload = mcp_audit(args.repo_root, args.sessions_root, args.since, args.limit, args.include_sessions)
    elif args.command == "sync-guard":
        payload = sync_guard(args.repo_root, args.codex_home, args.commits)
    elif args.command == "package-contract":
        payload = package_contract(args.repo_root)
    elif args.command == "hook":
        payload = run_hook(
            args.repo_root,
            args.hook_name,
            changed_files=args.changed_files,
            spec_path=args.spec_path,
            task_id=args.task_id,
            result_path=args.result_path,
            severity_profile=args.severity_profile,
            advisory=args.advisory,
        )
    else:
        raise ValueError(args.command)
    payload = relativize_payload_paths(payload, output_repo_root_for_args(args))
    print_payload(payload)
    if args.command == "hook":
        return 1 if payload["blocked"] else 0
    if isinstance(payload.get("summary"), dict) and payload["summary"].get("error", 0):
        return 1
    if args.command == "closure-check" and not payload["ready"]:
        return 1
    return 0
