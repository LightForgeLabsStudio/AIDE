---
name: prime
description: Minimal project priming for AIDE-based repos. Loads AGENT_ORIENTATION.md and AGENTS.md (Tier 1) and returns a short prime summary plus the next input needed.
---

# AIDE Prime

Minimal project priming for AIDE-based repos. Use when starting a fresh session.

## Workflow

### 1. Locate repo root
Walk up from the current working directory until you find `AGENTS.md`. This is the repo root.

### 2. Read Tier 1 entry docs
- If `AGENT_ORIENTATION.md` exists at repo root, read it
- Always read `AGENTS.md` if present
- Do not read any other files yet

### 3. Extract Quick Constraints
Look for a `## Quick Constraints` section in `AGENTS.md`:
- If found: extract all bullet points under that section
- If not found: use generic message "project-defined (see AGENTS.md)"

### 4. Output Prime Report (concise, <=10 lines)

Format:
```
Primed: AGENT_ORIENTATION.md: [yes/no] AGENTS.md: [yes/no]
Constraints: [semicolon-separated list or "project-defined (see AGENTS.md)"]
Next input needed: task spec or PR/issue link
If resuming work: provide handoff or PR link
```

### 5. Next Steps
After priming, ask the user:
- What task they want to work on (issue/PR/spec)
- OR if they need to choose a role workflow

## Important Notes
- Do NOT choose or assume a role
- Do NOT load role primers yet
- Do NOT run git commands or modify files
- Keep output concise and deterministic
- This is orientation only - the actual work happens after role selection