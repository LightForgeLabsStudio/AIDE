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
