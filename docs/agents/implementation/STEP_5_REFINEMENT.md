# Implementation Agent - Step 5: Code Refinement

**Navigation:** [Index](../IMPLEMENTATION_START.md) | Prev: [Step 4](STEP_4_SANITY_CHECK.md) | Next: [Step 6](STEP_6_PR_READY.md)

## Purpose
Cleanup, simplify, and align with best practices after the spec is verified, before requesting review.

## Prerequisites
- Step 4 complete (success criteria verified).

## Step Actions

Checklist:
- [ ] Remove dead code - unused functions, commented blocks, debug prints
- [ ] Simplify - reduce nesting, extract complex logic to functions, eliminate duplication
- [ ] Best practices - follow `{{BEST_PRACTICES_DOC}}` (technology-specific patterns)
- [ ] Scalability - abstract where extension likely (multiple similar entities -> data-driven)
- [ ] Clarity - self-documenting names, minimal comments (explain why, not what)

Output (concise):
```markdown
**Code Refinement:**
- Removed: [dead code items]
- Simplified: [what was refactored]
- Abstracted: [scalability improvements]
- No changes needed (already clean)
```

If no changes needed: state "No changes needed (already clean)" and proceed.

## Exit Criteria
- Refinement is complete (or explicitly unnecessary).
- Code aligns with repo patterns and best practices for the touched systems.

