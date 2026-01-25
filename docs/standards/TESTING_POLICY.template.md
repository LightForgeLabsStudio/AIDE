# Testing Policy

Keep test runs aligned with change scope and release expectations.

## Testing Approach

This project uses:

- **{{UNIT_TEST_FRAMEWORK}}**: For fast, isolated unit tests of pure logic
- **{{INTEGRATION_TEST_FRAMEWORK}}**: For integration tests requiring full component interaction
- **{{E2E_TEST_FRAMEWORK}}** (optional): For end-to-end user workflow testing

## Required Before PR

Run the test suite to ensure all tests pass:

```bash
{{RUN_ALL_TESTS_COMMAND}}
```

At minimum, run the fast unit tests:

```bash
{{RUN_UNIT_TESTS_COMMAND}}
```

If no automated tests exist yet, provide a short, repeatable manual checklist (steps + expected outcome) in the PR.

### Current Test Suites

**Unit Tests** (fast, isolated):
- `{{UNIT_TEST_PATH}}` - {{Description}}

**Integration Tests** (full component/system):
- `{{INTEGRATION_TEST_PATH}}` - {{Description}}

**E2E Tests** (optional, user workflows):
- `{{E2E_TEST_PATH}}` - {{Description}}

### Running Individual Tests

**Unit Tests:**
```bash
# Run all unit tests
{{RUN_UNIT_TESTS_COMMAND}}

# Run specific unit test file
{{RUN_SPECIFIC_UNIT_TEST_COMMAND}}
```

**Integration Tests:**
```bash
# Run all integration tests
{{RUN_INTEGRATION_TESTS_COMMAND}}

# Run specific integration test
{{RUN_SPECIFIC_INTEGRATION_TEST_COMMAND}}
```

**E2E Tests:**
```bash
# Run all e2e tests
{{RUN_E2E_TESTS_COMMAND}}
```

## Run When Relevant

- {{System A}} changes: {{Relevant tests}}
- {{System B}} changes: {{Relevant tests}}
- {{System C}} changes: {{Relevant tests}}

## Release/Pre-merge Sweep

- Run all available automated suites and test the core {{user/player/customer}} workflow
- Include commands/logs of the runs in the PR/commit description

## Writing New Tests

### When to Write Unit Tests

Write unit tests for:
- Pure logic functions (math, data transformations)
- {{Module/Service/Component}} classes
- Utility classes without external dependencies
- {{Domain logic}} and business rules
- State machines and FSM transitions
- {{Data processing}} and calculations

**Example structure:**
```{{LANGUAGE_EXTENSION}}
{{UNIT_TEST_EXAMPLE}}
```

Place unit tests in: `{{UNIT_TEST_PATH}}`

### When to Write Integration Tests

Write integration tests for:
- {{Component}} interactions
- {{API/Service}} endpoints
- {{Database/Storage}} operations
- Full {{workflow/feature}} flows
- {{UI/Frontend}} interactions

**Example structure:**
```{{LANGUAGE_EXTENSION}}
{{INTEGRATION_TEST_EXAMPLE}}
```

Place integration tests in: `{{INTEGRATION_TEST_PATH}}`

### Test Guidelines

- Don't alter existing tests without explicit approval and rationale
- Add new targeted tests alongside new features/fixes; keep them deterministic
- Prefer unit tests for fast feedback; use integration tests for end-to-end validation
- All tests should run in CI/automated environment
- Use descriptive test names: `test_<action>_<expected_result>`
- Keep tests focused: one concept per test function

## Test Coverage Goals

- **Critical paths:** 90%+ coverage
- **Core {{domain}} logic:** 80%+ coverage
- **Overall project:** {{TARGET_COVERAGE}}%+ coverage

## Customization for Your Project

Replace these placeholders:

- `{{UNIT_TEST_FRAMEWORK}}` -> "Jest", "pytest", "cargo test", "GUT"
- `{{INTEGRATION_TEST_FRAMEWORK}}` -> "Supertest", "pytest", "integration tests"
- `{{E2E_TEST_FRAMEWORK}}` -> "Playwright", "Cypress", "Selenium"
- `{{RUN_ALL_TESTS_COMMAND}}` -> "npm test", "pytest", "cargo test"
- `{{RUN_UNIT_TESTS_COMMAND}}` -> "npm run test:unit", "pytest tests/unit", "cargo test --lib"
- `{{RUN_INTEGRATION_TESTS_COMMAND}}` -> "npm run test:integration", "pytest tests/integration"
- `{{RUN_E2E_TESTS_COMMAND}}` -> "npm run test:e2e", "playwright test"
- `{{RUN_SPECIFIC_UNIT_TEST_COMMAND}}` -> Example command to run one test file
- `{{RUN_SPECIFIC_INTEGRATION_TEST_COMMAND}}` -> Example command
- `{{UNIT_TEST_PATH}}` -> "tests/unit/", "src/__tests__/", "tests/"
- `{{INTEGRATION_TEST_PATH}}` -> "tests/integration/", "e2e/"
- `{{E2E_TEST_PATH}}` -> "tests/e2e/", "playwright/"
- `{{LANGUAGE_EXTENSION}}` -> "ts", "py", "rs", "gd"
- `{{UNIT_TEST_EXAMPLE}}` -> Example test code for your language/framework
- `{{INTEGRATION_TEST_EXAMPLE}}` -> Example integration test code
- `{{TARGET_COVERAGE}}` -> "70", "80", "90"
