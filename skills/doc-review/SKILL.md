---
name: doc-review
description: Review documentation for accuracy and drift (no code changes) and propose edits.
---

# Doc Review

Review documentation for correctness, alignment with code/GitHub state, and minimal duplication.

## Documentation Loading (role-based)

- Always use: project constraints + the docs/PR being reviewed.
- Stage-load: `docs/DOCUMENTATION_POLICY.md`.
- Stage-load (as needed): `docs/CONTRIBUTING.md`, `docs/DEVELOPMENT.md`, `docs/TESTING_POLICY.md` (only to validate doc claims), and relevant `design/` pillar(s).

## Inputs (ask first)

- Which docs (or PR) to review.
- Audience focus (dev workflow vs player-facing).

## Workflow

1) **Read doc rules**
   - Use project constraints + `docs/DOCUMENTATION_POLICY.md` (as needed).

2) **Cross-check**
   - Validate claims against code, GitHub state (issues/PRs), and design pillars.
   - Flag duplication and recommend the single best source of truth.

3) **Report**
   - Findings grouped by severity with `path:line` and suggested fix.

## Reference

- AIDE doc review primer: `.aide/docs/agents/DOC_REVIEW_START.md`
