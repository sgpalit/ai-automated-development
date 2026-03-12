# Developer Implementation Prompt

## Date
2026-03-12

## Selected Task
- Code: `TASK-023`
- File: `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md`
- Goal: developer agent schould commit and push after he finishes his task, then the reviewer should check his commit

## Implementation Objective
Translate the latest analyst findings into concrete implementation work aligned with this goal: developer agent schould commit and push after he finishes his task, then the reviewer should check his commit

## Exact Files Likely To Change
- `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md`
- `AGENTS.md`
- `docs/agents.md`
- `prompts/agents/developer.md`
- `docs/human-approval-checklists.md`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Implementing the task itself
- Out of scope: Introducing unrelated refactors

## Exact Acceptance Criteria
- Backlog task is specific and executable
- Acceptance criteria are testable
- Dependencies are explicitly listed

## Step-by-Step Implementation Plan
1. Review `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `AGENTS.md`, `docs/agents.md`, `prompts/agents/developer.md`, `docs/human-approval-checklists.md`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md` to `done` only after the acceptance criteria are met.
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
Goal: developer agent schould commit and push after he finishes his task, then the reviewer should check his commit
Selected task file: `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md`

Files likely to change:
- `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md`
- `AGENTS.md`
- `docs/agents.md`
- `prompts/agents/developer.md`
- `docs/human-approval-checklists.md`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Implementing the task itself
- Out of scope: Introducing unrelated refactors

Acceptance criteria:
- Backlog task is specific and executable
- Acceptance criteria are testable
- Dependencies are explicitly listed

Implementation plan:
1. Review `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `AGENTS.md`, `docs/agents.md`, `prompts/agents/developer.md`, `docs/human-approval-checklists.md`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-023-developer-agent-schould-commit-and-push.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-023 Planner Follow-up: developer agent schould commit and push after he finishes his task, then the reviewer should check his commit

## Status
todo

## Priority
high

## Objective
Translate the latest analyst findings into concrete implementation work aligned with this goal: developer agent schould commit and push after he finishes his task, then the reviewer should check his commit

## Scope
- Use `agents/analysis/repo-analysis.md` as the planning input
- Define one focused implementation slice that can be completed in a single cycle
- Keep task boundaries explicit and implementation-ready

## Out of Scope
- Implementing the task itself
- Introducing unrelated refactors

## Acceptance Criteria
- Backlog task is specific and executable
- Acceptance criteria are testable
- Dependencies are explicitly listed

## Dependencies
- None

## Notes
Generated by `scripts/run_planner.py` (planner phase).
Slug: `developer-agent-schould-commit-and-push`

```

````
