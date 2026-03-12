# TASK-019 Agent Artifact Templates Library

## Status
done

## Priority
medium

## Objective
Add reusable templates for agent outputs so handoffs are faster, more consistent, and easier for humans to review.

## Scope
- Add `docs/templates/` with templates for Analyst, Planner, Developer, Reviewer, and Tester outputs.
- Ensure each template follows `docs/agent-handoff-contract.md` required sections.
- Add short usage notes explaining when each template should be copied.
- Link templates from `docs/agents.md` and/or `docs/workflow.md`.

## Out of Scope
- Building a template rendering CLI.
- Converting historical artifacts to the new templates.
- Defining role behavior beyond output structure.

## Implementation Notes
Templates should be minimal but complete, with placeholders that reduce free-form ambiguity in agent responses.

## Acceptance Criteria
- `docs/templates/` contains one template per core delivery agent role.
- Template sections are consistent with the handoff contract.
- Entry-point docs include links to the template library.

## Dependencies
- TASK-010
- TASK-011
- TASK-012
- TASK-013
- TASK-015
