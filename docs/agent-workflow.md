# Agent Workflow

## Purpose
This document defines how AI agents should operate in this repository so task execution stays consistent, scoped, and reliable.

## Next Task Selection Rule
Select the next task from `agents/<target-name>/backlog/tasks/` using this order:

1. Keep only tasks with `Status: todo`.
2. Prefer highest priority (`high` over `medium` over `low`).
3. Keep only tasks whose dependencies are all marked `done`.
4. If multiple tasks remain, select the lowest task number.

Example tie-break:

- `TASK-003` and `TASK-004` are both `todo`, `high`, and unblocked.
- Select `TASK-003` because it has the lower number.

## Empty Backlog Rule
If a promptless local run finds no eligible `todo` or `in-progress` task, do not crash and do not invent an unrelated free-text goal.

Instead:

1. Read `docs/mvp.md`.
2. Read `agents/<target-name>/analysis/repo-analysis.md`.
3. Generate exactly one new implementation-ready backlog task in `agents/<target-name>/backlog/tasks/` using the next sequential `TASK-###` number.
4. Include at least:
   - `Status`
   - `Priority`
   - `Objective`
   - `Scope`
   - `Out of Scope`
   - `Acceptance Criteria`
   - `Dependencies`
5. Keep the task small and grounded in the next missing MVP slice described by the MVP and repository analysis.
6. Reference real repository paths and runnable commands that match the current runner/layout.
7. If the task introduces a new artifact location, explain whether it replaces or complements any existing artifact path.
8. If the task depends on an existing helper, config loader, dataclass, or CLI contract, use the exact names from the current source rather than inventing renamed variants.
9. Stop and surface the generated task for human review before implementation continues.

For automation-facing planner integrations:

- if planner cannot derive a grounded next task, it should stop with an explicit machine-readable reason such as `no-grounded-next-task`
- if planner generates a new task but does not continue into implementation, it should stop with an explicit review/policy reason rather than a generic silent stop

If either required input is missing, unreadable, or insufficient to derive a grounded next task, stop cleanly with an operator-facing explanation.

## Task State Updates
Before implementation:

1. Open the selected task file.
2. Set `## Status` to `in-progress`.

After implementation and validation:

1. Set `## Status` to `done`.
2. Leave the rest of the task content unchanged, except for small clarifications when needed.

## Implementation Rules
- Keep changes small and focused on the current task.
- Avoid unrelated refactoring.
- Prefer simple, maintainable solutions.
- Keep the repository in a working state.

## Reporting Format
When a task is complete, report:

- Summary of changes
- List of modified files
- Assumptions made
- Possible follow-up tasks
- Verification commands and outcomes
- Pushed commit hash when developer execution commits work

## Follow-up Task Creation
If implementation reveals additional work, create follow-up tasks in `agents/<target-name>/backlog/tasks/` rather than expanding the scope of the current task.

## Human Review Loop
Keep work review-friendly for humans by limiting scope to the current task, preserving repository usability, and providing clear completion reporting.

Tasks generated because the backlog is empty are proposals only until a human reviews them.

## MVP Auto-Continue
When the runner is explicitly started in MVP auto-continue mode, it may continue through existing eligible tasks without waiting for a human between every cycle.

Constraints:

- auto-continue is valid only while the target repository state is `MVP`
- stop reasons must be written as visible target-scoped artifacts
- newly generated backlog tasks may still pause the loop for human review
- reviewer and tester outputs must remain evidence-based and target-scoped
- planner stop conditions should be explicit enough for the orchestrator to distinguish backlog exhaustion from human-review pauses

## Branch Strategy (MVP Phase)
During MVP bootstrap, agents may commit and push directly to `main`.

Constraints:

- Only implement the current backlog task.
- Keep changes small and focused.
- Do not perform unrelated refactoring.
- Ensure the repository remains usable after changes.

After MVP, the workflow will move to feature branches, pull requests, and review.
