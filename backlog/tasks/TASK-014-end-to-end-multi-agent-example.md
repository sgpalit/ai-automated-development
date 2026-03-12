# TASK-014 End-to-End Multi-Agent Example Runbook

## Status
todo

## Priority
high

## Objective
Document one concrete end-to-end example showing the full multi-agent loop from analysis to human approval.

## Scope
- Add `docs/examples/multi-agent-loop.md`.
- Walk through a single sample cycle: Analyst → Planner → Human review → Developer → Reviewer → Tester → Human approval.
- Include expected artifacts at each step using the handoff contract format.
- Link the runbook from `README.md` and/or `docs/agents.md`.

## Out of Scope
- Building orchestration automation.
- Covering multiple branching workflow variants.
- Adding production deployment guidance.

## Implementation Notes
Use a realistic but lightweight scenario so the example is understandable in one read.

## Acceptance Criteria
- `docs/examples/multi-agent-loop.md` exists and covers the full loop end-to-end.
- The example references the agent prompt files used in the loop.
- Entry-point documentation links to the example for discoverability.

## Dependencies
- TASK-011
- TASK-012
- TASK-013
