---
name: check-pr
description: Inspect PR review feedback and report what needs addressing.
---

# Check PR

Inspect an existing pull request for reviewer feedback and summarize the actionable items.

## Inputs

- PR number or URL
- Optional user note about what kind of feedback to prioritize

## Workflow

1. **Verify context** - Use `gh api user --jq .login` if identity matters. The author is expected to use this skill to inspect reviewer feedback on their own PR, so do not block on matching identities unless a separate reviewer context is explicitly required by the user.
2. **Load PR** - Run `gh pr view <n>` and `gh pr diff <n>`. Read the linked issue if the PR references one.
3. **Read feedback** - Inspect PR review threads and comments. Treat existing external review findings as the source of truth for this skill.
4. **Triage** - Group findings by severity and note whether each item is blocking, non-blocking, or already resolved in the branch.
5. **Report** - Return a concise summary with file and line references, plus a clear answer: needs changes, needs clarification, or no actionable feedback.
6. **Stop or hand off** - Do not change code in this skill. If the user wants fixes applied, switch to the implementation workflow and address only the accepted findings.

## Reference

- [AGENTS.md](../../AGENTS.md) for repo invariants and review boundaries
- [`pr-review`](../pr-review/SKILL.md) for the full PR review workflow
