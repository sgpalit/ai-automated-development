# TASK-018 Target Repository Onboarding Runbook

## Status
done

## Priority
high

## Objective
Create a step-by-step runbook for onboarding a new target repository so teams can start the multi-agent loop quickly and consistently.

## Scope
- Add `docs/target-repo-onboarding.md`.
- Define required inputs: repository URL/path, goal statement, constraints, and success criteria.
- Provide a pre-analysis checklist based on `docs/target-repo-context.md`.
- Include expected first-session outputs: analysis file location and initial backlog task batch.

## Out of Scope
- Building automation for repository cloning or environment setup.
- Supporting advanced multi-repo orchestration.
- Implementing target-repository-specific custom prompts.

## Implementation Notes
Optimize for first-time users who need a reliable setup flow before running Analyst and Planner prompts.

## Acceptance Criteria
- `docs/target-repo-onboarding.md` exists with clear preconditions, steps, and outputs.
- The runbook references existing docs for workflow and target-repo context.
- A user can follow the document to produce an initial analysis artifact and task proposal set.

## Dependencies
- TASK-011
- TASK-015
