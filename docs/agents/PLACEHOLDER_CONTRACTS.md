# AIDE Placeholder Contracts

This document defines all placeholders that AIDE primers expect projects to provide. Projects using AIDE **must** map these placeholders in their agent configuration (typically `AGENTS.md`).

---

## Required Placeholders (Core Primers)

These placeholders are used in core agent primers and **must** be mapped for proper operation.

### Project Identity

| Placeholder | Purpose | Example |
|-------------|---------|---------|
| `{{PROJECT_NAME}}` | Project display name | `MyApp` |
| `{{TECH_STACK}}` | Primary technologies | `Node.js 20 + TypeScript 5.3` |
| `{{PROJECT_DOMAIN}}` | Domain for agent signatures | `myapp.dev` |
| `{{MAIN_BRANCH}}` | Primary branch name | `main` |

### Documentation Paths

| Placeholder | Purpose | Example |
|-------------|---------|---------|
| `{{DEVELOPMENT_DOC}}` | Architecture reference | `docs/DEVELOPMENT.md` |
| `{{CODING_GUIDELINES_DOC}}` | Code style rules | `docs/CODING_GUIDELINES.md` |
| `{{TESTING_POLICY_DOC}}` | Test requirements | `docs/TESTING_POLICY.md` |
| `{{CONTRIBUTING_DOC}}` | Workflow and PR process | `docs/CONTRIBUTING.md` |
| `{{DOCUMENTATION_POLICY_DOC}}` | Doc standards | `docs/DOCUMENTATION_POLICY.md` |
| `{{BEST_PRACTICES_DOC}}` | Tech-specific patterns | `docs/REACT_PATTERNS.md` |
| `{{HIGH_LEVEL_VISION_DOC}}` | Project vision/goals | `docs/VISION.md` |
| `{{PROJECT_DESIGN_DOCS}}` | Design documentation | `docs/architecture/` |
| `{{GITHUB_QUERIES_DOC}}` | GitHub CLI query reference | `.aide/docs/agents/GITHUB_QUERIES.md` |

### Testing Commands

| Placeholder | Purpose | Example |
|-------------|---------|---------|
| `{{UNIT_TEST_TYPE}}` | Unit test description | `Jest unit tests` |
| `{{INTEGRATION_TEST_TYPE}}` | Integration test description | `Playwright e2e tests` |
| `{{RUN_ALL_TESTS_COMMAND}}` | Run full test suite | `npm test` |
| `{{RUN_UNIT_TESTS_COMMAND}}` | Run unit tests only | `npm run test:unit` |
| `{{LINT_COMMAND}}` | Run linter | `npm run lint` |
| `{{SMOKE_TEST_COMMAND}}` | Quick validation | `npm run smoke` |

---

## Optional Placeholders (Templates Only)

These placeholders appear in example templates but are **not required** for core primer operation. Map them only if using the corresponding templates.

### Language/Framework

| Placeholder | Purpose |
|-------------|---------|
| `{{LANGUAGE}}` | Programming language |
| `{{LANGUAGE_EXTENSION}}` | File extension (e.g., `.ts`) |
| `{{FRAMEWORK}}` | Framework name |
| `{{STYLE_GUIDE_NAME}}` | Style guide reference |
| `{{STYLE_GUIDE_LINK}}` | Style guide URL |

### Testing (Extended)

| Placeholder | Purpose |
|-------------|---------|
| `{{UNIT_TEST_FRAMEWORK}}` | Test framework name |
| `{{UNIT_TEST_PATH}}` | Test file location |
| `{{UNIT_TEST_EXAMPLE}}` | Example test code |
| `{{INTEGRATION_TEST_FRAMEWORK}}` | Integration framework |
| `{{INTEGRATION_TEST_PATH}}` | Integration test location |
| `{{INTEGRATION_TEST_EXAMPLE}}` | Example integration test |
| `{{RUN_SPECIFIC_UNIT_TEST_COMMAND}}` | Run single unit test |
| `{{RUN_SPECIFIC_INTEGRATION_TEST_COMMAND}}` | Run single integration test |
| `{{RUN_INTEGRATION_TESTS_COMMAND}}` | Run all integration tests |
| `{{TARGET_COVERAGE}}` | Coverage target percentage |

### Project Setup

| Placeholder | Purpose |
|-------------|---------|
| `{{INSTALL_COMMAND}}` | Dependency install command |
| `{{RUN_COMMAND}}` | Start application command |
| `{{TEST_COMMAND}}` | Generic test command |
| `{{LICENSE_TYPE}}` | License identifier |
| `{{DESIGN_DOCS_PATH}}` | Design docs directory |
| `{{DOMAIN_SPECIFIC_GUIDANCE}}` | Domain-specific notes |

---

## Declaration Location

Projects **must** declare placeholder mappings in one of:

1. **`AGENTS.md`** (recommended) — Dedicated agent configuration at repo root
2. **`AGENT_ORIENTATION.md`** — If combined with orientation
3. **Custom location** — Must be referenced from AI entry point

### Mapping Format

Use a table format for clarity:

```markdown
## AIDE Placeholder Mappings

| AIDE Placeholder | Project Value |
|------------------|---------------|
| `{{PROJECT_NAME}}` | MyApp |
| `{{TECH_STACK}}` | Node.js + TypeScript |
...
```

---

## Validation

A project satisfies this contract when:

- [ ] All **Required Placeholders** are mapped
- [ ] Mapping document is referenced from AI orientation/entry point
- [ ] Mapped paths resolve to existing files
- [ ] Commands are valid for the project's environment

---

*This document defines AIDE expectations. Projects satisfy them via explicit mappings.*
