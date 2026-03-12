# TASK-009 Backlog Health Check Script

## Status
todo

## Priority
low

## Objective
Add a small helper script that performs basic backlog hygiene checks so contributors can catch obvious task-format issues quickly.

## Scope
- Add `scripts/check-backlog.sh`.
- Validate that task filenames follow `TASK-###-description.md`.
- Validate each task file includes required headings: Status, Priority, Objective, Scope, Out of Scope, Acceptance Criteria, Dependencies.
- Print actionable output and non-zero exit code on failures.

## Out of Scope
- Full markdown linting
- Dependency graph validation beyond basic presence checks
- CI integration

## Implementation Notes
Use POSIX shell + common utilities available by default.

## Acceptance Criteria
- `scripts/check-backlog.sh` exists and is executable.
- Script detects at least one intentional malformed task in a local manual check.
- Script exits successfully when backlog task files are valid.

## Dependencies
- TASK-008
