# End-to-End Example: Multi-Agent Loop

This runbook shows one complete cycle:

Analyst → Planner → Human review or MVP auto-continue → Developer → Reviewer → Tester → Orchestrator decision

## Scenario

- Target repository: `example-project/`
- Goal: Improve onboarding documentation and backlog hygiene

## Step 1: Analyst

- Prompt file: `prompts/agents/analyst.md`
- Output artifact: `agents/<target-name>/analysis/repo-analysis.md`
- Contract sections used: Context, Decisions, Artifacts, Open Questions / Risks, Recommended Next Step

## Step 2: Planner

- Prompt file: `prompts/agents/planner.md`
- Inputs: analysis + `docs/mvp.md` + existing backlog
- Output artifacts: `agents/<target-name>/backlog/tasks/TASK-XXX-*.md`

## Step 3: Human review gate

Human approves task definitions, priorities, and dependencies before implementation in supervised mode.

In `MVP` auto-continue mode, the loop may continue automatically through existing eligible tasks, but a newly generated backlog task may still pause for human review.

## Step 4: Developer

- Prompt file: `prompts/agents/developer.md`
- Task state: set to `in-progress`
- Output artifacts: repository changes + implementation handoff summary

## Step 5: Reviewer

- Prompt file: `prompts/agents/reviewer.md`
- Output artifact: review report with `APPROVED` or `CHANGES REQUIRED`

## Step 6: Tester

- Prompt file: `prompts/agents/tester.md`
- Output artifact: validation report with `READY`, `RETRY`, or `BLOCKED`

## Step 7: Orchestrator or Human decision gate

The orchestrator or human reviews implementation + reviewer + tester artifacts.

If accepted:
- mark task `done`
- continue loop with next eligible task

## Expected Artifact Set for One Cycle

- `agents/<target-name>/analysis/repo-analysis.md` (latest analysis)
- `agents/<target-name>/backlog/tasks/TASK-XXX-*.md` (selected task)
- Developer handoff summary (contract format)
- Reviewer decision artifact under `agents/<target-name>/review/`
- Tester decision artifact under `agents/<target-name>/test/`

## Related Docs

- `docs/agent-handoff-contract.md`
- `docs/human-approval-checklists.md`
- `docs/workflow.md`
