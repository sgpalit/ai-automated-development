# Agent Instructions

This repository is designed to be worked on by both humans and AI coding agents.

## Source of Truth

All work is tracked in the local backlog:

    backlog/tasks/

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
