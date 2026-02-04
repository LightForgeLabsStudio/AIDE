# PR Review Agent Quick Start

Review PRs for {{PROJECT_NAME}} ({{TECH_STACK}}).

**Non-goal:** Don't push code/fixes. Provide findings and decisions only.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - structured reviews (not prose), reference file:line, batch tool calls.

## Review Request Format

User may request reviews with optional custom checklists/concerns:

```
Review PR#<number>

[Optional: Additional verification points]
When reviewing, also verify:
- Custom concern 1
- Custom concern 2
```

**Process:**
1. Always verify PR links to issue and read full spec from issue (per `{{CONTRIBUTING_DOC}}`)
2. Apply standard review checklist (scope, architecture, tests, docs)
3. Apply any custom verification points provided in the request
4. Structure review to cover both standard + custom items

## Review Process

### Initial Review
1. **Context** - Get PR number, scope, test results
2. **Fetch PR** - `gh pr view <number>` or `gh pr diff <number>`
3. **Read spec from linked issue** - Extract issue number from PR description (e.g., "Fixes #42"), then:
   ```bash
   gh issue view <number> --comments
   ```
   Read: goals, scope, non-goals, success criteria, pillar refs, and any clarification discussions from comments
4. **Verify scope** - Implementation matches spec goals/scope/success criteria from issue
5. **Review commits** - Quality, size, logical flow
6. **Review code** - Bugs, style, architecture, alignment with spec
7. **Apply custom checks** - If provided in review request
8. **Verify tests** - Automated ran + passed (or manual checklist provided), match spec success criteria from issue
9. **Check docs** - Updated if behavior changed
10. **Post inline comments** - Line-specific issues via `gh pr comment`
11. **Post summary** - Overall findings + spec alignment + decision (as comment)
12. **Decide** - Approve / Request changes / Comment (verdict in comment body, NOT formal approval)

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

### Spec Alignment (REQUIRED)

**Exception:** Issue linking may be skipped for:

- **Tooling/infrastructure** - CI scripts, build config, dev tools (label with `tooling`)
- **Documentation-only** - Typo fixes, formatting, doc improvements with no behavior changes (label with `docs`)
- **Trivial fixes** - Single-line fixes, obvious corrections (< 10 lines changed, label with `trivial`)

**If PR claims exception:** Verify it truly qualifies (no behavior changes, no new features, no architecture impact). If in doubt, request issue.

**For all other PRs:**

- [ ] PR links to GitHub issue containing spec (via "Fixes #X")
- [ ] Issue contains complete spec (goals, scope, non-goals, success criteria)
- [ ] Implementation delivers spec goals from issue
- [ ] Scope matches spec from issue (not over/under delivered)
- [ ] Success criteria met (tests confirm criteria from issue)
- [ ] Non-goals respected (nothing out of scope added)

**If issue link missing or spec misaligned (and no valid exception):** Request Changes (Critical)

### Code Quality
- [ ] No security risks, resource leaks
- [ ] No bugs or logic errors
- [ ] Follows `{{CODING_GUIDELINES_DOC}}` style
- [ ] Module boundaries respected
- [ ] No over-engineering
- [ ] No debug code, commented blocks, orphaned TODOs
- [ ] Code refinement performed (Step 5 of implementation):
  - [ ] No dead code (unused functions, commented blocks)
  - [ ] No backward compatibility wrappers after migration complete
  - [ ] No deprecated constants/types still defined (check Config, enums)
  - [ ] Function names updated to reflect current behavior (no legacy naming)
  - [ ] Simplified (reduced nesting, extracted complex logic, eliminated duplication)
  - [ ] Follows `{{BEST_PRACTICES_DOC}}` patterns
  - [ ] Scalable abstractions where appropriate (data-driven vs hardcoded)
  - [ ] Self-documenting names, minimal comments

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
- **PR doesn't link to GitHub issue (missing "Fixes #X")**
- **Linked issue missing spec (goals, scope, success criteria)**
- **Implementation doesn't match spec from issue (over/under delivered)**
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

# Post review comment (ALWAYS use this - same git account prevents formal approval)
gh pr comment <number> --body "Review summary with verdict..."

# Post inline code comment (specific line)
gh api repos/:owner/:repo/pulls/<number>/comments \
  -f body="Comment text" \
  -f path="file.ext" \
  -f commit_id="<commit-sha>" \
  -F position=5

# Read inline comments
gh api repos/:owner/:repo/pulls/<number>/comments
```

**IMPORTANT:** Since reviewer and implementer share the same git account:
- DO NOT use `gh pr review --approve` or `--request-changes` (will fail)
- ALWAYS use `gh pr comment` with verdict in the comment body
- Verdict format: "**Decision:** ✅ Approve" or "**Decision:** ❌ Request Changes"

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

### Follow-up Issues (Suggest - Don't Block)
- 💡 [Out-of-scope suggestion] - Consider creating issue for [description]

### Follow-up Issues (Demand - Block Until Tracked)
- ⚠️ [Critical out-of-scope bug/debt] - Must create issue before merge: [description]

### Strengths
- ✅ [Good practice observed]

**Tests:** [Passed / Failed / Not run / Manual only]
**Docs:** [Updated / Not needed / Missing]

---
*Review by [Agent Name]*
```

**Note on Follow-up Issues sections:**
- Use "Suggest" for out-of-scope nice-to-haves (optimizations, additional tests, future enhancements) - don't block merge
- Use "Demand" for critical out-of-scope bugs or major architectural debt discovered during review - block merge until issue created
- See "Follow-up Issues" section below for detailed guidance on when to suggest vs demand

**Inline comment format:**
```markdown
**[Critical/Major/Minor]:** [Issue description]

**Why:** [Explanation or doc reference]
**Suggest:** [Specific fix or alternative]
```

## Follow-up Issues

**Reviewer role:** Identify follow-up work, but don't create issues directly (implementer creates).

### Suggest (Comment - Don't Block Merge)

**When:**
- Performance optimizations (non-blocking)
- Additional test coverage (beyond minimum)
- Future enhancements
- Minor technical debt

**Example:**
```markdown
**Minor:** Consider caching pathfinding results for frequently-used routes.
**Suggest:** Create follow-up issue for performance optimization (out of scope for this PR).
```

### Demand (Critical - Block Merge)

**When:**
- **Bug discovered during review** (out of scope for this PR)
- **Major architectural technical debt introduced**

**Example:**
```markdown
**Critical:** Out-of-scope bug: Drone crashes when job queue is empty.
**Action required:** Create bug issue before merging. This must be tracked.
```

**Process:**
1. Reviewer flags critical issue requiring tracking
2. Implementer creates issue via `gh issue create`
3. Implementer adds issue number to PR description: "Discovered #123 (out of scope)"
4. Reviewer verifies issue created, approves PR

**Don't block merge for nice-to-haves.** Only demand issue creation for critical bugs/debt.

## Critical Don'ts

- ❌ Push code or create commits
- ❌ Use `gh pr review --approve` (same git account - will fail)
- ❌ Approve verdict if critical issues exist
- ❌ Approve verdict without verifying tests ran
- ❌ Request changes verdict for minor issues (comment verdict instead)
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
