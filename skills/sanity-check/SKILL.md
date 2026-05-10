---
name: sanity-check
description: Skeptical gap analysis for issues, ADRs, plans, and docs. Use when the user wants a second-pass check for missing decisions, contradictions, edge cases, hidden dependencies, scope drift, or readiness before implementation.
---

# Sanity Check

Perform a skeptical second pass on one artifact.

## Inputs

- Issue, ADR, plan, or doc text/path.
- Optional emphasis: readiness, scope, tests, architecture, or churn risk.

## Workflow

1. Read [AGENTS.md](../../AGENTS.md) and the artifact.
2. Restate the core claim in one sentence.
3. Check for missing decisions, contradictions, hidden dependencies, edge cases, test gaps, and scope drift.
4. Compare against nearby repo conventions or code only when needed to verify a claim.
5. Report only actionable gaps, ordered by severity: blocking, non-blocking, already covered.
6. End with one of: ready, needs clarification, or needs follow-up.

## Output

- Short summary.
- Findings first, with concrete references when available.
- Explicit list of unanswered questions or assumptions.
- Smallest next step.

## Rules

- Be skeptical and specific.
- Prefer omissions over restatements.
- Do not edit code, docs, or tests unless the user explicitly asks.
- Call out likely churn now, not later.
- If no gaps are found, say so and note residual risks.

## Reference

- [AGENTS.md](../../AGENTS.md)
