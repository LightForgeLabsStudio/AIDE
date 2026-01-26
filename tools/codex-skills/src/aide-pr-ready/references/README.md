# AIDE PR Ready Skill References

This skill:
- Reads `AGENTS.md` to find project quality commands (`{{LINT_COMMAND}}`, `{{RUN_UNIT_TESTS_COMMAND}}`, `{{RUN_ALL_TESTS_COMMAND}}`, `{{SMOKE_TEST_COMMAND}}`).
- Runs validation (full by default; `-Fast` runs lint + unit tests).
- Posts a PR comment with a concise summary.
- Marks the PR ready via `gh pr ready` only if validation passes.

Arguments:
- `-Pr <number|url>` (required)
- `-Repo owner/repo` (optional)
- `-Fast` (optional)
- `-DryRun` (optional)

