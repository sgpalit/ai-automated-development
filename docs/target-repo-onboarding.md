# Target Repository Onboarding Runbook

Use this runbook to prepare a new repository for the multi-agent loop.

## Required Inputs

Collect these before starting analysis:

- Repository URL or local path
- Goal statement
- Constraints:
  - time or deadline limits
  - tooling limits
  - compliance or policy requirements
  - explicit scope boundaries
- Success criteria:
  - desired outcome
  - quality bar
  - expected deliverables
- Approval contact or human owner
- Available run/test/build instructions, if any

## Preconditions

- Access to repository files
- Ability to inspect documentation and configuration files
- Human owner available for approvals
- A place to store onboarding notes and analysis artifacts

## First-Session Checklist

Before planning begins, confirm the following:

### Intake
- [ ] Goal, constraints, and success criteria are written down
- [ ] Repository path or URL is confirmed
- [ ] Human owner and approval expectations are known
- [ ] The operating expectation for implementation cycles is known: developer completes verification, commits and pushes the task work, and reviewer checks that pushed commit

### Repository Understanding
Based on `docs/target-repo-context.md`:

- [ ] Repository purpose and primary users are identified
- [ ] Current architecture and major components are known
- [ ] Technology stack and tooling are identified
- [ ] Operational constraints and non-goals are documented
- [ ] Quality baseline is understood:
  - tests
  - docs
  - CI status
  - lint/format tooling
- [ ] Key risks or documentation gaps are captured

### Analysis Readiness
- [ ] Enough repository evidence has been collected to produce `agents/analysis/repo-analysis.md`
- [ ] Improvement opportunities are specific enough to turn into backlog tasks
- [ ] The first implementation slice looks small enough for a single cycle

## Recommended First-Session Flow

1. Capture the goal, constraints, success criteria, and approval contact in session notes.
2. Review primary repository docs:
   - `README.md`
   - `docs/`
   - contribution or setup guides
3. Inspect repository structure and key configuration files.
4. Confirm the implementation-cycle workflow for this repository: developer verifies changes, creates a focused commit, pushes it, and hands off the commit reference for review.
5. Run Analyst using `prompts/agents/analyst.md`.
6. Save the analysis artifact to `agents/analysis/repo-analysis.md`.
7. Confirm the analysis includes repository purpose, stack, architecture, conventions, quality signals, risks, and improvement opportunities.
8. Run Planner using `prompts/agents/planner.md`.
9. Propose an initial backlog batch in `agents/backlog/tasks/`.
10. Human reviews and approves the first implementation candidate.

## Expected Output Artifacts Before Planning

The following should exist or be captured before planning starts:

- Session notes containing:
  - goal
  - constraints
  - success criteria
  - approvals/contact
  - implementation-cycle expectations, including developer commit/push and reviewer commit verification
- `agents/analysis/repo-analysis.md` containing:
  - repository overview
  - technology stack
  - architecture summary
  - key components
  - conventions
  - quality signals
  - risks and gaps
  - improvement opportunities
- Enough repository evidence to justify the proposed backlog tasks

## Expected First-Session Outputs

- `agents/analysis/repo-analysis.md`
- Initial task batch: `agents/backlog/tasks/TASK-XXX-*.md`
- Human-approved first task for implementation

## Related Docs

- `docs/workflow.md`
- `docs/running-the-system.md`
- `docs/target-repo-context.md`
