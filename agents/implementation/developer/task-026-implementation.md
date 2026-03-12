# Developer Implementation Prompt

## Date
2026-03-12

## Selected Task
- Code: `TASK-026`
- File: `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md`
- Goal: Extend the developer execution path so completed MVP tasks are committed, pushed, and handed off with the pushed commit hash for reviewer follow-up.

## Implementation Objective
Extend the developer execution path so completed MVP tasks are committed, pushed, and handed off with the pushed commit hash for reviewer follow-up.

## Exact Files Likely To Change
- `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md`
- `scripts/run_developer.py`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Feature-branch or pull-request workflow changes outside the MVP direct-to-main path
- Out of scope: Deployment automation or merge orchestration
- Out of scope: Broad refactors unrelated to developer commit/push handoff behavior

## Exact Acceptance Criteria
- `scripts/run_developer.py --execute` performs focused commit/push steps after successful task implementation
- The developer handoff artifact records the pushed commit hash for the selected task
- Reviewer inputs can reference the pushed commit instead of relying only on the local worktree
- Verification includes at least one dry-run or guarded command path showing the commit/push workflow without silently skipping it

## Step-by-Step Implementation Plan
1. Review `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_developer.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md` to `done` only after the acceptance criteria are met.
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
Goal: Extend the developer execution path so completed MVP tasks are committed, pushed, and handed off with the pushed commit hash for reviewer follow-up.
Selected task file: `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md`

Files likely to change:
- `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md`
- `scripts/run_developer.py`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Feature-branch or pull-request workflow changes outside the MVP direct-to-main path
- Out of scope: Deployment automation or merge orchestration
- Out of scope: Broad refactors unrelated to developer commit/push handoff behavior

Acceptance criteria:
- `scripts/run_developer.py --execute` performs focused commit/push steps after successful task implementation
- The developer handoff artifact records the pushed commit hash for the selected task
- Reviewer inputs can reference the pushed commit instead of relying only on the local worktree
- Verification includes at least one dry-run or guarded command path showing the commit/push workflow without silently skipping it

Implementation plan:
1. Review `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_developer.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-026-automate-developer-commit-push-in-mvp-mode.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-026 Automate developer commit and push in MVP mode

## Status
in-progress

## Priority
high

## Objective
Extend the developer execution path so completed MVP tasks are committed, pushed, and handed off with the pushed commit hash for reviewer follow-up.

## Scope
- Update `scripts/run_developer.py` so successful `--execute` runs create a focused git commit for the selected task changes
- Push the new commit with the existing repository git remote configuration and capture the pushed commit hash
- Include the pushed commit hash in the developer handoff artifact so downstream phases can reference the exact committed state
- Adjust reviewer/task handoff logic only as needed so reviewer follow-up can use the pushed commit reference

## Out of Scope
- Feature-branch or pull-request workflow changes outside the MVP direct-to-main path
- Deployment automation or merge orchestration
- Broad refactors unrelated to developer commit/push handoff behavior

## Acceptance Criteria
- `scripts/run_developer.py --execute` performs focused commit/push steps after successful task implementation
- The developer handoff artifact records the pushed commit hash for the selected task
- Reviewer inputs can reference the pushed commit instead of relying only on the local worktree
- Verification includes at least one dry-run or guarded command path showing the commit/push workflow without silently skipping it

## Dependencies
None

## Notes
Generated by `scripts/run_planner.py` because the backlog was exhausted during a promptless MVP run.
Grounding:
- `docs/mvp.md` requires developer commit/push behavior and reviewer evaluation of the pushed commit in MVP mode
- `agents/analysis/repo-analysis.md` still flags later workflow integration gaps and heuristic planning risk
- Repository evidence: `scripts/run_developer.py` applies file changes but does not run git commit/push automation yet
- Repository evidence: `scripts/run_reviewer.py` does not yet consume a pushed commit hash from developer output
Slug: `automate-developer-commit-push-in-mvp-mode`

```

````
