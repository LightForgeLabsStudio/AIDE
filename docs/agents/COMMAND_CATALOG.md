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

**Reads (minimum):**
- Project `AGENT_ORIENTATION.md` (or project `AGENTS.md` if no orientation doc)
- Project Tier 1 docs listed there (at least `AGENTS.md`)

**Outputs:**
- Which role primer to load (AIDE `docs/agents/*`)
- What the next action is (ask for spec, request PR link, etc.)

### `/plan`

**Intent:** convert a task spec into a plan with explicit success criteria.

**Inputs:** issue/PR description or user-provided spec.

**Outputs:**
- Steps with ordering and exit criteria
- Files likely touched
- Validation commands to run (project-provided)
- Risks/unknowns + questions (if needed)

### `/quality`

**Intent:** run the project's standard quality gates for the current change.

**Outputs:** pass/fail summary and failing logs (if any).

**Notes:** use project placeholder mappings for exact commands.

### `/tests`

**Intent:** run the smallest relevant test scope first, then broaden.

**Outputs:** pass/fail summary, failing tests, and reproduction hints.

### `/handoff`

**Intent:** produce a session handoff artifact for context resets or async work.

**Outputs:** a filled handoff note using `docs/core/SESSION_HANDOFF.template.md`.

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

**Outputs:**
- Proposed change type (Tier 1 constraint vs Tier 2 guidance vs automation)
- Where to apply it (file + section)
- Example of the new rule in practice

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

