# ADR: Documentation Taxonomy — Living Specs, Dated Decisions, GitHub-Issue Plans

**Date:** 2026-06-10
**Status:** Accepted
**Area:** Documentation / AI Workflow

---

## Context

AIDE's documentation guidance grew organically and host projects show the strain. An audit of the first adopter (Lightborn Exile, issue #973) found:

- **ADRs doing double duty as specs.** `/design` is hard-wired to emit an ADR, so 31 "decision records" accumulated where roughly a third are durable decisions and the rest are feature specs or already-executed work. Superseded decisions carry no machine-readable status; knowing which is live requires tribal knowledge.
- **Transient artifacts filed as documentation.** Session handoffs, PR findings files from an abandoned review protocol, and one-shot reports sit alongside canonical truth.
- **Pointer stubs that bounce into the submodule.** Project doc policy was a stub deferring to `.aide/docs/core/DOCUMENTATION_POLICY.md` — an extra discovery hop, and the submodule pin can drift from what the project actually does.
- **No creation policy.** Nothing states when a contract/spec/ADR should exist, so categories were invented ad hoc (`docs/contracts/`, `docs/reports/`, `docs/review/`).

The [Build-A-Better-Business/docs-template](https://github.com/Build-A-Better-Business/docs-template) repository offers a documentation kernel — a document taxonomy plus documentation principles (pointer/canonical/on-demand patterns, anti-pattern list, decision framework). AIDE has the workflow layer (skills, issue tooling, agent primers) that template lacks. The question was whether AIDE should absorb the kernel, and what taxonomy fits AIDE's model where GitHub issues — not plan documents — carry execution.

## Decision

AIDE absorbs a documentation kernel adapted from docs-template. AIDE defines **shapes** (taxonomy, frontmatter schemas, principles, templates); host projects own all **instances**. No project document may point into `.aide` for its substance.

### Taxonomy: six homes, two flavors

The dividing line is **time**, not content. A document either *claims to be current* (living — the only maintenance burden) or *records a moment* (dated — append-only, cannot drift because it does not claim currency).

| Home | Question answered | Flavor |
|---|---|---|
| `design/` (or project equivalent) | Why does this product exist and feel this way? | Living |
| `docs/specs/` | What is true of this system now, and what must remain true? | Living — matures with the architecture |
| `docs/decisions/` | What did we choose that is hard to reverse, and why? | Dated, append-only |
| GitHub epics/issues | How and when? | Executed and closed — these **are** the plans |
| `docs/evaluations/` | What did we learn? | Dated, append-only |
| Conventions (coding guidelines, testing policy, contributing) | How do we work? | Living |

### Specs are living system documents

A spec is the canonical description of a system as it exists and should exist: its model, its shape, and an explicit **Invariants** section carrying binding "what must remain true" rules (the role previously played by standalone contract documents, which fold into specs). Specs are updated as architecture matures and carry status frontmatter:

```yaml
---
title: <system name>
description: <one line>
status: draft | accepted | superseded
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

### Creation rule (one line)

> System truth → spec. Hard-to-reverse choice → ADR. Execution → issue.

ADR threshold (from docs-template): real alternatives existed, the choice constrains future work, and a newcomer could accidentally reverse it. Most features never need one.

### There is no plans folder

Execution detail lives in GitHub epics and issues produced by `/scope` via the issue-creator tool. Plan documents are explicitly rejected: they would duplicate the issue tracker and rot.

### Workflow changes

- `/design` no longer emits an ADR by default. It **creates or updates the relevant system spec**, extracts a slim ADR only when the threshold is met, then hands to `/scope`.
- `/scope` reads the spec (and ADR if present) and decomposes into issues. Unchanged otherwise.
- Closing step of any accepted spec or executed epic that establishes new invariants: update the relevant living spec. This is how living docs stay current without a separate audit habit.

### Naming

- Dated records: `YYYY-MM-DD-slug.md` (retained over docs-template's `NNNN-slug` — better for small teams, no renumbering churn).
- Living specs: `slug.md` named for the system, not the feature increment.

## Rationale

- **Two flavors is the solo-dev/agent maintainability answer.** The living set is the entire maintenance burden; keep it small (a handful of specs + conventions). Dated records accumulate freely without rotting.
- **Folding contracts into specs removes a category without losing teeth.** Existing contract docs already blend system description with invariants; the Invariants section preserves binding force on the load-before-you-touch path.
- **Specs-as-living matches docs-template intent** (RFC/superseded are *statuses* with `last_updated`; documents mature) while plans-as-issues matches AIDE's existing tooling.
- **Shapes-vs-instances fixes pointer-stub drift.** Projects instantiate real policy files from AIDE templates instead of deferring into a submodule pin.

## Consequences

- AIDE gains canonical kernel docs (taxonomy + documentation principles) adapted from docs-template; `.aide/docs/core/DOCUMENTATION_POLICY.md` and the standards templates are rewritten around the taxonomy and creation rule.
- `/design` and `/scope` skill definitions need updating (spec-first output, ADR threshold).
- Project templates (`PROJECT_SUMMARY`, `README`, doc-policy) updated to instantiate rather than point.
- Host projects migrate incrementally: classify existing decisions with status frontmatter in place (no mass rewrites), fold contracts into `docs/specs/`, rename `reports/` → `docs/evaluations/`, archive or delete transient artifacts.
- First adopter migration is tracked in Lightborn Exile issue #973 and its follow-up issues.
