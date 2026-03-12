# TASK-017 Human Approval Checklists

## Status
done

## Priority
medium

## Objective
Provide practical human review checklists so approval decisions are consistent at backlog, implementation, and release-loop checkpoints.

## Scope
- Add `docs/human-approval-checklists.md`.
- Define separate checklists for: task approval, implementation acceptance, and loop continuation.
- Include required evidence per checkpoint (analysis summary, task file, review result, tester result).
- Link the checklists from `docs/workflow.md` and `docs/running-the-system.md`.

## Out of Scope
- Policy or compliance frameworks for enterprise governance.
- Automating checklist enforcement.
- Replacing existing workflow documentation.

## Implementation Notes
Keep each checklist short enough to use during a live session while still preventing ambiguous approvals.

## Acceptance Criteria
- `docs/human-approval-checklists.md` exists with at least three workflow-stage checklists.
- Documentation links from workflow entry points make the checklists discoverable.
- Checklist items clearly map to artifacts produced by agent roles.

## Dependencies
- TASK-014
