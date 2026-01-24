# Implementation Agent - Step 2: Implementation Plan + Draft PR Setup

## Purpose
Produce a measurable plan mapped to success criteria, get approval, then open a draft PR with the plan as a checklist.

## Prerequisites
- Step 1 complete (targeted survey done; alignment concerns resolved or documented).

## Step Actions

After codebase survey, present implementation plan and get approval.

## Two-Layer Planning

**Layer 1 (constraints):** Capture project constraints and non-negotiables (Tier 1 rules, design pillars, architecture boundaries, determinism requirements). Keep it short and explicit.

**Layer 2 (task plan):** A short, ordered plan with exit criteria, likely files, validation commands, and risks. This is the plan you seek approval for.

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

