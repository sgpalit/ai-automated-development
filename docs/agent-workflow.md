## Follow-up Task Creation

After completing a task, the agent should propose and add new backlog tasks when useful.

Rules:

- Add only **small, concrete, implementation-ready** follow-up tasks
- Do not create vague or oversized tasks
- Use the next sequential task number
- Set initial status to `todo`
- Include priority, scope, out of scope, acceptance criteria, and dependencies
- Prefer tasks that logically follow from the work just completed

The agent must not start the newly created tasks automatically unless explicitly instructed.

## Human Review Loop

Workflow:

1. Agent picks the next approved `todo` task
2. Agent implements the task
3. Agent marks it as `done` if completed
4. Agent proposes one or more follow-up tasks if relevant
5. Human reviews and edits the newly proposed backlog tasks
6. Agent waits for the next explicit instruction before continuing

This repository uses a human-reviewed iterative workflow.
