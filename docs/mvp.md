# MVP Definition

## Purpose

This project is an open-source framework for running multiple AI agents against a software repository in a controlled development loop.

The goal is to simulate a small software delivery team where different agents take different responsibilities such as analysis, planning, implementation, review, and testing.

This repository is not only a documentation project.

Its purpose is to provide the structure, prompts, workflows, and conventions required to run semi-automated software development against a target repository.

---

## Core Idea

A human should be able to point the system at a target repository and use defined AI agents to:

- inspect the repository
- understand its structure and conventions
- identify useful next work
- create or update backlog tasks
- implement approved tasks
- review changes
- validate quality
- continue in a controlled loop

The human remains in control, but the agents perform most of the repetitive delivery work.

---

## MVP Goal

The MVP should prove that this repository can support a practical multi-agent development workflow against a target repository.

A successful MVP demonstrates:

- clear agent role definitions
- clear responsibilities per agent
- clear handoff format between agents
- a repeatable workflow from analysis to implementation
- a human review and approval loop
- at least one end-to-end example run

---

## Target Workflow

The intended workflow is:

1. Human selects a target repository and defines the goal
2. Analyst agent inspects the repository
3. Planner agent creates or updates backlog tasks
4. Human reviews and approves the next task
5. Developer agent implements the task
6. Reviewer agent reviews the change
7. Tester agent validates the result
8. Human decides whether to accept, adjust, or continue
9. The loop repeats

---

## MVP Agent Roles

### 1. Orchestrator

Responsible for controlling the workflow.

Responsibilities:

- decide which agent runs next
- enforce the defined process
- ensure agents stay within scope
- prevent uncontrolled autonomous behavior

### 2. Analyst

Responsible for understanding the target repository.

Responsibilities:

- inspect repository structure
- identify technologies and conventions
- identify gaps, risks, and opportunities
- summarize findings for planning

### 3. Planner

Responsible for turning findings into actionable work.

Responsibilities:

- generate backlog tasks
- refine existing tasks
- prioritize work toward the stated goal
- keep tasks small and implementation-ready

### 4. Developer

Responsible for implementing one approved task.

Responsibilities:

- make focused code or documentation changes
- stay within scope
- avoid unrelated refactoring
- report changed files and assumptions

### 5. Reviewer

Responsible for reviewing the developer output.

Responsibilities:

- check scope compliance
- check code quality
- check maintainability and safety
- suggest required fixes or approve the work

### 6. Tester

Responsible for validating the change.

Responsibilities:

- run or define validation checks
- verify acceptance criteria
- report failures, risks, and gaps
- confirm whether the task is ready

### 7. Human Approver

Responsible for final control.

Responsibilities:

- approve goals
- approve backlog direction
- approve or reject important changes
- decide whether the loop continues

---

## MVP Deliverables

The MVP should include at least the following:

### Agent Definitions

Clear documents for each agent role explaining:

- purpose
- inputs
- outputs
- responsibilities
- constraints
- handoff expectations

### Workflow Definitions

Clear documentation describing:

- sequence of agent execution
- decision points
- human approval points
- retry and correction flow

### Prompt Assets

Reusable prompts for each agent role, for example:

- repository analysis
- backlog generation
- task implementation
- code review
- test validation

### Backlog System

A local backlog that agents can read and update in a deterministic way.

### Example End-to-End Run

At least one example showing the full loop from repository analysis to completed task.

---

## Non-Goals for MVP

The MVP does not need:

- complex distributed orchestration
- autonomous background services
- advanced infrastructure
- full CI/CD automation
- multi-repository coordination
- fully automatic merge/deploy behavior

The MVP should focus on a simple, controlled, practical workflow.

---

## Definition of Done

The MVP is complete when a human can:

- choose a target repository
- define a development goal
- run the agent workflow step by step
- receive analysis and proposed backlog tasks
- approve one task
- have that task implemented, reviewed, and tested
- continue the loop with clear human control

without needing to redesign the workflow manually each time.

---

## Guiding Principle

This project should behave like a small AI-assisted software company operating on a repository.

Different agents should have different responsibilities.

The system should optimize for:

- clarity
- control
- repeatability
- safe automation
- practical software delivery
