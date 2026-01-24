# Implementation Agent - Step 2.5: Context Reset Checkpoint

## Purpose
Create a handoff artifact when work will pause, span sessions, or switch roles, so execution can resume without re-reading deep context.

## Prerequisites
- Step 2 complete (plan approved).

## When to Use
- You will pause before implementation.
- The task spans multiple sessions.
- You are handing work to another agent or role.

## Step Actions

1) Fill the handoff template:
- Use `docs/core/SESSION_HANDOFF.template.md`.
- Capture decisions, open questions, and the exact next action.

2) If the project maintains a context bundle:
- Link or update it using `docs/core/PROJECT_CONTEXT_BUNDLE.template.md` (optional, project-defined).

## Exit Criteria
- A handoff note exists and reflects the current plan and next action.
- Any optional context bundle reference is linked or updated.
