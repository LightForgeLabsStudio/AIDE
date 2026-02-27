# ADR: AIDE Core Reduction

**Date:** 2026-02-27
**Status:** Accepted
**Area:** Process / AI Workflow

---

## Context

AIDE grew organically to ~100 files and 4.4 MB. The original intent — prevent AI drift, enforce spec discipline, establish repeatable workflows — was sound. But the mechanism accumulated weight:

- **Role primers** loaded personality/framing before task definition. This consumed context for framing identity rather than doing work. The role *framed* me; the task *directed* me. Task direction is strictly more useful.
- **11-step implementation workflow** spread across individual files (`STEP_0` through `STEP_10`) made it difficult to know which steps applied to a given task. Most tasks only need 4–5 of them.
- **Separate coding/testing/development docs** (`CODING_GUIDELINES.md`, `TESTING_POLICY.md`, `DEVELOPMENT.md`) were rich project-specific references but not pointed to from anywhere an AI would load. They existed but weren't being surfaced.
- **Design sessions rushed to GitHub issues** without capturing design rationale. Issues became the container for both *decision-making* and *task-tracking*, making reviews harder and losing the "why" behind decisions.
- **Primers as mandatory ritual** — loading a primer before every task mode worked but was heavier than needed. The insight: a skill can *be* the primer.

---

## Decision

Restructure AIDE around three tiers and a progressive discovery model.

### Tier 0 — Always Available: `AGENTS.md`

Expand `AGENTS.md` into a universal project introduction. Every conversation has everything it needs without loading any other file. Contains:

- Project identity and tech stack
- Critical invariants (binding constraints for AI)
- Test and lint commands
- Essential architectural patterns (1–2 lines each)
- Progressive discovery pointers to Tier 2 references

Adds pointers to project Tier 2 references (`CODING_GUIDELINES.md`, `TESTING_POLICY.md`, `DEVELOPMENT.md`). Those files stay where they are.

### Tier 1 — Mode Starters: Skills

Skills define *what we are doing*, not *who I am*. No role framing. 30–50 lines each. Invoking a skill sets the conversation mode and defines what "done" looks like. Skills are self-contained except for pointing at `AGENTS.md`.

Skill set:

- `implement` — pointed at an issue or spec → inline constraint check + steps → code → verify
- `scope` — reads an ADR → outputs a spec file in issue-creator format → runs `issue-creator.py` to create GitHub issues; points to `issue-creator-ref.md` for format and error handling
- `design` — explore → ADR draft
- `pr-review` — alignment, architecture, tests, delta summary
- `pr-draft` — create a draft PR from existing branch work
- `pr-ready` — mark PR ready for review + post validation summary
- `codebase-review` — drift, dead code, gaps; no fixes
- `doc-review` — accuracy, staleness, proposed edits; no code changes
- `handoff` — session state for context reset
- `sync` — clean branch, push, verify
- `issue` — create a single labeled GitHub issue (one-off, no ADR required)
- `quality` — run lint + tests
- `evolve` — turn repeated mistakes into rules or automation; reads `SYSTEM_EVOLUTION.md`
- `skill-author` — create or update skills with correct YAML frontmatter

### Tier 2 — Progressive Discovery: Compact Reference Files

Loaded on demand when a specific task requires them. Max 50 lines each. Not primers — pure reference. Only consulted when needed, not preloaded. Examples: `github-labels.md`, `error-recovery.md`.

### ADR-First Design Flow

Design sessions produce an Architecture Decision Record before producing GitHub issues.

Flow: **`/design` → ADR → `/scope` → GitHub issues → `/implement`**

- Two canonical ADR roots by scope:
  - `.aide/docs/decisions/` — AIDE framework decisions (e.g. this file)
  - `docs/decisions/` — project/game decisions
- Both use `YYYY-MM-DD-<slug>.md` naming
- `/design` outputs an ADR draft only — no issues
- `/scope` reads the ADR and creates the issues; issues are the spec (goal + success criteria + ADR reference)
- `/implement` is pointed at a single issue and executes it; inline two-layer plan (constraint check + ordered steps) lives here
- Simple work skips `/design` and `/scope` — just `/implement` with a description
- `/scope` avoids naming conflict with Claude Code's native plan mode (`EnterPlanMode`)

### Cross-Cutting Review Protocol

A `/review` skill that is artifact-agnostic. Any skill output — ADR, issue body, PR body — can be put into a review loop without changing the author skill.

**Two-file protocol:**

- `<artifact-slug>.findings.md` — owned exclusively by the reviewer context
- `<artifact-slug>.response.md` — owned exclusively by the author context
- Each context writes only to its own file and reads the other's
- The artifact itself is only ever written by the author context
- Both files are ephemeral — deleted when the artifact is accepted

**One review round:**

1. Reviewer reads artifact + `response.md` (if exists) → overwrites `findings.md`
2. Author reads `findings.md` → updates artifact body + overwrites `response.md`
3. Repeat until both contexts are satisfied

**Author skills are review-aware:** each skill gains one optional step — if a findings file exists for the current artifact, read it before proceeding. This is the only coupling between `/review` and any author skill.

**No copy-paste between windows.** The filesystem is the message bus. Switching contexts requires only pointing the new chat at the relevant file, not copying and pasting output text.

---

## Rationale

**Why task definition over role framing?**
Role framing tells me *how to frame myself*. Task definition tells me *what to do and what done looks like*. When both are available, task definition does more work per token.

**Why collapse skills + primers?**
The skill invocation already establishes the conversation mode. A separate primer document loading the same information is duplication. The skill *is* the primer.

**Why AGENTS.md as Tier 0?**
Any conversation — with or without a skill — needs project basics to avoid inventing rules. A single authoritative file that's always in context eliminates the risk of an AI guessing conventions.

**Why progressive discovery instead of staged loading?**
Context budget is finite. Load what is always needed; discover the rest when needed. This is how good engineers read an unfamiliar codebase — they don't read every file first.

**Why ADRs before issues?**
Issues are task trackers. They answer "what to do." ADRs answer "why we decided this and what we considered." Without ADRs, design rationale lives only in chat history, which is ephemeral. Issues that carry design weight become too large to review cleanly.

**Why a cross-cutting review protocol rather than per-skill review steps?**
Any artifact benefits from independent review — ADRs, implementation plans, specs, PR bodies. A single protocol that all skills opt into is more useful than separate review mechanisms per skill type. Strict file ownership (each context writes only its own file) eliminates the risk of one context corrupting another's output. The filesystem as message bus removes copy-paste friction without requiring any shared infrastructure.

---

## Consequences

**Enables:**

- Faster conversation starts — fewer files to load before work begins
- Better token efficiency — progressive discovery instead of preloading
- Preserved design history — decisions are durable, not lost in session context
- Smaller, cleaner GitHub issues — they reference ADRs for context, not carry it themselves
- Simpler AIDE maintenance — ~15 files instead of ~100

**Forecloses:**

- Multi-agent role protocols (staged role handoffs, separate implementer/reviewer identity loading) — these were rarely used in practice
- Per-role context isolation via primer loading — skills replace this more simply

**Risk to manage:**

- `AGENTS.md` must stay under ~150 lines or it becomes its own bloat problem. If a section grows past 10–15 lines, move it to a Tier 2 reference file and add a pointer.

---

## Implementation Scope

Changes to make following this ADR:

1. **Rewrite `AGENTS.md`** — add pointers to Tier 2 references; extract key facts from deleted files (see items 3–4); keep under 150 lines
2. **Rewrite all skills** — task-focused, 30–50 lines, no role framing, self-contained; add review-aware step to artifact-producing skills only (implement, design, pr-review, codebase-review, doc-review). Full skill set: `implement`, `scope`, `design`, `pr-review`, `pr-draft`, `pr-ready`, `codebase-review`, `doc-review`, `handoff`, `sync`, `issue`, `quality`, `evolve`, `skill-author`, `review`. Replace existing `/plan` skill with `/scope`. Two-layer planning logic folds back into `/implement`.
3. **Delete — pure ritual, no unique content:**
   - `.aide/docs/agents/DESIGN_WORKSHOP_START.md`
   - `.aide/docs/agents/DOC_REVIEW_START.md`
   - `.aide/docs/agents/AGENT_PRIMER_TEMPLATE.md`
   - `.aide/docs/agents/SKILL_ROUTER.md`
   - `.aide/docs/agents/WORKFLOW_STRUCTURE_EVALUATION.md`
   - `.aide/docs/agents/implementation/STEP_*.md` (11 files: `STEP_0_SPEC_INTAKE.md` through `STEP_10_SYNC_MAIN.md`) and `IMPLEMENTATION_ONE_PAGER.md`
   - `.aide/docs/agents/IMPLEMENTATION_START.md`, `PR_REVIEW_START.md`, `CODEBASE_REVIEW_START.md` (after extracting — see item 4)
4. **Extract then delete** — move these specific facts to `AGENTS.md` before deleting source files:
   - From `.aide/docs/agents/IMPLEMENTATION_START.md`: GitHub identity/auth setup pattern (`GH_CONFIG_DIR`)
   - From `.aide/docs/agents/PR_REVIEW_START.md`: three-tier severity framework (Critical/Major/Minor) + follow-up issue protocol
   - From `.aide/docs/agents/CODEBASE_REVIEW_START.md`: focus areas checklist
5. **Keep as Tier 2 references, compress to ≤50 lines:**
   - `.aide/docs/agents/ERROR_RECOVERY.md` — recovery loop, escalation protocol, failure mode checklists
   - `.aide/docs/agents/SYSTEM_EVOLUTION.md` — decision tree for scoping rules
   - `.aide/docs/agents/GITHUB_QUERIES.md` — GraphQL queries for issue relationships
   - `.aide/docs/agents/AGENT_COLLABORATION.md` — spec gap decision tree, cross-role handoff patterns
   - `.aide/docs/agents/GITHUB_LABELS.md` — label taxonomy and conventions (kept; unique content)
   - `.aide/docs/agents/COMMAND_CATALOG.md` — skill directory with chaining flows (kept; unique content)
   - `.aide/docs/agents/PLACEHOLDER_CONTRACTS.md` — placeholder resolution rules (kept; unique content)
   - Merge `.aide/docs/agents/AGENT_TOKEN_ECONOMY.md` + `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` into one compressed doc
   - `.aide/docs/agents/ISSUE_BATCH_CREATOR_START.md` → compress to `issue-creator-ref.md` (format spec, error handling, label commands); referenced by `/scope`
6. **Keep project docs as Tier 2 references, add pointers from `AGENTS.md` (do not move or delete):**
   - `docs/CODING_GUIDELINES.md` — Godot/GDScript-specific conventions and gotchas
   - `docs/TESTING_POLICY.md` — GUT-specific rules and gotchas
   - `docs/DEVELOPMENT.md` — architecture reference
7. **Establish ADR pattern** — two roots: `.aide/docs/decisions/` (AIDE) and `docs/decisions/` (project). This file is the first AIDE-level ADR.
8. **Write `/review` skill** — artifact-agnostic, implements two-file protocol
9. **No separate `review-protocol.md`** — deliberately omitted. The `/review` skill is the protocol. A separate reference file would duplicate it with no operational gain.
10. **Update `.aide/docs/core/DOCUMENTATION_POLICY.md`** — remove "agent primer files" guidance; replace with tiered skill-first model description

**Rollout order (prevents broken skill references mid-migration):**

1. Rewrite all skills (item 2) — skills no longer reference primer files
2. Delete primer and step files (items 3–4)
3. Compress Tier 2 references (item 5)
4. Update `AGENTS.md` (item 1) and `DOCUMENTATION_POLICY.md` (item 10)

---

## Notes

This ADR was itself produced using the new design flow it describes — design conversation first, ADR before implementation. That was intentional.

**Future upgrade path:** The two-file review protocol is designed to be relay-agnostic. Currently the human switches windows and triggers each round. A future parallel sub-agent setup could remove the human from the relay loop entirely — the author and reviewer agents would exchange files autonomously until convergence. The protocol contract (file ownership, overwrite semantics) does not need to change for this.

Reference: [`docs/reports/aide_core_reduction_proposal.md`](../reports/aide_core_reduction_proposal.md)
