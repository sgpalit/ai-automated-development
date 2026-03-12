# Developer Implementation Prompt

## Date
2026-03-13

## Selected Task
- Code: `TASK-032`
- File: `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md`
- Goal: Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task.

## Implementation Objective
Make the workflow write a visible target-scoped stop artifact when the planner cannot derive a grounded next task after backlog exhaustion, so MVP stop conditions are observable and compliant with the orchestrator requirements.

## Exact Files Likely To Change
- `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md`
- `scripts/run_cycle.py`
- `scripts/shared/artifact_paths.py`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Changing planner task generation heuristics or adding new MVP task inference logic.
- Out of scope: Implementing notifications, scheduling, or broader observability dashboards.
- Out of scope: Refactoring unrelated phase runners or changing reviewer/tester report formats.

## Exact Acceptance Criteria
- When `scripts/run_cycle.py --auto-continue --dry-run` reaches the `planner-stopped-no-grounded-next-task` path, the console output includes the exact target-scoped stop artifact path that would be written under `agents/ai-automated-development/orchestrator/stop-reasons/`.
- When executed without `--dry-run` in a setup that triggers planner exhaustion, a markdown artifact is created under `agents/ai-automated-development/orchestrator/stop-reasons/` containing the stop reason `planner-stopped-no-grounded-next-task`, the target repository state, and a timestamp.
- Verification must use a command path that actually reaches planner exhaustion in the current runner, not only the default single-cycle stop path.
- `python -m py_compile scripts/run_cycle.py scripts/shared/artifact_paths.py` succeeds after the change.

## Step-by-Step Implementation Plan
1. Review `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md` and confirm the task is still in scope.
2. Update `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_cycle.py`, `scripts/shared/artifact_paths.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

## Copy-Paste Prompt For The Coding Agent
````text
# Developer Agent Prompt

You are the **Developer Agent**.

## Mission

Implement exactly one approved backlog task in a focused change set.

## Required Inputs

- Selected task file in `agents/<target-name>/backlog/tasks/`
- Repository context and relevant docs
- `AGENTS.md`
- `docs/agent-workflow.md`
- `docs/agent-handoff-contract.md`

## Execution Rules

1. Confirm the selected task is approved and currently `todo`.
2. Set task status to `in-progress` before implementation.
3. Implement only in-scope changes required by the task.
4. Keep unrelated refactors out of scope.
5. Run the task-appropriate verification commands and record their outcomes.
6. After acceptance criteria are met, create a small focused commit for the task changes and push that commit to the active branch.
7. Include the pushed commit hash in the developer handoff so the reviewer can review the exact committed state.
8. Set task status to `done` after acceptance criteria are met and the handoff is ready for review.

If blocked, set status to `blocked` and explain why.

Do not treat task-file-only edits, prompt-only edits, or handoff-only churn as task completion.
Do not mark the task `done` if the intended implementation files were not changed or required verification did not pass.

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
- Developer handoff includes changed files, verification evidence, and pushed commit hash

Repository path: `/home/sp/workspace/github/ai-automated-development`
Goal: Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task.
Selected task file: `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md`

Files likely to change:
- `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md`
- `scripts/run_cycle.py`
- `scripts/shared/artifact_paths.py`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Changing planner task generation heuristics or adding new MVP task inference logic.
- Out of scope: Implementing notifications, scheduling, or broader observability dashboards.
- Out of scope: Refactoring unrelated phase runners or changing reviewer/tester report formats.

Acceptance criteria:
- When `scripts/run_cycle.py --auto-continue --dry-run` reaches the `planner-stopped-no-grounded-next-task` path, the console output includes the exact target-scoped stop artifact path that would be written under `agents/ai-automated-development/orchestrator/stop-reasons/`.
- When executed without `--dry-run` in a setup that triggers planner exhaustion, a markdown artifact is created under `agents/ai-automated-development/orchestrator/stop-reasons/` containing the stop reason `planner-stopped-no-grounded-next-task`, the target repository state, and a timestamp.
- Verification must use a command path that actually reaches planner exhaustion in the current runner, not only the default single-cycle stop path.
- `python -m py_compile scripts/run_cycle.py scripts/shared/artifact_paths.py` succeeds after the change.

Implementation plan:
1. Review `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md` and confirm the task is still in scope.
2. Update `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_cycle.py`, `scripts/shared/artifact_paths.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/ai-automated-development/backlog/tasks/TASK-032-ai-auto-stop-artifact-no-task.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-032 Implement target-state aware stop artifact for planner no-task exhaustion

## Status
todo

## Priority
high

## Objective
Make the workflow write a visible target-scoped stop artifact when the planner cannot derive a grounded next task after backlog exhaustion, so MVP stop conditions are observable and compliant with the orchestrator requirements.

## Scope
- Update `scripts/run_cycle.py` to persist a stop artifact when auto-continue or a normal cycle stops for `planner-stopped-no-grounded-next-task`, including target name, repository state, phase, reason, timestamp, and cycle count.
- Add a deterministic artifact helper in `scripts/shared/artifact_paths.py` for a target-scoped stop path pattern under `agents/<target-name>/orchestrator/stop-reasons/`, such as a latest file and/or timestamped markdown file.
- Ensure the stop artifact content follows the handoff-style visible artifact pattern and is written for the active target repository, not a repo-global path.
- Keep the existing `agents/<target-name>/logs/continuation/` JSON run log behavior unless this task explicitly adds the new markdown stop artifact as a complementary human-facing layer.

## Out of Scope
- Changing planner task generation heuristics or adding new MVP task inference logic.
- Implementing notifications, scheduling, or broader observability dashboards.
- Refactoring unrelated phase runners or changing reviewer/tester report formats.

## Acceptance Criteria
- When `scripts/run_cycle.py --auto-continue --dry-run` reaches the `planner-stopped-no-grounded-next-task` path, the console output includes the exact target-scoped stop artifact path that would be written under `agents/ai-automated-development/orchestrator/stop-reasons/`.
- When executed without `--dry-run` in a setup that triggers planner exhaustion, a markdown artifact is created under `agents/ai-automated-development/orchestrator/stop-reasons/` containing the stop reason `planner-stopped-no-grounded-next-task`, the target repository state, and a timestamp.
- Verification must use a command path that actually reaches planner exhaustion in the current runner, not only the default single-cycle stop path.
- `python -m py_compile scripts/run_cycle.py scripts/shared/artifact_paths.py` succeeds after the change.

## Dependencies
- None

## Notes
Generated by `scripts/run_planner.py` because the backlog was exhausted during an AI-backed MVP gap evaluation.
Grounding:
- `docs/mvp.md` requires that autonomous MVP stop reasons be written as visible artifacts for human follow-up, and `docs/agent-workflow.md` repeats that stop reasons must be written as visible target-scoped artifacts.
- Repository evidence shows `scripts/run_cycle.py` defines stop reasons including `planner-stopped-no-grounded-next-task`, but the current visible artifact path is still the JSON continuation log under `agents/<target-name>/logs/continuation/`, not a dedicated human-facing stop artifact under `agents/<target-name>/orchestrator/stop-reasons/`.
- The target-scoped analysis at `agents/ai-automated-development/analysis/repo-analysis.md` explicitly says future phases still need integration points and output contracts, which fits this missing orchestrator-to-human stop artifact contract.
Slug: `ai-auto-stop-artifact-no-task`

```

````
