# Implementation Agent - Step 3: Implement

## Purpose
Implement the approved plan with small, focused commits; keep tests passing; keep the PR checklist updated.

## Prerequisites
- Step 2 complete (approved plan + draft PR opened).

## Step Actions

Now implement the plan, updating the PR checklist as you go.

After completing each task:

```bash
# Make focused commit
git add <files>
git commit -m "<Task description>

<Details if needed>

Co-Authored-By: [Agent Name] <agent@{{PROJECT_DOMAIN}}>"

# Push
git push

# Update PR checklist (replace [ ] with [x])
gh pr edit <number> --body "$(cat <<'EOF'
## Summary
[1-2 sentences]

**Implements:** #<issue-number>

## Implementation Plan

- [x] Task 1 (file.ext:lines)
- [ ] Task 2 (file.ext:lines)
- [ ] Task 3 (file.ext:lines)

...
EOF
)"
```

Or update via GitHub web UI:
- Navigate to PR
- Edit description
- Check off completed tasks
- Save

Track discovered work:
- Create GitHub issues for out-of-scope bugs/features (see "Handling Out-of-Scope Work" below)
- Add new tasks to PR checklist if within scope

## Critical Constraints

- Extend, don't replace - reuse existing patterns
- No test modifications - without explicit approval + explanation
- Design compliance - don't contradict docs without permission

## Testing

Follow `{{TESTING_POLICY_DOC}}`. Derive test intent from spec success criteria.

Coverage (fast first):
- `{{UNIT_TEST_TYPE}}` for logic
- `{{INTEGRATION_TEST_TYPE}}` for flows
- Manual checklist only if automation impractical (state why in PR)

Commands:
```bash
{{RUN_ALL_TESTS_COMMAND}}      # All suites (before PR)
{{RUN_UNIT_TESTS_COMMAND}}     # Fast iteration
```

## Handling Out-of-Scope Work

If you discover bugs or issues outside the current spec:

1. Document the problem clearly
2. Create GitHub issue to track it:
   ```bash
   gh issue create \
     --title "Brief description" \
     --body "Description, reproduction steps, code location" \
     --label "priority: [level],area: [system]"
   python .aide/tools/set-issue-type.py --issue <number> --type bug
   ```
3. Comment in PR that issue was discovered and tracked
4. Continue with current implementation (don't expand scope)

Example:
> Note: Discovered pathfinding issue with diagonal obstacles during testing. Created #42 to track. Out of scope for this PR.

Don't:
- Fix out-of-scope bugs in current PR (expands scope)
- Ignore problems without tracking them
- Let technical debt accumulate silently

## Exit Criteria
- All planned tasks are implemented (or explicitly deferred with issue(s) filed).
- PR checklist reflects completed work.
- Relevant tests pass and failures are addressed immediately (no red mainline).

