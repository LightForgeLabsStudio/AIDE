# Implementation Workflow Structure Evaluation

This document supports **Task 5** of AIDE workflow improvements: evaluate whether agents prefer single-file vs multi-file workflow docs, prototype alternatives, and implement the winning approach.

## Goals

- Reduce navigation friction (finding the right step fast).
- Reduce token waste (loading too much unnecessary context).
- Preserve correctness (agents follow the intended workflow; fewer skipped steps).

## What We’re Evaluating

### A) Consolidated view (single-file friendly)

Provide an "all-in-one" entrypoint that works well in tools that don’t follow nested links reliably.

Prototype: `IMPLEMENTATION_ONE_PAGER.md` (compact single-file summary with links).

### B) Navigation aids (multi-file friendly)

Keep step docs split, but add consistent navigation links (Index / Prev / Next).

Prototype: nav line added to each `docs/agents/implementation/STEP_*.md`.

### C) Resume mechanism

Make “where am I in the workflow?” explicit and easy to resume after interruptions.

Prototype ideas (not implemented here):
- Standard “If resuming here…” block in every step doc
- A handoff/resume template snippet that captures the current step and exit criteria

## Survey Template (Copy/Paste)

Ask agents after they complete an implementation loop:

1) Which do you prefer for workflow guidance?
- ( ) One file (single scroll)
- ( ) Multiple files (per-step)
- ( ) No preference

2) What was the biggest friction point?
- ( ) Finding the right doc/step
- ( ) Loading too much context
- ( ) Remembering where I was (resume)
- ( ) Approval gates / when to ask
- ( ) Other: ________

3) Which prototype helped more?
- ( ) One-pager
- ( ) Prev/Next navigation links
- ( ) Neither

4) Any changes you’d make? (1–3 bullets)

## Suggested Metrics (Lightweight)

Use approximate, tool-agnostic measurements:

- **Doc hops:** number of different workflow files opened to complete a loop.
- **Wrong turns:** number of times an agent opened an irrelevant doc/step.
- **Resume time:** time/effort to resume after interruption (self-reported).
- **Token waste (proxy):** “I had to load X but only used Y” (self-reported).

## Decision Rule (When to Promote a Winner)

Promote a prototype to “default recommended” when:

- Majority preference is clear across multiple sessions, AND
- It reduces doc hops/wrong turns, AND
- It doesn’t increase drift risk (avoid duplicating full step content).

## Where the Prototypes Live

- One-pager: `docs/agents/IMPLEMENTATION_ONE_PAGER.md`
- Step navigation: `docs/agents/implementation/STEP_*.md` nav line

