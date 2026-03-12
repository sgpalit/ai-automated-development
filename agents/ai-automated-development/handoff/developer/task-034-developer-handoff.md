# Developer Handoff

## Goal
Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task.

## Date
2026-03-13

## Repository Path
`/home/sp/workspace/github/ai-automated-development`

## Selected Task Code
`TASK-034`

## Source Task File Path
`agents/ai-automated-development/backlog/tasks/TASK-034-align-running-guide-with-target-scoped-workflow.md`

## Objective
Update the main running guide so it matches the current target-scoped artifact layout, reviewer/tester paths, and MVP auto-continue behavior, reducing operator confusion and keeping the documented workflow aligned with the actual runner.

## Required Inputs
- `agents/ai-automated-development/backlog/tasks/TASK-034-align-running-guide-with-target-scoped-workflow.md`
- `agents/ai-automated-development/analysis/repo-analysis.md`
- `AGENTS.md`
- `docs/agent-workflow.md`
- `docs/agent-handoff-contract.md`

## Implementation Rules
- Implement exactly one approved backlog task in a focused change set.
- Set the selected task status to `in-progress` before implementation.
- Implement only in-scope changes required by the task.
- Keep unrelated refactors out of scope.
- Run relevant checks before completion.
- Set task status to `done` when acceptance criteria are met, or `blocked` if work cannot proceed.

## Expected Output
- A small, working repository change set that implements the selected task.
- The selected backlog task updated through the required status transitions.
- A developer handoff/report aligned with `docs/agent-handoff-contract.md` and ready for reviewer follow-up.
- Pushed commit hash for reviewer reference: `94e6ec83f043224366eb718768c606194022243d`

## Commit Reference
- Pushed commit hash: `94e6ec83f043224366eb718768c606194022243d`
- Reviewer should inspect the pushed commit referenced below, not only the local worktree.

## Full Task Content
```md
# TASK-034 Align running guide with target-scoped workflow

## Status
done

## Priority
medium

## Objective
Update the main running guide so it matches the current target-scoped artifact layout, reviewer/tester paths, and MVP auto-continue behavior, reducing operator confusion and keeping the documented workflow aligned with the actual runner.

## Scope
- Update `docs/running-the-system.md` to use the current target-scoped artifact paths under `agents/<target-name>/...`.
- Correct stale developer, reviewer, and tester artifact references so they match the current helpers in `scripts/shared/artifact_paths.py`.
- Align the running guide with the current runner behavior for `./run-agents.sh`, `--dry-run`, `--execute`, and `MVP` auto-continue wording.
- Keep the change documentation-focused and limited to the main running guide unless one directly linked line in another doc must be adjusted for consistency.

## Out of Scope
- Changing runner code in `scripts/`.
- Redesigning the workflow or artifact model.
- Broad documentation cleanup beyond the main running guide and one directly necessary consistency fix if required.

## Implementation Notes
- Exact existing file that should change:
  - `docs/running-the-system.md`
- Use the current target-scoped artifact model as the source of truth:
  - `agents/<target-name>/analysis/`
  - `agents/<target-name>/backlog/tasks/`
  - `agents/<target-name>/handoff/developer/`
  - `agents/<target-name>/implementation/developer/`
  - `agents/<target-name>/review/reviewer/`
  - `agents/<target-name>/test/`
  - `agents/<target-name>/orchestrator/stop-reasons/`

## Acceptance Criteria
- `docs/running-the-system.md` no longer references stale paths like `agents/handoff/...`, `agents/implementation/...`, `agents/review/...`, or `agents/test/...` without the active target name segment.
- The guide describes the current wrapper behavior for `./run-agents.sh`, `./run-agents.sh --dry-run`, and the distinction between supervised runs and `MVP` auto-continue.
- Reviewer and tester output examples in the guide match the current target-scoped artifact paths and terminology.
- `rg -n "agents/(handoff|implementation|review|test)/" docs/running-the-system.md` returns no matches.

## Dependencies
None

## Notes
Generated from a manual MVP gap audit after the planner stopped cleanly without deriving another grounded task.
Grounding:
- `docs/mvp-readiness-checklist.md` still marks docs/scripts alignment to the target-scoped artifact model and state-aware auto-continue behavior as partial.
- `docs/running-the-system.md` still contains stale artifact paths and older supervised-flow wording that no longer matches the current runner and target-scoped artifact helpers.

```
