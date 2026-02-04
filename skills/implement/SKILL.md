---
name: implement
description: Implementation entrypoint for AIDE repos: intake spec, plan, branch, draft PR, implement, validate, push.
---

# Implement

Implement a feature/bug end-to-end using the AIDE implementation workflow.

## Inputs (ask first)

- Issue/PR link or pasted spec text (goals, scope, success criteria).
- Any must-not-change constraints beyond `AGENTS.md`.

If there is no spec yet, switch to `/design` (exploration) before implementing.

## Workflow

1) **Read Tier 1 rules**
   - Read `AGENTS.md` (constraints + placeholder commands).
   - Load relevant design pillar(s) only if the spec touches them.

2) **Preflight**
   - Ensure you are not working on `main` (create a branch).
   - Identify authoritative systems (e.g., `InventoryService`, `JobSystem`) and avoid duplicating state.

3) **Plan before coding**
   - Produce a short two-layer plan (constraints + steps with exit criteria).
   - Wait for user approval before making code changes.

4) **Draft PR early**
   - Create a draft PR as soon as the plan is approved.
   - Ensure PR links the issue (e.g., "Fixes #123") and includes a validation checklist.

5) **Implement**
   - Extend existing patterns (do not replace architecture).
   - Keep simulation deterministic (no unseeded randomness in core logic).
   - Do not modify existing tests without explicit approval.

6) **Validate**
   - Run lint/tests using commands from `AGENTS.md` placeholder mappings.
   - Confirm success criteria are met.

7) **Land the plane**
   - Commit cleanly, then `git push` (required by project rules).

## Reference

- AIDE implementation primer: `.aide/docs/agents/IMPLEMENTATION_START.md`
- Step docs: `.aide/docs/agents/implementation/`
