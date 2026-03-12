# Developer Implementation Prompt

## Date
2026-03-13

## Selected Task
- Code: `TASK-036`
- File: `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md`
- Goal: Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task.

## Implementation Objective
Make the developer commit/push workflow produce a reviewable pushed task state that includes the final task status and any required developer artifacts, so reviewer inspection is grounded in a coherent pushed snapshot rather than a mix of pushed code and local-only artifacts.

## Exact Files Likely To Change
- `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md`
- `scripts/run_developer.py`
- `scripts/run_reviewer.py`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Switching to feature branches or pull requests.
- Out of scope: Changing analyst artifact handling.
- Out of scope: Reworking tester logic beyond consuming the consistent pushed/developer-review state.

## Exact Acceptance Criteria
- After a successful developer execution, the pushed commit contains the final task file marked `done` and the developer artifacts required for reviewer follow-up.
- Reviewer follow-up can inspect the pushed commit and find the expected task-completion artifacts in committed repository state rather than relying on a local-only handoff write after push.
- `python -m py_compile scripts/run_developer.py scripts/run_reviewer.py` succeeds after the change.

## Step-by-Step Implementation Plan
1. Review `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md` and confirm the task is still in scope.
2. Update `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_developer.py`, `scripts/run_reviewer.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md` to `done` only after the acceptance criteria are met.
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
Selected task file: `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md`

Files likely to change:
- `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md`
- `scripts/run_developer.py`
- `scripts/run_reviewer.py`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Switching to feature branches or pull requests.
- Out of scope: Changing analyst artifact handling.
- Out of scope: Reworking tester logic beyond consuming the consistent pushed/developer-review state.

Acceptance criteria:
- After a successful developer execution, the pushed commit contains the final task file marked `done` and the developer artifacts required for reviewer follow-up.
- Reviewer follow-up can inspect the pushed commit and find the expected task-completion artifacts in committed repository state rather than relying on a local-only handoff write after push.
- `python -m py_compile scripts/run_developer.py scripts/run_reviewer.py` succeeds after the change.

Implementation plan:
1. Review `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md` and confirm the task is still in scope.
2. Update `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_developer.py`, `scripts/run_reviewer.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/ai-automated-development/backlog/tasks/TASK-036-include-review-artifacts-in-pushed-task-state.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-036 Include review-relevant artifacts in pushed task state

## Status
todo

## Priority
high

## Objective
Make the developer commit/push workflow produce a reviewable pushed task state that includes the final task status and any required developer artifacts, so reviewer inspection is grounded in a coherent pushed snapshot rather than a mix of pushed code and local-only artifacts.

## Scope
- Update `scripts/run_developer.py` commit ordering so the pushed commit contains the final task file plus the review-relevant developer artifacts needed for downstream review.
- If the pushed commit hash must appear inside a committed artifact, use a deterministic finalization strategy such as a second local rewrite plus amend/recommit before push.
- Keep the workflow focused on the existing MVP direct-to-main model and the current target-scoped artifact layout.
- Ensure the resulting pushed state stays consistent with reviewer consumption in `scripts/run_reviewer.py`.

## Out of Scope
- Switching to feature branches or pull requests.
- Changing analyst artifact handling.
- Reworking tester logic beyond consuming the consistent pushed/developer-review state.

## Implementation Notes
- Exact existing files that should change:
  - `scripts/run_developer.py`
  - `scripts/run_reviewer.py` only if needed for the updated artifact expectation
- The final design should avoid leaving the committed task state and the local developer handoff out of sync.
- Keep the commit history focused; do not introduce unrelated workflow refactors.

## Acceptance Criteria
- After a successful developer execution, the pushed commit contains the final task file marked `done` and the developer artifacts required for reviewer follow-up.
- Reviewer follow-up can inspect the pushed commit and find the expected task-completion artifacts in committed repository state rather than relying on a local-only handoff write after push.
- `python -m py_compile scripts/run_developer.py scripts/run_reviewer.py` succeeds after the change.

## Dependencies
None

## Notes
Generated from a manual workflow audit after the developer push flow was observed to write the final handoff after commit/push, leaving review-relevant artifacts outside the pushed task snapshot.
Grounding:
- `scripts/run_developer.py` currently creates the git commit before writing the final developer handoff, so the pushed commit and the latest local handoff can diverge.
- `docs/mvp.md` requires reviewer decisions to be grounded in the pushed task result and recorded developer verification evidence.

```

````
