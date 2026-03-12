# TASK-012 Developer Agent Prompt

## Status
done

## Priority
high

## Objective
Create a Developer prompt that implements one approved backlog task at a time while preserving scope control and reporting consistency.

## Scope
- Add `prompts/agents/developer.md`.
- Define task selection and execution constraints for a single-task implementation cycle.
- Require status update behavior (`in-progress` to `done`) consistent with repo workflow.
- Define completion output format aligned with `docs/agent-handoff-contract.md`.

## Out of Scope
- Implementing reviewer or tester prompt content.
- Creating orchestration scripts.
- Performing backlog planning in this task.

## Implementation Notes
Reference existing repository rules in `AGENTS.md` and `docs/agent-workflow.md` to avoid conflicting guidance.

## Acceptance Criteria
- `prompts/agents/developer.md` exists and is scoped to implementation behavior.
- Prompt enforces one-task-at-a-time execution and minimal unrelated changes.
- Output/reporting format aligns with `docs/agent-handoff-contract.md`.

## Dependencies
- TASK-010
- TASK-002
