# TASK-022 Document post-implementation commit/push and reviewer commit verification workflow

## Status
done

## Priority
high

## Objective
Define a single implementation-ready workflow update that requires the developer agent to commit and push its completed work before handoff, and requires the reviewer to verify the review against that pushed commit.

## Scope
- Update the developer instructions so task completion explicitly includes:
  - creating a small focused commit after verification passes
  - pushing the commit to the active branch before handoff
  - reporting the commit hash in the developer handoff
- Update human/operator documentation so repository supervisors know that reviewer approval should reference the developer's pushed commit
- Update onboarding/checklist documentation to make commit/push and reviewer commit verification part of the expected operating procedure for this repository

## Out of Scope
- Enforcing commits or pushes through automation or hooks
- Changing branch strategy beyond documenting the expected MVP behavior
- Introducing unrelated workflow refactors
- Implementing reviewer-side prompt changes beyond the minimum documentation needed to make the workflow executable

## Acceptance Criteria
- `prompts/agents/developer.md` explicitly instructs the developer agent to commit and push after successful verification and to include the pushed commit hash in its handoff
- `AGENTS.md` states that, during the current MVP workflow, the developer should commit and push completed task changes before reviewer handoff and that review should be performed against that commit
- `docs/human-approval-checklists.md` includes checklist items requiring confirmation that the developer shared a pushed commit reference and that review/approval is tied to that commit
- `docs/target-repo-onboarding.md` mentions the commit/push expectation and reviewer verification of the pushed commit as part of onboarding or first-session operating expectations
- Documentation changes remain limited to the workflow update described in this task

## Dependencies
- None

## Notes
Generated from planner output and refined into an implementation-ready documentation task.
Slug: `developer-schould-commit-and-push-after`
