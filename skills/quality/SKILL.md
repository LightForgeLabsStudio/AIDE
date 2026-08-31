---
name: quality
description: Run project quality gates. Executes lint and tests based on project placeholder mappings.
---

# Quality

Run project quality gates and report results.

## Inputs

Ask the user for scope. Choose one of the following options:
- **default**: lint + unit tests (fast feedback)
- **full**: all tests + smoke tests
- **dry-run**: print commands without executing

If the user provides an invalid scope option, respond with an error message indicating valid options: default, full, or dry-run.

## Workflow

1. **Load commands** from project placeholder mappings:
   - `{{LINT_COMMAND}}`
   - `{{RUN_UNIT_TESTS_COMMAND}}` (optional)
   - `{{RUN_ALL_TESTS_COMMAND}}`
   - `{{SMOKE_TEST_COMMAND}}` (optional)

2. **Execute** in order: lint → tests → smoke (if full scope).

3. **Report:**
   ```
   ## Quality Gate Results
   Scope: default | full | dry-run

   Results:
   ✅/❌ Lint: passed | failed
   ✅/❌ Tests: X passed, Y failed
   ✅/❌ Smoke: passed | failed | skipped

   [If failures: show failing test names and relevant log lines]

   Next: Fix failures | Proceed with PR
   ```

## Notes

- Stop immediately if lint or tests fail.
- Do not modify test files.
- For CI/PR workflows, always run at least lint + tests before marking ready.
