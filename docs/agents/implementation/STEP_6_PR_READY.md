# Implementation Agent - Step 6: Mark PR Ready for Review

## Purpose
Finalize and mark the PR ready only when the checklist is complete and quality gates are green.

## Prerequisites
- Step 5 complete (refinement done).

## Step Actions

Pre-flight checklist:
- [ ] All implementation plan tasks checked off in PR description
- [ ] Smoke tests passing (`{{SMOKE_TEST_COMMAND}}`)
- [ ] Linting passing (`{{LINT_COMMAND}}`)
- [ ] All tests passing (`{{RUN_ALL_TESTS_COMMAND}}`)
- [ ] Code refinement complete (Step 5)
- [ ] PR description updated with final summary
- [ ] Issue reference included (`Fixes #<number>`)

Mark ready:
```bash
# Flip from draft to ready
gh pr ready <number>

# Add comment summarizing completion
gh pr comment <number> --body "All implementation tasks complete. Smoke tests, linting, and tests passing. Ready for review."
```

PR is now visible to reviewers and will auto-close the linked issue on merge.

## Exit Criteria
- PR is marked ready (not draft).
- A completion comment is posted with test status.

