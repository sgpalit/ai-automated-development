# Running the Multi-Agent Development System

## Purpose

This document explains how a human runs the multi-agent development workflow against a repository.

The system simulates a small software team using AI agents.

The human remains in control of the workflow.

---

# Overview

The system uses multiple specialized agents:

- Orchestrator
- Analyst
- Planner
- Developer
- Reviewer
- Tester

Each agent performs a specific step in the development loop.

---

# Preparation

Before running the system, ensure the repository contains:

- agent definitions (`docs/agents.md`)
- workflow definition (`docs/workflow.md`)
- MVP definition (`docs/mvp.md`)
- agent prompts (`prompts/agents/`)
- backlog system (`backlog/tasks/`)

Create these directories if they do not exist:

    analysis/
    reviews/
    validation/

---


## Thin-Slice CLI (Analyst + Planner)

Install dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Set environment variables (recommended via `.env`):

    cp .env.example .env
    # Edit .env and set OPENAI_API_KEY

Minimum `.env` values:

    OPENAI_API_KEY=<your_api_key>
    OPENAI_MODEL=gpt-4o
    TARGET_REPO_PATH=.

Run the Analyst phase:

    python3 scripts/run_analyst.py

This creates:

    analysis/repo-analysis.md

Run the Planner phase:

    python3 scripts/run_planner.py

This creates one or more backlog task files in:

    backlog/tasks/TASK-###-short-description.md

These scripts are intentionally minimal so additional agent runners can be added later (`run_developer.py`, `run_reviewer.py`, `run_tester.py`).

---

# Step 1 — Define the Goal

The human defines the goal for the target repository.

Examples:

- analyze a legacy repository
- add a feature
- improve documentation
- refactor a module
- prepare the project for release

Example goal:

    Improve the repository structure and documentation to make the project easier for new contributors.

---

# Step 2 — Run the Analyst Agent

The Analyst agent inspects the repository.

Prompt the agent with:

    Read docs/mvp.md, docs/agents.md, and prompts/agents/analyst.md.

    Analyze the repository and produce a structured analysis.

Expected output:

    analysis/repo-analysis.md

---

# Step 3 — Run the Planner Agent

The Planner agent converts analysis into backlog tasks.

Prompt the agent with:

    Read docs/mvp.md, docs/agents.md, prompts/agents/planner.md, and analysis/repo-analysis.md.

    Review the repository and generate backlog tasks that move the project toward the MVP.

Expected output:

    backlog/tasks/TASK-XXX-*.md

The human reviews these tasks before implementation begins.

---

# Step 4 — Select the Next Task

The human selects the next task from the backlog.

Typical rule:

- choose a task with status `todo`
- prefer higher priority tasks
- ensure dependencies are completed

---

# Step 5 — Run the Developer Agent

The Developer agent implements the selected task.

Prompt example:

    Read the selected backlog task and prompts/agents/developer.md.

    Implement the task and produce the implementation summary.

Outputs:

- repository changes
- summary of work
- list of modified files

---

# Step 6 — Run the Reviewer Agent

The Reviewer agent evaluates the implementation.

Prompt example:

    Read the task, the developer output, and prompts/agents/reviewer.md.

    Review the implementation and produce a review report.

Output file:

    reviews/review-TASK-XXX.md

Possible outcomes:

- APPROVED
- CHANGES REQUIRED

If changes are required, the Developer agent revises the implementation.

---

# Step 7 — Run the Tester Agent

The Tester agent validates the implementation.

Prompt example:

    Read the task, developer output, and reviewer report.

    Validate that the implementation satisfies the acceptance criteria.

Output file:

    validation/test-TASK-XXX.md

Possible outcomes:

- PASSED
- FAILED

---

# Step 8 — Human Approval

The human reviews:

- implementation
- review report
- validation result

The human decides whether the task is accepted.

If accepted, the task status becomes:

    done

---

# Iteration Loop

After completing a task:

1. Planner may update backlog tasks
2. Human selects the next task
3. Developer implements it
4. Reviewer reviews the change
5. Tester validates the result

The loop continues until the project goal is achieved.

---

# Key Principle

The system is **human-supervised automation**.

Agents assist with:

- analysis
- planning
- implementation
- review
- validation

The human remains responsible for:

- defining goals
- approving tasks
- accepting results

# Approval and Readiness References

- Human approval checklists: `docs/human-approval-checklists.md`
- Target repo onboarding runbook: `docs/target-repo-onboarding.md`
- MVP readiness checklist: `docs/mvp-readiness-checklist.md`
