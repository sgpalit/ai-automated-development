# Codex Task: Bootstrap local backlog and agent workflow for AI Automated Development

You are working in the `ai-automated-development` repository.

## Goal

Set up the repository so AI agents can work on it step by step in a controlled and repeatable way.

The workflow must use:

- a **local backlog in the repo** as the source of truth for tasks
- **small incremental tasks**
- clear documentation for how an agent picks the next task
- optional hooks for **Slack notifications**
- a structure that can later support **Codex CLI** and **OpenAPI-based tools**

Do **not** overengineer this. Prefer simple markdown and Python scripts over heavy frameworks.

## What to build

Create an initial working foundation for agent-driven development in this repo.

### 1. Backlog in repo

Add a local backlog structure inside the repository.

Recommended structure:

    backlog/
      README.md
      tasks/
        TASK-001-project-structure.md
        TASK-002-agent-workflow.md
        TASK-003-codex-cli-bootstrap.md
        TASK-004-slack-notification-design.md
        TASK-005-openapi-tooling-plan.md

Requirements:

- `backlog/README.md` explains task lifecycle and format
- each task file contains:
  - id
  - title
  - status (`todo`, `in-progress`, `blocked`, `done`)
  - priority (`high`, `medium`, `low`)
  - objective
  - scope
  - out of scope
  - implementation notes
  - acceptance criteria
  - dependencies

### 2. Generate first backlog

Create the first backlog for this project.

At minimum include tasks for:

- repository structure cleanup / bootstrap
- agent instructions
- prompt library structure
- workflow docs
- Codex CLI usage doc
- local task runner or helper script
- Slack integration design
- OpenAPI integration design
- contribution guide for humans + agents

Keep tasks practical and small enough for an agent to complete in one focused PR.

### 3. Agent workflow documentation

Create documentation describing how an AI agent should work in this repo.

Add a file like:

    docs/agent-workflow.md

It should define:

- how the agent selects the next task from the local backlog
- how the agent marks a task as in-progress
- how the agent documents assumptions
- how the agent reports changed files
- how the agent avoids unrelated cleanup
- how the agent proposes follow-up tasks
- how the agent closes a task

### 4. Codex CLI bootstrap

Add a short guide for using Codex CLI on this repo.

Add a file like:

    docs/codex-cli.md

Include:

- expected workflow
- how to point Codex to the repo
- how to ask it to pick the next local backlog item
- how to keep changes small and reviewable

Do not assume a specific secret setup. Use placeholders where needed.

### 5. Slack communication design

Add a lightweight design doc for Slack-based agent communication.

Add a file like:

    docs/slack-agent-communication.md

The design should cover:

- when the agent sends Slack messages
- message types:
  - task started
  - task blocked
  - task completed
  - review needed
- how to keep Slack optional
- use environment variables for webhook configuration
- no hardcoded secrets

Do not fully implement Slack unless trivial. A design plus minimal stub is enough.

### 6. OpenAPI tooling plan

Add a design doc for using OpenAPI-described tools with agents.

Add a file like:

    docs/openapi-tooling.md

Cover:

- why OpenAPI can help agents call internal tools safely
- possible future tools:
  - backlog API
  - repo analysis API
  - CI/CD status API
  - documentation search API
- recommended minimal first step
- security considerations

### 7. Helper script

Add a very small Python helper script to inspect backlog tasks.

Recommended file:

    scripts/backlog.py

Minimum features:

- list tasks
- filter by status
- print the next recommended todo task based on priority and dependencies

Prefer standard library only.

### 8. Root documentation update

Update `README.md` so new contributors understand:

- this repo uses a local backlog
- agents work task by task
- docs live under `docs/`
- scripts live under `scripts/`

## Decision guidance

Use these defaults unless the repo already has a better pattern:

- **source of truth for work**: local markdown backlog in the repo
- **agent communication**: optional Slack notifications via webhook
- **execution model**: Codex CLI runs one task at a time
- **tool integration**: document OpenAPI direction, do not overbuild yet
- **language for helpers**: Python
- **task size**: small, reviewable, incremental

## Recommendation

For this stage:

- use **local backlog first**
- use **Codex CLI** as the worker
- use **Slack only for notifications**
- use **OpenAPI later** when you have internal tools worth exposing

## Constraints

- Keep everything simple and repo-native
- No databases
- No complex orchestration
- No background services required
- No hardcoded secrets
- No unrelated refactors
- Keep files small and easy to read

## Expected output

Make the changes directly in the repository.

At the end, provide:

1. a short summary of what was created
2. the list of changed files
3. any assumptions made
4. suggested next backlog tasks

If some file names need to differ to match existing repo conventions, keep the same intent and explain the deviation.
