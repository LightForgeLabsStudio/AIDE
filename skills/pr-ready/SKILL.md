---
name: pr-ready
description: Run validation, post a summary, and flip a PR from draft to ready.
---

# PR Ready

Validate and mark a PR ready for review. Run quality gates before flipping.

## Inputs

PR number or URL. Optional: `-Fast` (lint + unit tests only), `-DryRun` (print actions only).

## Workflow

1. **Run validation** — Read [project workflow configuration](../../docs/agents/PROJECT_WORKFLOW.md). Prefer the complete validation command, running it once. If separate gates are required, resolve:
   - `{{LINT_COMMAND}}`
   - `{{RUN_UNIT_TESTS_COMMAND}}`
   - `{{RUN_ALL_TESTS_COMMAND}}`
   - `{{SMOKE_TEST_COMMAND}}` (optional)

   Default: the complete delivery gate. `-Fast` gives focused feedback only; it cannot mark the PR ready unless the project explicitly permits it as the delivery gate. Do not rerun an identical command under multiple mappings.

2. **Check CI** — Run `gh pr checks <pr> --watch`. Wait for green.

3. **Post summary** — Comment on the PR with what ran and whether it passed:
   ```
   gh pr comment <pr> --body "..."
   ```

4. **Mark ready** — Only if all gates pass and CI is green:
   ```
   gh pr ready <pr>
   ```

## Notes

- If any gate fails, post a failing summary. Do not mark ready.
- If CI is not green, do not mark ready. Wait or report the failure.
