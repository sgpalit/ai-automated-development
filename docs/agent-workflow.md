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

Human review is required before the next task is executed.
