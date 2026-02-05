# Agent Collaboration Protocols

Use this when coordinating across roles (designer ↔ implementer ↔ reviewer) or when you discover a spec gap mid-work.

Primary goals:
- Keep discussion **in one place** (GitHub issue/PR threads) so context isn’t dropped.
- Reduce agent paralysis by making escalation **mechanical**.
- Preserve clean handoffs without adding process bloat.

## Part 1: Handling Spec Gaps (Decision Tree)

When you discover the spec is insufficient during implementation, categorize it:

1) **Is it a critical blocker?** (spec is unimplementable)
- Yes -> Scenario A
- No -> continue

2) **Is the fix obvious and low-risk?** (one reasonable approach)
- Yes -> Scenario B
- No -> Scenario C

### Scenario A: Critical blocker (spec unimplementable)

Protocol:
- Stop implementation work on that thread of work.
- Create a new issue titled: `Spec gap: <short description>`.
- Comment on the original issue/PR with:
  - What is blocked and why
  - The minimal missing decision/information needed
  - Link: `Blocked by #<new-issue>`
- Wait for designer/user decision before proceeding.

### Scenario B: Minor gap (obvious extension)

Protocol:
- Implement the minimum extension needed (keep it narrow).
- Document in the PR description or a PR comment:
  - `Added <X> (not explicitly in spec) because it is required for <Y>.`
- Ensure tests/validation still reflect the original success criteria.

### Scenario C: Ambiguous gap (multiple plausible approaches)

Protocol:
- Stop and ask a focused question in the issue/PR thread:
  - What is unclear
  - Options A/B (max 2) with a recommendation and tradeoff summary
- Wait for an explicit decision before implementing.

## Part 2: Cross-Role Handoff Patterns

### Design -> Implementation
- Designer produces an issue with goals/scope/non-goals/success criteria.
- Implementer links the issue in the PR (`Fixes #<issue>`).
- If a spec gap is found, implementer asks in the same issue/PR thread using the scenario protocol above.

### Implementation -> Review
- Implementer marks PR ready with a checklist and validation summary.
- Reviewer posts a structured review summary (Critical/Major/Minor).
- Implementer addresses findings systematically and re-validates.

### Review -> Design (Escalation)
- If reviewer finds a fundamental design flaw (not just code style/bugs):
  - Reviewer posts: `Critical design issue: <problem>. Recommend design review.`
  - Link to the affected success criteria/pillar/assumption.
- Designer (or user) responds with a decision, or requests a follow-up spec/issue.
- If roles are split across separate agent sessions, include a 1-paragraph recap + link to the decision thread to avoid re-litigating context.

**Example:**
```markdown
Critical design issue: Cargo capacity conflicts with Pillar X (link). Recommend design review.
Impact: Current implementation assumes 2 slots; pillar implies 1. Need decision: allow 2, or redesign inventory flow?
```

### Clarification Pattern (Any role)

Use this template when asking for a decision:

```markdown
**Question:** [What is unclear]
**Context:** [1–2 sentences]
**Options:**
- A) [Option] — [tradeoff]
- B) [Option] — [tradeoff]
**Recommendation:** A because [reason]
**Blocked until:** [Decision / confirmation]
```

## Part 3: Tagging & Threading Conventions

- Keep related discussion in a single GitHub thread (avoid fragmenting across multiple issues unless Scenario A).
- Quote specific lines or link to file:line when referencing code/spec.
- Prefer decisions in writing (“Choose A”) over implicit approvals.
- Resolve threads when addressed:
  - Implementer resolves after fixing.
  - Reviewer verifies and may re-open if insufficient.

## Related Docs

- Error recovery: `ERROR_RECOVERY.md`
- Implementation workflow: `IMPLEMENTATION_START.md` and `IMPLEMENTATION_ONE_PAGER.md`

