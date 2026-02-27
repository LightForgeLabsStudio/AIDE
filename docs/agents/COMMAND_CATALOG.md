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
| `/implement` | Execute a GitHub issue or spec end-to-end |
| `/design` | Design a feature into a reviewed ADR |
| `/scope` | Decompose an accepted ADR into GitHub issues |
| `/review` | Cross-cutting artifact review (two-file protocol) |
| `/pr-review` | Review a PR for spec alignment, arch, tests, docs |
| `/pr-draft` | Create a draft PR with validated body |
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
/design → ADR → /scope → GitHub issues → /implement → /pr-draft → /pr-ready
                                       ↑                           ↓
                                  /review                      /pr-review
```

## Implementation Guidance

- Use project placeholder mappings for exact commands (`{{LINT_COMMAND}}`, etc.).
- Prefer automation (CI checks) when a failure mode is enforceable.
- Keep outputs structured and brief; link to authoritative docs for detail.
