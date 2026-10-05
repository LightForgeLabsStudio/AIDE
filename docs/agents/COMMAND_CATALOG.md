# AIDE Command Catalog

Tool-agnostic skill definitions. Authority lives in each skill's `SKILL.md`; this catalog is a navigation aid.

## Design Goals

- Reduce "agent parses prose" variability
- Keep default context lean (link out, don't preload)
- Respect project Tier 1 rules and constraints
- Be composable — small commands that chain

## Skill Set

| Skill | Intent |
| --- | --- |
| `/implement` | Implement a ticket or requirements through a draft PR and review handoff |
| `/design` | Design a feature into a reviewed ADR |
| `/scope` | Decompose an accepted ADR into GitHub issues |
| `/findings` | Cross-cutting review protocol that writes reviewer findings files |
| `/pr-review` | Review the current PR head against its ticket and submit commit-specific findings |
| `/pr-draft` | Create or update a draft PR with validated body |
| `/pr-ready` | Validate and flip a PR from draft to ready |
| `/codebase-review` | Holistic read-only codebase health review |
| `/doc-review` | Documentation accuracy and drift review |
| `/quality` | Run lint and tests from project placeholder mappings |
| `/handoff` | Session handoff note for context resets |
| `/sync` | End-of-session git sync (pull, push, verify) |
| `/issue` | Create a labeled GitHub issue |
| `/evolve` | Turn repeated failures into rules or automation |
| `/skill-author` | Create or update an AIDE skill |

## Chaining Flow

```text
/design → ADR → /scope → GitHub issues → /implement (includes draft PR)
                                           ↓
                                      /pr-review
                                           ↓
                           accepted findings → /implement

/pr-ready marks the validated PR ready when requested; merging is a separate action.
```

## Implementation Guidance

- Use project placeholder mappings for exact commands (`{{LINT_COMMAND}}`, etc.).
- Prefer automation (CI checks) when a failure mode is enforceable.
- Keep outputs structured and brief; link to authoritative docs for detail.
