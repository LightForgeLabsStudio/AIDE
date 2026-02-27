# AIDE Placeholder Contracts

Placeholders that AIDE skills and docs expect projects to define. Declare mappings in `AGENTS.md`.

## Required Placeholders

| Placeholder | Purpose |
| --- | --- |
| `{{PROJECT_NAME}}` | Project display name |
| `{{TECH_STACK}}` | Primary technologies |
| `{{MAIN_BRANCH}}` | Primary branch name |
| `{{PROJECT_DOMAIN}}` | Domain for agent commit signatures |

## Documentation Paths

| Placeholder | Purpose |
| --- | --- |
| `{{DEVELOPMENT_DOC}}` | Architecture reference |
| `{{CODING_GUIDELINES_DOC}}` | Code style rules |
| `{{TESTING_POLICY_DOC}}` | Test requirements |
| `{{CONTRIBUTING_DOC}}` | Workflow and PR process |
| `{{DOCUMENTATION_POLICY_DOC}}` | Doc standards |
| `{{BEST_PRACTICES_DOC}}` | Tech-specific patterns |
| `{{PROJECT_DESIGN_DOCS}}` | Design documentation directory |

## Quality Commands

| Placeholder | Purpose |
| --- | --- |
| `{{RUN_ALL_TESTS_COMMAND}}` | Run full test suite |
| `{{RUN_UNIT_TESTS_COMMAND}}` | Run unit tests only |
| `{{LINT_COMMAND}}` | Run linter |

## Required Label Conventions

- **`status:*`** — `status:ready`, `status:in-progress`, `status:needs-review` (required by `/issue`, `/implement`)
- **`area:*`** — `area:combat`, `area:ui` (required by `/issue`)
- **`priority:*`** — `priority:high`, `priority:medium`, `priority:low` (required by `/issue`)
- **GitHub Issue Type** — Feature, Bug, Technical Debt, Chore (set via `set-issue-type.py`)

## Declaration Format in AGENTS.md

```markdown
## AIDE Placeholder Mappings

| AIDE Placeholder | Project Value |
| --- | --- |
| `{{PROJECT_NAME}}` | Lightborn Exile: Divinity Engine |
| `{{LINT_COMMAND}}` | cmd /c lint.bat |
```
