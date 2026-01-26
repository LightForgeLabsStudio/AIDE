# AIDE Quality Skill References

This skill reads `AGENTS.md` at the repo root to discover the project's quality commands via AIDE placeholders:

- `{{RUN_ALL_TESTS_COMMAND}}`
- `{{RUN_UNIT_TESTS_COMMAND}}`
- `{{LINT_COMMAND}}`
- `{{FORMAT_COMMAND}}`
- `{{SMOKE_TEST_COMMAND}}`

Default run is lint + unit tests. Use `-Full` to run all tests (and smoke if present). Use `-DryRun` to print commands only.

