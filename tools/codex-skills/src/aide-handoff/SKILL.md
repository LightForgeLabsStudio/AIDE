---
name: aide-handoff
description: Generate a session handoff note for AIDE-based repos. Use when the user types /handoff or asks to summarize current state for a context reset. Outputs a PR/issue-comment-ready handoff (no file writes by default).
---

# AIDE Handoff

## Overview

Produce a concise, structured handoff note using the AIDE template so another session/agent can resume without re-reading deep context.

## Workflow

### 1) Locate repo root
- Walk up from current working directory until `AGENTS.md` is found.

### 2) Load the handoff template
- Prefer `.aide/docs/core/SESSION_HANDOFF.template.md` if it exists in the repo.
- If missing, fall back to the built-in template structure from this skill.

### 3) Ask for missing fields (if not provided)
- Current stage
- Branch
- PR link (or not created yet)
- Completed / In Progress / Blockers / Next Actions / Validation

### 4) Output (<=20 lines when possible)
- Print the handoff note ready for a PR/issue comment.
- Do not write files by default.

## Notes

- Prefer PR/issue comments over committing handoff files.
- If the user explicitly requests a file, write it to a local, ignored path (e.g., `docs/handoffs/`).

## Posting (Optional)

This skill can optionally post the handoff directly via GitHub CLI:

- PR comment: `scripts/handoff.ps1 -Post -Pr <number> [-Repo owner/repo]`
- Issue comment: `scripts/handoff.ps1 -Post -Issue <number> [-Repo owner/repo]`

