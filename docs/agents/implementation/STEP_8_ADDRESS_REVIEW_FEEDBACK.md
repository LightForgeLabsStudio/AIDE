# Implementation Agent - Step 8: Address Review Feedback

**Navigation:** [Index](../IMPLEMENTATION_START.md) | Prev: [Step 7](STEP_7_REPORT_BACK.md) | Next: [Step 9](STEP_9_MERGE.md)

## Purpose
Systematically fix review feedback (critical -> major -> minor), keep tests green, and wait for approval before merging.

## Prerequisites
- Reviewer feedback exists on the PR.

## Step Actions

Implementer addresses feedback (not reviewer). Review agent identifies issues; implementation agent fixes them.

Process:

1. Read review comments:
```bash
gh pr view <number> --comments
gh api repos/:owner/:repo/pulls/<number>/comments
```

2. Categorize feedback by severity:
- Critical: blocks merge (bugs, security, broken tests)
- Major: should fix (design violations, poor patterns, tech debt)
- Minor: nice to have (style, naming, comments)

3. Fix systematically (Critical -> Major -> Minor):
```bash
git add <files>
git commit -m "Fix [issue] from PR review

[Details]

Co-Authored-By: [Agent Name] <agent@{{PROJECT_DOMAIN}}>"

git push
```

4. Update PR checklist if new tasks added:
```bash
gh pr edit <number> --body "...
## Implementation Plan
- [x] Task 1
- [x] Task 2
- [x] Task 3

## Review Feedback
- [ ] Fix: [critical issue]
- [ ] Refactor: [major issue]
..."
```

5. Re-run smoke tests, linting, and tests after fixes:
```bash
{{SMOKE_TEST_COMMAND}}
{{LINT_COMMAND}}
{{RUN_ALL_TESTS_COMMAND}}
```

6. Post summary comment:
```bash
gh pr comment <number> --body "**Addressed PR Review Feedback**

**Critical Fixed:**
- [Issue] (commit: abc123)

**Major Fixed:**
- [Issue] (commit: def456)

**Smoke tests:** Passing.
**Linting:** Passing.
**Tests:** All passing.

Ready for re-review."
```

7. Request re-review:
```bash
gh pr review <number> --request
```

WAIT for approval before proceeding to merge.

## Exit Criteria
- All feedback addressed (or explicitly deferred with agreement).
- Quality gates re-run and passing.
- Re-review requested and approval received.

