---
name: pr-ready
description: Mark a PR as ready and post a validation summary for AIDE-based repos. Use when the user types /pr-ready or asks to flip a PR from draft to ready.
---

# AIDE PR Ready

## Overview

Standardize the "PR Ready" step: run validation, post a summary, and flip a PR from draft to ready.

## Workflow

### Inputs
- PR number or PR URL (required)
- Optional repo override (`owner/repo`)
- Optional `-DryRun` to print actions only
- Optional `-Fast` to run lint + unit tests only

### Actions
1) Assume the current workspace is the repo root.
2) Use project placeholder mappings and extract quality commands:
   - `{{LINT_COMMAND}}`
   - `{{RUN_UNIT_TESTS_COMMAND}}`
   - `{{RUN_ALL_TESTS_COMMAND}}`
   - `{{SMOKE_TEST_COMMAND}}` (optional)
3) Run validation:
   - Default: lint + all tests (+ smoke if defined)
   - `-Fast`: lint + unit tests
4) Check CI status and wait for green (e.g., `gh pr checks <pr> --watch`).
5) Post a PR comment with the validation summary.
6) Mark the PR ready only if CI is green: `gh pr ready <pr>`.

### Output
- A short log of what ran and whether it passed.

## Notes
- If any gate fails, do not mark the PR ready; post a failing summary instead.
- If CI is not green, do not mark the PR ready; post a note and wait/retry.
