# Human Approval Checklists

Use these checklists at explicit workflow gates.

## 1) Task Approval Checklist (before implementation)

Required evidence:
- Repository analysis summary
- Candidate task file in `backlog/tasks/`

Checklist:
- [ ] Objective is clear and MVP-relevant
- [ ] Scope and out-of-scope boundaries are explicit
- [ ] Acceptance criteria are testable
- [ ] Dependencies are correct and satisfied
- [ ] Priority is appropriate

## 2) Implementation Acceptance Checklist (after review + test)

Required evidence:
- Developer summary
- Reviewer result (`APPROVED` / `CHANGES REQUIRED`)
- Tester result (`PASSED` / `FAILED`)

Checklist:
- [ ] Implementation stayed within approved scope
- [ ] Acceptance criteria are demonstrably met
- [ ] Reviewer result is `APPROVED`
- [ ] Tester result is `PASSED`
- [ ] Risks/open questions are acceptable or tracked

## 3) Loop Continuation Checklist (before next iteration)

Required evidence:
- Updated task status
- Latest backlog state
- Outstanding risks/questions from last cycle

Checklist:
- [ ] Completed task status updated correctly
- [ ] Next eligible task is dependency-safe
- [ ] Any blockers are documented
- [ ] Human confirms continue/pause/reprioritize decision
