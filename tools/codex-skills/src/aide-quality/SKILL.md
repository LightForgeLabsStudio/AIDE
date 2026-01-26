---
name: aide-quality
description: Run project quality gates for AIDE-based repos. Use when the user types /quality or asks to run tests/lint/format gates. Reads AGENTS.md to locate the project commands and runs them (or prints them if asked to dry-run).
---

# AIDE Quality

## Overview

Run or report the projects standard quality gates using commands defined in AGENTS.md placeholder mappings.

## Workflow

### 1) Locate repo root
- Walk up from current directory until `AGENTS.md` is found.

### 2) Load quality commands
- Read `AGENTS.md` and extract:
  - `{{RUN_ALL_TESTS_COMMAND}}`
  - `{{RUN_UNIT_TESTS_COMMAND}}` (optional)
  - `{{LINT_COMMAND}}`
  - `{{FORMAT_COMMAND}}` (optional)
  - `{{SMOKE_TEST_COMMAND}}` (optional)

### 3) Execute or report
- Default behavior: run lint + unit tests (fast) when available.
- If user asks for full or all: run `{{RUN_ALL_TESTS_COMMAND}}` (and smoke if defined).
- If user asks for dry-run: print the commands without running.

### 4) Output format (<=12 lines)
Include:
1) Repo root path
2) Commands detected
3) What was run (or reported)
4) Summary (pass/fail per command)

## Notes

- Never modify tests.
- If commands are missing, ask for the correct command or file path.

