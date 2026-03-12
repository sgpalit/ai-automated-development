# TASK-002 Agent Workflow Definition

## Status
done

## Priority
high

## Objective
Define a clear, repo-native workflow for AI agents (Codex) so they can consistently pick the next task, execute it, and update the backlog.

## Scope
- Create `docs/agent-workflow.md` describing:
  - how to select the “next task” (rule: priority, dependencies, then lowest task number)
  - how to mark tasks `in-progress` and `done`
  - how to keep changes small and avoid unrelated refactors
  - how to report output (summary + changed files + assumptions + follow-ups)
- Update `AGENTS.md` to reference `docs/agent-workflow.md` as the detailed source.
- Ensure the workflow explicitly allows **push directly to `main` until MVP** (already agreed).

## Out of Scope
- Slack integration
- backlog helper scripts
- OpenAPI tooling
- CI/CD pipelines

## Implementation Notes
Keep it simple and copy-paste friendly for Codex-in-browser usage.

## Acceptance Criteria
- `docs/agent-workflow.md` exists and is clear
- `AGENTS.md` points to it
- Task selection rule is explicit and deterministic

## Dependencies
- TASK-001
