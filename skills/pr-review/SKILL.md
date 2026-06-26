---
name: pr-review
description: Review a pull request for spec alignment, architecture, tests, and docs. No code changes.
---

# PR Review

Review a PR against its linked issue and project constraints. Do not push fixes.

## Inputs

PR number or URL. Reviewer GitHub login (must not be PR author). Any custom concerns.

## Workflow

1. **Verify identity** — Run `gh api user --jq .login`. If reviewer == PR author, stop and request an identity switch.

   If you need a separate reviewer identity (e.g., work vs. personal account):
   ```bash
   # One-time setup for a reviewer account
   GH_CONFIG_DIR=~/.config/gh-reviewer gh auth login
   # Then prefix all gh commands with GH_CONFIG_DIR=~/.config/gh-reviewer
   GH_CONFIG_DIR=~/.config/gh-reviewer gh api user --jq .login
   ```

   If `gh` is configured with multiple accounts in the default config, do not stop after the first identity check. Inspect `gh auth status`, look for an available reviewer account (for this repo that is typically `lightforgelabsdev-review`), and switch with:
   ```bash
   gh auth switch -u lightforgelabsdev-review
   ```

   Important: in Codex shell sessions, the GitHub account may be reset at the start of each new shell command. When you need to switch accounts for a review, perform the switch, identity verification, and `gh pr review ...` submission inside the same shell invocation rather than separate commands.

2. **Load PR + spec** — Run `gh pr view <n>` and `gh pr diff <n>`. Extract linked issue (`Fixes #X`) and read its full spec.

3. **Review** — Check:
   - Spec alignment (goals, scope, success criteria)
   - Architecture compliance (AGENTS.md invariants, authoritative systems)
   - Testing posture (new tests where appropriate; no unjustified test edits)
   - Docs drift or duplication
   - Git hygiene (commit structure, no debug leftovers)
   - If a check is red, compare against `main` and inspect the full PR commit range before classifying it. If the failure appears anywhere in the PR range, treat it as branch-owned regression and review it as part of the PR. Do not label a failure as `pre-existing` unless that baseline comparison proves it.

4. **Report findings** — Group by severity (Critical/Major/Minor) with `path:line` references. State a clear decision: approve / request changes / non-blocking.

5. **Submit** — Post findings directly as a GitHub PR review:
   ```
   gh pr review <n> --request-changes --body "..."
   ```
   (Use `--approve` or `--comment` as appropriate.) Do not review as the PR author.

   In this repository, if you had to switch to a reviewer account first, prefer a single shell invocation such as:
   ```bash
   gh auth switch -u lightforgelabsdev-review && gh api user --jq .login && gh pr review <n> --request-changes --body "..."
   ```
