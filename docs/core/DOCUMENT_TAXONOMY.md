# Document Taxonomy

Canonical AIDE documentation kernel. Defined by ADR [2026-06-10-documentation-taxonomy-living-specs.md](../decisions/2026-06-10-documentation-taxonomy-living-specs.md), adapted from [Build-A-Better-Business/docs-template](https://github.com/Build-A-Better-Business/docs-template).

**AIDE defines shapes; projects own instances.** No project document may point into `.aide/` for its substance — projects instantiate real files from AIDE templates. The submodule pin must never be a project's source of truth.

## Six Homes, Two Flavors

The dividing line is **time**, not content. A document either *claims to be current* (living — the only maintenance burden) or *records a moment* (dated — append-only, cannot drift because it does not claim currency).

| Home | Question answered | Flavor |
| --- | --- | --- |
| `design/` (or project equivalent) | Why does this product exist and feel this way? | **Living** |
| `docs/specs/` | What is true of this system now, and what must remain true? | **Living** |
| `docs/decisions/` | What did we choose that is hard to reverse, and why? | Dated |
| GitHub epics/issues | How and when? | Executed and closed — these **are** the plans |
| `docs/evaluations/` | What did we learn? | Dated |
| Conventions (coding guidelines, testing policy, contributing) | How do we work? | **Living** |

Plus `docs/archive/` for superseded material retained as historical context.

## Creation Rule

> **System truth → spec. Hard-to-reverse choice → ADR. Execution → issue.**

ADR threshold: real alternatives existed, the choice constrains future work, and a newcomer could accidentally reverse it. Most features never need one.

## Specs Are Living System Documents

A spec is the canonical description of a **system** (not a feature increment): its model, its current shape, and an explicit **Invariants** section carrying binding "what must remain true" rules. Specs are updated as architecture matures — they are the load-before-you-touch layer for agents.

Frontmatter schema:

```yaml
---
title: <system name>
description: <one line>
status: draft | accepted | superseded
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

Closing step of any executed epic or accepted decision that establishes new invariants: **update the relevant living spec.** This is how living docs stay current without a separate audit habit.

## Dated Records

- **Decisions (ADRs)** — slim records: Context, Decision, Rationale, Consequences. Status values: `Accepted (durable decision — current)`, `Executed (historical record)`, `Superseded by <file>`. Never edited after the fact except to update status.
- **Evaluations** — audits, reviews, research, retrospectives. Replaces `reports/` naming.

## Explicitly Rejected Categories

- **No `plans/` folder.** Execution detail lives in GitHub epics and issues. Plan documents duplicate the tracker and rot.
- **No `contracts/` folder.** Invariants live inside the relevant spec's Invariants section — on the load path, not in a separate archive.
- **No `reports/` / `review/` / `handoffs/` folders.** Evaluations are dated records in `docs/evaluations/`; PR reviews live on GitHub; session handoffs are transient (archive or delete).
- **No implementation-status snapshots.** Query GitHub (`gh`) for live state.

## Naming

- Dated records: `YYYY-MM-DD-slug.md` (preferred over `NNNN-slug` — no renumbering churn).
- Living specs: `slug.md`, named for the system, not the feature increment.

## See Also

- [DOCUMENTATION_PRINCIPLES.md](DOCUMENTATION_PRINCIPLES.md) — design principles, patterns, anti-patterns
- [DOCUMENTATION_POLICY.md](DOCUMENTATION_POLICY.md) — instantiable project policy template
