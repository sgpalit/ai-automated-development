# Developer Implementation Prompt

## Date
2026-03-12

## Selected Task
- Code: `TASK-021`
- File: `backlog/tasks/TASK-021-improve-onboarding-documentation.md`
- Goal: Improve onboarding documentation

## Implementation Objective
Translate the latest analyst findings into concrete implementation work aligned with this goal: Improve onboarding documentation

## Exact Files Likely To Change
- `backlog/tasks/TASK-021-improve-onboarding-documentation.md`
- `docs/target-repo-onboarding.md`
- `docs/target-repo-context.md`
- `scripts/run_analyst.py`
- `scripts/run_cycle.py`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `backlog/tasks/TASK-021-improve-onboarding-documentation.md`.
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
1. Review `backlog/tasks/TASK-021-improve-onboarding-documentation.md` and confirm the task is still in scope.
2. Update `backlog/tasks/TASK-021-improve-onboarding-documentation.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `docs/target-repo-onboarding.md`, `docs/target-repo-context.md`, `scripts/run_analyst.py`, `scripts/run_cycle.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `backlog/tasks/TASK-021-improve-onboarding-documentation.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

## Copy-Paste Prompt For The Coding Agent
````text
# Developer Agent Prompt

You are the **Developer Agent**.

## Mission

Implement exactly one approved backlog task in a focused change set.

## Required Inputs

- Selected task file in `backlog/tasks/`
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
6. Set task status to `done` after acceptance criteria are met.

If blocked, set status to `blocked` and explain why.

## Required Output Format

Use the handoff contract sections:

- Context
- Decisions
- Artifacts
- Open Questions / Risks
- Recommended Next Step

Include changed files, assumptions, and verification commands in `Artifacts`.

## Done Criteria

- Acceptance criteria satisfied
- Status updated (`in-progress` → `done`)
- Output ready for Reviewer

Repository path: `/home/sp/workspace/github/ai-automated-development`
Goal: Improve onboarding documentation
Selected task file: `backlog/tasks/TASK-021-improve-onboarding-documentation.md`

Files likely to change:
- `backlog/tasks/TASK-021-improve-onboarding-documentation.md`
- `docs/target-repo-onboarding.md`
- `docs/target-repo-context.md`
- `scripts/run_analyst.py`
- `scripts/run_cycle.py`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `backlog/tasks/TASK-021-improve-onboarding-documentation.md`.
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
1. Review `backlog/tasks/TASK-021-improve-onboarding-documentation.md` and confirm the task is still in scope.
2. Update `backlog/tasks/TASK-021-improve-onboarding-documentation.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `docs/target-repo-onboarding.md`, `docs/target-repo-context.md`, `scripts/run_analyst.py`, `scripts/run_cycle.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `backlog/tasks/TASK-021-improve-onboarding-documentation.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-021 Planner Follow-up: Improve onboarding documentation

## Status
todo

## Priority
high

## Objective
Translate the latest analyst findings into concrete implementation work aligned with this goal: Improve onboarding documentation

## Scope
- Use `analysis/repo-analysis.md` as the planning input
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
Slug: `improve-onboarding-documentation`

```

````
