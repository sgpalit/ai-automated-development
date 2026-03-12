# Human Approval Checklists

Use these checklists at explicit workflow gates.

## 1) Task Approval Checklist (before implementation)

Required evidence:
- Repository analysis summary
- Candidate task file in `agents/<target-name>/backlog/tasks/`

Checklist:
- [ ] Objective is clear and MVP-relevant
- [ ] Scope and out-of-scope boundaries are explicit
- [ ] Acceptance criteria are testable
- [ ] Dependencies are correct and satisfied
- [ ] Priority is appropriate

## 2) Implementation Acceptance Checklist (after review + test)

Required evidence:
- Developer summary
- Developer commit hash and confirmation that it was pushed
- Reviewer result (`APPROVED` / `CHANGES REQUIRED`)
- Tester result (`READY` / `RETRY` / `BLOCKED`)

Checklist:
- [ ] Implementation stayed within approved scope
- [ ] Acceptance criteria are demonstrably met
- [ ] Developer provided the pushed commit reference for the completed task
- [ ] Reviewer checked the developer's pushed commit, not an uncommitted working tree
- [ ] Reviewer result is `APPROVED`
- [ ] Tester result is `READY`
- [ ] Risks/open questions are acceptable or tracked

## 3) Loop Continuation Checklist (before next iteration)

Required evidence:
- Updated task status
- Latest backlog state
- Outstanding risks/questions from last cycle
- Orchestrator stop/continue artifact when auto-continue mode is used

Checklist:
- [ ] Completed task status updated correctly
- [ ] Next eligible task is dependency-safe
- [ ] Any blockers are documented
- [ ] Human confirms continue/pause/reprioritize decision when the loop is supervised
