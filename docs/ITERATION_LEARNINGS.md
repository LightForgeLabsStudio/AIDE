Iteration Learnings (Process-Focused)
=====================================

- Prefer small, scoped iterations. Isolate a single concern per PR to reduce churn and simplify review.
- Centralize shared math/logic and add unit tests alongside each change; this cuts duplication and catches regressions early.
- Enable lightweight structured logging early; add context-rich messages to debug without heavy breakpoints.
- Guard risky features behind flags (e.g., path smoothing) to validate behavior safely and disable quickly if needed.
- Avoid long-lived rebases; merge main frequently or branch fresh to minimize conflict loops.
- Require feature spec in PR description (Summary, Goals, Scope, Non-Goals, Success Criteria, Implementation Approach, Impacted Files) for reviewer contract verification.
- Update IMPLEMENTATION_STATUS.md in PR (docs travel with code), not post-merge; keeps main branch in sync.
- Promote stable practices into project-facing docs only after they prove reliable; keep exploratory notes here until then.
- Prefer direct data handoff over recomputation for shared state; e.g., register occupancy from placement rather than recalculating from world transforms.
- Add lightweight guardrails to flaky subsystems (region caps, collision-triggered replans, blocked-cell sanitation) before considering rewrites.
- Invest early in debug visibility (overlay/metrics) to make invisible state obvious and reduce time spent guessing.
- Remove or fix stub/“SKIP” tests rather than keeping placeholders that can mask regressions.
- Keep PRs focused; large cross-cutting changes are harder to review and reason about.
