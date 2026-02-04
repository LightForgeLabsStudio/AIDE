# Skill Router (Role Entrypoints)

Use this page when you (or the user) is unsure which **role/skill** to start with.

## Fast Decision Tree

1) Do you need to **change code/docs/config** (not just talk about it)?
- Yes -> go to **Implementation** (`/implement`)
- No -> continue

2) Do you need to **review** an existing change (PR/diff) without fixing it?
- Yes -> **PR Review** (`/pr-review`)
- No -> continue

3) Do you need to **explore options / shape requirements** (no spec yet)?
- Yes -> **Design** (`/design`)
- No -> continue

4) Do you need to **audit overall health** (dead code, drift, gaps) without fixing it?
- Yes -> **Codebase Review** (`/codebase-review`)
- No -> continue

5) Is the task primarily **documentation accuracy** (no code changes)?
- Yes -> **Doc Review** (`/doc-review`)
- No -> continue

6) Still unsure?
- If you have a concrete spec but mixed concerns -> start **Implementation** and do a careful Step 0/1 intake/survey.
- If the spec is missing/ambiguous -> start **Design** and draft a spec first.

## Common Intents -> Skill

| User intent | Start with | Notes |
|------------|------------|-------|
| "Add feature X" | `/design` or `/implement` | `/implement` only if a spec/success criteria exist. |
| "Fix bug Y" | `/implement` | Intake: repro steps + expected vs actual. |
| "Can you review my PR?" | `/pr-review` | No fixes; produce findings and questions. |
| "Is the architecture healthy?" | `/codebase-review` | No fixes; file issues/follow-ups if needed. |
| "Are these docs correct?" | `/doc-review` | Propose edits; avoid code changes. |

## When to Switch Roles

- Design -> Implement: once goals/scope/success criteria are written and agreed.
- Review -> Implement: only after explicit approval to make changes.
- Implement -> Review: when you need a dedicated pass for quality/architecture feedback.

## Utility Commands (If Available)

These are not roles, but often answer "what should I do next?" questions:

- `/plan` - turn a spec into a two-layer plan with exit criteria
- `/quality` - run the project's standard lint/tests gates
- `/handoff` - produce a context-reset handoff note
- `/sync` - end-of-session cleanup (sync branch with remote, verify clean state)
- `/issue` - create a follow-up issue for out-of-scope work
- `/evolve` - convert repeated failures into rules or automation

## Related References

- Command catalog (tool-agnostic): `COMMAND_CATALOG.md`
- Implementation index: `IMPLEMENTATION_START.md`
