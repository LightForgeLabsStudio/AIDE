---
name: scope
description: Decompose an accepted spec (and its ADR, if one exists) into GitHub issues using the issue-creator tool.
---

# Scope

Turn an accepted system spec into a set of GitHub issues. Read AGENTS.md if not in context.

## Inputs

Path to the accepted spec in `docs/specs/` (or paste contents). If the design produced an ADR, read it too. Optionally: repo override (`owner/repo`).

## Workflow

1. **Read the spec** (and ADR if present) — Extract: the change being made, Invariants affected, Success Criteria, and any explicit scope boundaries.

2. **Identify work units** — Break the decision into discrete, independently deliverable chunks. Each chunk becomes one issue.

3. **Write spec file** — Create a temporary spec in issue-creator batch format:

   ```
   ## Epic: <title>
   Goal: <from the spec's design/change section>
   Spec: <path-to-spec>   (plus ADR path if one exists)

   ### Issue: <title>
   Goal: <what this chunk delivers>
   Success Criteria:
   - <measurable criterion>
   Non-Goals: <explicit exclusions>
   ```

4. **Run issue-creator** — Execute:
   ```
   python .aide/tools/issue-creator/issue-creator.py <spec-file>
   ```

5. **Verify** — Confirm each issue was created with correct labels and GitHub Issue Type. Output issue URLs.

6. **Cleanup** — Delete the temporary spec file.

## Reference

- Issue-creator format + errors: `.aide/docs/agents/issue-creator-ref.md`
- Full tool docs: `.aide/tools/issue-creator/README.md`
