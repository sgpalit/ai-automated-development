# Developer Implementation Prompt

## Date
2026-03-13

## Selected Task
- Code: `TASK-033`
- File: `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md`
- Goal: Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task.

## Implementation Objective
Make the reviewer phase verify the developer's pushed commit hash with local git evidence and refuse approval-ready review results when the pushed commit is missing, malformed, or not inspectable, so reviewer decisions are grounded in the pushed task result as required by the MVP.

## Exact Files Likely To Change
- `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md`
- `scripts/run_reviewer.py`

## Exact Constraints
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Changing developer commit/push behavior in `scripts/run_developer.py`.
- Out of scope: Expanding reviewer into a full semantic code-review engine beyond pushed-commit evidence enforcement.
- Out of scope: Changing tester outcome handling or orchestrator continuation policy outside what reviewer evidence strictly needs.

## Exact Acceptance Criteria
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff has no usable `Pushed commit hash:` line produces a reviewer report that explicitly states pushed-commit evidence is missing and does not return an approval-ready decision.
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff contains a non-existent commit hash produces a reviewer report that explicitly states the pushed commit could not be inspected in the target repository.
- When the developer handoff contains a valid local commit hash, the reviewer report includes that exact hash and states that review findings were grounded in inspecting the commit rather than only the local worktree/task artifacts.
- `python -m py_compile scripts/run_reviewer.py` succeeds after the change.

## Step-by-Step Implementation Plan
1. Review `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md` and confirm the task is still in scope.
2. Update `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_reviewer.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md` to `done` only after the acceptance criteria are met.
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
Selected task file: `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md`

Files likely to change:
- `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md`
- `scripts/run_reviewer.py`

Constraints:
- Implement exactly one approved backlog task in a focused change set.
- Keep changes scoped to the selected task `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md`.
- Avoid unrelated refactors.
- Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
- If blocked, set the task status to `blocked` and explain why.
- Out of scope: Changing developer commit/push behavior in `scripts/run_developer.py`.
- Out of scope: Expanding reviewer into a full semantic code-review engine beyond pushed-commit evidence enforcement.
- Out of scope: Changing tester outcome handling or orchestrator continuation policy outside what reviewer evidence strictly needs.

Acceptance criteria:
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff has no usable `Pushed commit hash:` line produces a reviewer report that explicitly states pushed-commit evidence is missing and does not return an approval-ready decision.
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff contains a non-existent commit hash produces a reviewer report that explicitly states the pushed commit could not be inspected in the target repository.
- When the developer handoff contains a valid local commit hash, the reviewer report includes that exact hash and states that review findings were grounded in inspecting the commit rather than only the local worktree/task artifacts.
- `python -m py_compile scripts/run_reviewer.py` succeeds after the change.

Implementation plan:
1. Review `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md` and confirm the task is still in scope.
2. Update `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md` status from `todo` to `in-progress` before making changes.
3. Apply the required repository changes in `scripts/run_reviewer.py`.
4. Run the smallest relevant verification commands for the changed files.
5. Update `agents/ai-automated-development/backlog/tasks/TASK-033-reviewer-pushed-commit-verification.md` to `done` only after the acceptance criteria are met.
6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.

Selected task content:
```md
# TASK-033 Implement reviewer pushed-commit verification

## Status
todo

## Priority
high

## Objective
Make the reviewer phase verify the developer's pushed commit hash with local git evidence and refuse approval-ready review results when the pushed commit is missing, malformed, or not inspectable, so reviewer decisions are grounded in the pushed task result as required by the MVP.

## Scope
- Update `scripts/run_reviewer.py` to require and parse the pushed commit hash from the developer handoff and include explicit findings about pushed-commit availability in the reviewer report.
- Add focused git inspection logic in `scripts/run_reviewer.py` or a small helper under `scripts/shared/` only if needed, using the selected target repository path from the current runner contract.
- Keep reviewer outputs on the existing target-scoped artifact path under `agents/<target-name>/review/reviewer/` via the current artifact path helpers.
- Update reviewer decision logic so missing or uninspectable pushed commits cannot result in an approval-ready review outcome.

## Out of Scope
- Changing developer commit/push behavior in `scripts/run_developer.py`.
- Expanding reviewer into a full semantic code-review engine beyond pushed-commit evidence enforcement.
- Changing tester outcome handling or orchestrator continuation policy outside what reviewer evidence strictly needs.

## Implementation Notes
- Exact existing files that should change:
  - `scripts/run_reviewer.py`
- If a helper is added, keep it under `scripts/shared/` and reuse the current target repository path/target name contracts instead of inventing a new config surface.
- Keep the reviewer artifact format aligned with `docs/agent-handoff-contract.md`.

## Acceptance Criteria
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff has no usable `Pushed commit hash:` line produces a reviewer report that explicitly states pushed-commit evidence is missing and does not return an approval-ready decision.
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff contains a non-existent commit hash produces a reviewer report that explicitly states the pushed commit could not be inspected in the target repository.
- When the developer handoff contains a valid local commit hash, the reviewer report includes that exact hash and states that review findings were grounded in inspecting the commit rather than only the local worktree/task artifacts.
- `python -m py_compile scripts/run_reviewer.py` succeeds after the change.

## Dependencies
None

## Notes
Generated from a manual MVP gap audit after the planner stopped cleanly without deriving another grounded task.
Grounding:
- `docs/mvp.md` requires that reviewer decisions are grounded in the pushed task result and the recorded developer verification evidence.
- `scripts/run_reviewer.py` currently extracts `Pushed commit hash:` text but does not verify that the commit exists or is inspectable in the target repository.
- `docs/mvp-readiness-checklist.md` still marks reviewer/tester/orchestrator evidence handling as only partially standardized end to end.

```

````
