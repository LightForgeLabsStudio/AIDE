# AIDE Core Reduction Proposal

## Purpose

This document analyzes which parts of AIDE are structurally essential versus ceremonial. The goal is to reduce AIDE to a lean "Core" that preserves reliability and drift resistance while removing unnecessary process weight.

This is not a rejection of AIDE. It is a structural compression exercise.

---

# What Is Essential (AIDE Core)

These elements prevent concrete failure modes (drift, ambiguity, architectural inconsistency, AI misalignment).

## 1. Authority + Routing (Single Entry Point)

Keep:
- One clear "Start Here" document.
- Explicit authority hierarchy (Project > Framework > Examples).
- Role routing (which primer to load and when).

Why it matters:
- Prevents AI from inventing rules.
- Prevents reading non-authoritative docs.
- Reduces context thrashing.

Failure mode prevented: epistemic drift.

---

## 2. Spec Contract (Strict but Small)

Keep a required spec shape containing:
- Goal
- Scope / Out-of-scope
- Success Criteria (testable)
- Integration Points
- Constraints / Non-goals

Why it matters:
- Most implementation errors originate in vague specs.
- Step 0 eliminates 80% of future rework.

Failure mode prevented: scope creep and ambiguous success conditions.

---

## 3. Implementation Loop (Compressed to 3 Gates)

Replace the 10-step ladder with 3 structural gates.

### Gate A — Intake
- Validate spec quality
- Confirm scope boundaries

### Gate B — Survey & Plan
- Targeted codebase survey
- Explicit plan (files touched + test approach)
- Confirm architectural alignment

### Gate C — Validate
- Verify success criteria
- Run tests / sanity checks
- Report delta vs spec

Why it matters:
- Maintains determinism.
- Prevents blind coding.
- Preserves review clarity.

Failure mode prevented: chaotic PRs and misaligned implementations.

---

## 4. Token Discipline (Operational Minimalism)

Keep:
- Read targeted, not exhaustive.
- Communicate concisely.
- Cite file/line instead of quoting large blocks.
- Avoid narration.

Why it matters:
- Preserves context budget.
- Increases signal-to-noise ratio.

Failure mode prevented: token waste and context collapse.

---

## 5. Project Mapping / Placeholder Table

Keep:
- One authoritative mapping file (e.g., AGENTS.md).
- All placeholders resolved in one location.

Why it matters:
- Prevents duplication.
- Enables reuse of framework across projects.

Failure mode prevented: config drift and copy-paste inconsistency.

---

# What Is Ceremonial or Optional

These are valuable but not structurally mandatory.

## A. Full 10-Step Workflow Ritual

Issue:
- Heavy for small PRs.
- Can become performative.

Recommendation:
- Keep as reference.
- Default to 3-Gate Loop for most tasks.

---

## B. Stage-Specific Micro-Documents

Issue:
- Can create documentation bloat.
- High risk of drift.

Recommendation:
- Collapse into one Implementation One-Pager.
- Move detailed references into an appendix.

---

## C. GitHub Identity Switching Ceremony

Issue:
- Only required if multiple identities are actively used.

Recommendation:
- Make optional policy toggle.
- Not part of AIDE Core.

---

## D. Extensive Label Taxonomy

Issue:
- Label sprawl increases cognitive load.

Minimal viable set:
- status:ready
- status:in-progress
- status:blocked

Everything else is optional.

---

## E. Template Proliferation

Issue:
- Too many templates increase onboarding complexity.

Recommendation:
Keep only:
- Spec template
- Session handoff template

Move all others to /reference or /examples.

---

## F. Hard Prohibition on Skipping Steps

Issue:
- Removes flexibility.
- Encourages mechanical process compliance.

Recommendation:
- Allow skipping steps.
- Require explicit statement of what is skipped and why.

---

# Proposed AIDE Core Structure

If reduced aggressively, AIDE Core could consist of:

1. START_HERE.md
2. SPEC_CONTRACT.md
3. IMPLEMENTATION_LOOP.md (3 Gates)
4. TOKEN_DISCIPLINE.md
5. PROJECT_MAPPINGS.template.md

Optional folders:
- /reference
- /examples
- /tools

Everything else becomes non-core.

---

# Ceremony Test (Heuristic)

A document is ceremonial if:
- It repeats information already defined elsewhere.
- It exists primarily for formality.
- It is rarely consulted during actual execution.
- It does not prevent a named failure mode.

If it fails this test, archive or merge it.

---

# Design Philosophy Moving Forward

AIDE should:
- Constrain workflow boundaries.
- Preserve architectural intent.
- Prevent entropy.

AIDE should NOT:
- Replace thinking.
- Prevent exploration.
- Enforce unnecessary ritual.

Structure at the boundary.
Intelligence inside the box.

---

# Conclusion

AIDE is not too constrictive by design.
It becomes constrictive when all components are treated as mandatory.

Reducing AIDE to its structural essentials preserves reliability while restoring fluidity.

This document can be used as a basis for creating an "AIDE Core" branch or experimental trimmed variant.

