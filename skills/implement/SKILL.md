---
name: implement
description: Implementation entrypoint for AIDE repos: intake spec, plan, branch, draft PR, implement, validate, push.
---

# Implement

Implement a feature/bug end-to-end using the AIDE implementation workflow.

## Documentation Loading (role-based)

- Always use: project constraints + the task spec (issue/PR description).
- Stage-load (implementation work): `docs/CODING_GUIDELINES.md`, `docs/TESTING_POLICY.md`, `docs/CONTRIBUTING.md`, and `docs/DEVELOPMENT.md` as soon as planning/implementation begins.
- Stage-load (as needed): relevant `design/` pillar(s) for the feature/bug.

## Inputs (ask first)

- Issue/PR link or pasted spec text (goals, scope, success criteria).
- Any must-not-change constraints beyond the project's standard rules.

If there is no spec yet, switch to `/design` (exploration) before implementing.

## Workflow

1) **Read Tier 1 rules**
   - Use the project's constraints and placeholder commands (already loaded in this environment).
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
   - Run lint/tests using the project's placeholder-mapped commands.
   - Confirm success criteria are met.

7) **Land the plane**
   - Commit cleanly, then `git push` (required by project rules).

## Reference

- AIDE implementation primer: `.aide/docs/agents/IMPLEMENTATION_START.md`
- Step docs: `.aide/docs/agents/implementation/`
