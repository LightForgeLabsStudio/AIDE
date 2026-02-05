---
name: pr-review
description: Review a pull request (no code changes) covering spec alignment, architecture, tests, docs, and clear findings.
---

# PR Review

Review a PR against the linked issue spec and project constraints. Do not push fixes.

## Documentation Loading (role-based)

- Always use: project constraints + the linked issue spec.
- Stage-load (review work): `docs/CODING_GUIDELINES.md`, `docs/TESTING_POLICY.md`, `docs/CONTRIBUTING.md`, and `docs/DEVELOPMENT.md`.
- Stage-load (as needed): relevant `design/` pillar(s) and `docs/DOCUMENTATION_POLICY.md` if docs are in scope.

## Inputs (ask first)

- PR number or URL.
- Reviewer GitHub login to use for reviews (must not be the PR author).
- Any custom concerns/checks the requester wants verified.

## Workflow

1) **Read Tier 1 rules**
   - Use the project's constraints (already loaded in this environment) and stage-load the role-relevant Tier 1 docs (see above).

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
    - Clear decision: approve / request changes / non-blocking.
    - Prefer submitting as a formal GitHub Review via `gh pr review` (not only as a PR comment).
    - Switch to the reviewer identity before reviewing: `gh auth switch -u <reviewer_login>` (see `.aide/docs/agents/PR_REVIEW_START.md`).
    - If the reviewer identity == PR author, stop and request switching identities (do not review as the author).

## Reference

- AIDE PR review primer: `.aide/docs/agents/PR_REVIEW_START.md`
- Cross-role handoffs + escalation protocol: `.aide/docs/agents/AGENT_COLLABORATION.md`
