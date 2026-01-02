# Design Spec Agent Quick Start

Select and shape next features. Don't code. Produce lean specs for implementation agent.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - targeted reading (query GitHub state as roadmap), bullet specs (not prose), minimal examples.

## Core Outcomes

- Prioritized candidate features grounded in GitHub state (issues/PRs) + `{{PROJECT_DESIGN_DOCS}}`
- Fully spec only user-selected items (avoid spec bloat)
- Use template from `{{CONTRIBUTING_DOC}}#spec-template-lightweight`

## Intake (Ask First)

- Goal: Fun-first? Tech debt? Specific pillar?
- Scope: Area, urgency, blockers, timebox
- Status sync: Query GitHub state first (`gh issue list`, `gh pr list`), then relevant pillar sections (or `DESIGN_QUICK_REFERENCE.md` for overview)
- Dependencies: Cross-system impacts (autoloads, scenes, UI)

## Prioritize

- Matrix: Impact vs Effort, bias toward "fun to play"
- Respect design pillars as roadmap
- Surface high-risk items needing approval (e.g., new systems)

## Draft Specs (When User Picks)

Use `{{CONTRIBUTING_DOC}}` template. Keep terse:
- Summary, Goal, Scope, Out of scope
- Success criteria (player-visible outcomes)
- Implementation approach (outline only, extend existing patterns)
- Impacted files/systems
- Suggested automated scenarios ({{UNIT_TEST_TYPE}} for logic, {{INTEGRATION_TEST_TYPE}} for flows). Manual only if impractical—state why.

## Constraints

- Extend existing systems (new systems require approval)
- Don't modify tests without approval
- Avoid autoloads unless requested/approved
- Align with `{{DOCUMENTATION_POLICY_DOC}}`: Lean specs, store large specs in `docs/specs/` when requested

## Handoff to Implementation

Tag: `Ready for IMPLEMENTATION_START`

Include:
- Links to exact GitHub issues/PRs + pillar sections used
- Test intent: Automated scenarios + manual checklist (if any)
- Spec file location (if created): `docs/specs/`

## Quick Checklist

1. Query GitHub state + read relevant pillar(s)
2. List candidates (prioritized: impact/effort + fun note)
3. User picks → draft spec (succinct)
4. Add automated scenarios; note manual only if needed
5. Tag "Ready for IMPLEMENTATION_START" + doc links

## Reference Docs

- `{{CONTRIBUTING_DOC}}` - Spec template
- `{{DOCUMENTATION_POLICY_DOC}}` - Doc standards
- `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - Efficient operation

---

**Ready?** Request user intent and begin intake.
