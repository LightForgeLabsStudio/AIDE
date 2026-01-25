# System Evolution (Decision Tree + Triggers)

Use this when a mistake repeats or a new invariant becomes clear. The goal is to prevent recurrence with the smallest effective change.

## Trigger Criteria (any)
- The same mistake happens in 2+ sessions or PRs
- A design or architecture decision affects multiple systems or future work
- A failure is easily enforceable via automation (lint/test/script/CI)

## Decision Tree (choose the smallest effective scope)

1) **Is the failure enforceable by automation?**
- Yes -> add or update tooling/CI checks (preferred)
- No -> go to 2

2) **Does the rule need to be project-wide and binding?**
- Yes -> add a Tier 1 constraint (AGENTS / CODING_GUIDELINES / TESTING_POLICY / CONTRIBUTING)
- No -> go to 3

3) **Is it system-specific or contextual?**
- Yes -> add Tier 2 guidance (DEVELOPMENT.md, design pillar, or system doc)
- No -> document as reference-only (examples or optional templates)

## How to Write the Rule
- Write a positive constraint ("Do X"), not only a prohibition ("Don't do Y")
- Place it at the narrowest scope that prevents repeats
- Reference the motivating issue/PR in the new rule or commit/PR description

## Output Checklist
- Decision: automation vs Tier 1 vs Tier 2 vs reference-only
- Location: file and section to update
- Example: one concrete rule or check
