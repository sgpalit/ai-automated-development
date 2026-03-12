# Agent Context

This file defines the minimal context required for AI agents.

Agents should read this file first and follow the instructions below.

---

## Primary Documents

Agents should read the following documents in this order:

1. AGENTS.md
2. docs/workflow.md
3. docs/agent-io-contracts.md

These define the operational workflow.

---

## Agent Role Definitions

Agent prompts are located in:

prompts/agents/

Agents should only read the prompt file corresponding to their role.

Examples:

- prompts/agents/analyst.md
- prompts/agents/planner.md
- prompts/agents/developer.md
- prompts/agents/reviewer.md
- prompts/agents/tester.md
- prompts/agents/orchestrator.md

---

## Backlog

Tasks are located in:

backlog/tasks/

Agents must only implement tasks from this backlog.

---

## Output Locations

Agents should store outputs in:

analysis/
reviews/
validation/

These directories are used for inter-agent communication.

---

## Ignore These For Execution

The following documents are informational and not required for task execution:

docs/mvp.md  
docs/agents.md  
docs/running-the-system.md  
docs/target-repo-context.md  

Agents may consult them if needed, but they are not required for normal workflow.

---

## Operational Principle

Agents should focus on executing the workflow and completing tasks.

Avoid reading unnecessary documentation unless required.
