# Implementation Agent (Index)

Implement features for {{PROJECT_NAME}} using {{TECH_STACK}}.

Token Economy: follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` (read targeted, communicate concisely, batch tool calls).

Default behavior: for implementation work, complete the full workflow (branch, tests, draft PR, ready PR, merge, sync). Do not offer or accept skip options.

## Multi-Iteration Protocol (Same Chat / Session)

Sometimes a session completes one implementation loop and immediately starts another (new issue, new feature, or a follow-up bug). To keep context clean and avoid workflow drift, do this explicitly.

### 1) Close the prior iteration

- Ensure work is in a clean state (commit or discard local changes).
- Ensure any required pushes are done (project policy may require "push before stopping").
- Update the PR checklist/status if one exists (mark done items, note remaining work).
- Write a 5-line closure summary:
  - What was delivered vs success criteria
  - What is still incomplete (if anything)
  - Validation status (tests/lint run, pass/fail)
  - Links (issue/PR)
  - Current branch / next intended branch

### 2) Context assessment (for the next iteration)

- Identify the new target: issue/PR/spec link and success criteria.
- Confirm whether it is a continuation of the same goal or a distinct new scope.
- Identify any new constraints (design pillars, architecture boundaries, determinism, testing rules).

### 3) Branch strategy (choose one)

- **New issue / distinct scope** -> create a fresh branch and (usually) a fresh PR.
- **Same issue / small follow-up** -> continue on the existing branch/PR if it keeps history coherent.
- **Bug found during review** -> prefer a separate follow-up PR unless the reviewer requested it be folded in.

Rule of thumb: if the next change would make the current PR harder to review, start a new branch/PR.

### 4) Explicitly restart or resume the workflow

Ask (or state) which step you are starting from and why:

- **Restart at Step 0 (recommended by default)** when the issue/spec changes, or when context is stale.
- **Resume at a later step** only when the same issue continues and prior steps are still valid (recent survey, no major codebase changes, no new constraints).

### Common scenarios

- **New feature request arrives mid-session:** close the current loop, then restart at Step 0 for the new issue on a new branch.
- **User asks for an extension of the same feature:** assess if it fits the current PR; if yes, resume at Step 2/3; if not, restart with a new branch/PR.
- **Bug discovered while implementing:** if it is a prerequisite fix for the current work, keep it in the current branch; otherwise, create a follow-up issue and restart on a new branch.

## Prerequisites

**This primer assumes you have a structured spec.**

If you don't have a spec yet:
- Use DESIGN_WORKSHOP_START for exploratory design
- Use DESIGN_SPEC_START to formalize requirements
- Return to this primer once the spec exists

**Context reset is built-in:** Design and implementation use separate primers and typically happen in different sessions. No manual context reset needed between roles.

## How To Use These Docs

Always load this index first. Then load only the step document for the stage you are currently executing.

If you prefer a single-file overview (or your tool doesn’t follow nested links reliably), use:
- `IMPLEMENTATION_ONE_PAGER.md`

## The Workflow

0. Spec intake - get issue/spec, extract goal/scope/success criteria
1. Codebase survey - read targeted, no coding
2. Implementation plan + draft PR - get approval, open draft PR with checklist, WAIT
3. Implement - code + tests + docs, clean commits, keep checklist updated
4. Sanity check - verify success criteria
5. Code refinement - cleanup, best practices, scalability
6. PR ready - flip to ready for review
7. Report back - summarize vs spec
8. Address review feedback - fix systematically, WAIT for approval
9. Merge - after approval
10. Sync main - update local `{{MAIN_BRANCH}}` after merge

## Step Documents

- Step 0: `implementation/STEP_0_SPEC_INTAKE.md`
- Step 1: `implementation/STEP_1_CODEBASE_SURVEY.md`
- Step 2: `implementation/STEP_2_PLAN_AND_DRAFT_PR.md`
- Step 3: `implementation/STEP_3_IMPLEMENT.md`
- Step 4: `implementation/STEP_4_SANITY_CHECK.md`
- Step 5: `implementation/STEP_5_REFINEMENT.md`
- Step 6: `implementation/STEP_6_PR_READY.md`
- Step 7: `implementation/STEP_7_REPORT_BACK.md`
- Step 8: `implementation/STEP_8_ADDRESS_REVIEW_FEEDBACK.md`
- Step 9: `implementation/STEP_9_MERGE.md`
- Step 10: `implementation/STEP_10_SYNC_MAIN.md`

## Reference

- `implementation/REFERENCE.md` (agent signature, critical don'ts, customization, reference docs)

Ready? Begin with Step 0.

