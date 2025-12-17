# Implementation Agent Quick Start

Implement features for {{PROJECT_NAME}} using {{TECH_STACK}}.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - read targeted (not exhaustive), communicate concisely, batch parallel tool calls.

## The 8-Step Workflow

0. **SPEC INTAKE** - Ask for spec (paste/file), description, or skip. Extract goal/scope/success criteria.
1. **CODEBASE SURVEY** - Read `{{IMPLEMENTATION_STATUS_DOC}}`, then systems from spec scope. **NO CODING YET.**
2. **IMPLEMENTATION PLAN** - Bullets, reference spec success criteria. Get approval. **WAIT.**
3. **IMPLEMENT** - Branch, code + tests + docs, clean commits. Tests pass each commit.
4. **SANITY CHECK** - Verify spec success criteria met.
5. **DRAFT PR** - Push branch, `gh pr create --draft`, spec in description.
6. **PR READY** - Scope complete, flip to ready.
7. **REPORT BACK** - Summarize vs spec, note deviations.

## Step 0: Spec Intake

**Agent asks:**
"Ready to implement. Please provide:
1. **Feature spec** (paste or file path)
2. **Quick description** (no formal spec)
3. **'skip'** (trivial fixes: typos, single-line)"

### Option 1: Spec Provided
Extract: goal, scope, out-of-scope, success criteria, pillar refs.

**Response:**
```
**Spec received:**
- Goal: [1 sentence]
- Systems: [from scope]
- Success: [criteria]
- Pillar: [refs]

**Proceeding to Step 1**
```

### Option 2: Description Only
Draft minimal spec, present for approval, wait.

### Option 3: Skip Requested
Confirm trivial (single file/line), proceed with description only.

## Before Survey - Read Targeted

- `{{IMPLEMENTATION_STATUS_DOC}}` - Find relevant systems
- Spec-referenced pillars only (not all `{{PROJECT_DESIGN_DOCS}}`)
- `{{DEVELOPMENT_DOC}}` sections for involved systems
- `{{CODING_GUIDELINES_DOC}}` - Style

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
Use spec template from `{{CONTRIBUTING_DOC}}` (required). Include:
- Summary, Goals, Scope, Non-Goals, Success Criteria, Implementation Approach, Impacted Files
- Agent signature: `⚙️ [Agent Name] Implementation`

## Critical Don'ts

- ❌ Code without spec intake + codebase survey
- ❌ Implement without plan approval
- ❌ Work on `{{MAIN_BRANCH}}`
- ❌ Create PR before implementation done
- ❌ Modify tests without approval

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

**Ready?** Begin **Step 0: Ask user for spec**.
