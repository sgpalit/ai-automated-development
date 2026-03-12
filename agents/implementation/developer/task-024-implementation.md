# Developer Implementation Prompt

## Date
2026-03-12

## Selected Task
- Code: `TASK-024`
- File: `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md`
- Goal: Make the local runner and planner continue the MVP loop when all existing backlog tasks are completed by generating one new implementation-ready backlog task from `docs/mvp.md` and the latest repository analysis instead of crashing.

## Implementation Objective
Make the local runner and planner continue the MVP loop when all existing backlog tasks are completed by generating one new implementation-ready backlog task from `docs/mvp.md` and the latest repository analysis instead of crashing.

## Exact Files Likely To Change
- `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md`
- `docs/workflow.md`
- `docs/agent-workflow.md`
- `prompts/codex/bootstrap-agent-workflow.md`
- `AGENTS.md`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Generating multiple new tasks in one pass
- Out of scope: Reopening completed tasks automatically
- Out of scope: Broad changes to the overall branch/review strategy
- Out of scope: Unrelated refactors to analyst, developer, reviewer, or tester behavior

## Exact Acceptance Criteria
- Running `./run-agents.sh --dry-run` with no eligible backlog task does not raise `FileNotFoundError`
- The planner creates a new `TASK-024+` style backlog file in `agents/backlog/tasks/` when the backlog is exhausted
- The generated task includes `Status`, `Priority`, `Objective`, `Scope`, `Out of Scope`, `Acceptance Criteria`, and `Dependencies`
- The generated task is clearly grounded in `docs/mvp.md` and the latest analysis artifact rather than a generic placeholder
- Runner output explains which new task was created and that it requires human review before further implementation
- If no task is generated, runner output stops cleanly and explains why no next MVP task could be produced

## Step-by-Step Implementation Plan
1. Review `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `docs/workflow.md`, `docs/agent-workflow.md`, `prompts/codex/bootstrap-agent-workflow.md`, `AGENTS.md`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

## Copy-Paste Prompt For The Coding Agent
````text
# Developer Agent Prompt

You are the **Developer Agent**.

## Mission

Implement exactly one approved backlog task in a focused change set.

## Required Inputs

- Selected task file in `agents/backlog/tasks/`
- Repository context and relevant docs
- `AGENTS.md`
- `docs/agent-workflow.md`
- `docs/agent-handoff-contract.md`

## Execution Rules

1. Confirm the selected task is approved and currently `todo`.
2. Set task status to `in-progress` before implementation.
3. Implement only in-scope changes required by the task.
4. Keep unrelated refactors out of scope.
5. Run relevant checks.
6. After acceptance criteria are met, create a small focused commit for the task changes and push that commit to the active branch.
7. Include the pushed commit hash in the developer handoff so the reviewer can review the exact committed state.
8. Set task status to `done` after acceptance criteria are met and the handoff is ready for review.

If blocked, set status to `blocked` and explain why.

## Required Output Format

Use the handoff contract sections:

- Context
- Decisions
- Artifacts
- Open Questions / Risks
- Recommended Next Step

Include changed files, assumptions, verification commands, and the pushed commit hash in `Artifacts`.

## Done Criteria

- Acceptance criteria satisfied
- Relevant verification completed
- Task changes committed and pushed
- Status updated (`in-progress` → `done`)
- Output ready for Reviewer

Repository path: `/home/sp/workspace/github/ai-automated-development`
Goal: Make the local runner and planner continue the MVP loop when all existing backlog tasks are completed by generating one new implementation-ready backlog task from `docs/mvp.md` and the latest repository analysis instead of crashing.
Selected task file: `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md`

Files likely to change:
- `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md`
- `docs/workflow.md`
- `docs/agent-workflow.md`
- `prompts/codex/bootstrap-agent-workflow.md`
- `AGENTS.md`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Generating multiple new tasks in one pass
- Out of scope: Reopening completed tasks automatically
- Out of scope: Broad changes to the overall branch/review strategy
- Out of scope: Unrelated refactors to analyst, developer, reviewer, or tester behavior

Acceptance criteria:
- Running `./run-agents.sh --dry-run` with no eligible backlog task does not raise `FileNotFoundError`
- The planner creates a new `TASK-024+` style backlog file in `agents/backlog/tasks/` when the backlog is exhausted
- The generated task includes `Status`, `Priority`, `Objective`, `Scope`, `Out of Scope`, `Acceptance Criteria`, and `Dependencies`
- The generated task is clearly grounded in `docs/mvp.md` and the latest analysis artifact rather than a generic placeholder
- Runner output explains which new task was created and that it requires human review before further implementation
- If no task is generated, runner output stops cleanly and explains why no next MVP task could be produced

Implementation plan:
1. Review `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `docs/workflow.md`, `docs/agent-workflow.md`, `prompts/codex/bootstrap-agent-workflow.md`, `AGENTS.md`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-024-generate-next-mvp-task-when-backlog-is-empty.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-024 Generate the next MVP task when the backlog is empty

## Status
todo

## Priority
high

## Objective
Make the local runner and planner continue the MVP loop when all existing backlog tasks are completed by generating one new implementation-ready backlog task from `docs/mvp.md` and the latest repository analysis instead of crashing.

## Scope
- Update the local planner/backlog selection flow so promptless runs detect when no eligible `todo` or `in-progress` task exists
- Generate exactly one new task file in `agents/backlog/tasks/` using `docs/mvp.md` and `agents/analysis/repo-analysis.md` as inputs
- Keep the generated task small, implementation-ready, and aligned with the next missing MVP slice
- If no task can be generated from the available MVP and analysis inputs, stop the runner cleanly with a clear operator-facing message
- Preserve the human-supervised workflow by stopping at task generation or clearly surfacing the new task for review before implementation continues

## Out of Scope
- Generating multiple new tasks in one pass
- Reopening completed tasks automatically
- Broad changes to the overall branch/review strategy
- Unrelated refactors to analyst, developer, reviewer, or tester behavior

## Implementation Notes
- Prefer reusing the existing planner/task template logic rather than introducing a second task format
- The empty-backlog path should fail gracefully if required inputs such as `docs/mvp.md` or `agents/analysis/repo-analysis.md` are missing
- Human control still matters: the new task should be easy to inspect and approve before autonomous implementation proceeds

## Acceptance Criteria
- Running `./run-agents.sh --dry-run` with no eligible backlog task does not raise `FileNotFoundError`
- The planner creates a new `TASK-024+` style backlog file in `agents/backlog/tasks/` when the backlog is exhausted
- The generated task includes `Status`, `Priority`, `Objective`, `Scope`, `Out of Scope`, `Acceptance Criteria`, and `Dependencies`
- The generated task is clearly grounded in `docs/mvp.md` and the latest analysis artifact rather than a generic placeholder
- Runner output explains which new task was created and that it requires human review before further implementation
- If no task is generated, runner output stops cleanly and explains why no next MVP task could be produced

## Dependencies
None

```

````
