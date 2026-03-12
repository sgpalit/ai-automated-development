# Multi-Agent Development Workflow

## Purpose

This document defines how multiple AI agents collaborate to analyze, plan, implement, review, and validate changes to a target repository.

The workflow simulates a small software development team.

Each agent performs a specific role and hands off its output to the next agent.

A human remains in control of the process.

---

## Overview

The workflow consists of the following roles:

- Human Approver
- Orchestrator Agent
- Analyst Agent
- Planner Agent
- Developer Agent
- Reviewer Agent
- Tester Agent

Each role has a clearly defined responsibility.

Agents must operate sequentially and within their scope.

---

## Workflow Steps

### 1. Goal Definition (Human)

The human defines the objective.

Examples:

- improve documentation
- add a feature
- refactor a module
- prepare a release
- analyze a legacy codebase

Inputs:

- target repository
- development goal
- constraints or priorities

### 2. Repository Analysis (Analyst)

The Analyst agent inspects the target repository.

Responsibilities:

- analyze repository structure
- identify technologies used
- summarize architecture
- identify risks and improvement opportunities

Output file:

    analysis/repo-analysis.md

This file contains the structured analysis of the repository.

### 3. Planning (Planner)

The Planner agent reads:

- project goal
- MVP definition
- repository analysis
- existing backlog

The planner then generates or updates backlog tasks.

Output location:

    backlog/tasks/TASK-XXX-*.md

Tasks must be:

- small
- concrete
- implementation-ready

The planner must focus on work that moves the project toward the MVP.

### 4. Human Review

The human reviews the proposed backlog tasks.

The human may:

- approve tasks
- modify priorities
- split tasks
- reject tasks

Only approved tasks may be implemented.

### 5. Task Implementation (Developer)

The Developer agent implements one approved task.

Responsibilities:

- implement only the selected task
- keep changes small
- respect repository conventions
- avoid unrelated modifications

Outputs:

- repository changes
- summary of changes
- list of modified files

### 6. Code Review (Reviewer)

The Reviewer agent evaluates the implementation.

Responsibilities:

- verify the task scope was respected
- check code quality
- detect risks or mistakes
- ensure maintainability

Outputs:

- review summary
- approval or required corrections

If corrections are required, the Developer agent may need to update the implementation.

### 7. Validation (Tester)

The Tester agent validates that the task was implemented correctly.

Responsibilities:

- verify acceptance criteria
- check functional behavior
- detect regressions

Outputs:

- validation result
- test findings

### 8. Human Approval

The human reviews the results of:

- implementation
- review
- validation

The human decides whether:

- the task is accepted
- additional fixes are required
- the workflow continues

---

## Iteration Loop

After a task is completed and accepted, the workflow repeats:

1. Planner updates backlog if necessary
2. Human selects the next task
3. Developer implements the task
4. Reviewer reviews the change
5. Tester validates the result

This loop continues until the goal or MVP is reached.

---

## Key Principles

### Controlled Automation

Agents do not run freely.

Each step requires explicit instruction or approval.

### Small Iterations

Work should proceed through small, incremental tasks.

Large changes should be broken into multiple tasks.

### Human Oversight

Humans remain responsible for:

- defining goals
- approving backlog direction
- approving significant changes

### Clear Agent Responsibilities

Each agent must stay within its defined role.

Agents must not take responsibilities belonging to other roles.

---

## Future Evolution

Future versions of the system may include:

- automated orchestrators
- CLI-based agent runners
- CI/CD integration
- automated testing pipelines
- multi-repository coordination

These are beyond the MVP scope.

## Human Approval Checklists

Use `docs/human-approval-checklists.md` at task-approval, implementation-acceptance, and loop-continuation gates.

## Artifact Templates

Use reusable role output templates in `docs/templates/` with the handoff contract in `docs/agent-handoff-contract.md`.
