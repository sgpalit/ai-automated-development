# AI Automated Development

AI Automated Development is an open-source foundation for structured, backlog-driven, AI-assisted software delivery.

## Goals

- Provide a practical multi-agent workflow
- Keep humans in control at key approval gates
- Use local backlog tasks as the source of truth
- Make implementation loops repeatable and auditable

## Repository Structure

- `backlog/` — backlog process docs, task checklist, and task files
- `docs/` — workflow, agent contracts, runbooks, and templates
- `prompts/` — reusable prompts for each agent role
- `scripts/` — helper scripts for local workflow checks
- `agents/` — reserved area for agent-related supporting assets
- `examples/` — example walkthroughs and scenario artifacts

## Usage Quickstart

1. Review project operating rules and workflow docs:
   - `AGENTS.md`
   - `docs/agent-workflow.md`
   - `docs/contributing.md`
   - `docs/codex-cli.md`
2. List backlog tasks and inspect current statuses:
   - `rg "^# TASK-|^## Status|^## Priority" backlog/tasks/TASK-*.md`
3. Pick the next eligible task (todo + highest priority + dependencies done):
   - `python scripts/select-next-task.py` *(if you add your own selector)*
   - or manual review using `backlog/tasks/`
4. Validate backlog/task format and run local checks:
   - `./scripts/check-backlog.sh`
5. Implement one approved task, then update task status (`in-progress` → `done`) with a concise summary.
6. Continue the loop using `docs/workflow.md` and the end-to-end example in `docs/examples/multi-agent-loop.md`.

## Key References

- Workflow: `docs/workflow.md`
- Agent roles: `docs/agents.md`
- Agent handoff contract: `docs/agent-handoff-contract.md`
- Human approval checklists: `docs/human-approval-checklists.md`
- Target repo onboarding: `docs/target-repo-onboarding.md`
- MVP definition: `docs/mvp.md`
- MVP readiness checklist: `docs/mvp-readiness-checklist.md`

## License

This project is licensed under the **MIT License**.
