# TASK-023 Developer workflow: require pushed task commit and reviewer commit-based review

## Status
done

## Priority
high

## Objective
Update the documented developer and reviewer workflow so each implementation cycle requires the developer agent to commit and push the completed task changes before handoff, and requires the reviewer to review the exact pushed commit identified by the developer.

## Scope
- Update agent-facing workflow documentation to require developers to create a focused task commit and push it before reviewer handoff
- Update role documentation so reviewer expectations explicitly reference the developer-provided pushed commit hash
- Update human approval guidance to confirm review is performed against the pushed commit rather than an uncommitted local working tree
- Keep the change limited to workflow and prompt documentation for the existing multi-agent loop

## Out of Scope
- Changing repository automation or Git hooks
- Implementing enforcement scripts for commit or push behavior
- Introducing broader workflow refactors outside the developer/reviewer handoff expectation

## Acceptance Criteria
- `AGENTS.md` states that developer agents must verify, commit, push, and report the pushed commit hash before review
- `prompts/agents/developer.md` requires a focused commit, push, and inclusion of the pushed commit hash in the developer handoff
- `docs/agents.md` states that reviewers verify the developer's pushed commit rather than an uncommitted working tree
- `docs/human-approval-checklists.md` includes checklist items confirming the pushed commit hash is provided and reviewed
- Dependencies remain explicitly listed and correct for this documentation-only workflow change

## Dependencies
- None

## Notes
Derived from `agents/analysis/repo-analysis.md` analyst findings for the multi-agent MVP workflow.
Slug: `developer-agent-schould-commit-and-push`
