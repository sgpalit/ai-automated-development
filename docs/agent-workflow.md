# Agent Workflow

## Purpose
This document defines how AI agents should operate in this repository so task execution stays consistent, scoped, and reliable.

## Next Task Selection Rule
Select the next task from `backlog/tasks/` using this order:

1. Keep only tasks with `Status: todo`.
2. Prefer highest priority (`high` over `medium` over `low`).
3. Keep only tasks whose dependencies are all marked `done`.
4. If multiple tasks remain, select the lowest task number.

Example tie-break:

- `TASK-003` and `TASK-004` are both `todo`, `high`, and unblocked.
- Select `TASK-003` because it has the lower number.

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

## Follow-up Task Creation
If implementation reveals additional work, create follow-up tasks in `backlog/tasks/` rather than expanding the scope of the current task.

## Human Review Loop
Keep work review-friendly for humans by limiting scope to the current task, preserving repository usability, and providing clear completion reporting.

## Branch Strategy (MVP Phase)
During MVP bootstrap, agents may commit and push directly to `main`.

Constraints:

- Only implement the current backlog task.
- Keep changes small and focused.
- Do not perform unrelated refactoring.
- Ensure the repository remains usable after changes.

After MVP, the workflow will move to feature branches, pull requests, and review.
