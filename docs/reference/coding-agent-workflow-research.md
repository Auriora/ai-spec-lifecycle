---
title: Coding agent workflow research
doc_type: reference
status: draft
owner: platform
last_reviewed: 2026-06-02
---

# Coding Agent Workflow Research

## Purpose

This note captures current evidence and recommendations for working effectively
with coding agents. It is written from the position that established software
delivery approaches such as waterfall, agile, DevOps, and modern QA share the
same durable core: clarify intent, design enough, implement in controlled
slices, verify evidence, review risk, document durable behavior, and learn from
feedback.

Coding agents do not remove that core. They change the economics and cadence.
They make exploration, drafting, implementation, test generation, and review
faster, but they also increase the risk of plausible incomplete work. The best
workflow is therefore not "agent autonomy" or "manual process as before"; it is
a tailored operator-agent system where the developer operator supplies judgment,
taste, context, constraints, and innovation, while agents supply speed,
parallel exploration, broad recall, and tireless verification.

## Evidence Summary

### What appears to work

- Repository-specific instructions materially improve agent output. GitHub
  recommends custom repository instructions that tell the agent how to
  understand, build, test, and validate the project; it also states that agents
  produce better pull requests when they can build, test, and validate changes
  in their own environment:
  <https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results>
- Explore first, plan next, then code is a recurring best practice. Anthropic's
  Claude Code guidance explicitly recommends giving the agent a way to verify
  its work, then exploring, planning, and implementing:
  <https://code.claude.com/docs/en/best-practices>
- Evidence beats assertions. Anthropic recommends having the agent show command
  output, test results, screenshots, or equivalent proof instead of merely
  claiming success:
  <https://code.claude.com/docs/en/best-practices>
- Subagents and parallel sessions are useful when work can be split cleanly:
  one agent can investigate or review while another implements, provided edit
  scope and ownership are controlled:
  <https://code.claude.com/docs/en/best-practices>
- Supervised agents are the pragmatic industry direction. Thoughtworks describes
  coding agents as promising but emphasizes supervised usage, human steering,
  and vigilance in code review:
  <https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/04/tr_technology_radar_vol_32_en.pdf>
- Human-in-the-loop agent workflows are more realistic than fully automated
  issue-to-code pipelines. HULA research reports perceived time and effort
  reduction, especially for coding plans and straightforward tasks, while still
  noting code quality concerns:
  <https://arxiv.org/abs/2411.12924>
- Agent-authored pull requests can be accepted in real projects when scoped and
  reviewed. One empirical study of 567 Claude Code PRs across 157 repositories
  found high merge rates, with agent use concentrated in refactoring,
  documentation, and testing:
  <https://arxiv.org/abs/2509.14745>

### What cautions against naive agent use

- A METR randomized controlled trial with experienced open-source developers
  found that early-2025 AI tooling made tasks take longer on average in that
  setting, despite expectations of speedup:
  <https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf>
- Stack Overflow's 2025 developer survey shows the trust gap is real. Most
  professional developers were not "vibe coding", and AI trust remained a
  central workflow concern:
  <https://survey.stackoverflow.co/2025/ai>
- DORA 2025 reports broad AI adoption and perceived productivity/code-quality
  gains, but this is survey evidence and should be paired with local outcome
  measurement rather than treated as proof that every team or task gets faster:
  <https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/>

## Interpretation

The most effective coding-agent workflows appear to be:

- supervised, not hands-off;
- evidence-driven, not assertion-driven;
- context-rich, not prompt-only;
- task-sliced, not broad unbounded autonomy;
- documentation-aware, not code-only;
- review-heavy where risk is high;
- lighter where risk is low and feedback is immediate.

The developer operator becomes more important, not less. Their role shifts
toward:

- defining intent and non-goals;
- choosing the right workflow weight;
- deciding where quality gates belong;
- spotting conceptual drift and architectural shortcuts;
- delegating bounded exploration and verification;
- preserving durable knowledge;
- making the final judgment about acceptance.

## Recommended Operating Model

### 1. Keep the classic QA spine

Use the same underlying quality spine that successful waterfall, agile, lean,
and DevOps workflows share:

```text
intent -> requirements -> design -> implementation -> verification -> review -> durable docs -> release/close -> feedback
```

Do not make every change heavy. Instead, scale the ceremony to risk.

Low-risk examples:

- typo fixes;
- isolated doc updates;
- small UI copy or style changes;
- simple generated tests around existing behavior.

Use a lightweight flow:

```text
intent -> patch -> local check -> evidence -> done
```

Higher-risk examples:

- behavior changes;
- integrations;
- migrations;
- security-sensitive code;
- data model or API changes;
- user-visible workflows;
- changes crossing module boundaries.

Use a fuller flow:

```text
durable baseline -> spec delta -> design -> tasks -> implementation slice -> verification -> review -> durable promotion -> closure
```

### 2. Treat documentation as agent memory and QA surface

Agents perform better when the repository tells them:

- what the system is;
- how it is built and tested;
- what conventions matter;
- what quality gates are non-negotiable;
- where durable source-of-truth docs live;
- how to close temporary implementation specs.

Recommended repository surfaces:

- `AGENTS.md` or equivalent: agent instructions, build/test commands, coding
  standards, boundaries, escalation rules.
- Durable docs: current architecture, requirements, runbooks, contracts,
  reference docs, ADRs.
- Temporary specs: active delivery scaffolding, not permanent truth.
- Validation docs: commands, expected evidence, residual risk.

The useful distinction is:

- Durable docs describe the current system and should live with the code.
- Specs describe how a change is being delivered and should have a finite
  lifetime.

### 3. Use agents for the work they are currently best at

Good targets:

- repo exploration and summarization;
- migration inventories;
- test generation from clear requirements;
- documentation updates;
- refactoring with narrow scope;
- code review passes;
- finding inconsistent docs;
- drafting plans and task lists;
- producing candidate implementations for bounded slices.

Riskier targets:

- underspecified product behavior;
- architectural decisions without operator review;
- security-sensitive changes;
- deep concurrency or distributed-systems behavior;
- production data mutation;
- broad refactors with weak tests;
- "just fix it" prompts with no acceptance criteria.

### 4. Make agents prove work before claiming completion

Every meaningful agent change should produce evidence:

- tests run and result;
- build/lint/typecheck result;
- manual validation notes;
- screenshots or traces for UI/visual work;
- before/after behavior;
- changed files;
- residual risks;
- commands that could not run and why.

The operator should review evidence first, then code. Evidence narrows the
review surface and reveals whether the agent understood the task.

### 5. Use subagents for independent work, not vague parallelism

Subagents work best for:

- read-only exploration;
- independent review perspectives;
- test-target ranking;
- fixture validation;
- comparing docs against implementation;
- scanning for risks in a bounded area.

Avoid using subagents when:

- tasks overlap heavily;
- write scopes conflict;
- the main path is blocked waiting for their result;
- the prompt cannot be made concrete.

Good pattern:

```text
main agent: owns implementation slice
explore agent: maps existing behavior and conventions
review agent: inspects final diff for risks
verification agent: runs or designs focused validation
operator: makes decisions and accepts/rejects
```

### 6. Prefer explicit gates over implicit trust

Decision gates that matter for coding agents:

- Is this a low-risk direct patch or does it need a spec?
- Is existing durable documentation authoritative or stale?
- Is the task old-format and does it need migration?
- Is implementation blocked by unresolved decisions?
- Are tests sufficient to prove behavior?
- Does generated code introduce dependencies, hidden behavior, or excessive
  abstraction?
- Is durable documentation updated before closure?

### 7. Measure local outcomes

The external evidence is mixed enough that local measurement matters.

Track:

- cycle time per task type;
- rework rate after agent changes;
- test failures introduced;
- review findings per PR;
- docs updated before closure;
- percentage of tasks with evidence;
- operator time spent steering vs reviewing;
- defect escape rate;
- subjective operator confidence.

The goal is not to prove "AI is faster"; it is to learn where agents are net
positive in your projects.

## Recommended Workflow Shape

### Intake

Classify the request:

- direct patch;
- research;
- bug fix;
- feature;
- migration;
- external repo contribution;
- production-risk change.

Choose the lightest process that still protects quality.

### Baseline

Read:

- repo instructions;
- durable docs;
- current tests;
- relevant code;
- existing specs or issues.

Record whether durable docs are current, stale, missing, or conflicting.

### Spec or Task Plan

For non-trivial work, create or update a temporary spec:

- requirements;
- design;
- Kiro-style tasks/subtasks;
- change impact if existing behavior changes;
- verification plan;
- open decisions.

### Implementation

Work in coherent slices. For each slice:

- state selected tasks;
- state files likely affected;
- implement only that slice;
- run focused validation;
- record evidence;
- update task status only when defensible.

### Review

Use separate review modes:

- correctness review;
- architecture review;
- test/QA review;
- docs/durable-source review;
- security/operations review where relevant.

### Promotion and Closure

Before closing:

- promote durable behavior into durable docs;
- move decisions into ADRs/history/reference docs;
- move operational steps into runbooks/checklists;
- move deferred work into backlog or follow-up specs;
- remove the spec from active indexes;
- archive or remove the spec according to lifecycle rules.

## Proposed Principles For Our Environment

1. **Human operator owns intent and acceptance.** Agents can propose, implement,
   and verify, but the operator decides what is right.
2. **Specs are temporary; durable docs are truth.** Specs guide delivery, then
   close.
3. **Evidence is mandatory for completion.** No task is done because an agent
   says it is done.
4. **Process scales with risk.** Small changes stay light; risky changes get
   explicit gates.
5. **Agents work best with context.** Invest in repo instructions, durable docs,
   validation commands, and conventions.
6. **Parallelism needs boundaries.** Subagents need clear read/write scope and
   independent outputs.
7. **Review remains essential.** Agentic speed increases the need for targeted
   review, not the opposite.
8. **Measure outcomes locally.** External studies are useful, but project
   results should guide adoption.

## Open Questions

- What is the minimum spec package for a medium-risk change?
- Which project types should adopt the durable-doc templates?
- How should we measure operator time vs agent time?
- Which review roles should be mandatory for security, data, and production
  mutation changes?
- When should a closed spec be archived rather than removed?
- What fixture trials best represent the projects this environment will support?

## Sources

- GitHub Docs, "Get the best results with Copilot coding agent":
  <https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results>
- Anthropic, "Best practices for Claude Code":
  <https://code.claude.com/docs/en/best-practices>
- METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source
  Developer Productivity":
  <https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf>
- Google DORA 2025 overview:
  <https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/>
- Stack Overflow 2025 Developer Survey, AI section:
  <https://survey.stackoverflow.co/2025/ai>
- Thoughtworks Technology Radar, Volume 32:
  <https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/04/tr_technology_radar_vol_32_en.pdf>
- HULA paper:
  <https://arxiv.org/abs/2411.12924>
- Empirical study of Claude Code PRs:
  <https://arxiv.org/abs/2509.14745>
