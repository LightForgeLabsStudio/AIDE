---
name: aide-evolve
description: Apply the AIDE system evolution workflow to repeated mistakes. Use when the user types /evolve or asks to turn a recurring issue into a rule/check. Reads `.aide/docs/agents/SYSTEM_EVOLUTION.md` and outputs a concrete proposal (automation vs Tier 1 vs Tier 2 vs reference-only) with exact file/section targets and example wording.
---

# AIDE Evolve

## Overview

Turn repeated agent failures into durable guardrails using the AIDE decision tree (smallest effective change).

## Workflow

### 1) Inputs to collect
- What happened? (failure pattern)
- How many times? (2+ sessions/PRs)
- Evidence links (PR/issue URLs or brief excerpts)
- Where it should have been caught (tooling? docs? invariant?)

### 2) Read the decision tree
- `.aide/docs/agents/SYSTEM_EVOLUTION.md`

### 3) Decide smallest effective change
- Prefer automation if enforceable
- Otherwise Tier 1 if project-wide binding
- Otherwise Tier 2 if system-specific guidance
- Otherwise reference-only

### 4) Output a concrete proposal
Must include:
- Decision: automation vs Tier 1 vs Tier 2 vs reference-only
- Location: exact file path + section heading to update
- Example change: proposed wording (positive constraint) or check
- Rationale: 1-2 lines referencing trigger criteria

## Notes

- This skill proposes changes; it should not modify repo files unless explicitly instructed.

