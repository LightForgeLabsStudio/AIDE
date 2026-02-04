---
name: codebase-review
description: Holistic codebase health review (no fixes): find architecture drift, dead code, test/doc gaps, and file follow-up issues.
---

# Codebase Review

Do a strategic, read-only review of the codebase (not PR-specific) and produce actionable findings.

## Inputs (ask first)

- Scope (domains/systems) and timebox.
- Target branch (default `main`).

## Workflow

1) **Read Tier 1 rules**
   - `AGENTS.md` + relevant project docs (architecture/testing/docs policy).

2) **Sample strategically**
   - Use recent GitHub activity to choose hotspots (issues/PRs, churn areas).
   - Check for determinism violations, duplicated systems, autoload/UI coupling, dead code/assets.

3) **Report**
   - Findings grouped by severity with `path:line` and impact.

4) **Track everything**
   - Create GitHub issues for all Critical/Major findings (use `/issue` workflow).

## Reference

- AIDE codebase review primer: `.aide/docs/agents/CODEBASE_REVIEW_START.md`
