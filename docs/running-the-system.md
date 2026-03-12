# Running the Multi-Agent Development System

## Purpose

This document explains how a human runs the multi-agent development workflow against a repository.

The system simulates a small software team using AI agents.

The workflow may be human-supervised or run in controlled `MVP` auto-continue mode, depending on target repository state and runner configuration.

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

Artifacts are written under the active target namespace:

- `agents/<target-name>/analysis/`
- `agents/<target-name>/backlog/tasks/`
- `agents/<target-name>/handoff/developer/`
- `agents/<target-name>/implementation/developer/`
- `agents/<target-name>/review/reviewer/`
- `agents/<target-name>/test/`
- `agents/<target-name>/orchestrator/stop-reasons/`

---

# Preparation

Before running the system, ensure the repository contains:

- agent definitions (`docs/agents.md`)
- workflow definition (`docs/workflow.md`)
- MVP definition (`docs/mvp.md`)
- agent prompts (`prompts/agents/`)
- generated backlog artifacts (`agents/<target-name>/backlog/tasks/`)

## Wrapper behavior

The `run-agents.sh` wrapper starts the local cycle runner in tester execution mode by default so a normal run can reach developer, reviewer, and tester in one cycle:

    ./run-agents.sh
    ./run-agents.sh "Your goal here"

This is equivalent to invoking:

    python3 scripts/run_cycle.py --phase tester --execute
    python3 scripts/run_cycle.py --phase tester --execute "Your goal here"

Use a dry run when you want to inspect what would execute without making changes:

    ./run-agents.sh --dry-run
    ./run-agents.sh "Your goal here" --dry-run

Use the Python entry points directly when you want more control over a specific phase or a non-executing artifact-only pass.

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

## Direct phase commands

Run the Analyst phase:

    python3 scripts/run_analyst.py

This creates:

    agents/<target-name>/analysis/repo-analysis.md

Run the Planner phase:

    python3 scripts/run_planner.py

This creates one or more backlog task files in:

    agents/<target-name>/backlog/tasks/TASK-###-short-description.md

Run the Developer artifact phase:

    python3 scripts/run_developer.py
    python3 scripts/run_developer.py "Your goal here"

This creates:

    agents/<target-name>/handoff/developer/task-###-developer-handoff.md
    agents/<target-name>/implementation/developer/task-###-implementation.md

Run the Developer execution mode:

    python3 scripts/run_developer.py --execute
    python3 scripts/run_developer.py "Your goal here" --execute

This writes the same developer artifacts and then applies repository file changes returned by the local OpenAI prompt utility.

Without `--execute`, `run_developer.py` prepares developer artifacts only.

When no goal is provided, the local runner uses `docs/mvp.md` as default context and selects the next eligible backlog task automatically.

In supervised runs, a human typically reviews each phase outcome before continuing to the next step.

An explicit `--phase tester` run in `MVP` now performs a single-cycle validation pass. Repeated tester-gated iteration still requires `--auto-continue`.

In `MVP` auto-continue mode, the orchestrator may continue automatically when the current repository state and agent outputs allow it, and it stops when approval, retries, or blockers require intervention. Stop reasons are recorded under:

    agents/<target-name>/orchestrator/stop-reasons/

These scripts are intentionally file-based. Reviewer and tester runners are available as `run_reviewer.py` and `run_tester.py`.

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

    agents/<target-name>/analysis/repo-analysis.md

---

# Step 3 — Run the Planner Agent

The Planner agent converts analysis into backlog tasks.

Prompt the agent with:

    Read docs/mvp.md, docs/agents.md, prompts/agents/planner.md, and agents/<target-name>/analysis/repo-analysis.md.

    Review the repository and generate backlog tasks that move the project toward the MVP.

Expected output:

    agents/<target-name>/backlog/tasks/TASK-XXX-*.md

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

The Developer agent works from the selected task and developer artifacts.

Prompt example:

    Read the selected backlog task and prompts/agents/developer.md.

    Implement the task and produce the implementation summary.

Current local runner outputs:

- `agents/<target-name>/handoff/developer/task-XXX-developer-handoff.md`
- `agents/<target-name>/implementation/developer/task-XXX-implementation.md`

Execution mode:

- run `./run-agents.sh`
- or run `./run-agents.sh "Your goal here"`
- for inspection only, run `./run-agents.sh --dry-run`
- the wrapper uses tester execution mode by default so reviewer and tester phases can run in the same cycle when planner/developer succeed
- the selected task is moved to `in-progress`
- repository file changes returned by the local OpenAI prompt utility are applied locally when execution is enabled

Developer execution outputs, when a coding agent actually performs the task:

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

    agents/<target-name>/review/reviewer/task-XXX-review.md

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

    agents/<target-name>/test/task-XXX-test.md

Possible outcomes:

- READY
- RETRY
- BLOCKED

---

# Step 8 — Human Approval

The human reviews:

- implementation
- review report
- validation result

In supervised mode, the human decides whether the task is accepted before the loop advances.

In `MVP` auto-continue mode, the orchestrator may continue or stop based on reviewer/tester outputs and the current state-aware policy.

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

The loop continues until the project goal is achieved or the orchestrator records a clear stop reason.

---

# Key Principle

The system is **state-aware automation with human oversight**.

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
- handling blockers or state transitions that require intervention

# Approval and Readiness References

- Human approval checklists: `docs/human-approval-checklists.md`
- Target repo onboarding runbook: `docs/target-repo-onboarding.md`
- MVP readiness checklist: `docs/mvp-readiness-checklist.md`
