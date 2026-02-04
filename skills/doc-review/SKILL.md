---
name: doc-review
description: Review documentation for accuracy and drift (no code changes): cross-check against sources of truth and propose edits.
---

# Doc Review

Review documentation for correctness, alignment with code/GitHub state, and minimal duplication.

## Inputs (ask first)

- Which docs (or PR) to review.
- Audience focus (dev workflow vs player-facing).

## Workflow

1) **Read doc rules**
   - `AGENTS.md` + `docs/DOCUMENTATION_POLICY.md` (as needed).

2) **Cross-check**
   - Validate claims against code, GitHub state (issues/PRs), and design pillars.
   - Flag duplication and recommend the single best source of truth.

3) **Report**
   - Findings grouped by severity with `path:line` and suggested fix.

## Reference

- AIDE doc review primer: `.aide/docs/agents/DOC_REVIEW_START.md`
