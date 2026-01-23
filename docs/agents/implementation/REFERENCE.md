# Implementation Agent - Reference

This file contains reference material that is not required to execute a single workflow step, but is useful when customizing or integrating AIDE.

## Agent Signature

Commits:
```bash
git commit -m "Brief imperative summary

Details.

Co-Authored-By: [Agent Name] <agent@{{PROJECT_DOMAIN}}>"
```

PR body:
Use spec template from `{{CONTRIBUTING_DOC}}` (required). Include:
- Summary, Goals, Scope, Non-Goals, Success Criteria, Implementation Approach, Impacted Files
- Issue reference: `Fixes #<number>` (auto-closes issue on merge)
- Agent signature: `[Agent Name] Implementation`

Commit messages: reference issue number for traceability:
```bash
git commit -m "Add job prioritization (refs #42)"
```

## Critical Don'ts

- Do not code without spec intake + codebase survey
- Do not implement without plan approval
- Do not work on `{{MAIN_BRANCH}}`
- Do not create PR before implementation done
- Do not modify tests without approval

## Reference Docs

- `{{GITHUB_QUERIES_DOC}}` - GitHub queries for implementation status
- `BEADS_USAGE.md` - AI working memory and task tracking with bd (beads)
- `{{CONTRIBUTING_DOC}}` - Full workflow
- `{{CODING_GUIDELINES_DOC}}` - Code style
- `{{TESTING_POLICY_DOC}}` - Testing requirements
- `{{DEVELOPMENT_DOC}}` - Architecture
- `{{BEST_PRACTICES_DOC}}` - Technology-specific patterns (e.g., Godot, React, Rust)
- `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - Efficient operation

## Customization for Your Project

Replace these placeholders with your project specifics:

- `{{PROJECT_NAME}}` -> Your project name
- `{{TECH_STACK}}` -> "Godot 4.5 + GDScript", "Node.js + TypeScript", "Rust + Actix"
- `{{MAIN_BRANCH}}` -> "main", "master", "develop"
- `{{PROJECT_DOMAIN}}` -> "example.com", "yourproject.dev"
- `{{GITHUB_QUERIES_DOC}}` -> ".aide/docs/agents/GITHUB_QUERIES.md"
- `{{PROJECT_DESIGN_DOCS}}` -> "design/", "docs/adr/"
- `{{DEVELOPMENT_DOC}}` -> "docs/DEVELOPMENT.md", "docs/ARCHITECTURE.md"
- `{{CODING_GUIDELINES_DOC}}` -> "docs/CODING_GUIDELINES.md"
- `{{TESTING_POLICY_DOC}}` -> "docs/TESTING_POLICY.md"
- `{{CONTRIBUTING_DOC}}` -> "docs/CONTRIBUTING.md"
- `{{BEST_PRACTICES_DOC}}` -> "docs/GODOT_BEST_PRACTICES.md", "docs/REACT_PATTERNS.md"
- `{{UNIT_TEST_TYPE}}` -> "GUT unit tests", "Jest tests", "pytest"
- `{{INTEGRATION_TEST_TYPE}}` -> "GUT integration tests", "Playwright e2e"
- `{{RUN_ALL_TESTS_COMMAND}}` -> "cmd /c run_tests.bat", "npm test", "cargo test"
- `{{RUN_UNIT_TESTS_COMMAND}}` -> "Godot_v4.5.1_console.exe --headless -s addons/gut/gut_cmdln.gd"
- `{{LINT_COMMAND}}` -> "cmd /c lint.bat", "npm run lint", "cargo clippy"
- `{{SMOKE_TEST_COMMAND}}` -> "cmd /c smoke_test.bat", "npm run smoke", "cargo run --example smoke_test"

