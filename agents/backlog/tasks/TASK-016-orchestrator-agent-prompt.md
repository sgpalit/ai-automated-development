# TASK-016 Orchestrator Agent Prompt

## Status
done

## Priority
high

## Objective
Define an Orchestrator prompt that coordinates agent sequencing, enforces human approval points, and keeps the workflow controlled.

## Scope
- Add or update `prompts/agents/orchestrator.md`.
- Specify how the Orchestrator chooses the next agent based on workflow state and artifacts.
- Define stop/continue rules around human approval gates.
- Require structured orchestration outputs aligned with `docs/agent-handoff-contract.md`.

## Out of Scope
- Building autonomous orchestration services.
- Executing multiple agents automatically in one run.
- Adding CI/CD integration.

## Implementation Notes
Keep the prompt operational for manual Codex-driven sessions, with clear state-tracking expectations per iteration.

## Acceptance Criteria
- `prompts/agents/orchestrator.md` exists (or is updated) with explicit sequencing rules.
- The prompt includes human-gate checkpoints before implementation and before acceptance.
- Orchestrator outputs reference required artifacts from prior agents.

## Dependencies
- TASK-002
- TASK-010
