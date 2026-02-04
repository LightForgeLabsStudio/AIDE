---
name: codebase-review
description: Holistic codebase health review (no fixes): find architecture drift, dead code, test/doc gaps, and file follow-up issues.
---

# Codebase Review

Do a strategic, read-only review of the codebase (not PR-specific) and produce actionable findings.

## Documentation Loading (role-based)

- Always use: project constraints + current GitHub activity (issues/PRs).
- Stage-load: `docs/DEVELOPMENT.md`, `docs/CODING_GUIDELINES.md`, `docs/TESTING_POLICY.md`, `docs/DOCUMENTATION_POLICY.md`.
- Stage-load (as needed): relevant `design/` pillar(s) and `docs/DESIGN_QUICK_REFERENCE.md`.

## Inputs (ask first)

- Scope (domains/systems) and timebox.
- Target branch (default `main`).

## Workflow

1) **Read Tier 1 rules**
   - Use the project's constraints (already loaded in this environment) + relevant project docs (architecture/testing/docs policy).

2) **Sample strategically**
   - Use recent GitHub activity to choose hotspots (issues/PRs, churn areas).
   - Check for determinism violations, duplicated systems, autoload/UI coupling, dead code/assets.

3) **Report**
   - Findings grouped by severity with `path:line` and impact.

4) **Track everything**
   - Create GitHub issues for all Critical/Major findings (use `/issue` workflow).

## Reference

- AIDE codebase review primer: `.aide/docs/agents/CODEBASE_REVIEW_START.md`
