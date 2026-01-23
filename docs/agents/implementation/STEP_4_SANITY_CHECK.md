# Implementation Agent - Step 4: Sanity Check

## Purpose
Verify the spec success criteria is actually met (beyond "code compiles") before refinement and review.

## Prerequisites
- Step 3 complete (implementation done; tests are not failing).

## Step Actions
- Verify each success criterion directly (prefer deterministic / scriptable checks).
- Run the repo's required quality gates:
  - `{{SMOKE_TEST_COMMAND}}`
  - `{{LINT_COMMAND}}`
  - `{{RUN_ALL_TESTS_COMMAND}}`
- If the spec implies manual verification, record a concise checklist in the PR description.

## Exit Criteria
- You can demonstrate (and briefly describe in the PR) that success criteria is met.
- Smoke tests, lint, and all tests are passing.

