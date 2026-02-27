# Agent Collaboration Protocols

Use when coordinating across roles or when you discover a spec gap mid-work.

## Spec Gap Decision Tree

When the spec is insufficient during implementation:

1. **Critical blocker** (spec unimplementable)
   - Stop. Create an issue: `Spec gap: <short description>`.
   - Comment on original issue/PR: what's blocked, decision needed, `Blocked by #<new-issue>`.
   - Wait for decision before proceeding.

2. **Minor gap** (obvious extension, one reasonable approach)
   - Implement the minimum. Document in PR: `Added <X> (not in spec) because <Y>.`
   - Verify success criteria still hold.

3. **Ambiguous gap** (multiple plausible approaches)
   - Ask in the issue/PR thread: what's unclear + options A/B + recommendation.
   - Wait for an explicit decision.

## Cross-Role Handoff Patterns

- **Design → Implementation**: Designer produces an issue with goals/scope/non-goals/success criteria. Implementer links via `Fixes #<issue>`.
- **Implementation → Review**: Implementer marks PR ready with a validation summary. Reviewer posts structured findings (Critical/Major/Minor). Implementer fixes systematically.
- **Review → Design (escalation)**: Reviewer flags a fundamental design flaw with clear description and affected criteria. Designer (or user) decides before work continues.

## Clarification Template

```markdown
**Question:** [What is unclear]
**Context:** [1–2 sentences]
**Options:**
- A) [Option] — [tradeoff]
- B) [Option] — [tradeoff]
**Recommendation:** A because [reason]
**Blocked until:** [Decision]
```

## Threading

- Keep discussion in a single GitHub thread. Fragment only for Scenario 1 (Spec Gap issue).
- Quote `file:line` when referencing code or spec.
- Prefer written decisions ("Choose A") over implicit approvals.
- Implementer resolves threads after fixing; reviewer verifies.

## Reference

- Error recovery: `ERROR_RECOVERY.md`
