---
name: quality
description: Run project quality gates from AGENTS.md placeholder mappings. Executes lint and tests based on project configuration.
---

# AIDE Quality

Run project quality gates from AGENTS.md placeholder mappings.

## Workflow

### 1. Locate repo root
Walk up from current directory until you find `AGENTS.md`.

### 2. Load quality commands
Read `AGENTS.md` and extract these placeholder mappings:
- `{{RUN_ALL_TESTS_COMMAND}}` - Full test suite
- `{{RUN_UNIT_TESTS_COMMAND}}` - Unit tests only (optional)
- `{{LINT_COMMAND}}` - Linting
- `{{FORMAT_COMMAND}}` - Formatting (optional)
- `{{SMOKE_TEST_COMMAND}}` - Smoke tests (optional)

### 3. Determine scope
Ask the user what scope they want:
- **Default (recommended):** Lint + unit tests (fast feedback)
- **Full:** All tests + smoke tests
- **Dry-run:** Print commands without executing

### 4. Execute validation
Run the selected commands in this order:
1. Lint (if defined)
2. Unit tests OR all tests (depending on scope)
3. Smoke tests (if full scope and defined)

### 5. Output format (<=15 lines)
```
## Quality Gate Results

Repo: [repo root path]
Scope: [default/full/dry-run]

Commands:
- Lint: [command or "not defined"]
- Tests: [command or "not defined"]
- Smoke: [command or "not defined"]

Results:
✅/❌ Lint: [passed/failed/skipped]
✅/❌ Tests: [X passed, Y failed/skipped]
✅/❌ Smoke: [passed/failed/skipped]

[If failures: show failing test names and logs]

Next: [Fix failures OR proceed with PR if all passed]
```

## Important Notes
- Never modify test files
- If commands are missing from AGENTS.md, ask user to provide them
- Stop immediately if lint or tests fail - do not proceed
- For CI/PR workflows, always run at least lint + tests before marking ready