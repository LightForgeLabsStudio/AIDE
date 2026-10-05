---
name: check-pr
description: Inspect PR review feedback and report what needs addressing.
---

# Check PR

Inspect an existing pull request for reviewer feedback and summarize the actionable items. If the PR number or URL is invalid, respond with an error message indicating the issue and request a valid input.

## Inputs

- PR number or URL
- If provided, a user note about specific areas of concern to prioritize as a guideline for the feedback summary

## Workflow

1. **Verify context** - Use `gh api user --jq .login` if identity matters. The author is expected to use this skill to inspect reviewer feedback on their own PR, so do not block on matching identities unless a separate reviewer context is explicitly required by the user.
2. **Load PR** - Run `gh pr view <n>` and `gh pr diff <n>`. Record the current head SHA, checks, review decision and draft state. Read the linked issue and its current comments if the PR references one.
3. **Read feedback** - Inspect PR review threads and comments. Treat existing external review findings as the source of truth for this skill.
4. **Triage** - Group findings by severity and note whether each item is blocking, non-blocking, or already resolved in the branch. Identify the reviewed commit: approval of an earlier head is not verification of new changes. Confirm claimed fixes against the current diff without replacing the external reviewer.
5. **Report** - Return a concise summary with file and line references, plus a clear answer: needs changes, needs clarification, or no actionable feedback.
6. **Stop or hand off** - Do not change code in this skill. If the user wants fixes applied, switch to the implementation workflow and address only the accepted findings.

## Reference

- The consuming project's root AGENTS.md for invariants and review boundaries
- [`pr-review`](../pr-review/SKILL.md) for the full PR review workflow
