---
name: implement
description: Implementation entrypoint for AIDE repos (intake spec, plan, branch, draft PR, implement, validate, push).
---

# Implement

Implement a feature/bug end-to-end using the AIDE implementation workflow.

## Documentation Loading (role-based)

- Always use: project constraints + the task spec (issue/PR description).
- Stage-load (implementation work): `docs/CODING_GUIDELINES.md`, `docs/TESTING_POLICY.md`, `docs/CONTRIBUTING.md`, and `docs/DEVELOPMENT.md` as soon as planning/implementation begins.
- Stage-load (as needed): relevant `design/` pillar(s) for the feature/bug.

## Inputs (ask first)

- Issue/PR link or pasted spec text (goals, scope, success criteria).
- Any must-not-change constraints beyond the project's standard rules.

If there is no spec yet, switch to `/design` (exploration) before implementing.

## Workflow

This skill follows the canonical Implementation workflow. The step list below is generated from the workflow manifest to prevent drift.

<!-- AIDE-GEN:IMPLEMENT_WORKFLOW_START -->
Canonical workflow (also see: `.aide/docs/agents/IMPLEMENTATION_ONE_PAGER.md`).

0) **Spec intake** -> confirm goal/scope/success criteria (`.aide/docs/agents/implementation/STEP_0_SPEC_INTAKE.md`)
1) **Codebase survey** -> read targeted, no coding (`.aide/docs/agents/implementation/STEP_1_CODEBASE_SURVEY.md`)
2) **Plan + draft PR** -> plan, get approval, open draft PR (`.aide/docs/agents/implementation/STEP_2_PLAN_AND_DRAFT_PR.md`)
3) **Implement** -> code + tests + docs (`.aide/docs/agents/implementation/STEP_3_IMPLEMENT.md`)
4) **Sanity check** -> verify success criteria (`.aide/docs/agents/implementation/STEP_4_SANITY_CHECK.md`)
5) **Refinement** -> cleanup, best practices (`.aide/docs/agents/implementation/STEP_5_REFINEMENT.md`)
6) **PR ready** -> mark ready for review (`.aide/docs/agents/implementation/STEP_6_PR_READY.md`)
7) **Report back** -> summarize vs spec (`.aide/docs/agents/implementation/STEP_7_REPORT_BACK.md`)
8) **Address feedback** -> fix review findings (`.aide/docs/agents/implementation/STEP_8_ADDRESS_REVIEW_FEEDBACK.md`)
9) **Merge** -> implementer merges after approval (`.aide/docs/agents/implementation/STEP_9_MERGE.md`)
10) **Sync main** -> update local main after merge (`.aide/docs/agents/implementation/STEP_10_SYNC_MAIN.md`)
<!-- AIDE-GEN:IMPLEMENT_WORKFLOW_END -->

**Phases (compressed guidance):**
- Intake + survey (Steps 0–1): confirm spec and map the change surface (no coding).
- Plan + draft PR (Step 2): write two-layer plan, get approval, open draft PR.
- Implement + verify (Steps 3–5): implement, verify success criteria, refine.
- Ship (Steps 6–10): mark PR ready, report back, address feedback, merge, sync main.

## Reference

- AIDE implementation primer: `.aide/docs/agents/IMPLEMENTATION_START.md`
- Step docs: `.aide/docs/agents/implementation/`
- Spec gaps + cross-role handoffs: `.aide/docs/agents/AGENT_COLLABORATION.md`
