---
name: quality
description: Run project quality gates. Executes lint and tests based on project placeholder mappings.
---

# Quality

Run project quality gates and report results.

## Inputs

Use the requested scope, or default to full when none is supplied:
- **default**: lint + unit tests (fast feedback)
- **full**: all tests + smoke tests
- **dry-run**: print commands without executing

If the user provides an invalid scope option, respond with an error message indicating valid options: default, full, or dry-run.

## Workflow

1. **Load commands** using [project workflow configuration](../../docs/agents/PROJECT_WORKFLOW.md). Prefer its complete validation command for full scope. Otherwise resolve the project mappings:
   - `{{LINT_COMMAND}}`
   - `{{RUN_UNIT_TESTS_COMMAND}}` (optional)
   - `{{RUN_ALL_TESTS_COMMAND}}`
   - `{{SMOKE_TEST_COMMAND}}` (optional)

2. **Execute** the complete validation command for full scope, or lint → tests → smoke as configured. Run identical commands once. A complete gate already including lint and smoke replaces separate invocations.

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
