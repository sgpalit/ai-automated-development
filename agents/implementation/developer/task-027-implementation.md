# Developer Implementation Prompt

## Date
2026-03-12

## Selected Task
- Code: `TASK-027`
- File: `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md`
- Goal: Introduce explicit target repository state handling so the local runner can enforce different behavior for `MVP`, `MVP_DONE`, `TEST`, and `PROD`.

## Implementation Objective
Introduce explicit target repository state handling so the local runner can enforce different behavior for `MVP`, `MVP_DONE`, `TEST`, and `PROD`.

## Exact Files Likely To Change
- `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md`
- `.env`
- `scripts/run_cycle.py`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Production deployment automation
- Out of scope: Full policy enforcement for every future environment rule
- Out of scope: Infrastructure provisioning or observability services

## Exact Acceptance Criteria
- The runner accepts an explicit target repository state input without requiring a hidden `.env`-only workflow
- `scripts/run_cycle.py` surfaces and uses the configured state in at least one orchestration decision
- The supported states include `MVP`, `MVP_DONE`, `TEST`, and `PROD`
- Verification demonstrates the state-aware runner path with a dry-run command

## Step-by-Step Implementation Plan
1. Review `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `.env`, `scripts/run_cycle.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

## Copy-Paste Prompt For The Coding Agent
````text
# Developer Agent Prompt

You are the **Developer Agent**.

## Mission

Implement exactly one approved backlog task in a focused change set.

## Required Inputs

- Selected task file in `agents/backlog/tasks/`
- Repository context and relevant docs
- `AGENTS.md`
- `docs/agent-workflow.md`
- `docs/agent-handoff-contract.md`

## Execution Rules

1. Confirm the selected task is approved and currently `todo`.
2. Set task status to `in-progress` before implementation.
3. Implement only in-scope changes required by the task.
4. Keep unrelated refactors out of scope.
5. Run relevant checks.
6. After acceptance criteria are met, create a small focused commit for the task changes and push that commit to the active branch.
7. Include the pushed commit hash in the developer handoff so the reviewer can review the exact committed state.
8. Set task status to `done` after acceptance criteria are met and the handoff is ready for review.

If blocked, set status to `blocked` and explain why.

## Required Output Format

Use the handoff contract sections:

- Context
- Decisions
- Artifacts
- Open Questions / Risks
- Recommended Next Step

Include changed files, assumptions, verification commands, and the pushed commit hash in `Artifacts`.

## Done Criteria

- Acceptance criteria satisfied
- Relevant verification completed
- Task changes committed and pushed
- Status updated (`in-progress` → `done`)
- Output ready for Reviewer

Repository path: `/home/sp/workspace/github/ai-automated-development`
Goal: Introduce explicit target repository state handling so the local runner can enforce different behavior for `MVP`, `MVP_DONE`, `TEST`, and `PROD`.
Selected task file: `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md`

Files likely to change:
- `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md`
- `.env`
- `scripts/run_cycle.py`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Production deployment automation
- Out of scope: Full policy enforcement for every future environment rule
- Out of scope: Infrastructure provisioning or observability services

Acceptance criteria:
- The runner accepts an explicit target repository state input without requiring a hidden `.env`-only workflow
- `scripts/run_cycle.py` surfaces and uses the configured state in at least one orchestration decision
- The supported states include `MVP`, `MVP_DONE`, `TEST`, and `PROD`
- Verification demonstrates the state-aware runner path with a dry-run command

Implementation plan:
1. Review `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `.env`, `scripts/run_cycle.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-027-add-explicit-target-repository-state-handling.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-027 Add explicit target repository state handling to the runner

## Status
todo

## Priority
high

## Objective
Introduce explicit target repository state handling so the local runner can enforce different behavior for `MVP`, `MVP_DONE`, `TEST`, and `PROD`.

## Scope
- Add a tracked runner/config input for target repository state instead of relying on hidden `.env` conventions
- Teach `scripts/run_cycle.py` to read and surface the active repository state during orchestration
- Define the minimum behavior differences for `MVP`, `MVP_DONE`, `TEST`, and `PROD` in the local runner path
- Update the relevant workflow docs only as needed to match the implemented state-aware runner behavior

## Out of Scope
- Production deployment automation
- Full policy enforcement for every future environment rule
- Infrastructure provisioning or observability services

## Acceptance Criteria
- The runner accepts an explicit target repository state input without requiring a hidden `.env`-only workflow
- `scripts/run_cycle.py` surfaces and uses the configured state in at least one orchestration decision
- The supported states include `MVP`, `MVP_DONE`, `TEST`, and `PROD`
- Verification demonstrates the state-aware runner path with a dry-run command

## Dependencies
None

## Notes
Generated by `scripts/run_planner.py` because the backlog was exhausted during a promptless MVP run.
Grounding:
- `docs/mvp.md` defines an explicit repository state model with `MVP`, `MVP_DONE`, `TEST`, and `PROD`
- `agents/analysis/repo-analysis.md` still calls out workflow integration gaps that should be turned into concrete runner behavior
- Repository evidence: `scripts/run_cycle.py` currently has no explicit target repository state handling
- Repository evidence: `.env.example` already contains unrelated runtime secrets but no target repository state entry
Slug: `add-explicit-target-repository-state-handling`

```

````
