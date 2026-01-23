# AIDE Agent Orientation

**AIDE** — AI-Assisted Development Environment. A universal framework for structured AI-human software collaboration.

---

## Agent Roles

| Role | Purpose | Primer |
|------|---------|--------|
| **Implementation** | Build features, fix bugs | [IMPLEMENTATION_START.md](docs/agents/IMPLEMENTATION_START.md) |
| **PR Review** | Review code quality, architecture | [PR_REVIEW_START.md](docs/agents/PR_REVIEW_START.md) |
| **Codebase Review** | Holistic health audits | [CODEBASE_REVIEW_START.md](docs/agents/CODEBASE_REVIEW_START.md) |
| **Design Spec** | Prioritize and spec features | [DESIGN_SPEC_START.md](docs/agents/DESIGN_SPEC_START.md) |
| **Design Workshop** | High-level design exploration | [DESIGN_WORKSHOP_START.md](docs/agents/DESIGN_WORKSHOP_START.md) |
| **Doc Review** | Documentation accuracy | [DOC_REVIEW_START.md](docs/agents/DOC_REVIEW_START.md) |

---

## Document Authority Hierarchy

### Tier 1: Authoritative (Binding)
Project-side documents satisfy AIDE contracts. Agents MUST read project's authority mapping first.

| Expectation | Project Must Provide |
|-------------|---------------------|
| Placeholder mappings | `AGENTS.md` or equivalent with `{{PLACEHOLDER}}` → value table |
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
0. Spec Intake      → Get issue/spec, extract goals
1. Codebase Survey  → Read targeted, NO CODING
2. Plan + Draft PR  → Get approval, create branch
3. Implement        → Code + tests, clean commits
4. Sanity Check     → Verify success criteria
5. Refinement       → Cleanup, best practices
6. PR Ready         → Mark for review
7. Report Back      → Summarize vs spec
8. Address Feedback → Fix review issues
9. Merge            → After approval
10. Sync Main       → Update local
```

---

## Entry Workflow

1. **Project provides orientation** → Read project's `AGENT_ORIENTATION.md` or `AGENTS.md`
2. **Resolve placeholders** → Map `{{PLACEHOLDERS}}` using project's table
3. **Load role primer** → Read appropriate primer from `docs/agents/`
4. **Execute workflow** → Follow primer end-to-end

---

## Required Project Contracts

Projects using AIDE MUST provide configuration. See [PLACEHOLDER_CONTRACTS.md](docs/agents/PLACEHOLDER_CONTRACTS.md) for:

- Required vs optional placeholder mappings
- Required GitHub label conventions (status, area, priority)
- Declaration format and validation checklist

---

*This document defines AIDE expectations. Projects satisfy them via explicit mappings.*
