# TASK-021 Improve onboarding documentation with a concrete repo intake checklist

## Status
done

## Priority
high

## Objective
Make repository onboarding more actionable by adding a concrete intake checklist and required analysis outputs so an agent or human can prepare a new target repository consistently in a single session.

## Scope
- Update `docs/target-repo-onboarding.md` with a step-by-step first-session onboarding flow
- Expand `docs/target-repo-context.md` with a concrete repository intake checklist and expected evidence to collect
- Align `scripts/run_analyst.py` output so the generated `analysis/repo-analysis.md` references the onboarding/context expectations

## Out of Scope
- Changes to planner, developer, reviewer, or tester prompts beyond what is required for analyst/onboarding alignment
- New automation for repository setup
- Broad workflow refactors or process redesign

## Acceptance Criteria
- `docs/target-repo-onboarding.md` includes:
  - required inputs for onboarding
  - a first-session checklist
  - explicit output artifacts expected before planning begins
- `docs/target-repo-context.md` includes:
  - a concrete checklist covering repository purpose, stack, structure, architecture, conventions, quality signals, and risks
  - clear guidance on what evidence the analyst should capture
- `scripts/run_analyst.py` generated markdown includes:
  - a reference to onboarding/context-driven analysis expectations
  - a repository snapshot section that supports the new documentation
- Verification:
  - `python scripts/run_analyst.py "Improve onboarding documentation" --dry-run`
  - review generated dry-run output for the updated analysis structure

## Dependencies
- `analysis/repo-analysis.md` as the planning reference for this documentation improvement slice
- Existing onboarding docs:
  - `docs/target-repo-onboarding.md`
  - `docs/target-repo-context.md`

## Notes
This task converts the planner follow-up placeholder into a single executable documentation slice focused on onboarding clarity.
Slug: `improve-onboarding-documentation`
