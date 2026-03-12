# TASK-003 Codex CLI Quickstart

## Status
done

## Priority
high

## Objective
Replace the placeholder Codex CLI document with a practical quickstart so contributors can run a consistent local agent workflow.

## Scope
- Expand `docs/codex-cli.md` with:
  - prerequisites
  - setup steps
  - basic command examples for common repository tasks
  - troubleshooting notes for common local issues
- Keep instructions tool-agnostic enough to remain useful without deep platform lock-in.

## Out of Scope
- Installing or scripting Codex CLI automatically
- Adding CI/CD integration
- Covering advanced multi-agent orchestration

## Implementation Notes
Keep it concise, copy-paste friendly, and aligned with the backlog workflow already defined in `docs/agent-workflow.md`.

## Acceptance Criteria
- `docs/codex-cli.md` is no longer a placeholder
- A new contributor can follow the doc to run a basic local Codex session
- The guide references the backlog-driven workflow used in this repository

## Dependencies
- TASK-002
