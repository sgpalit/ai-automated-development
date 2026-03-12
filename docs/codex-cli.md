# Codex CLI Quickstart

This guide explains how to use Codex CLI in this repository with the same backlog-first workflow used by human contributors and other agents.

## Prerequisites

- Codex CLI installed and available on your `PATH`
- Access to this repository locally
- Git configured with your user name and email

Verify your environment:

```bash
codex --version
git --version
```

## Recommended Workflow in This Repository

Before starting a coding session:

1. Read `AGENTS.md`
2. Read `docs/agent-workflow.md`
3. Scan `backlog/tasks/` and choose the next eligible task (`todo`, highest priority, dependencies done, lowest task number)
4. Mark the selected task as `in-progress`

After finishing implementation and checks:

1. Mark the task as `done`
2. Commit with a message that references the task ID (example: `TASK-003 codex cli quickstart`)
3. Provide a completion report with:
   - summary of changes
   - modified files
   - assumptions
   - possible follow-up tasks

## Basic Commands

Run Codex in the current repository:

```bash
codex
```

Run Codex with a direct instruction:

```bash
codex "Read AGENTS.md, pick the next todo task, and implement it with small focused changes."
```

Optional: include repository context in your prompt:

```bash
codex "Use backlog/tasks as source of truth, follow docs/agent-workflow.md, and keep one-task scope."
```

## Typical Session Pattern

A practical loop for this project:

1. Start from repository root.
2. Ask Codex to inspect `AGENTS.md` and backlog tasks.
3. Confirm the selected task is marked `in-progress`.
4. Implement only that task's scope.
5. Run relevant checks.
6. Mark task `done`.
7. Commit using the task ID.

## Troubleshooting

### `codex: command not found`

Codex CLI is not installed or not on `PATH`.

- Re-open the terminal after installation
- Confirm the install location is on `PATH`
- Retry `codex --version`

### Git commit fails due to missing identity

Configure Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Agent chooses the wrong task

Re-check task selection order in `docs/agent-workflow.md`:

1. `todo` only
2. highest priority
3. dependencies done
4. lowest task number tie-breaker

## Notes

This quickstart intentionally stays lightweight for MVP. Advanced automation (scripts, CI integration, orchestration) should be added in later backlog tasks.
