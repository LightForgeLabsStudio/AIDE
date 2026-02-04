# AIDE Agent Orientation

**AIDE** — AI-Assisted Development Environment. A universal framework for structured AI-human software collaboration.

---

## Agent Roles

| Role | Purpose | Primer |
|------|---------|--------|
| **Implementation** | Build features, fix bugs | [IMPLEMENTATION_START.md](docs/agents/IMPLEMENTATION_START.md) |
| **PR Review** | Review code quality, architecture | [PR_REVIEW_START.md](docs/agents/PR_REVIEW_START.md) |
| **Codebase Review** | Holistic health audits | [CODEBASE_REVIEW_START.md](docs/agents/CODEBASE_REVIEW_START.md) |
| **Design** | Design exploration + issue-ready specs | [DESIGN_WORKSHOP_START.md](docs/agents/DESIGN_WORKSHOP_START.md) + [DESIGN_SPEC_REFERENCE.md](docs/agents/design/DESIGN_SPEC_REFERENCE.md) |
| **Doc Review** | Documentation accuracy | [DOC_REVIEW_START.md](docs/agents/DOC_REVIEW_START.md) |

---

## Document Authority Hierarchy

### Tier 1: Authoritative (Binding)
Project-side documents satisfy AIDE contracts. Agents MUST read project's authority mapping first.

| Expectation | Project Must Provide |
|-------------|---------------------|
| Placeholder mappings | `AGENTS.md` or equivalent with `{{PLACEHOLDER}}` -> value table |
| Code style rules | `{{CODING_GUIDELINES_DOC}}` |
| Test requirements | `{{TESTING_POLICY_DOC}}` |
| Workflow rules | `{{CONTRIBUTING_DOC}}` |

### Tier 2: Framework Reference (AIDE)
AIDE provides workflow structure. Projects customize via placeholder mappings.

| Document | Purpose |
|----------|---------|
| [docs/agents/*.md](docs/agents/) | Role-specific workflow primers |
| [docs/core/*.md](docs/core/) | Process templates |
| [AGENT_OPERATIONAL_TOKEN_ECONOMY.md](docs/agents/AGENT_OPERATIONAL_TOKEN_ECONOMY.md) | Efficiency guidelines |

### Tier 3: Examples (Non-Binding)
Reference implementations. Copy and customize, do not follow directly.

| Path | Purpose |
|------|---------|
| [docs/examples/](docs/examples/) | Tech-stack-specific templates |

---

## Workflow Stages (Implementation)

```
0. Spec Intake      -> Get issue/spec, extract goals
1. Codebase Survey  -> Read targeted, NO CODING
2. Plan + Draft PR  -> Get approval, create branch
3. Implement        -> Code + tests, clean commits
4. Sanity Check     -> Verify success criteria
5. Refinement       -> Cleanup, best practices
6. PR Ready         -> Mark for review
7. Report Back      -> Summarize vs spec
8. Address Feedback -> Fix review issues
9. Merge            -> After approval
10. Sync Main       -> Update local
```

---

## Entry Workflow

1. **Project provides orientation** -> Read project's `AGENT_ORIENTATION.md` or `AGENTS.md`
2. **Resolve placeholders** -> Map `{{PLACEHOLDERS}}` using project's table
3. **Pick the right role** -> If unsure, use [SKILL_ROUTER.md](docs/agents/SKILL_ROUTER.md)
4. **Load role primer** -> Read appropriate primer from `docs/agents/`
5. **Execute workflow** -> Follow primer end-to-end

If you hit failures mid-work (tests failing, conflicts, scope pivots), use: [ERROR_RECOVERY.md](docs/agents/ERROR_RECOVERY.md)

---

## Documentation Loading Policy (Always-Load vs On-Demand)

To enforce token discipline, agent-facing documentation is classified by when it should be loaded.

### Always-loaded (minimal, authoritative)
Load these by default at session start:

- Project `AGENT_ORIENTATION.md` or `AGENTS.md` (Tier 1 authority and placeholder mappings)
- This document: `AGENT_ORIENTATION.md` (AIDE entry + authority model)

### Stage-loaded (situational, load only when you reach the stage)
Load these only when the current task/stage needs them:

- Role primer for the active role (for example, `docs/agents/IMPLEMENTATION_START.md`)
- `docs/agents/AGENT_OPERATIONAL_TOKEN_ECONOMY.md` when doing implementation/review work
- `docs/agents/GITHUB_QUERIES.md` when querying issues/PRs via `gh`
- `docs/agents/GITHUB_LABELS.md` when applying/creating labels
- `docs/agents/PLACEHOLDER_CONTRACTS.md` when validating or authoring project placeholder mappings
- `docs/agents/SYSTEM_EVOLUTION.md` when applying `/evolve` or updating constraints

### Optional (tooling/skills)
If your tool supports reusable commands (skills), consult:

- `docs/agents/COMMAND_CATALOG.md` for a tool-agnostic slash-command catalog
- `docs/core/SESSION_HANDOFF.template.md` for a standard session handoff format

### Reference-only (on-demand deep reads)
Load only when explicitly needed for a decision or template:

- `docs/core/` templates
- `docs/examples/` examples
- Any long-form guidance not required to execute the current stage

Rule of thumb: default startup should not preload deep reference material. Prefer targeted reads linked from the current role/stage doc.

---

## Required Project Contracts

Projects using AIDE MUST provide configuration. See [PLACEHOLDER_CONTRACTS.md](docs/agents/PLACEHOLDER_CONTRACTS.md) for:

- Required vs optional placeholder mappings
- Required GitHub label conventions (status, area, priority)
- Declaration format and validation checklist

---

*This document defines AIDE expectations. Projects satisfy them via explicit mappings.*
