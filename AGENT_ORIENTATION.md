# AIDE Agent Orientation

**AIDE** — AI-Assisted Development Environment. A universal framework for structured AI-human software collaboration.

---

## Agent Workflow Model

AIDE uses **skills** — task-focused, self-contained workflow definitions — instead of role primers.

| Skill | Purpose |
| --- | --- |
| `/implement` | Build features, fix bugs, end-to-end |
| `/design` | Design exploration → ADR |
| `/scope` | Decompose ADR into GitHub issues |
| `/pr-review` | Review code quality, architecture |
| `/pr-draft`, `/pr-ready` | PR lifecycle |
| `/codebase-review` | Holistic health audits |
| `/doc-review` | Documentation accuracy |
| `/findings` | Cross-cutting review protocol that writes reviewer findings files |
| `/quality`, `/handoff`, `/sync`, `/issue`, `/evolve`, `/skill-author` | Utilities |

Full catalog: `docs/agents/COMMAND_CATALOG.md`

---

## Document Authority Hierarchy

### Tier 0: Always-Available

Project's `AGENTS.md` — placeholder mappings, critical invariants, skill entry workflow. Always in context.

### Tier 1: Authoritative (Binding)
Project-side documents satisfy AIDE contracts.

| Expectation | Project Must Provide |
| --- | --- |
| Placeholder mappings | `AGENTS.md` with `{{PLACEHOLDER}}` → value table |
| Code style rules | `{{CODING_GUIDELINES_DOC}}` |
| Test requirements | `{{TESTING_POLICY_DOC}}` |
| Workflow rules | `{{CONTRIBUTING_DOC}}` |

### Tier 2: Compact Reference (On-Demand)

AIDE provides compact reference files in `docs/agents/`. Skills load these only when needed — not preloaded.

| File | Purpose |
| --- | --- |
| `COMMAND_CATALOG.md` | Skill directory with chaining flows |
| `GITHUB_QUERIES.md` | GraphQL queries for issue relationships |
| `GITHUB_LABELS.md` | Label taxonomy and conventions |
| `PLACEHOLDER_CONTRACTS.md` | Placeholder resolution rules |
| `issue-creator-ref.md` | Issue creator format and error handling |
| `ERROR_RECOVERY.md` | Recovery loop and failure modes |
| `AGENT_COLLABORATION.md` | Spec gap decision tree |
| `TOKEN_ECONOMY.md` | Context budget strategies |
| `SYSTEM_EVOLUTION.md` | Decision tree for scoping rules |

### Tier 3: Examples (Non-Binding)
`docs/examples/` — tech-stack-specific templates. Copy and customize; do not follow directly.

---

## Entry Workflow

1. **Read project `AGENTS.md`** — placeholders, invariants, skill entry workflow
2. **Resolve placeholders** — map `{{PLACEHOLDERS}}` using project's table
3. **Choose a skill** — invoke the right skill for the task; consult `COMMAND_CATALOG.md` if unsure
4. **Execute workflow** — skills are self-contained; follow end-to-end; load Tier 2 refs only when needed

---

## Documentation Loading

- **Tier 0:** Project `AGENTS.md` — always in context
- **Tier 1:** Skills — loaded on invocation, self-contained
- **Tier 2:** `docs/agents/` compact refs — loaded on demand from skills
- **Rule:** Never preload deep reference material. Default startup should read only `AGENTS.md`.

---

## Required Project Contracts

Projects using AIDE MUST provide configuration. See `docs/agents/PLACEHOLDER_CONTRACTS.md` for:

- Required vs optional placeholder mappings
- Required GitHub label conventions (status, area, priority)
- Declaration format and validation checklist

---

*This document defines AIDE expectations. Projects satisfy them via explicit mappings in `AGENTS.md`.*
