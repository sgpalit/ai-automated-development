# TASK-011 Analyst Agent Prompt

## Status
done

## Priority
high

## Objective
Add an Analyst prompt that produces repository analysis outputs tailored for backlog planning and the multi-agent handoff contract.

## Scope
- Add `prompts/agents/analyst.md`.
- Define analyst responsibilities, constraints, and expected analysis depth.
- Require output sections aligned with `docs/agent-handoff-contract.md`.
- Include a short example output skeleton for consistency.

## Out of Scope
- Implementing planner, developer, reviewer, or tester prompts.
- Running or validating a full end-to-end workflow.

## Implementation Notes
Prioritize practical repository insights that directly inform backlog task creation.

## Acceptance Criteria
- `prompts/agents/analyst.md` exists with clear, implementation-ready instructions.
- Prompt output format aligns with `docs/agent-handoff-contract.md`.
- The prompt explicitly avoids implementation and focuses on analysis deliverables.

## Dependencies
- TASK-010
