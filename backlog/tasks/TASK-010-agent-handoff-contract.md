# TASK-010 Agent Handoff Contract Specification

## Status
done

## Priority
high

## Objective
Define a single, reusable handoff contract so all agents exchange work in a consistent format across the multi-agent loop.

## Scope
- Add `docs/agent-handoff-contract.md`.
- Define required sections for agent-to-agent outputs (context, decisions, artifacts, open questions, recommended next step).
- Include a minimal Markdown template that Analyst, Planner, Developer, Reviewer, and Tester can reuse.
- Link the contract from `docs/agents.md`.

## Out of Scope
- Rewriting all existing docs to the new format.
- Building automation to enforce the contract.
- Implementing any agent prompts in this task.

## Implementation Notes
Keep the contract short and practical so it can be copied directly into prompt outputs.

## Acceptance Criteria
- `docs/agent-handoff-contract.md` exists and defines a concrete handoff format.
- The format includes required fields that reduce ambiguity in agent transitions.
- `docs/agents.md` references the new handoff contract.

## Dependencies
- TASK-002
