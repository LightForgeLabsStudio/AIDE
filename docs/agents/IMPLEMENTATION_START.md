# Implementation Agent Quick Start

Implement features for {{PROJECT_NAME}} using {{TECH_STACK}}.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - read targeted (not exhaustive), communicate concisely, batch parallel tool calls.

## The 7-Step Workflow

1. **CODEBASE SURVEY** - Read `{{IMPLEMENTATION_STATUS_DOC}}` first, then relevant modules. Identify design/code mismatches. **NO CODING YET.**
2. **IMPLEMENTATION PLAN** - Extend patterns, reuse architecture, bullets not prose. Get approval. **WAIT.**
3. **BRANCH + DRAFT PR** - Never on `{{MAIN_BRANCH}}`. Create `feature/<name>`, commit, push, `gh pr create --draft`.
4. **GIT-FIRST DEV** - Clean commits, builds pass, tests pass. Commit milestones: setup → core → tests → docs.
5. **SANITY CHECK** - Test {{user/player/customer}} workflow, edge cases.
6. **PR READY** - Scope complete, tests pass, docs updated. Flip from draft → ready.
7. **REPORT BACK** - Summarize changes, architectural fit, limitations.

## Before Coding - Read These

- `{{IMPLEMENTATION_STATUS_DOC}}` - What's implemented, planned (READ THIS FIRST)
- `{{PROJECT_DESIGN_DOCS}}` - Authoritative design requirements
- `{{DEVELOPMENT_DOC}}` - Architecture patterns
- `{{CODING_GUIDELINES_DOC}}` - Style, module boundaries

**Key Systems:** See `{{DEVELOPMENT_DOC}}` for details:
- `{{SYSTEM_1}}`: {{Brief description}}
- `{{SYSTEM_2}}`: {{Brief description}}
- `{{SYSTEM_3}}`: {{Brief description}}

## Critical Constraints

- **Extend, don't replace** - Reuse existing patterns
- **No test modifications** - Without explicit approval + explanation
- **Design compliance** - Don't contradict docs without permission

## Testing

Follow `{{TESTING_POLICY_DOC}}`. Derive test intent from spec success criteria.

**Coverage (fast first):**
- `{{UNIT_TEST_TYPE}}` for logic
- `{{INTEGRATION_TEST_TYPE}}` for flows
- Manual checklist only if automation impractical (state why in PR)

**Commands:**
```bash
{{RUN_ALL_TESTS_COMMAND}}      # All suites (before PR)
{{RUN_UNIT_TESTS_COMMAND}}     # Fast iteration
```

## Agent Signature

**Commits:**
```bash
git commit -m "Brief imperative summary

Details.

Co-Authored-By: [Agent Name] <agent@{{PROJECT_DOMAIN}}>"
```

**PR body:**
```markdown
**⚙️ [Agent Name] Implementation**

## Summary
[Changes]
```

## Critical Don'ts

- ❌ Code without codebase survey
- ❌ Implement without plan approval
- ❌ Work on `{{MAIN_BRANCH}}`
- ❌ Rewrite systems (extend instead)
- ❌ Modify tests without approval
- ❌ Create spec files unless requested

## PR Review Feedback

**Implementer addresses feedback** (not reviewer).

**Process:**
1. Read review: `gh pr view <number> --comments`
2. Read inline comments: `gh api repos/:owner/:repo/pulls/<number>/comments`
3. Fix systematically: Critical → Major → Minor
4. Commit with reference: `"Fix [issue] from PR review"`
5. Re-run tests
6. Post summary comment with fixes + test status
7. Request re-review

**Summary comment format:**
```markdown
**Addressed PR Review Feedback**

**Critical Fixed:**
- ✅ [Issue] (commit: abc123)

**Tests:** All passing.

Ready for re-review.
```

## Merging After Approval

**Implementer merges** after approval.

```bash
gh pr merge <number> --squash --delete-branch
```

**Merge conflicts:**
1. `git checkout {{MAIN_BRANCH}} && git pull`
2. `git checkout feature/branch && git merge {{MAIN_BRANCH}}`
3. Resolve conflicts, test
4. `git add . && git commit -m "Merge {{MAIN_BRANCH}} to resolve conflicts"`
5. `git push`
6. Re-run `{{RUN_ALL_TESTS_COMMAND}}`
7. Comment: "Resolved conflicts. Tests passing."

## Reference Docs

- `{{CONTRIBUTING_DOC}}` - Full workflow
- `{{CODING_GUIDELINES_DOC}}` - Code style
- `{{TESTING_POLICY_DOC}}` - Testing requirements
- `{{DEVELOPMENT_DOC}}` - Architecture
- `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - Efficient operation

---

**Ready?** Confirm you've read this, then begin **Step 1: Codebase Survey**.
