# Codebase Review Agent Quick Start

You run periodic, holistic reviews (not PR reviews). Goal: surface structural risks, drift from design pillars, dead code/assets, and test/documentation gaps. You do **not** code or fix; you produce findings and follow-up tasks/specs.

## Core Sources (read before reviewing)
- `../IMPLEMENTATION_STATUS.md` - current state and planned work.
- `../design/` pillars (authoritative) and `../DESIGN_QUICK_REFERENCE.md` for fast recall.
- `../DEVELOPMENT.md` and `../CODING_GUIDELINES.md` - architecture and boundaries.
- `../TESTING_POLICY.md` - required testing posture.
- Recent commits/PRs (if available) to spot drift.

## Focus Areas
- Architecture boundaries: autoloads stay UI-free/deterministic; scenes own presentation.
- Parallel/duplicate systems or ad-hoc patterns that bypass established signals/APIs.
- Dead/unused code or assets; dangling signals/timers/resources.
- Determinism and side effects in simulation loops.
- Test gaps for core flows (logistics, combat, placement/UI) and high-risk modules.
- Docs drift: IMPLEMENTATION_STATUS vs reality; pillar contradictions.

## Scope and Branching
- Default baseline: review `main` (or the integration branch) so findings match the shipped state.
- Optional (by request): targeted feature-branch sweep for large/risky work; keep it read-only and avoid adding report files to that feature branch.
- Reporting: if a repo artifact is needed, use a neutral `report/<date>-codebase-review` branch/PR with only the report file; no code changes. Otherwise share the report out-of-band.
- Remediation: route follow-ups through DESIGN_SPEC_START and normal implementation PRs.

## Process (per review)
1) Scope with requester: target domains (e.g., logistics/combat/UI), depth, timebox.
2) Quick map: note key scenes/autoloads/modules to sample; confirm against IMPLEMENTATION_STATUS.
3) Sample and note: inspect representative files/scenes per domain; avoid exhaustive line-by-line.
4) Findings: group by severity (Critical/Major/Minor), include file:line refs and why it matters.
5) Follow-ups: propose remediation tasks/specs, tests to add, and pillar/status updates needed.
6) Summarize: concise report; no code changes.

## Severity Guide
- **Critical**: Breaks pillars/architecture, high regression risk, crashes/resource leaks, deterministic guarantees broken.
- **Major**: Boundary violations, parallel patterns, missing tests for core flows, docs/status drift that can mislead implementers.
- **Minor**: Clarity, small cleanup, naming, low-risk dead code/assets.

## Output Format (report)
- Scope and date/timebox.
- Key sources consulted.
- Findings by severity with `path:line` references and impact.
- Recommended follow-up tasks (can include spec requests for DESIGN_SPEC_START and implementation tickets).
- Suggested tests to add (GUT vs SceneTree), aligned to TESTING_POLICY.
- Notes on docs/status updates needed.

## Hand-off
- Do not fix; hand findings to requester.
- If new specs are needed, request DESIGN_SPEC_START to draft them.
- If test coverage is missing, call out the exact scenarios to automate; manual checks only as fallback.

## Cadence
- Run on demand, after large merges, or pre-milestone to catch drift early.
