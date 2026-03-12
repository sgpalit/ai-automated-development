# TASK-036 Include review-relevant artifacts in pushed task state

## Status
done

## Priority
high

## Objective
Make the developer commit/push workflow produce a reviewable pushed task state that includes the final task status and any required developer artifacts, so reviewer inspection is grounded in a coherent pushed snapshot rather than a mix of pushed code and local-only artifacts.

## Scope
- Update `scripts/run_developer.py` commit ordering so the pushed commit contains the final task file plus the review-relevant developer artifacts needed for downstream review.
- If the pushed commit hash must appear inside a committed artifact, use a deterministic finalization strategy such as a second local rewrite plus amend/recommit before push.
- Keep the workflow focused on the existing MVP direct-to-main model and the current target-scoped artifact layout.
- Ensure the resulting pushed state stays consistent with reviewer consumption in `scripts/run_reviewer.py`.

## Out of Scope
- Switching to feature branches or pull requests.
- Changing analyst artifact handling.
- Reworking tester logic beyond consuming the consistent pushed/developer-review state.

## Implementation Notes
- Exact existing files that should change:
  - `scripts/run_developer.py`
  - `scripts/run_reviewer.py` only if needed for the updated artifact expectation
- The final design should avoid leaving the committed task state and the local developer handoff out of sync.
- Keep the commit history focused; do not introduce unrelated workflow refactors.

## Acceptance Criteria
- After a successful developer execution, the pushed commit contains the final task file marked `done` and the developer artifacts required for reviewer follow-up.
- Reviewer follow-up can inspect the pushed commit and find the expected task-completion artifacts in committed repository state rather than relying on a local-only handoff write after push.
- `python -m py_compile scripts/run_developer.py scripts/run_reviewer.py` succeeds after the change.

## Dependencies
None

## Notes
Generated from a manual workflow audit after the developer push flow was observed to write the final handoff after commit/push, leaving review-relevant artifacts outside the pushed task snapshot.
Grounding:
- `scripts/run_developer.py` currently creates the git commit before writing the final developer handoff, so the pushed commit and the latest local handoff can diverge.
- `docs/mvp.md` requires reviewer decisions to be grounded in the pushed task result and recorded developer verification evidence.
