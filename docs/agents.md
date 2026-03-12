# Agent Roles

This document defines role boundaries for the multi-agent workflow.

## Roles

- Orchestrator
- Analyst
- Planner
- Developer
- Reviewer
- Tester
- Human Approver

## Shared Handoff Standard

All role outputs must use the required format in `docs/agent-handoff-contract.md`.

Reusable role-specific output templates are available in `docs/templates/`.

## Role Summaries

### Orchestrator
- Chooses next agent based on workflow state and available artifacts
- Enforces human approval gates before implementation and final acceptance

### Analyst
- Analyzes repository context, risks, and opportunities
- Produces planning-ready insights

### Planner
- Creates or refines small, implementation-ready backlog tasks
- Maintains dependency correctness and priority ordering

### Developer
- Implements one approved task at a time
- Keeps changes focused and updates task status flow

### Reviewer
- Verifies scope compliance and quality risks
- Returns clear decision: `APPROVED` or `CHANGES REQUIRED`

### Tester
- Verifies acceptance criteria and regression risk
- Returns clear decision: `PASSED` or `FAILED`

### Human Approver
- Approves goals, backlog changes, implementation acceptance, and loop continuation

## Related Documentation

- Workflow: `docs/workflow.md`
- Running guide: `docs/running-the-system.md`
- Human approval checklists: `docs/human-approval-checklists.md`
- Example loop runbook: `docs/examples/multi-agent-loop.md`
