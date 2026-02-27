# Implementation Reference

Quick reference for commit format, critical rules, and placeholder values for this project.

## Agent Signature

```bash
git commit -m "Brief imperative summary (#issue)

Details if needed.

Co-Authored-By: [Agent Name] <agent@{{PROJECT_DOMAIN}}>"
```

Reference the issue number for traceability: `#42 Add drone return-to-base`.

## PR Body (required)

- `Fixes #<number>` — auto-closes issue on merge
- `## Summary` — what changed and why
- `## Implementation Plan` — `- [ ]` checklist
- `## Validation` — `- [ ]` checklist

## Critical Don'ts

- Do not code without spec intake + codebase survey
- Do not implement without an explicit Layer 2 plan
- Do not work on `{{MAIN_BRANCH}}`
- Do not modify tests without explicit approval
- Do not submit a PR marked ready if tests or lint fail

## Project Placeholder Values

| Placeholder | Value |
| --- | --- |
| `{{MAIN_BRANCH}}` | `main` |
| `{{RUN_ALL_TESTS_COMMAND}}` | `cmd /c run_tests.bat` |
| `{{RUN_UNIT_TESTS_COMMAND}}` | `Godot_v4.5.1_console.exe --headless -s addons/gut/gut_cmdln.gd` |
| `{{LINT_COMMAND}}` | `cmd /c lint.bat` |
| `{{SMOKE_TEST_COMMAND}}` | `cmd /c smoke_test.bat` |
