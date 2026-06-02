# Skill Validation Fixtures

These fixture repositories validate the repo-local `spec-lifecycle-manager`
skill. They are intentionally small and are not runnable application projects.

Each fixture includes enough documentation structure for a prompt trial agent to
apply the skill and report expected versus observed behavior.

## Fixtures

| Fixture | Scenario |
|---------|----------|
| `fresh-feature-own-repo/` | Create a new feature spec in an owned repo. |
| `bug-fix-durable-source/` | Create a bug-fix spec that references durable source-of-truth docs and uses `change-impact.md`. |
| `old-format-resume/` | Resume an old-format `spec.md`/`plan.md` package and use a migration decision gate. |
| `external-partition/` | Work in an external project while keeping lifecycle docs under `docs/agent-lifecycle/`. |
| `completed-spec-close/` | Close a completed spec with promotion targets and closure blockers. |
| `governance-conflict/` | Detect a governance conflict and stop for a decision. |
