# Development Guide

Technical reference for extending and debugging {{PROJECT_NAME}}.

## Architecture Overview

**{{Architecture Pattern}}**

- **{{Component Type 1}}**: {{Description and responsibilities}}
- **{{Component Type 2}}**: {{Description and responsibilities}}
- **{{Component Type 3}}**: {{Description and responsibilities}}

## Core Components

### 1. {{Component Name 1}}

- {{Responsibility}}
- {{Key interfaces/APIs}}
- {{Location in codebase}}

### 2. {{Component Name 2}}

- {{Responsibility}}
- {{Key interfaces/APIs}}
- {{Location in codebase}}

### 3. {{Component Name 3}}

- {{Responsibility}}
- {{Key interfaces/APIs}}
- {{Location in codebase}}

## {{Domain}} Architecture Notes

{{Domain-specific architecture details}}

## Testing

- Prefer small, deterministic tests for {{core logic}}
- Use {{test framework}} for {{test type}}
- Avoid visual-only verification; expose testable interfaces

## Common Tasks

| Task | How To |
|------|--------|
| {{Task 1}} | {{Instructions}} |
| {{Task 2}} | {{Instructions}} |
| {{Task 3}} | {{Instructions}} |
| {{Task 4}} | {{Instructions}} |
| {{Task 5}} | {{Instructions}} |

## Reference Docs

- [CONTRIBUTING.md](../core/CONTRIBUTING.md) - Full workflow
- [CODING_GUIDELINES.md](CODING_GUIDELINES.md) - Code standards
- `{{PROJECT_DESIGN_DOCS}}` - Design documentation
- [agents/PR_REVIEW_START.md](../agents/PR_REVIEW_START.md) - Review checklist

## Customization for Your Project

Replace these placeholders:

- `{{PROJECT_NAME}}` -> Your project name
- `{{Architecture Pattern}}` -> "Microservices", "MVC", "Component-Based", "Scene-Driven"
- `{{Component Type 1/2/3}}` -> Your architecture's main components
- `{{Component Name 1/2/3}}` -> Specific key components in your project
- `{{Domain}}` -> "Web", "Game", "CLI", "Mobile", "Backend"
- `{{PROJECT_DESIGN_DOCS}}` -> "docs/design/", "docs/architecture/"
