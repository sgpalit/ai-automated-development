# AGENTS.md

## Purpose

This repository is designed to be developed collaboratively by humans and AI coding agents.

Agents should work in a structured, predictable workflow driven by the local backlog and clear project goals.

The objective is to build an open-source foundation for AI-assisted software development workflows.

Agents must prioritize practical progress toward a usable MVP, not just small repository improvements.

---

## Project Goal

The goal of this repository is to provide a practical open-source framework for AI-driven development.

It should help developers and teams:

- structure repositories for AI-assisted development
- manage work through a local backlog
- collaborate with AI agents step by step
- reuse prompts and workflows
- understand how to run autonomous or semi-autonomous development loops

The repository should act as a reference implementation for AI-driven development workflows.

---

## MVP Definition

A usable MVP should include:

- clear agent instructions
- a local backlog workflow
- practical Codex usage documentation
- a prompt library structure
- contributor guidance for humans and agents
- at least one example workflow showing the full agent loop
- minimal helper tooling where it improves the workflow

Agents should prioritize tasks that help deliver this MVP.

Detailed MVP requirements are defined in `docs/mvp.md`.

---

## Source of Truth

All work is tracked in the repository backlog.

Path:

    backlog/tasks/

Agents must never invent work outside the backlog unless creating new backlog tasks for human review.

---

## Task Selection Rule

When asked to pick the next task, agents must:

1. Scan `backlog/tasks/`
2. Select tasks with status `todo`
3. Prefer higher priority tasks first
4. Ensure dependencies are `done`
5. If multiple tasks qualify, select the lowest `TASK-###` number

Agents must implement only one task at a time.

## Default Runner Behavior

If the local runner is started without a human goal prompt, agents must not invent a new free-text goal.

In that mode, use `docs/mvp.md` as the default project context and select the next eligible backlog task automatically.

Selection order:

1. Scan `agents/backlog/tasks/` first, then `backlog/tasks/` if present
2. Prefer tasks with status `todo`
3. If no `todo` task is eligible, resume the next eligible task with status `in-progress`
4. Prefer higher priority tasks first
5. Ensure dependencies are `done`
6. If multiple tasks qualify, select the lowest `TASK-###` number

If no eligible task exists, the planner should try to generate exactly one new implementation-ready backlog task from:

- `docs/mvp.md`
- `agents/analysis/repo-analysis.md`

Rules for that empty-backlog path:

- create only one new task
- use the next sequential `TASK-###` number in `agents/backlog/tasks/`
- keep the task small and implementation-ready
- include `Status`, `Priority`, `Objective`, `Scope`, `Out of Scope`, `Acceptance Criteria`, and `Dependencies`
- ground the task in the next missing MVP slice supported by the latest repository analysis
- stop after task generation and surface the result for human review
- if required inputs are missing or no grounded next task can be produced, stop cleanly and explain why

The planner should reuse the existing backlog in this mode before generating a new task.

---

## Task State Updates

Before starting work, change the task status to:

    in-progress

After completion, change the task status to:

    done

If the task cannot proceed, change the task status to:

    blocked

---

## Implementation Rules

Agents must follow these principles:

- keep changes small and focused
- avoid unrelated refactoring
- prefer simple solutions
- maintain a working repository state
- avoid overengineering
- respect the existing repository structure

Each task should ideally result in one pull request or one small commit set.

For the current MVP workflow, the developer agent must finish verification, create a focused commit for the completed task, push that commit, and hand off the pushed commit hash for review.

Reviewers must evaluate the developer's pushed commit, not an uncommitted local working tree.

---

## Reporting Format

When completing a task, agents should report:

- summary of work
- files changed
- assumptions made
- suggested follow-up tasks
- pushed commit hash for reviewer reference

---

## Follow-up Task Creation

After completing a task, the agent should evaluate whether additional backlog tasks are needed.

The agent must think about the overall project goal and MVP, not only the completed task.

Good follow-up tasks:

- move the repository closer to MVP
- are small and implementation-ready
- have clear acceptance criteria
- represent logical next steps

Rules:

- use the next sequential `TASK-###` number
- set status to `todo`
- include priority, objective, scope, out of scope, acceptance criteria, and dependencies
- do not start newly created tasks automatically

New tasks require human review before execution.

---

## Human Review Loop

Development follows a human-supervised workflow:

1. Agent picks a backlog task
2. Agent implements the task
3. Agent verifies the changes, commits them, and pushes the commit
4. Agent marks the task as `done`
5. Agent reports the pushed commit hash and proposes follow-up tasks
6. Human/reviewer checks that pushed commit
7. Human reviews backlog
8. Human instructs the agent to continue

If a new task is generated because the backlog is exhausted, the loop pauses at that point until a human reviews the generated task.

Agents must never continue automatically without instruction.

---

## Branch Strategy (MVP Phase)

Until the MVP is complete, agents may commit and push directly to `main`.

This is allowed to keep development fast during early bootstrap.

Rules:

- keep commits small
- maintain a working state
- avoid unrelated changes
- push the completed task commit before reviewer handoff

After MVP, the workflow may switch to:

- feature branches
- pull requests
- code review

---

## Repository Structure

Typical repository layout:

    backlog/     project tasks
    docs/        documentation
    prompts/     reusable AI prompts
    scripts/     helper scripts
    agents/      agent-related documentation

Agents should respect this structure and place new files appropriately.

---

## Final Principle

Agents should not only complete tasks.

They should help move the project toward a practical, usable MVP for AI-driven development workflows.

## Backlog Control Rule

The backlog currently contains a predefined set of tasks required to bootstrap the system.

Agents must not create new backlog tasks until all existing `todo` tasks are completed.

The goal of the current backlog is to reach the first working MVP of the multi-agent development workflow.

New tasks may only be created after the backlog is cleared, when the planner is explicitly handling the empty-backlog MVP continuation path, or when explicitly instructed by a human.
