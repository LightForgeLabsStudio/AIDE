---
name: aide-role
description: Route an AIDE-based repo task to the correct agent role and primer. Use when the user types /role or asks "which workflow/primer?" Chooses Implementation vs PR Review vs Codebase Review vs Design Spec vs Design Workshop vs Doc Review, then points to the correct `.aide/docs/agents/*` start doc and asks for the next required input.
---

# AIDE Role

## Overview

Select the appropriate AIDE role workflow and provide the next doc(s) and inputs needed to proceed.

## Workflow

### 1) Locate repo root
- Walk up from the current working directory until `AGENTS.md` is found.

### 2) Read routing docs (minimal)
- Read `AGENT_ORIENTATION.md` (if present) and `AGENTS.md`.
- Do not load deep docs or implementation files.

### 3) Decide role from user intent
Heuristics:
- If the user provides a PR link or asks to "review" -> PR Review
- If the user asks to implement/fix/add feature -> Implementation
- If the user asks for design exploration/options -> Design Workshop
- If the user asks to write a spec/shape scope -> Design Spec
- If the user asks for a holistic audit/health check -> Codebase Review
- If the user asks to review docs for accuracy -> Doc Review

### 4) Output (<=12 lines)
Print:
- Selected role
- Primer path under `.aide/docs/agents/`
- Next required input (issue/spec link, PR link, etc.)

## Notes

- This skill routes only. `/prime` is still the entrypoint for loading Tier 1 rules.
- Do not start editing code; follow the selected role primer.

