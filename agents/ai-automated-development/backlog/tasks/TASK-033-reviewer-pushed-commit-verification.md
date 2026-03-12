# TASK-033 Implement reviewer pushed-commit verification

## Status
done

## Priority
high

## Objective
Make the reviewer phase verify the developer's pushed commit hash with local git evidence and refuse approval-ready review results when the pushed commit is missing, malformed, or not inspectable, so reviewer decisions are grounded in the pushed task result as required by the MVP.

## Scope
- Update `scripts/run_reviewer.py` to require and parse the pushed commit hash from the developer handoff and include explicit findings about pushed-commit availability in the reviewer report.
- Add focused git inspection logic in `scripts/run_reviewer.py` or a small helper under `scripts/shared/` only if needed, using the selected target repository path from the current runner contract.
- Keep reviewer outputs on the existing target-scoped artifact path under `agents/<target-name>/review/reviewer/` via the current artifact path helpers.
- Update reviewer decision logic so missing or uninspectable pushed commits cannot result in an approval-ready review outcome.

## Out of Scope
- Changing developer commit/push behavior in `scripts/run_developer.py`.
- Expanding reviewer into a full semantic code-review engine beyond pushed-commit evidence enforcement.
- Changing tester outcome handling or orchestrator continuation policy outside what reviewer evidence strictly needs.

## Implementation Notes
- Exact existing files that should change:
  - `scripts/run_reviewer.py`
- If a helper is added, keep it under `scripts/shared/` and reuse the current target repository path/target name contracts instead of inventing a new config surface.
- Keep the reviewer artifact format aligned with `docs/agent-handoff-contract.md`.

## Acceptance Criteria
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff has no usable `Pushed commit hash:` line produces a reviewer report that explicitly states pushed-commit evidence is missing and does not return an approval-ready decision.
- Running `python scripts/run_reviewer.py --repo . --dry-run` for a task whose developer handoff contains a non-existent commit hash produces a reviewer report that explicitly states the pushed commit could not be inspected in the target repository.
- When the developer handoff contains a valid local commit hash, the reviewer report includes that exact hash and states that review findings were grounded in inspecting the commit rather than only the local worktree/task artifacts.
- `python -m py_compile scripts/run_reviewer.py` succeeds after the change.

## Dependencies
None

## Notes
Generated from a manual MVP gap audit after the planner stopped cleanly without deriving another grounded task.
Grounding:
- `docs/mvp.md` requires that reviewer decisions are grounded in the pushed task result and the recorded developer verification evidence.
- `scripts/run_reviewer.py` currently extracts `Pushed commit hash:` text but does not verify that the commit exists or is inspectable in the target repository.
- `docs/mvp-readiness-checklist.md` still marks reviewer/tester/orchestrator evidence handling as only partially standardized end to end.
