# TASK-013 Reviewer and Tester Agent Prompts

## Status
done

## Priority
high

## Objective
Add dedicated Reviewer and Tester prompts so quality review and acceptance validation are explicit roles in the MVP loop.

## Scope
- Add `prompts/agents/reviewer.md` and `prompts/agents/tester.md`.
- Define reviewer checks for scope adherence, code quality risks, and correction requests.
- Define tester checks for acceptance criteria validation and regression risk reporting.
- Standardize both outputs using `docs/agent-handoff-contract.md`.

## Out of Scope
- Implementing CI pipelines or automated test harnesses.
- Editing backlog tasks during review/testing.

## Implementation Notes
Keep prompts concise and operational so they are usable in a single Codex session.

## Acceptance Criteria
- `prompts/agents/reviewer.md` and `prompts/agents/tester.md` exist.
- Each prompt has clear pass/fail decision guidance.
- Both prompts produce outputs aligned with `docs/agent-handoff-contract.md`.

## Dependencies
- TASK-010
