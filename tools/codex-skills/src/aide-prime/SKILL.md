---
name: aide-prime
description: Minimal project priming for AIDE-based repos. Use when the user types /prime or asks to prime/orient/load docs. Reads only AGENT_ORIENTATION.md and AGENTS.md (Tier 1) and returns a short prime summary plus the next input needed. Does NOT choose a role or load role primers.
---

# AIDE Prime

## Overview

Provide a minimal, deterministic prime for an AIDE-based repo by loading only Tier 1 entry docs and asking for the task spec or PR/issue link.

## Workflow

### 1) Locate the repo root
- Walk up from the current working directory to find `AGENTS.md`.
- If found, treat that directory as the repo root.

### 2) Read only Tier 1 entry docs
- If `AGENT_ORIENTATION.md` exists at the repo root, read it.
- Always read `AGENTS.md` if present.
- Do not read any other files.

### 3) Output the Prime Report (<=10 lines)
Include:
1. `Primed: [AGENT_ORIENTATION.md: yes/no] [AGENTS.md: yes/no]`
2. `Constraints: Extend-not-replace; No test mods; No main; Deterministic; InventoryService/JobSystem authoritative; Autoloads UI-free`
3. `Next input needed: task spec or PR/issue link`
4. `If resuming work: provide handoff or PR link`

### 4) Missing-doc behavior
- If `AGENTS.md` is missing, report that and ask for the authoritative doc path.
- If `AGENT_ORIENTATION.md` is missing, proceed with `AGENTS.md` only.

## Notes

- Do not choose or assume a role. Role selection is a separate command (e.g., `/role`).
- Keep output concise and deterministic.
- Do not run git commands or modify files.

