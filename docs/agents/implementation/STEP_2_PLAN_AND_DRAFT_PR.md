# Implementation Agent - Step 2: Implementation Plan + Draft PR Setup

**Navigation:** [Index](../IMPLEMENTATION_START.md) | Prev: [Step 1](STEP_1_CODEBASE_SURVEY.md) | Next: [Step 3](STEP_3_IMPLEMENT.md)

## Purpose
Produce a measurable plan mapped to success criteria, get approval, then open a draft PR with the plan as a checklist.

## Prerequisites
- Step 1 complete (targeted survey done; alignment concerns resolved or documented).

## Step Actions

After codebase survey, present implementation plan and get approval.

## Autonomy Decision Tree (When to Auto-Proceed vs Ask)

This step exists to prevent wasted work and avoid unreviewable PRs. When in doubt, **ask before coding**.

### Auto-proceed (safe by default) when ALL are true

- The work is mechanical and low-risk (typos, refactors with no behavior change, wiring, doc updates).
- Only one reasonable approach exists (no product/design ambiguity).
- The change is small in surface area (roughly <5 files) and does not introduce new architecture/patterns.
- Tier 1 rules and design pillars are clearly satisfied.
- The success criteria are unambiguous and test/validation strategy is clear.

### Require approval when ANY are true

- Multiple plausible approaches or tradeoffs exist (architecture, UX, performance, data model).
- The change is large or cross-cutting (>5 files) or adds a new pattern/concept.
- It touches authoritative/shared systems (single sources of truth) or changes public APIs.
- It changes core gameplay/simulation behavior, determinism, or balance-sensitive logic.
- It modifies existing tests or requires relaxing test/tooling policy.
- The spec is missing, conflicting, or would change as a result of new information.

### If you already started coding and discover uncertainty

- Stop and summarize: what you learned, the options, and your recommended path.
- Update the plan/checklist accordingly before proceeding.

## Two-Layer Planning

**Layer 1 (constraints):** Capture project constraints and non-negotiables (Tier 1 rules, design pillars, architecture boundaries, determinism requirements). Keep it short and explicit.

**Layer 2 (task plan):** A short, ordered plan with exit criteria, likely files, validation commands, and risks. This is the plan you seek approval for.

If you hit failures mid-work, use: `docs/agents/ERROR_RECOVERY.md`

Present plan:
```markdown
**Implementation Plan:**

1. [Task 1] (file.ext:lines)
2. [Task 2] (file.ext:lines)
3. [Task 3] (file.ext:lines)

**Files touched:** [list]
**Testing:** [approach]

Ready to proceed?
```

After approval, create branch + draft PR:

Note: the PR body example uses a bash heredoc. For other shells, use the equivalent (e.g., PowerShell here-string) or edit the PR body in your editor.

```bash
# Create feature branch (never work on main)
git checkout -b feature/<brief-name>

# Make initial commit (can be empty to establish branch)
git commit --allow-empty -m "Start: <feature brief>

Implements: #<issue-number>

Co-Authored-By: [Agent Name] <agent@{{PROJECT_DOMAIN}}>"

# Push and create draft PR with plan as checklist
git push -u origin feature/<brief-name>

gh pr create --draft \
  --title "<Feature brief>" \
  --body "$(cat <<'EOF'
## Summary
[1-2 sentences]

**Implements:** #<issue-number>

## Implementation Plan

- [ ] Task 1 (file.ext:lines)
- [ ] Task 2 (file.ext:lines)
- [ ] Task 3 (file.ext:lines)

## Testing
- [ ] Unit tests for [scope]
- [ ] Integration tests for [scope]
- [ ] Manual verification: [criteria]

## Files Changed
- file1.ext - [description]
- file2.ext - [description]

---
[Agent Name] Implementation
EOF
)"
```

Key points:
- Plan becomes markdown checklist in PR description (`- [ ]` syntax)
- PR is draft (not ready for review yet)
- Each task is checkable - update as you complete them
- This PR checklist is your tactical tracking layer

## Exit Criteria
- Plan is approved.
- Branch is created (not on `{{MAIN_BRANCH}}`).
- Draft PR exists with plan checklist and testing approach.

