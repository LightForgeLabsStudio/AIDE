# Agent Primer Template

Use this skeleton to create new agent primers. Keep it concise, explicit, and enforceable.

## Purpose and Scope
- Mission: what the agent does.
- Non-goals: what it must not do (e.g., no code changes, read-only).

## Sources of Truth
- GitHub queries for current state (see `GITHUB_QUERIES.md` for issue/epic queries).
- Primary docs to read first (e.g., `../design/` pillars).
- Secondary/quick refs (e.g., `../DESIGN_QUICK_REFERENCE.md`).

## Workflow Steps (numbered, checkable)
1) Intake/context (what to ask, what approvals are needed).
2) Analysis/review/design steps (as applicable).
3) Branch/PR policy (if the agent commits code): never work on `main`; branch naming; draft PR timing.
4) Implementation/reporting steps (what “done” means for each).
5) Ready-for-review criteria (if applicable).

## Branch and PR Hygiene (if the agent commits code)
- Never work on `main`; create/confirm feature branch before edits.
- After first commit, push and open a draft PR (`gh pr create --draft`); keep pushing.
- Small, single-purpose commits with attribution/signature if required.
- Flip to “Ready for review” only when scope complete, tests pass, sanity check done, PR body updated.

## Testing
- When to define test intent (at spec/plan time).
- What suites to run; link to `../TESTING_POLICY.md`.
- How to report results in PRs/reports.

## Output and Handoff
- Artifacts to produce (reports, specs, comments), required tags (e.g., “Ready for IMPLEMENTATION_START”).
- File locations (e.g., `docs/contracts/`, `docs/reports/`).
- Links to relevant status/pillar lines used.

## Constraints
- No new systems without explicit approval (if relevant).
- Do not modify existing tests without approval.
- Respect design pillars/architecture boundaries; avoid doc duplication per `../DOCUMENTATION_POLICY.md`.

## Severity/Decision Rules (for review/reporting agents)
- Define Critical/Major/Minor and the expected action for each.

## Cadence (if periodic)
- When to run (on-demand, after merges, pre-milestone).

## Tone and Brevity
- Prefer concise checklists; add optional elaboration only if needed.
- Follow token economy best practices in `AGENT_TOKEN_ECONOMY.md`:
  - Use bullet points/checklists over paragraphs
  - Reference authoritative docs instead of duplicating content
  - Front-load critical constraints
  - One clear example > multiple redundant ones
  - Use token budgets by doc type (see "Token Budget Guidelines (By Document Type)")
  - Target 150-500 tokens for role primers depending on agent complexity

## Signature/Attribution (if required)
- Commit trailer or review prefix format.
