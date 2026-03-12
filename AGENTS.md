# Agent Instructions

This repository is designed to be worked on by both humans and AI coding agents.

## Source of Truth

All work is tracked in the local backlog:

    backlog/tasks/

For detailed operating rules, see:

    docs/agent-workflow.md

Agents must select tasks from this directory.

## Task Workflow

1. Scan `backlog/tasks/`
2. Select a task with status `todo`
3. Prefer higher priority tasks
4. Ensure dependencies are completed
5. Mark task as `in-progress`
6. Implement the task
7. Mark task as `done`

## Development Principles

Agents should follow these rules:

- Keep changes **small and focused**
- Avoid unrelated refactoring
- Prefer simple solutions
- Document assumptions
- Create follow-up tasks if needed

## Repository Structure

    backlog/     → project tasks
    docs/        → documentation
    prompts/     → AI prompts
    scripts/     → helper scripts
    agents/      → agent related docs

## Output Expectations

When completing a task, the agent should provide:

- summary of changes
- list of modified files
- assumptions made
- possible follow-up tasks

## Branch Strategy (MVP Phase)

Until the first MVP is completed, agents may **commit and push directly to the `main` branch**.

This is allowed to keep development fast and reduce overhead while the project is still in early bootstrap.

Rules:

- Keep changes **small and focused**
- Only implement the **current backlog task**
- Do not introduce unrelated refactoring
- Ensure the repository remains in a **working state**

After the MVP phase, the workflow will change to:

- feature branches
- pull requests
- code review

## Commit Messages

Use clear commit messages referencing the task id.

Example: 

TASK-001 bootstrap repository structure
