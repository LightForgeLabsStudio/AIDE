# Design Spec Reference (Project-Adapted)

Turn a chosen design direction into an implementable GitHub issue spec. Do not code.

This repo prefers lean specs as GitHub issues (and Epics + child issues when needed).

## Inputs (ask first)

- Goal (player feel vs systemic depth vs tech debt).
- Scope/timebox.
- Relevant pillar(s) and current GitHub state (what already exists/planned).

## Output (issue-ready spec)

Use the project spec template (see `{{CONTRIBUTING_DOC}}`) and keep it terse:

- **Summary / Goal**
- **Scope** (systems touched; extension points; explicit exclusions)
- **Non-goals / Out of scope**
- **Success criteria** (testable/measurable; include player-visible outcomes)
- **Test intent** (automated scenarios preferred; manual only if impractical)
- **Dependencies** (explicit only; otherwise omit)

## Constraints

- Do not propose new parallel systems without explicit approval.
- Do not modify tests without approval; specs may propose *new* tests.
- Keep outputs lean; reference pillars/docs instead of duplicating them.

## References

- Spec writing rules (normative): `.aide/docs/SPEC_WRITING_GUIDE.md`
- Batch issue creation format: `.aide/docs/ISSUE_CREATOR_GUIDE.md`
- Canonical example spec: `.aide/tools/issue-creator/example-spec.md`
