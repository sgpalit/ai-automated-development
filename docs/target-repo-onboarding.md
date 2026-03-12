# Target Repository Onboarding Runbook

Use this runbook to prepare a new repository for the multi-agent loop.

## Required Inputs

- Repository URL or local path
- Goal statement
- Constraints (time, tooling, compliance, scope limits)
- Success criteria (what "done" looks like)

## Preconditions

- Access to repository files
- Basic run/test instructions (if available)
- Human owner available for approvals

## Pre-Analysis Checklist

Based on `docs/target-repo-context.md`:

- [ ] Repository purpose and primary users are identified
- [ ] Current architecture and major components are known
- [ ] Operational constraints and non-goals are documented
- [ ] Quality baseline is understood (tests, docs, CI status)

## Steps

1. Capture goal + constraints + success criteria in session notes.
2. Run Analyst using `prompts/agents/analyst.md`.
3. Save analysis artifact to `analysis/repo-analysis.md`.
4. Run Planner using `prompts/agents/planner.md`.
5. Propose initial backlog batch in `backlog/tasks/`.
6. Human reviews and approves first implementation candidate.

## Expected First-Session Outputs

- `analysis/repo-analysis.md`
- Initial task batch: `backlog/tasks/TASK-XXX-*.md`
- Human-approved first task for implementation

## Related Docs

- `docs/workflow.md`
- `docs/running-the-system.md`
- `docs/target-repo-context.md`
