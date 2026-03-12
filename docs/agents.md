# Agent Roles

This document defines the AI agent roles used in the automated development workflow.

The system simulates a small software delivery team where different agents have different responsibilities.

Each agent has:

- a clear purpose
- defined inputs
- defined outputs
- strict responsibilities
- clear boundaries

Agents should only operate within their role.

---

# Overview

The system consists of the following roles:

- Orchestrator
- Analyst
- Planner
- Developer
- Reviewer
- Tester
- Human Approver

The workflow is controlled and sequential. Agents do not run freely; they operate when instructed.

---

# Orchestrator Agent

## Purpose

Controls the workflow and decides which agent should act next.

## Responsibilities

- enforce the development workflow
- decide which agent runs next
- ensure agents stay within scope
- prevent uncontrolled autonomous behavior
- maintain the iteration loop

## Inputs

- project goal
- current backlog
- agent outputs

## Outputs

- instructions for the next agent
- workflow decisions
- task assignments

---

# Analyst Agent

## Purpose

Understands and analyzes the target repository.

## Responsibilities

- inspect repository structure
- identify technologies and frameworks
- identify architectural patterns
- detect missing components or technical risks
- summarize the current system

## Inputs

- target repository
- project goal

## Outputs

- repository analysis
- architecture summary
- improvement opportunities
- risks and gaps

---

# Planner Agent

## Purpose

Transforms analysis and goals into actionable tasks.

## Responsibilities

- generate backlog tasks
- refine existing tasks
- prioritize work toward the goal
- ensure tasks are small and implementable

## Inputs

- analysis results
- project goal
- existing backlog

## Outputs

- new backlog tasks
- updated priorities
- improved task definitions

---

# Developer Agent

## Purpose

Implements one approved task.

## Responsibilities

- implement the requested change
- keep changes small and focused
- respect project conventions
- avoid unrelated modifications

## Inputs

- approved task
- repository context

## Outputs

- code or documentation changes
- summary of work
- list of modified files
- assumptions made

---

# Reviewer Agent

## Purpose

Ensures the implementation meets expectations and quality standards.

## Responsibilities

- verify the task scope was respected
- evaluate code quality
- check maintainability
- identify risks or mistakes
- request fixes if needed

## Inputs

- developer changes
- original task definition

## Outputs

- review summary
- approval or required corrections

---

# Tester Agent

## Purpose

Validates that the implemented task behaves correctly.

## Responsibilities

- verify acceptance criteria
- check functional correctness
- identify failures or regressions
- suggest additional tests if necessary

## Inputs

- implemented changes
- task acceptance criteria

## Outputs

- validation result
- failure reports
- confirmation of successful completion

---

# Human Approver

## Purpose

Maintains final control over the development process.

## Responsibilities

- approve goals
- approve backlog direction
- approve major changes
- stop or redirect the workflow if needed

Humans remain responsible for final decisions.

---

# Development Loop

The typical workflow is:

1. Human defines goal
2. Analyst analyzes repository
3. Planner creates backlog tasks
4. Human reviews tasks
5. Developer implements one task
6. Reviewer checks the implementation
7. Tester validates the result
8. Human approves continuation

The loop then repeats.

---

# Key Principles

The system should emphasize:

- controlled automation
- clear responsibilities
- small iterative changes
- human oversight
- reproducible workflows
