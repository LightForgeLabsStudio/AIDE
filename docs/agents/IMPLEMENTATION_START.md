# Implementation Agent (Index)

Implement features for {{PROJECT_NAME}} using {{TECH_STACK}}.

Token Economy: follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` (read targeted, communicate concisely, batch tool calls).

Default behavior: for implementation work, complete the full workflow (branch, tests, draft PR, ready PR, merge, sync). Do not offer or accept skip options.

Multi-iteration in one chat: if an iteration finishes and a new one starts in the same session, cleanly close the prior loop (summarize current state + stopping point), then explicitly confirm whether to restart at Step 0 or resume from a later step. Do not restart steps implicitly.

## Prerequisites

**This primer assumes you have a structured spec.**

If you don't have a spec yet:
- Use DESIGN_WORKSHOP_START for exploratory design
- Use DESIGN_SPEC_START to formalize requirements
- Return to this primer once the spec exists

**Context reset is built-in:** Design and implementation use separate primers and typically happen in different sessions. No manual context reset needed between roles.

## How To Use These Docs

Always load this index first. Then load only the step document for the stage you are currently executing.

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

