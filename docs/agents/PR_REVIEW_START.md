# PR Review Agent Quick Start

Review PRs for {{PROJECT_NAME}} ({{TECH_STACK}}).

**Non-goal:** Don't push code/fixes. Provide findings and decisions only.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - structured reviews (not prose), reference file:line, batch tool calls.

## Review Process

### Initial Review
1. **Context** - Get PR number, scope, test results
2. **Fetch** - `gh pr view <number>` or `gh pr diff <number>`
3. **Review commits** - Quality, size, logical flow
4. **Review code** - Bugs, style, architecture
5. **Verify tests** - Automated ran + passed (or manual checklist provided)
6. **Check docs** - Updated if behavior changed
7. **Post inline comments** - Line-specific issues via `gh pr comment`
8. **Post summary** - Overall findings + decision
9. **Decide** - Approve / Request changes / Comment

### Re-Review (After Fixes)
1. Read implementer's status comment
2. Verify fixes in new commits
3. Check tests still pass
4. Decide: Approve / Request more / Comment

**Comment resolution:**
- Implementers MAY resolve as they fix
- Reviewers verify, may re-open if insufficient
- Reviewers resolve remaining when approving

## What to Review

### Code Quality
- [ ] No security risks, resource leaks
- [ ] No bugs or logic errors
- [ ] Follows `{{CODING_GUIDELINES_DOC}}` style
- [ ] Module boundaries respected
- [ ] No over-engineering
- [ ] No debug code, commented blocks, orphaned TODOs

### Architecture
- [ ] Follows design docs + patterns (`{{DEVELOPMENT_DOC}}`)
- [ ] No core architecture violations
- [ ] Integrates with existing patterns (not parallel systems)
- [ ] Fits within module boundaries

**References:**
- `{{DEVELOPMENT_DOC}}` - Architecture
- `{{CODING_GUIDELINES_DOC}}` - Style
- `{{PROJECT_DESIGN_DOCS}}` - Design docs

### Testing
- [ ] Automated tests ran + passed OR manual checklist provided
- [ ] Relevant scenarios checked
- [ ] No tests modified without justification
- [ ] New tests for new functionality

### Docs
- [ ] User docs updated if behavior changed
- [ ] `{{DEVELOPMENT_DOC}}`/`{{CONTRIBUTING_DOC}}` updated if arch/workflow changed
- [ ] No unnecessary spec files

### Git Hygiene
- [ ] Small, single-purpose commits
- [ ] Clear commit messages
- [ ] No debug prints, commented code
- [ ] Targets `{{MAIN_BRANCH}}`

## Issue Severity

**Request Changes (Critical - blocking):**
- Violates architecture (`{{DEVELOPMENT_DOC}}`, design docs)
- Breaks functionality, regressions
- Tests not run, failing, or missing required manual verification
- Missing required doc updates
- Modifies tests without justification
- Security risks, crashes

**Request Changes or Comment (Major):**
- Over-engineering, poor commits, style violations
- Module boundary violations
- Missing tests (where feasible)

**Comment Only (Minor):**
- Typos, naming, small simplifications

## GitHub CLI Commands

```bash
# View PR
gh pr view <number>
gh pr diff <number>

# Post inline comment
gh pr comment <number> --body "Comment on general PR"

# Post inline code comment (specific line)
gh api repos/:owner/:repo/pulls/<number>/comments \
  -f body="Comment text" \
  -f path="file.ext" \
  -f commit_id="<commit-sha>" \
  -F position=5

# Read inline comments
gh api repos/:owner/:repo/pulls/<number>/comments

# Approve
gh pr review <number> --approve --body "LGTM. Summary..."

# Request changes
gh pr review <number> --request-changes --body "Summary..."

# Comment only
gh pr review <number> --comment --body "Summary..."
```

## Review Output Format

**Summary comment structure:**
```markdown
## PR Review Summary

**Decision:** [Approve / Request Changes / Comment]

### Critical Issues (must fix before merge)
- ❌ [Issue description] (file.ext:line)

### Major Issues (fix or discuss)
- ⚠️ [Issue description] (file.ext:line)

### Minor Issues (optional)
- 💡 [Suggestion] (file.ext:line)

### Strengths
- ✅ [Good practice observed]

**Tests:** [Passed / Failed / Not run / Manual only]
**Docs:** [Updated / Not needed / Missing]

---
*Review by [Agent Name]*
```

**Inline comment format:**
```markdown
**[Critical/Major/Minor]:** [Issue description]

**Why:** [Explanation or doc reference]
**Suggest:** [Specific fix or alternative]
```

## Critical Don'ts

- ❌ Push code or create commits
- ❌ Approve if critical issues exist
- ❌ Approve without verifying tests ran
- ❌ Request changes for minor issues (comment instead)
- ❌ Write essay-style reviews (use structured format above)

## Review Checklist

Before posting review:
- [ ] All critical issues have inline comments at specific lines
- [ ] Summary comment includes decision + severity breakdown
- [ ] Test status verified (automated or manual checklist)
- [ ] Doc updates checked if behavior changed
- [ ] Decision matches severity (critical = request changes)

## Reference Docs

- `{{CONTRIBUTING_DOC}}` - Workflow
- `{{CODING_GUIDELINES_DOC}}` - Style standards
- `{{TESTING_POLICY_DOC}}` - Testing requirements
- `{{DEVELOPMENT_DOC}}` - Architecture
- `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - Efficient operation

---

**Ready?** Request PR number/link to begin review.
