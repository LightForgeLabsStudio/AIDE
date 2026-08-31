---
name: scope
description: Decompose an accepted spec (and its ADR, if one exists) into GitHub issues — or, when the project elects a docs/plans/ layer, an optional staged plan file.
---

# Scope

Turn an accepted system spec into independently-deliverable work units. Read AGENTS.md if not in context.

## Inputs

Path to the accepted spec in `docs/specs/` (or paste contents). If the design produced an ADR, read it too. Optionally: repo override (`owner/repo`).

## Workflow

1. **Read the spec** (and ADR if present) — Extract: the change being made, Invariants affected, Success Criteria, and any explicit scope boundaries.

2. **Identify work units** — Break the decision into discrete, independently deliverable chunks with their ordering and dependencies. Each chunk becomes one issue (issues output) or maps onto one stage (plan output).

3. **Choose output** — **GitHub issues is the default.** Use the optional **plan output** only if the project documentation explicitly includes a `docs/plans/` execution layer or if the user requests a plan output. Most projects stay issues-only.

### Issues output (default)

4. **Write spec file** — Create a temporary spec in issue-creator batch format:

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

5. **Run issue-creator** — Execute:
   ```
   python .aide/tools/issue-creator/issue-creator.py <spec-file>
   ```

6. **Verify** — Confirm each issue was created with correct labels and GitHub Issue Type. Output issue URLs.

7. **Cleanup** — Delete the temporary spec file.

### Plan output (optional — only when the project elects a `docs/plans/` layer)

4. **Write the plan** — Create `docs/plans/<slug>.md` (slug from the spec) using the project's plan frontmatter:

   ```yaml
   ---
   title: <plan title>
   description: One-line summary of what this plan implements
   status: active
   created: YYYY-MM-DD
   last_updated: YYYY-MM-DD
   review_status: review-required
   spec: docs/specs/<spec>.md
   adr: docs/adr/<nnnn-slug>.md   # omit if none
   ---
   ```

5. **Stage the work** — The body is ordered **stages**, each with a goal, the steps to implement it, and **exit criteria / validation gates**. The work units from step 2 map onto stages in dependency order. A plan **sequences** — it must not restate the spec's design (link it) or duplicate an issue tracker.

6. **Confirm** — Leave `status: active`. When executed it moves to `closed` (archive under `docs/plans/_closed/` if it keeps reference value). A stage may later be `/scope`d into issues if granular tracking is wanted.

## Reference

- Issue-creator format + errors: `.aide/docs/agents/issue-creator-ref.md`
- Full tool docs: `.aide/tools/issue-creator/README.md`
