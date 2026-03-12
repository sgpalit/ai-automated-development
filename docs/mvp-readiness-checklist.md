# MVP Readiness Checklist and Gap Report

This checklist maps to `docs/mvp.md` and helps humans decide whether MVP is usable.

Status scale: `done` / `partial` / `missing`.

## Criteria Mapping

| MVP Criterion (`docs/mvp.md`) | Status | Evidence |
|---|---|---|
| Clear agent instructions | done | `docs/agents.md`, `prompts/agents/*.md` |
| Local backlog workflow | done | `backlog/README.md`, `backlog/tasks/` |
| Practical Codex usage docs | done | `docs/codex-cli.md`, `docs/running-the-system.md` |
| Prompt library structure | done | `prompts/agents/`, role prompt files |
| Contributor guidance | done | `docs/contributing.md`, `AGENTS.md` |
| Example full agent loop | done | `docs/examples/multi-agent-loop.md` |
| Minimal helper tooling | done | `scripts/check-backlog.sh` |

## Initial Gap Report

### Current gaps

- `partial`: No automated enforcement of handoff templates (manual process only).
- `partial`: Validation/report artifact storage conventions are documented but not yet standardized in dedicated directories.

### Suggested follow-up tasks (post-bootstrap backlog)

- Add optional script to scaffold reviewer/tester artifact files from templates.
- Add non-blocking lint check for handoff section presence in role artifacts.

## Evidence Links

- MVP definition: `docs/mvp.md`
- Handoff contract: `docs/agent-handoff-contract.md`
- Templates: `docs/templates/`
- Workflow: `docs/workflow.md`
- Running guide: `docs/running-the-system.md`
