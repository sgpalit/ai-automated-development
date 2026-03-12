# Developer Implementation Prompt

## Date
2026-03-12

## Selected Task
- Code: `TASK-025`
- File: `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md`
- Goal: Add the missing tester-phase runner and task-level validation report so the local multi-agent loop can complete review and test handoff coverage required by the MVP.

## Implementation Objective
Add the missing tester-phase runner and task-level validation report so the local multi-agent loop can complete review and test handoff coverage required by the MVP.

## Exact Files Likely To Change
- `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md`
- `scripts/run_tester.py`
- `scripts/run_cycle.py`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Broad workflow refactors outside the tester phase
- Out of scope: Automatic merge or deployment behavior
- Out of scope: Reworking analyst, planner, or developer prompts beyond the minimum needed for tester integration

## Exact Acceptance Criteria
- `scripts/run_tester.py` exists and writes a tester report artifact for the selected task
- `scripts/run_cycle.py --phase tester --dry-run` reaches the tester phase without raising an unimplemented-phase error
- The tester report references the selected task, the available implementation/review artifacts, and a clear pass/fail or ready/not-ready outcome
- The task remains grounded in `docs/mvp.md` and the latest `agents/analysis/repo-analysis.md` finding that later workflow phases still need integration points and output contracts
- Verification includes a dry-run command that demonstrates the new tester phase path

## Step-by-Step Implementation Plan
1. Review `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_tester.py`, `scripts/run_cycle.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md` to `done` only after the acceptance criteria are met.
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
Goal: Add the missing tester-phase runner and task-level validation report so the local multi-agent loop can complete review and test handoff coverage required by the MVP.
Selected task file: `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md`

Files likely to change:
- `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md`
- `scripts/run_tester.py`
- `scripts/run_cycle.py`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Broad workflow refactors outside the tester phase
- Out of scope: Automatic merge or deployment behavior
- Out of scope: Reworking analyst, planner, or developer prompts beyond the minimum needed for tester integration

Acceptance criteria:
- `scripts/run_tester.py` exists and writes a tester report artifact for the selected task
- `scripts/run_cycle.py --phase tester --dry-run` reaches the tester phase without raising an unimplemented-phase error
- The tester report references the selected task, the available implementation/review artifacts, and a clear pass/fail or ready/not-ready outcome
- The task remains grounded in `docs/mvp.md` and the latest `agents/analysis/repo-analysis.md` finding that later workflow phases still need integration points and output contracts
- Verification includes a dry-run command that demonstrates the new tester phase path

Implementation plan:
1. Review `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md` and confirm the task is still in scope.
2. Update `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_tester.py`, `scripts/run_cycle.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/backlog/tasks/TASK-025-implement-local-tester-runner.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-025 Implement a local tester phase runner

## Status
done

## Priority
high

## Objective
Add the missing tester-phase runner and task-level validation report so the local multi-agent loop can complete review and test handoff coverage required by the MVP.

## Scope
- Add `scripts/run_tester.py` to read the selected backlog task plus developer and reviewer artifacts and write a tester report to `agents/test/`
- Extend `scripts/run_cycle.py` so `--phase tester` runs the tester handler after reviewer
- Keep the tester output file-based and aligned with the existing artifact path conventions
- Use the latest repository analysis and MVP workflow expectations to keep the tester slice implementation-ready and limited to one cycle

## Out of Scope
- Broad workflow refactors outside the tester phase
- Automatic merge or deployment behavior
- Reworking analyst, planner, or developer prompts beyond the minimum needed for tester integration

## Acceptance Criteria
- `scripts/run_tester.py` exists and writes a tester report artifact for the selected task
- `scripts/run_cycle.py --phase tester --dry-run` reaches the tester phase without raising an unimplemented-phase error
- The tester report references the selected task, the available implementation/review artifacts, and a clear pass/fail or ready/not-ready outcome
- The task remains grounded in `docs/mvp.md` and the latest `agents/analysis/repo-analysis.md` finding that later workflow phases still need integration points and output contracts
- Verification includes a dry-run command that demonstrates the new tester phase path

## Dependencies
None

## Notes
Generated by `scripts/run_planner.py` because the backlog was exhausted during a promptless MVP run.
Grounding:
- `docs/mvp.md` target workflow includes tester validation before human acceptance
- `agents/analysis/repo-analysis.md` notes that later workflow phases still need integration points and output contracts
- Repository evidence: `scripts/run_reviewer.py` exists, and this task adds `scripts/run_tester.py` plus tester integration in `scripts/run_cycle.py`
Slug: `implement-local-tester-runner`

```

````
