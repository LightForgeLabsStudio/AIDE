---
name: design
description: Relaxed design exploration aligned to pillars; optionally create GitHub issues directly from the outcome.
---

# Design

Run a lightweight design exploration session, then (optionally) turn outcomes into GitHub issues.

## Documentation Loading (role-based)

- Always use: project constraints + the design question/topic.
- Stage-load (as needed): relevant `design/` pillar(s), `docs/DESIGN_QUICK_REFERENCE.md`, and GitHub state (`gh issue list`, `gh pr list`).
- Stage-load (only if creating issues): `docs/CONTRIBUTING.md` (workflow expectations) plus `.aide/docs/SPEC_WRITING_GUIDE.md` and `.aide/docs/ISSUE_CREATOR_GUIDE.md`.
- Usually skip: `docs/TESTING_POLICY.md` and `docs/CODING_GUIDELINES.md` unless the design output explicitly includes test strategy or coding constraints.

## Inputs (ask first)

- Topic/question and timebox.
- Desired output: one decision? multiple options? roadmap slice?

## Exploration Workflow (default)

1) **Pillar + state check**
   - Use the project's constraints (already loaded in this environment).
   - Reference relevant `design/` pillar(s) and `docs/DESIGN_QUICK_REFERENCE.md` as needed.
   - Query GitHub state (`gh issue list`, `gh pr list`) to avoid proposing already-built/conflicting work.

2) **Shape options**
   - Produce 1 recommended option (+ 1 alternative max).
   - Include: pros/cons, risks, dependencies, and how to validate success.

3) **Decide next step**
   - If proceeding, convert the recommendation into one or more issue drafts.

## Create GitHub Issues (optional, in-session)

When requested, create issues directly (follow `/issue` workflow):

1) Draft each issue body using:
   - `.aide/docs/SPEC_WRITING_GUIDE.md` (normative structure)
   - `.aide/docs/ISSUE_CREATOR_GUIDE.md` (batch format if needed)
2) Create issues:
   - `gh issue create --title ... --body ... --label "priority:<x>,area:<y>,status:<z>"`
   - `.aide/tools/set-issue-type.py --issue <n> --type <type>`

## Reference

- Exploration primer: `.aide/docs/agents/DESIGN_WORKSHOP_START.md`
- Spec reference (project-adapted): `.aide/docs/agents/design/DESIGN_SPEC_REFERENCE.md`
