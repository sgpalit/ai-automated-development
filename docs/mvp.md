# MVP Definition

## Purpose

This project should become a practical framework for running a multi-agent software delivery loop against a target repository with minimal human intervention.

The MVP is not just a set of prompts. It should prove that a repository can be analyzed, planned, implemented, reviewed, tested, committed, pushed, observed, and resumed by agents in a repeatable way.

The system must work both for this repository and for other target repositories without redesigning the workflow each time.

---

## Core Idea

A human should be able to point the system at a target repository, configure the desired operating mode, and let the agent loop keep moving the repository toward MVP completion.

In MVP mode, the system should:

- inspect and understand the target repository
- identify the next valuable work
- create or refine backlog tasks
- implement tasks
- review and test changes
- commit and push completed work
- continue iterating until the repository reaches MVP readiness

The human defines direction and constraints up front, but the loop should not require manual approval between every task while the repository is still in MVP mode.

---

## Repository State Model

The workflow must be driven by an explicit target repository state property, not by ad-hoc environment variables.

Required states:

- `MVP`
- `MVP_DONE`
- `TEST`
- `PROD`

Rules:

- The active target repository state should be passed as tracked configuration or runtime properties, not as a hidden `.env` convention.
- Agents must adapt behavior based on this state.
- `MVP` allows aggressive iteration and direct automation to reach a usable first product.
- `MVP_DONE` shifts the system from bootstrap mode to controlled improvement mode.
- `TEST` and `PROD` require stricter safety rules, approvals, and deployment boundaries.

---

## MVP Goal

The MVP should prove that this repository can support an autonomous or near-autonomous multi-agent development workflow against a configurable target repository.

A successful MVP demonstrates:

- clear agent role definitions
- clear handoff contracts between agents
- a repeatable workflow from analysis to pushed task completion
- automatic continuation while the target repository state is `MVP`
- task-level commit and push behavior by the developer agent
- repository-aware planning grounded in the current target codebase
- at least one end-to-end example run that reaches a real completed task

---

## Target Workflow

The intended MVP workflow is:

1. Human selects a target repository and initial constraints
2. Human sets the target repository state to `MVP`
3. Analyst agent inspects the repository
4. Planner agent creates or refines backlog tasks
5. Developer agent implements one task
6. Developer agent verifies, commits, and pushes the task result
7. Reviewer agent reviews the pushed commit
8. Tester agent validates the task result and workflow readiness
9. Orchestrator decides whether to continue with the next task
10. The loop repeats automatically until the repository reaches `MVP_DONE` or a stop condition is hit

During `MVP`, the default assumption is continuous autonomous progress.

Human interaction is required only for:

- initial setup and constraints
- secrets and infrastructure access configuration
- high-risk failures or blocked states
- switching the repository state out of `MVP`

---

## Stop Conditions

The autonomous MVP loop should stop cleanly when one of the following is true:

- the target repository reaches `MVP_DONE`
- no grounded next task can be derived
- the loop is blocked by missing credentials, infrastructure, or permissions
- tests or review repeatedly fail beyond the configured retry policy
- a policy rule for `TEST` or `PROD` would be violated

The stop reason must be written as a visible artifact for human follow-up.

---

## MVP Agent Roles

### 1. Orchestrator

Responsible for controlling the workflow.

Responsibilities:

- decide which agent runs next
- enforce state-aware process rules
- continue automatically while the target repository state is `MVP`
- stop cleanly on blockers or policy violations
- record why the loop continued or stopped

### 2. Analyst

Responsible for understanding the target repository.

Responsibilities:

- inspect repository structure, stack, conventions, and risks
- summarize findings for planning
- refresh analysis as the repository evolves
- support repository portability when the target repository changes

### 3. Planner

Responsible for turning findings into actionable work.

Responsibilities:

- generate backlog tasks
- refine existing tasks
- prioritize work toward MVP completion
- keep tasks small, testable, and implementation-ready
- adapt planning to the current target repository rather than this repo only

### 4. Developer

Responsible for implementing one approved task.

Responsibilities:

- make focused repository changes
- stay within scope
- run the required verification
- create a focused commit
- push the commit in `MVP` mode
- report the pushed commit hash for reviewer/tester usage

### 5. Reviewer

Responsible for reviewing the developer output.

Responsibilities:

- review the pushed commit, not only the local worktree
- check scope compliance
- check quality, maintainability, and safety
- approve or request changes with explicit reasoning

### 6. Tester

Responsible for validating the change.

Responsibilities:

- run or define validation checks
- verify acceptance criteria
- confirm task readiness
- report whether the loop can safely continue

### 7. Memory / Context Layer

Responsible for retaining useful project context across cycles.

Responsibilities:

- preserve durable project facts, decisions, and task history
- support retrieval of relevant repository context for later runs
- avoid repeating the same analysis every cycle when durable memory is sufficient

This may be implemented with a simple artifact store first and optionally with RAG infrastructure later.

### 8. Human Operator

Responsible for defining direction and exception handling.

Responsibilities:

- choose the target repository
- define high-level goals and constraints
- provide credentials and infrastructure access
- review blockers, failures, or state transitions when required

---

## MVP Deliverables

The MVP should include at least the following.

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
- state-dependent behavior
- autonomous continuation rules
- stop conditions
- retry and correction flow

### Prompt Assets

Reusable prompts for each agent role, including:

- repository analysis
- backlog generation
- task implementation
- code review
- test validation
- autonomous loop continuation

### Backlog System

A local backlog that agents can read, update, and extend deterministically.

### Commit and Push Automation

Developer output must be able to:

- create a focused commit for the completed task
- push that commit
- hand off the exact commit hash for review

### State-Aware Runner

The runner must understand and enforce repository operating state such as `MVP`, `MVP_DONE`, `TEST`, and `PROD`.

### Repository Portability

The system must support retargeting to another repository without rewriting the whole workflow.

Minimum expectations:

- repository-specific configuration is explicit
- prompts and scripts do not assume this repository only
- onboarding and analysis can be rerun for a new target repository

### Example End-to-End Run

At least one example showing the full loop from repository analysis to committed, pushed, reviewed, and tested task completion.

---

## Optional but Valuable MVP Extensions

These are not required for the first thin slice, but they are in scope for the broader MVP direction and should be considered during planning.

### RAG / Vector Memory

A RAG layer can be useful if:

- the target repository is too large for direct prompt context
- durable memory across many cycles becomes important
- agents need retrieval over prior decisions, tasks, logs, or architecture notes

Qdrant or a similar vector store is a reasonable option if retrieval quality becomes a bottleneck.

### Infrastructure Coordination

An infra agent in another repository may be used to provision or update supporting services such as:

- Qdrant
- PostgreSQL
- Redis
- message brokers
- extra worker containers

This should remain optional and state-aware rather than mandatory for every target repository.

### Notifications

The loop should be able to notify humans when it:

- reaches `MVP_DONE`
- becomes blocked
- requires credentials or approval
- detects repeated failures

Microsoft Teams is a valid notification target.

### Observability

Prometheus and Grafana are useful for:

- loop health
- agent run counts
- task throughput
- failure rates
- queue depth
- resource consumption

### Scheduling

A cron job, scheduler, or worker loop is useful so the system can continue running until `MVP_DONE` instead of requiring manual restarts.

---

## Non-Goals for the First Thin Slice

The first thin slice does not need:

- complex distributed orchestration on day one
- full production-grade deployment automation
- mandatory infrastructure services for every repository
- perfect long-term memory on the first pass
- organization-wide change management workflows

But the MVP should not block these capabilities structurally.

---

## Definition of Done

The MVP is complete when a human can:

- point the system at a target repository
- set the repository state to `MVP`
- provide initial goals and constraints
- let the agent loop run with minimal intervention
- see the system create tasks, implement them, review them, test them, commit them, and push them
- receive a clear stop condition or completion signal
- switch behavior appropriately when the repository state changes
- reuse the workflow on another repository without redesigning the framework

The practical completion target is:

- the system can keep working until the target repository reaches `MVP_DONE`
- or it stops cleanly with actionable reasons that a human can resolve

---

## Guiding Principle

This project should behave like a small AI-assisted software company that can operate continuously on a repository, not just like a prompt collection.

The system should optimize for:

- clarity
- repeatability
- practical autonomy
- state-aware safety
- repository portability
- observable progress
- practical software delivery
