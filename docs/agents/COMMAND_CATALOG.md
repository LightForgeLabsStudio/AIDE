# AIDE Command Catalog (Tool-Agnostic Skills)

This catalog defines a **tool-agnostic** set of slash-style commands (skills) that help agents execute common workflows consistently across Codex, Claude, and other tooling.

Projects may implement these commands as:
- native tool skills (e.g., `/prime`)
- repo scripts
- a hybrid (skill -> script -> project tooling)

This document defines **behavior and inputs/outputs**; it does not mandate an implementation.

---

## Design Goals

- Reduce "agent parses prose" variability
- Keep default context lean (link out instead of preloading)
- Respect project Tier 1 rules and constraints
- Be composable (small commands that chain)

---

## Core Commands

### `/prime`

**Intent:** minimal cold-start orientation and routing.

**Inputs:**
- Optional task link (issue/PR/spec) if already known.

**Reads (minimum):**
- Project `AGENT_ORIENTATION.md` (or project `AGENTS.md` if no orientation doc)
- Project Tier 1 docs listed there (at least `AGENTS.md`)

**Outputs:**
- Resolved role primer to load (AIDE `docs/agents/*`)
- Required next action (request spec/PR link, or confirm starting stage)
- Any missing inputs required to proceed

### `/plan`

**Intent:** convert a task spec into a plan with explicit success criteria.

**Inputs:**
- Issue/PR description or user-provided spec
- Known constraints (Tier 1 rules, design pillars, architecture)

**Outputs:**
- **Layer 1 constraints** (Tier 1 rules, pillars, architecture boundaries)
- **Layer 2 plan** (ordered steps with exit criteria)
- Files likely touched
- Validation commands to run (project-provided)
- Risks/unknowns + questions (if needed)

### `/quality`

**Intent:** run the project's standard quality gates for the current change.

**Inputs:**
- Current branch/commit context
- Project-specific commands (from placeholders or docs)

**Outputs:**
- Commands executed
- Pass/fail summary and failing logs (if any)

**Notes:** use project placeholder mappings for exact commands.

### `/tests`

**Intent:** run the smallest relevant test scope first, then broaden.

**Outputs:** pass/fail summary, failing tests, and reproduction hints.

### `/handoff`

**Intent:** produce a session handoff artifact for context resets or async work.

**Inputs:**
- Current stage, branch, PR, issue (if any)
- Completed work, in-progress items, blockers
- Next actions and validation status

**Outputs:**
- A filled handoff note using `docs/core/SESSION_HANDOFF.template.md`

### `/draft-pr` and `/ready-pr`

**Intent:** standardize PR creation and completion.

**Draft PR includes:**
- Spec link and success criteria
- Validation checklist
- Risks/assumptions

**Ready PR includes:**
- Confirmation quality gates ran
- What reviewers should focus on

### `/evolve`

**Intent:** turn repeated mistakes into system improvements (constraints, docs, automation).

**Inputs:**
- Observed failure pattern (what happened, how often)
- Evidence (issue/PR links or excerpts)

**Outputs:**
- Proposed change type (Tier 1 constraint vs Tier 2 guidance vs automation)
- Where to apply it (file + section)
- Example of the new rule in practice
- Quick decision rationale (why this tier/automation)

See `SYSTEM_EVOLUTION.md` for the decision tree and trigger criteria.

---

## Optional Commands

### `/refs`
Validate doc references (project-provided tooling), then summarize any drift.

### `/issue`
Create an issue for out-of-scope bugs/tech debt (project policy).

---

## Implementation Guidance

- Prefer referencing project placeholders and Tier 1 docs over hardcoding commands here.
- Prefer automation (validators/CI) when a failure mode is enforceable.
- Keep command outputs structured and brief; link to authoritative docs for detail.

