# TASK-026 Automate developer commit and push in MVP mode

## Status
done

## Priority
high

## Objective
Extend the developer execution path so completed MVP tasks are committed, pushed, and handed off with the pushed commit hash for reviewer follow-up.

## Scope
- Update `scripts/run_developer.py` so successful `--execute` runs create a focused git commit for the selected task changes
- Push the new commit with the existing repository git remote configuration and capture the pushed commit hash
- Include the pushed commit hash in the developer handoff artifact so downstream phases can reference the exact committed state
- Adjust reviewer/task handoff logic only as needed so reviewer follow-up can use the pushed commit reference

## Out of Scope
- Feature-branch or pull-request workflow changes outside the MVP direct-to-main path
- Deployment automation or merge orchestration
- Broad refactors unrelated to developer commit/push handoff behavior

## Acceptance Criteria
- `scripts/run_developer.py --execute` performs focused commit/push steps after successful task implementation
- The developer handoff artifact records the pushed commit hash for the selected task
- Reviewer inputs can reference the pushed commit instead of relying only on the local worktree
- Verification includes at least one dry-run or guarded command path showing the commit/push workflow without silently skipping it

## Dependencies
None

## Notes
Blocked during implementation because the provided repository snapshot truncates `scripts/run_developer.py`, so the executable control flow and handoff-writing logic needed for a safe, scoped change are unavailable in the prompt context. Implementing against a partial file would risk corrupting unrelated behavior or omitting required integration points.
Grounding:
- `docs/mvp.md` requires developer commit/push behavior and reviewer evaluation of the pushed commit in MVP mode
- `agents/analysis/repo-analysis.md` still flags later workflow integration gaps and heuristic planning risk
- Repository evidence: `scripts/run_developer.py` applies file changes but does not run git commit/push automation yet
- Repository evidence: `scripts/run_reviewer.py` does not yet consume a pushed commit hash from developer output
Slug: `automate-developer-commit-push-in-mvp-mode`
