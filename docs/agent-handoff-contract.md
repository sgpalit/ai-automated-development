# Agent Handoff Contract

This contract defines the required structure for outputs passed between agents.

Use this format for all Analyst, Planner, Developer, Reviewer, Tester, and Orchestrator outputs.

## Required Sections

1. **Context**
   - Goal in scope
   - Task or workflow step being handled
   - Inputs reviewed (files/artifacts)
2. **Decisions**
   - Key decisions made in this step
   - Reasoning in 1-2 lines per decision
3. **Artifacts**
   - Created/updated files or output artifacts
   - Path + short purpose for each artifact
4. **Open Questions / Risks**
   - Unknowns, blockers, or risks that need follow-up
5. **Recommended Next Step**
   - Next agent role
   - Concrete instruction for that role

## Minimal Markdown Template

```md
## Context
- Goal: <goal>
- Current step: <agent-step>
- Inputs reviewed:
  - <file or artifact>

## Decisions
- <decision> — <reason>

## Artifacts
- <path>: <what was produced or changed>

## Open Questions / Risks
- <question or risk>

## Recommended Next Step
- Next agent: <role>
- Instruction: <exact next action>
```

## Usage Notes

- Keep each section concise and evidence-based.
- If a section has no items, explicitly write `None`.
- Do not omit required sections.
