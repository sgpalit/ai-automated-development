# Backlog

This directory contains the **local backlog** for the project.

The backlog is the **source of truth for work** in this repository.  
Both humans and AI agents should use this backlog to decide what to work on next.

Tasks are stored as **individual Markdown files** inside `backlog/tasks/`.

Example:

    backlog/
      README.md
      tasks/
        TASK-001-example.md

---

## Task lifecycle

Each task moves through these states:

| Status        | Meaning |
|--------------|---------|
| `todo`        | Ready to be picked up |
| `in-progress` | Currently being worked on |
| `blocked`     | Cannot continue due to dependency/issue |
| `done`        | Completed |

Only tasks with status `todo` should be picked up.

---

## Task naming convention

Task files must follow:

    TASK-###-short-description.md

Examples:

    TASK-001-project-structure.md
    TASK-002-agent-workflow.md
    TASK-003-codex-cli-bootstrap.md

Rules:

- Use a **three-digit number**
- Use **kebab-case** for the description
- Numbers should be sequential

---

## Task file template

Use this structure for each task file:

    # TASK-XXX Title

    ## Status
    todo

    ## Priority
    medium

    ## Objective
    Short description of what this task achieves.

    ## Scope
    What should be implemented.

    ## Out of Scope
    What must NOT be implemented.

    ## Implementation Notes
    Optional hints, constraints, or guidance.

    ## Acceptance Criteria
    - Condition 1
    - Condition 2

    ## Dependencies
    - TASK-000 (optional)

---

## How agents should use the backlog

When an AI agent works in this repository, it should:

1. Scan `backlog/tasks/` for tasks with status `todo`
2. Prefer `high` priority tasks first
3. Ensure dependencies are `done`
4. Mark the task as `in-progress` before starting
5. Implement changes in a small, reviewable set
6. Mark the task as `done` when completed
7. Add follow-up tasks when needed (new `TASK-###` files)

---

## Priority levels

| Priority | Meaning |
|---------|---------|
| `high`   | Foundational or blocking work |
| `medium` | Normal development work |
| `low`    | Nice-to-have improvements |

---

## Principles

- Keep tasks **small and focused**
- Aim for **one task = one PR**
- Avoid vague tasks; define scope + acceptance criteria
- Prefer **incremental progress** over big rewrites

---

## Adding a new task

1. Create a new file in `backlog/tasks/`
2. Use the next sequential number
3. Fill in the task template
4. Set initial status to `todo`

Example path:

    backlog/tasks/TASK-006-something.md
