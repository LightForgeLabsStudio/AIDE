# Implementation Agent - Step 9: Merge After Approval

## Purpose
Merge only after approval, verify issue closure, and keep mainline clean.

## Prerequisites
- PR is approved.
- Review feedback is addressed (Step 8).

## Step Actions

Pre-merge checklist:
- [ ] PR approved by reviewer
- [ ] All review feedback addressed
- [ ] Smoke tests passing
- [ ] Linting passing
- [ ] All tests passing
- [ ] No merge conflicts with `{{MAIN_BRANCH}}`

Merge:
```bash
gh pr merge <number> --squash --delete-branch
```

If preserving commits is important:
```bash
gh pr merge <number> --merge --delete-branch
```

Post-merge verification:
```bash
gh issue view <issue-number>  # Should show "Closed"
```

Report completion:
```markdown
**PR merged**

**PR:** #<pr-number> (merged to {{MAIN_BRANCH}})
**Issue:** #<issue-number> (closed)
**Commits:** Squashed to 1 commit on main

Feature is now live on {{MAIN_BRANCH}}.
```

Merge conflicts:
1. `git checkout {{MAIN_BRANCH}} && git pull`
2. `git checkout feature/branch && git merge {{MAIN_BRANCH}}`
3. Resolve conflicts, test
4. `git add . && git commit -m "Merge {{MAIN_BRANCH}} to resolve conflicts"`
5. `git push`
6. Re-run `{{SMOKE_TEST_COMMAND}}`, `{{LINT_COMMAND}}`, and `{{RUN_ALL_TESTS_COMMAND}}`
7. Comment: "Resolved conflicts. Smoke tests, linting, and tests passing."

## Exit Criteria
- PR is merged and branch is deleted.
- Issue is closed (auto-closed by Fixes/Resolves/Closes keywords).

