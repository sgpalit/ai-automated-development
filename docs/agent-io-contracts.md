# Agent Input / Output Contracts

## Purpose

This document defines how agents exchange information during the multi-agent development workflow.

Each agent must produce outputs that the next agent can consume in a predictable way.

Standardized outputs make it easier to automate the workflow using an AI CLI or orchestration tool.

---

## General Principles

All agent outputs should follow these rules:

- structured and easy to parse
- predictable file locations
- minimal ambiguity
- human-readable

Agents should write outputs to dedicated directories in the repository.

---

## Output Locations

The system uses the following directories for agent outputs.

    analysis/
    backlog/tasks/
    reviews/
    validation/

Each directory corresponds to a stage in the workflow.

---

## Analyst Agent Output

The Analyst agent writes repository analysis results.

Output file:

    agents/analysis/repo-analysis.md

Contents should include:

- repository overview
- technology stack
- architecture summary
- key components
- conventions
- risks
- improvement opportunities

This file becomes the primary input for the Planner agent.

---

## Planner Agent Output

The Planner agent creates backlog tasks.

Output location:

    backlog/tasks/

Each task must be a separate file using the naming format:

    TASK-###-short-description.md

Each task file must contain:

- status
- priority
- objective
- scope
- out of scope
- implementation notes
- acceptance criteria
- dependencies

These tasks become the input for the Developer agent.

---

## Developer Agent Output

The Developer agent modifies the repository to implement a task.

Outputs include:

- repository file changes
- implementation summary

The summary should contain:

- summary of work
- list of modified files
- assumptions made

This information becomes input for the Reviewer agent.

---

## Reviewer Agent Output

The Reviewer agent evaluates the developer changes.

Output location:

    reviews/

Example file:

    agents/review/reviewer/task-###-review.md

The review must include:

- review summary
- scope compliance
- acceptance criteria verification
- issues
- suggestions
- final decision (APPROVED or CHANGES REQUIRED)

---

## Tester Agent Output

The Tester agent validates the change.

Output location:

    validation/

Example file:

    agents/test/task-###-test.md

The validation report must include:

- validation summary
- acceptance criteria verification
- detected issues
- validation result (PASSED or FAILED)

---

## Human Decisions

Humans review outputs from:

- Planner
- Reviewer
- Tester

Humans decide whether:

- tasks are approved
- fixes are required
- the workflow continues

Human decisions may update backlog task status.

---

## File Naming Conventions

Agents should follow these naming rules.

Analysis:

    agents/analysis/repo-analysis.md

Backlog tasks:

    agents/backlog/tasks/TASK-###-description.md

Reviews:

    agents/review/reviewer/task-###-review.md

Validation:

    agents/test/task-###-test.md

---

## Automation Readiness

These contracts allow future tooling to:

- parse agent outputs
- trigger the next agent automatically
- maintain workflow state
- integrate with CLI runners or automation systems
