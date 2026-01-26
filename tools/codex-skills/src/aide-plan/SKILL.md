---
name: aide-plan
description: Create a two-layer AIDE implementation plan from an issue/PR spec. Use when the user types /plan or asks for a plan/checklist. Reads AGENTS.md for constraints and project commands and outputs a plan plus a draft PR checklist body.
---

# AIDE Plan

## Overview

Turn a task spec into a concise, reviewable plan (Layer 1 constraints + Layer 2 tasks) and a draft PR checklist body.

## Workflow

### Inputs
- Issue/PR spec text (preferred), or an issue number to fetch via `gh` (optional).
- Any constraints or acceptance criteria not in the spec.

### Steps
1) Locate repo root (walk up until `AGENTS.md`).
2) Read `AGENTS.md` to capture top invariants and the project's quality commands.
3) Produce **Layer 1 constraints** (short bullet list).
4) Produce **Layer 2 plan** (ordered tasks with exit criteria).
5) Output a PR draft body checklist (markdown `- [ ]`) that mirrors the plan.

### Output
- A plan block suitable for chat approval.
- A draft PR body template (ready to paste into `gh pr create --draft`).

## Notes
- Do not implement; planning only.
- Prefer the narrowest test scope first, then broaden.

