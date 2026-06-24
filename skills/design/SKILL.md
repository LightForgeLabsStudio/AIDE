---
name: design
description: Design a feature or change into a reviewed system spec (plus a slim ADR only when the decision threshold is met). Outputs an accepted spec ready for /scope.
---

# Design

Create or update the **living system spec** for a feature or change. Read AGENTS.md if not in context. Taxonomy: `.aide/docs/core/DOCUMENT_TAXONOMY.md`.

## Inputs

Design question or topic. Timebox if relevant.

## Review-aware

Before starting: check if `<artifact>.findings.md` exists for this topic. If it does, read it and incorporate findings before proceeding.

## Workflow

1. **GitHub state check** — Run `gh issue list` and `gh pr list` to avoid proposing already-built or conflicting work.

2. **Locate the system spec** — Find the relevant spec in `docs/specs/` (project) or `.aide/docs/` (AIDE framework work). If none exists for this system, you will create one named for the system, not the feature.

3. **Shape options** — Produce 1 recommended option (+ 1 alternative max). Include: pros/cons, risks, dependencies, success validation.

4. **Draft** — Create or update `docs/specs/<system>.md` with frontmatter (`status: draft` for new specs). Binding rules go in the spec's **Invariants** section.

5. **ADR threshold check** — Also write a slim ADR to `docs/decisions/YYYY-MM-DD-<slug>.md` **only if all three hold**: real alternatives existed; the choice constrains future work; a newcomer could accidentally reverse it. The ADR points to the spec. Most features need no ADR.

6. **Cross-review** — Use `/findings` to exchange findings before accepting. Do not accept unreviewed specs.

7. **Accept** — Set spec frontmatter `status: accepted` (and ADR status if one was written). Hand off to `/scope` to decompose into GitHub issues (or, when the project elects a `docs/plans/` layer, an optional staged plan).

## Spec frontmatter

```yaml
---
title: <system name>
description: <one line>
status: draft | accepted | superseded
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

## ADR format (when threshold is met)

```
# Title
**Status:** Accepted (durable decision — current) | Executed (historical record) | Superseded by <file>
## Context
## Decision
## Rationale
## Consequences
```

## Reference

- Taxonomy + creation rule: `.aide/docs/core/DOCUMENT_TAXONOMY.md`
- Design pillars: `design/` directory
- Quick reference: `docs/DESIGN_QUICK_REFERENCE.md`
