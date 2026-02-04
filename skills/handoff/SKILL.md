---
name: handoff
description: Generate a session handoff note for AIDE-based repos. Outputs a PR/issue-comment-ready handoff for context resets.
---

# AIDE Handoff

Generate a session handoff note for context resets or multi-day work.

## Workflow

### 1. Locate repo root
Assume the current workspace is the repo root.

### 2. Load handoff template (optional)
Check if `.aide/docs/core/SESSION_HANDOFF.template.md` exists in repo.
- If yes: Use its structure as a guide
- If no: Use the built-in structure below

### 3. Collect current state
Gather this information:
- Current branch: `git branch --show-current`
- Current PR number (if exists): `gh pr status` or ask user
- Related issue number (if exists): ask user or extract from PR
- Current workflow stage (0-10 from IMPLEMENTATION_START, or other role)
- Git status: `git status --short`
- Recent commits: `git log --oneline -5`

### 4. Ask for work context
Prompt user for:
- **Completed:** What tasks/steps have been finished?
- **In Progress:** What's currently mid-flight?
- **Blockers:** What's preventing progress?
- **Next Actions:** What should happen next? (ordered list)
- **Validation Status:** Are tests passing? Any known issues?

### 5. Output handoff note (<=25 lines)
```markdown
# Session Handoff: [Task Name]

**Date:** [current date]
**Branch:** [branch-name]
**PR:** #[number] (or "not created yet")
**Issue:** #[number] (or "none")
**Stage:** [current workflow stage]

## Context
[1-2 sentence summary of what this task is about]

## Completed
- [List with file references, e.g., "Updated InventoryService.cs:42-67"]
- [Use specific line numbers when possible]

## In Progress
- [Current work items with specific TODOs]
- [What's mid-flight but not finished]

## Blockers
- [What's preventing progress, if any]
- [Technical blockers, design decisions needed, etc.]

## Next Actions
1. [First thing to do when resuming]
2. [Second thing]
3. [Third thing]

## Validation Status
- Tests: [passing/failing - list failing tests if any]
- Lint: [passing/failing]
- Build: [passing/failing]
- Known issues: [any warnings or concerns]

## File References
[List key files touched with line ranges]
```

### 6. Where to post
Ask user where to post this:
- **PR comment (preferred):** `gh pr comment [pr-number] --body "[handoff]"`
- **Issue comment:** `gh issue comment [issue-number] --body "[handoff]"`
- **Print only:** Just display for user to copy

**Do NOT commit handoff files to the repository unless explicitly requested.**

## Important Notes
- Be specific with file paths and line numbers
- Include commit SHAs for key changes
- Keep it concise but complete
- Focus on "what needs to happen next" not "what I did today"
- This is for resumption, not a status report
