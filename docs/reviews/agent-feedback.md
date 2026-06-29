give feedback on your experince of the use of the spec skill and tools - benefits, drawbacks, improvements


• Benefits

  The spec skill kept the work disciplined. T012-T015 had clear acceptance criteria, dependencies, traceability, and validation expectations, so phase 4 did not drift into unrelated UI polish or later jobs/email work.

  The MCP tools were useful:

  - active_spec_preflight clearly identified the next task and showed T016 after phase 4.
  - task_context pulled requirement/design/verification context without rereading the whole package.
  - set_task_state made task evidence updates consistent and reduced manual formatting errors.
  - lint_spec_package gave a fast final health check before commit.

  The evidence model helped. Recording concrete commands, review findings, and validation outcomes made the final status defensible instead of just “done”.

  Drawbacks

  The workflow is verbose. For implementation-heavy phases, updating task state, verification tables, durable docs, and final evidence adds noticeable overhead.

  The spec package can lag behind code reality unless actively maintained. I had to update tasks, verification, product docs, architecture docs, and runbook docs separately.

  The tooling is mostly advisory. It can say the spec is lint-clean, but it cannot tell whether the implementation is actually correct. Runtime validation and human/code review still carry the real proof.

  Task granularity was broad. Phase 4 bundled admin CRUD, invitations, audit logging, settings, and app events. That is coherent as a phase, but each task still touched many files and security-sensitive behavior.

  Improvements

  - Add a “phase complete” helper that updates task evidence, verification task table, evidence log, and readiness status from one structured input.
  - Add clearer prompts for durable-doc promotion: which docs need current-state updates for each task.
  - Add a built-in “review findings addressed” evidence section so security/senior review outcomes are captured without manually fitting them into generic evidence rows.
  - Support task groups directly, e.g. set_task_state --tasks T012,T013,T014,T015, when a phase is implemented and validated as one slice.
  - Include expected validation commands from the actual repo docs/README, not just generic lifecycle script suggestions.
  - Add a warning when a task touches security-sensitive areas like auth, invitations, roles, or audit logging and require explicit review evidence before completion.

  Overall, the spec skill was valuable for sequencing, traceability, and evidence hygiene. Its main cost is documentation overhead, and its biggest opportunity is better batch support for phase-level implementation slices.

