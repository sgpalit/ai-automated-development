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

---

## Reporting Format

When completing a task, agents should report:

- summary of work
- files changed
- assumptions made
- suggested follow-up tasks

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
3. Agent marks the task as `done`
4. Agent proposes follow-up tasks
5. Human reviews backlog
6. Human instructs the agent to continue

Agents must never continue automatically without instruction.

---

## Branch Strategy (MVP Phase)

Until the MVP is complete, agents may commit and push directly to `main`.

This is allowed to keep development fast during early bootstrap.

Rules:

- keep commits small
- maintain a working state
- avoid unrelated changes

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
