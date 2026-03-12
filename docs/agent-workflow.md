# Agent Workflow

This document defines the detailed, repo-native workflow for AI agents working in this repository.

## 1) Select the Next Task (Deterministic Rule)

When choosing a task from `backlog/tasks/`, use this exact order:

1. Keep only tasks with `Status: todo`.
2. From those, keep the highest priority first (`high` > `medium` > `low`).
3. From that set, keep only tasks whose dependencies are all `done`.
4. If multiple tasks still qualify, pick the lowest task number.

Example tie-break:

- `TASK-003` and `TASK-004` are both `todo`, `high`, and unblocked.
- Pick `TASK-003` because it has the lower number.

## 2) Mark Task State in Backlog

Before making code changes:

1. Open the selected task file.
2. Change `## Status` to `in-progress`.

After implementation and validation are complete:

1. Change `## Status` to `done`.
2. Keep the rest of the task content intact unless a small clarification is required.

## 3) Implementation Rules

- Keep changes small and focused on the current task.
- Do not introduce unrelated refactors.
- Prefer simple, maintainable solutions.
- Keep the repository in a working state.

## 4) Reporting Format (Required)

At task completion, report:

- Summary of changes
- List of modified files
- Assumptions made
- Possible follow-up tasks

## 5) Branch Strategy (MVP Phase)

During MVP bootstrap, agents may commit and push directly to `main`.

Constraints:

- Only implement the current backlog task.
- Keep changes small and focused.
- Do not perform unrelated refactoring.
- Ensure the repository remains usable after changes.

After MVP, workflow will move to feature branches + pull requests + review.
