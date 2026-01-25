# Coding Guidelines

Standards to keep {{PROJECT_NAME}} consistent and predictable. See [CONTRIBUTING.md](../core/CONTRIBUTING.md) for workflow; this file focuses on style and architecture.

## Core Principles

- **Deterministic behavior:** Keep core logic deterministic and reproducible; avoid unseeded randomness in critical systems
- **Follow language conventions:** Use idiomatic {{LANGUAGE}} style and {{FRAMEWORK}} patterns
- **System-appropriate architecture:** Follow established patterns for {{your domain}}
- **Single sources of truth:** Use authoritative modules for shared state/config; avoid duplicating state
- **Small, focused changes:** Prefer minimal diffs with matching test hooks and doc updates

## {{LANGUAGE}} Style

Follow {{STYLE_GUIDE_NAME}}:
- {{Style rule 1}}
- {{Style rule 2}}
- {{Style rule 3}}

**Reference:** {{STYLE_GUIDE_LINK}}

### Naming Conventions

- {{Convention 1}}: {{When to use}}
- {{Convention 2}}: {{When to use}}
- {{Convention 3}}: {{When to use}}

### Code Organization

- Add concise docstrings/comments for non-obvious logic or data flow
- Prefer guard clauses and short functions to keep state handling readable
- Keep data structures simple; use language idioms ({{examples}})
- Avoid new dependencies unless agreed; base stack is {{TECH_STACK}}

## Architecture Boundaries

For detailed architecture patterns, see [{{DEVELOPMENT_DOC}}]({{DEVELOPMENT_DOC}}).

**Key Boundaries:**
- **{{Boundary 1}}:** {{Description and enforcement rule}}
- **{{Boundary 2}}:** {{Description and enforcement rule}}
- **{{Boundary 3}}:** {{Description and enforcement rule}}

## {{Domain-Specific}} Implementation

{{DOMAIN_SPECIFIC_GUIDANCE}}

**Implementation Standards:**
- {{Standard 1}}
- {{Standard 2}}
- {{Standard 3}}

## Testing & Verification

- Add deterministic tests for logic where feasible (see [TESTING_POLICY.md](TESTING_POLICY.md))
- Prefer unit-style checks for {{critical systems}}
- Avoid {{anti-pattern}}; expose testable interfaces

## Git Commits

- Keep commits small and single-purpose; one concern per commit/branch
- Use imperative subjects (e.g., "Add user authentication"); note tests run in the body when applicable
- Commit code, tests, and doc updates together so expectations match behavior
- Avoid committing {{artifacts to avoid}}; gate logs behind config flags

## Documentation & Changelog

Follow [DOCUMENTATION_POLICY.md](../core/DOCUMENTATION_POLICY.md) for all documentation updates:
- Update user-facing docs for behavior/balance changes
- Update `{{DEVELOPMENT_DOC}}` for architecture/extension notes
- Avoid duplicating the same detail across files; use references instead

## Logging & Debugging

- Prefer structured debug helpers ({{examples}}) over ad hoc prints
- Make debug logging opt-in via config flags or debug builds
- Avoid shipping noisy output to {{production/release}}

---

## Reference Docs

**Related Standards:**
- [CONTRIBUTING.md](../core/CONTRIBUTING.md) - Workflow and collaboration process
- [{{DEVELOPMENT_DOC}}]({{DEVELOPMENT_DOC}}) - Architecture patterns and component details
- [TESTING_POLICY.md](TESTING_POLICY.md) - Testing requirements and practices
- [DOCUMENTATION_POLICY.md](../core/DOCUMENTATION_POLICY.md) - Documentation standards

**Design References:**
- `{{PROJECT_DESIGN_DOCS}}` - Design documentation

**External Style Guides:**
- {{STYLE_GUIDE_LINK}}

## Customization for Your Project

Replace these placeholders:

- `{{PROJECT_NAME}}` -> Your project name
- `{{LANGUAGE}}` -> "TypeScript", "Python", "Rust", "GDScript"
- `{{FRAMEWORK}}` -> "React", "Django", "Actix", "Godot"
- `{{TECH_STACK}}` -> "Node.js 20 + TypeScript 5", "Python 3.11 + FastAPI"
- `{{STYLE_GUIDE_NAME}}` -> "Airbnb JavaScript Style Guide", "PEP 8", "Rust Book"
- `{{STYLE_GUIDE_LINK}}` -> URL to official style guide
- `{{DEVELOPMENT_DOC}}` -> "docs/DEVELOPMENT.md", "docs/ARCHITECTURE.md"
- `{{PROJECT_DESIGN_DOCS}}` -> "docs/design/", "docs/architecture/"
- `{{DOMAIN_SPECIFIC_GUIDANCE}}` -> Guidance specific to your domain (web, game, CLI, etc.)
