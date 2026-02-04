---
name: pr-review
description: Review a pull request (no code changes): spec alignment, architecture, tests, docs, and clear findings.
---

# PR Review

Review a PR against the linked issue spec and project constraints. Do not push fixes.

## Inputs (ask first)

- PR number or URL.
- Any custom concerns/checks the requester wants verified.

## Workflow

1) **Read Tier 1 rules**
   - `AGENTS.md`, `docs/CODING_GUIDELINES.md`, `docs/TESTING_POLICY.md`, `docs/CONTRIBUTING.md` (as needed).

2) **Load PR + spec**
   - Use `gh pr view <n>` / `gh pr diff <n>` to read the PR.
   - Extract linked issue ("Fixes #X") and read the full issue spec/comments.

3) **Review**
   - Spec alignment (goals/scope/success criteria).
   - Architecture and design pillar compliance.
   - Testing posture (new tests where appropriate; no unjustified test edits).
   - Docs drift/duplication.
   - Git hygiene (commit structure, no debug leftovers).

4) **Report**
   - Findings grouped by severity (Critical/Major/Minor) with `path:line` references.
   - Clear decision: approve / request changes / comment-only.

## Reference

- AIDE PR review primer: `.aide/docs/agents/PR_REVIEW_START.md`
