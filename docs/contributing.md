# Contributing Guide

This project uses a backlog-driven workflow so humans and agents follow the same process.

## 1) Choose a Backlog Task

1. Open `agents/<target-name>/backlog/tasks/`.
2. Keep only tasks with `Status: todo`.
3. Pick the highest priority (`high` > `medium` > `low`).
4. Keep only tasks whose dependencies are `done`.
5. If there is a tie, pick the lowest task number.
6. Before coding, set the selected task status to `in-progress`.

Reference: `docs/agent-workflow.md`

## 2) Implement with MVP Expectations

During MVP bootstrap, contributors may commit directly to `main`.

Rules:
- Keep changes small and focused on the selected task.
- Do not introduce unrelated refactoring.
- Keep the repository in a working state.

## 3) Commit Expectations

- Use clear commit messages that reference the task ID.
- Example: `TASK-004 contribution guide`

## 4) Pull Request Expectations (Post-MVP)

After MVP, work will move to a feature-branch + PR process:
- Create a feature branch for the selected task.
- Open a pull request with task context and validation notes.
- Complete review before merge.

## 5) Completion Report Format

When finishing a task, include:
- summary of changes
- list of modified files
- assumptions made
- possible follow-up tasks
- verification commands and outcomes
- pushed commit hash when applicable

## 6) Close the Task

After implementation and validation:
1. Update the task status to `done`.
2. Keep the rest of the task content unchanged except minor clarifications when needed.
