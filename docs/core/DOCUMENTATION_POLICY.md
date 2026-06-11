# Documentation Policy (Template)

> **Template — instantiate, don't point.** Copy this into your project as `docs/DOCUMENTATION_POLICY.md`, replace placeholders, and delete sections that don't apply. Do **not** ship a stub that defers to this file: the `.aide/` pin is not your project's source of truth. Kernel references: [DOCUMENT_TAXONOMY.md](DOCUMENT_TAXONOMY.md), [DOCUMENTATION_PRINCIPLES.md](DOCUMENTATION_PRINCIPLES.md).

## Taxonomy (six homes, two flavors)

| Home | Question answered | Flavor |
| --- | --- | --- |
| `{{DESIGN_DIRECTORY}}` | Why does this product exist and feel this way? | Living |
| `docs/specs/` | What is true of this system now, and what must remain true? | Living |
| `docs/decisions/` | What did we choose that is hard to reverse, and why? | Dated |
| GitHub epics/issues | How and when? | Executed and closed — these are the plans |
| `docs/evaluations/` | What did we learn? | Dated |
| Conventions ({{CODING_GUIDELINES_DOC}}, {{TESTING_POLICY_DOC}}, {{CONTRIBUTING_DOC}}) | How do we work? | Living |

**Living** docs claim to be current and are the only maintenance burden — keep the set small. **Dated** records are append-only and never edited after the fact (status lines only).

## Creation Rule

> System truth → spec. Hard-to-reverse choice → ADR. Execution → issue.

- A **spec** (`docs/specs/<system>.md`) is the living description of a system, with status frontmatter and a binding **Invariants** section. Load it before modifying that system. When executed work changes invariants, updating the spec is part of the work.
- An **ADR** (`docs/decisions/YYYY-MM-DD-slug.md`) is written only when real alternatives existed, the choice constrains future work, and a newcomer could accidentally reverse it.
- **Plans are GitHub issues.** There is no plans folder. No contracts/reports/review/handoffs folders either — see the taxonomy doc for where that content lives.

## Update Rules

- Update only the relevant source; never duplicate the same fact across files — link instead.
- When behavior changes: README for users, {{DEVELOPMENT_DOC}} for developers, the system spec for invariants.
- Implementation state is queried from GitHub (`{{IMPLEMENTATION_STATUS_QUERY}}`), never tracked in markdown snapshots.
- Git commits serve as the changelog during active development; a formal `CHANGELOG.md` is optional until public release.

## Allowed Exception: Token-Efficient Summaries

Condensed agent summaries (e.g. `DESIGN_QUICK_REFERENCE.md`) may duplicate content when they clearly state they are non-authoritative, link the source, and are kept synchronized.

## Placeholders

- `{{DESIGN_DIRECTORY}}` → `design/`, `docs/design/`
- `{{DEVELOPMENT_DOC}}` → `docs/DEVELOPMENT.md`, `docs/ARCHITECTURE.md`
- `{{CODING_GUIDELINES_DOC}}` / `{{TESTING_POLICY_DOC}}` / `{{CONTRIBUTING_DOC}}` → your convention docs
- `{{IMPLEMENTATION_STATUS_QUERY}}` → e.g. `gh issue list --label "status:in-progress"`
