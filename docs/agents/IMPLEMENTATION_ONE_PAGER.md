# Implementation Workflow One-Pager

This is a **single-file friendly** overview of the implementation workflow. Use it when:
- Your tool doesn’t follow nested links reliably, or
- You want a compact refresher before opening the exact step doc you need.

For full detail, use the per-step docs from `IMPLEMENTATION_START.md`.

## Quick Start (Decision)

- No spec / unclear requirements -> use Design role first.
- Spec exists -> start at Step 0 (or resume explicitly at the correct step).

## Steps (Overview)

0. **Spec intake** -> confirm goal/scope/success criteria (`implementation/STEP_0_SPEC_INTAKE.md`)
1. **Codebase survey** -> read targeted, no coding (`implementation/STEP_1_CODEBASE_SURVEY.md`)
2. **Plan + draft PR** -> plan, get approval, create draft PR (`implementation/STEP_2_PLAN_AND_DRAFT_PR.md`)
3. **Implement** -> code + tests + docs (`implementation/STEP_3_IMPLEMENT.md`)
4. **Sanity check** -> verify success criteria (`implementation/STEP_4_SANITY_CHECK.md`)
5. **Refinement** -> cleanup, best practices (`implementation/STEP_5_REFINEMENT.md`)
6. **PR ready** -> mark ready for review (`implementation/STEP_6_PR_READY.md`)
7. **Report back** -> summarize vs spec (`implementation/STEP_7_REPORT_BACK.md`)
8. **Address feedback** -> fix review findings (`implementation/STEP_8_ADDRESS_REVIEW_FEEDBACK.md`)
9. **Merge** -> implementer merges after approval (`implementation/STEP_9_MERGE.md`)
10. **Sync main** -> update local main after merge (`implementation/STEP_10_SYNC_MAIN.md`)

## If You’re Resuming Mid-Workflow

Write a 5-line resume note before continuing:

1) Current step number:
2) What’s done vs success criteria:
3) What’s next (1–3 bullets):
4) Validation status (commands run, pass/fail):
5) Links (issue/PR) + branch name:

## If Things Go Wrong

Use: `ERROR_RECOVERY.md`

