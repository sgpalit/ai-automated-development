# TASK-024 Generate the next MVP task when the backlog is empty

## Status
done

## Priority
high

## Objective
Make the local runner and planner continue the MVP loop when all existing backlog tasks are completed by generating one new implementation-ready backlog task from `docs/mvp.md` and the latest repository analysis instead of crashing.

## Scope
- Update the local planner/backlog selection flow so promptless runs detect when no eligible `todo` or `in-progress` task exists
- Generate exactly one new task file in `agents/backlog/tasks/` using `docs/mvp.md` and `agents/analysis/repo-analysis.md` as inputs
- Keep the generated task small, implementation-ready, and aligned with the next missing MVP slice
- If no task can be generated from the available MVP and analysis inputs, stop the runner cleanly with a clear operator-facing message
- Preserve the human-supervised workflow by stopping at task generation or clearly surfacing the new task for review before implementation continues

## Out of Scope
- Generating multiple new tasks in one pass
- Reopening completed tasks automatically
- Broad changes to the overall branch/review strategy
- Unrelated refactors to analyst, developer, reviewer, or tester behavior

## Implementation Notes
- Prefer reusing the existing planner/task template logic rather than introducing a second task format
- The empty-backlog path should fail gracefully if required inputs such as `docs/mvp.md` or `agents/analysis/repo-analysis.md` are missing
- Human control still matters: the new task should be easy to inspect and approve before autonomous implementation proceeds

## Acceptance Criteria
- Running `./run-agents.sh --dry-run` with no eligible backlog task does not raise `FileNotFoundError`
- The planner creates a new `TASK-024+` style backlog file in `agents/backlog/tasks/` when the backlog is exhausted
- The generated task includes `Status`, `Priority`, `Objective`, `Scope`, `Out of Scope`, `Acceptance Criteria`, and `Dependencies`
- The generated task is clearly grounded in `docs/mvp.md` and the latest analysis artifact rather than a generic placeholder
- Runner output explains which new task was created and that it requires human review before further implementation
- If no task is generated, runner output stops cleanly and explains why no next MVP task could be produced

## Dependencies
None
