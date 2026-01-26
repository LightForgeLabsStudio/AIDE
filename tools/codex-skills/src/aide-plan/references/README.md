# AIDE Plan Skill References

This skill produces a two-layer plan:

- Layer 1: constraints (Tier 1 rules + project quality commands)
- Layer 2: task plan (ordered steps + exit criteria)

It optionally fetches an issue body via `gh issue view` when `-Fetch -Issue <n>` is provided.

It outputs a PR checklist body (markdown) suitable for a draft PR.

