# Implementation Agent Quick Start

**You are implementing features for {{PROJECT_NAME}} using {{TECH_STACK}}.** This document contains everything you need to start.

## The 7-Step Workflow

**Follow these phases for every feature. No exceptions.**

1. **CODEBASE SURVEY** - Inspect current branch, relevant modules/components, and architecture. Identify design/code mismatches. **NO CODING YET.**
2. **MINIMAL IMPLEMENTATION PLAN** - Prefer extension over replacement, reuse established patterns, break into commits. Use spec template from [CONTRIBUTING.md](../core/CONTRIBUTING.md#spec-template-lightweight). **WAIT FOR APPROVAL.**
3. **BRANCH & DRAFT PR SETUP** - Never work on `{{MAIN_BRANCH}}`. Before any edits, create/confirm a feature branch (`git checkout -b feature/<name>`). After the first commit, push and open a draft PR via GitHub CLI (`gh pr create --draft`), then keep pushing as you work.
4. **GIT-FIRST DEVELOPMENT** - Clean, single-purpose commits that keep the project running (builds pass, tests pass). Commit at logical milestones (setup, core code, updates, tests/docs). Include `Co-Authored-By` for attribution.
5. **SANITY CHECK** - Exercise the {{user/player/customer}} workflow and identify edge cases; propose fixes.
6. **PR DRAFT** - Keep the PR updated: summarize changes, intent, impact, tests run, TODOs. Ensure test results are included. Flip from draft to "Ready for review" only when scope is complete, tests pass, sanity check done, docs/status touched if needed, and the PR body is up to date.
7. **DOCS + REPORT BACK** - Update high-level docs only if conceptually affected. **Create new specs only when explicitly requested.** Summarize what was done, architectural fit, and limitations.

## Critical Architecture Principles

Before implementing, familiarize yourself with the core architectural constraints documented in:
- **Implementation Status**: `{{IMPLEMENTATION_STATUS_DOC}}` - What's implemented, in-progress, and planned (READ THIS FIRST for context)
- **Design Documentation**: `{{PROJECT_DESIGN_DOCS}}` - Authoritative design decisions
- **Architecture Reference**: `{{DEVELOPMENT_DOC}}` - Technical implementation patterns
- **Code Standards**: `{{CODING_GUIDELINES_DOC}}` - Style and module boundaries

**Key Implementation Constraints:**
- **Extension Over Replacement** - Don't rewrite systems; extend existing patterns and interfaces
- **No Test Modifications** - Don't modify existing tests without explicit approval and explanation
- **Design Compliance** - Don't contradict design docs without explicit permission

## Key Systems Overview

For detailed architecture, see `{{DEVELOPMENT_DOC}}`. Quick reference:
- **{{SYSTEM_1}}**: {{Brief description}}
- **{{SYSTEM_2}}**: {{Brief description}}
- **{{SYSTEM_3}}**: {{Brief description}}

Consult `{{DEVELOPMENT_DOC}}` for component responsibilities and boundaries.

## Testing Expectations and Commands

Testing must follow `{{TESTING_POLICY_DOC}}`. Derive test intent from the approved spec (success criteria and suggested automated scenarios), add targeted tests as part of implementation, and avoid modifying existing tests without approval.

**Preferred coverage (fast first):**
- **{{UNIT_TEST_TYPE}}** for pure logic ({{modules/classes/functions}})
- **{{INTEGRATION_TEST_TYPE}}** for flows ({{workflows/APIs/UIs}})
- Manual checklist only if automation is impractical (state why in PR)

**Commands:**
```bash
# Run all suites (preferred before PR)
{{RUN_ALL_TESTS_COMMAND}}

# Fast unit-only pass (when iterating)
{{RUN_UNIT_TESTS_COMMAND}}
```

If no automated coverage exists yet, include a short, repeatable manual checklist in the PR and note the missing automation.

## Agent Signature Convention

**IMPORTANT:** When creating commits or PRs, use a consistent agent signature to distinguish your work from other agents working on the same repository.

**For Commits:**
Use the `Co-Authored-By` trailer with your agent identity:
```bash
git commit -m "Implement feature X

Implementation details here.

Co-Authored-By: [Your Agent Name] <agent@{{PROJECT_DOMAIN}}>"
```

**For PR Descriptions:**
Prefix PR body with your agent signature:
```markdown
**⚙️ [Your Agent Name] Implementation**

## Summary
[Implementation summary]

---
*Implemented by [Your Agent Name]*
```

**Examples:**
- `Co-Authored-By: Claude <claude@{{PROJECT_DOMAIN}}>` / `**⚙️ Claude Implementation**`
- `Co-Authored-By: Codex <codex@{{PROJECT_DOMAIN}}>` / `**⚙️ Codex Implementation**`

This ensures clear attribution when multiple AI agents collaborate on the same repository.

## Critical Don'ts

**Workflow Violations:**
- Don't start coding without completing the codebase survey
- Don't implement without getting plan approval
- Don't create new technical spec files unless explicitly requested

**Architecture Violations:**
- Don't rewrite existing systems (extend, don't replace)
- Don't contradict design docs without permission
- Don't violate documented architecture patterns

**Testing Violations:**
- Don't modify existing tests without approval and justification

## Addressing PR Review Feedback

When a PR receives review feedback with requested changes, **the original implementation agent addresses the feedback** (not the review agent).

**Process:**
1. Read the PR review summary at the PR URL
2. Read all inline comments on specific lines (critical context!)
3. Address issues systematically:
   - **Critical:** Must fix before merge (blocking)
   - **Major:** Fix or discuss with reviewer
   - **Minor:** Address if straightforward, or note for follow-up
4. Make focused commits addressing feedback (use descriptive commit messages referencing the review)
5. Re-run all affected tests
6. Push changes and comment on PR indicating what was addressed
7. Request re-review from the original reviewer

**Example workflow:**
```bash
# 1. Read review summary and general comments
gh pr view <number> --comments

# 2. Read inline review comments (specific lines with issues)
gh api repos/:owner/:repo/pulls/<number>/comments --jq '.[] | "\(.path):\(.line)\n\(.body)\n"'

# 3. Make fixes following the 7-step workflow (survey → plan → implement → test)

# 4. Commit with clear reference to review
git commit -m "Fix {{issue}} from PR review

{{Description of fix}}

Addresses: [PR review inline comments]"

# 5. Push and post status update
git push
gh pr comment <number> --body "**Addressed PR Review Feedback**

**Critical Issues Fixed:**
- ✅ {{Issue 1}}
- ✅ {{Issue 2}}

**Tests:** All passing.

Ready for re-review."
```

**How to Reply to Review Comments:**

**Best Practice - Post One Summary Comment:**
```bash
gh pr comment <number> --body "**Addressed PR Review Feedback**

**Critical Issues Fixed:**
- ✅ [Issue 1 description] (commit: abc123)

**Major Issues Fixed:**
- ✅ [Issue description] (commit: def456)

**Questions Answered:**
- Q: [Question from review]
- A: [Your answer]

**Tests:** All passing.

Ready for re-review."
```

**Don't:**
- ❌ Push fixes silently without any comment
- ❌ Use only generic "fixed" responses without details
- ❌ Argue with critical issues - discuss if unclear, but address them

**Do:**
- ✅ Post one comprehensive summary comment (required)
- ✅ Reference specific commits that address each issue
- ✅ Include test results
- ✅ Answer any questions raised

## Merging After Approval

**Who merges:** The implementer (original PR author) merges after receiving approval from the reviewer.

**Process:**
1. Wait for reviewer approval comment/review
2. Verify all tests pass
3. Merge the PR using GitHub CLI or UI

**Merge command:**
```bash
# Merge PR after approval (implementer responsibility)
gh pr merge <number> --squash --delete-branch
```

**Merge strategies:**
- **Squash merge** (recommended for most PRs): Combines all commits into one clean commit
- **Merge commit** (for multi-commit PRs with meaningful history): Preserves individual commits
- **Rebase** (if explicitly requested): Replays commits on top of main

Use squash merge by default unless the PR has a meaningful multi-commit history worth preserving.

### Handling Merge Conflicts

**When conflicts occur:**
GitHub will prevent merging if your branch conflicts with the base branch. The implementer must resolve conflicts before merging.

**Conflict resolution process:**

1. **Update your local {{MAIN_BRANCH}} branch:**
```bash
git checkout {{MAIN_BRANCH}}
git pull origin {{MAIN_BRANCH}}
```

2. **Merge {{MAIN_BRANCH}} into your feature branch (recommended) OR rebase:**
```bash
# Option A: Merge (safer, preserves history)
git checkout feature/your-branch
git merge {{MAIN_BRANCH}}

# Option B: Rebase (cleaner history, but rewrites commits)
git checkout feature/your-branch
git rebase {{MAIN_BRANCH}}
```

3. **Resolve conflicts in your editor:**
- Open conflicted files (marked with `<<<<<<<`, `=======`, `>>>>>>>`)
- Choose which changes to keep (yours, theirs, or combination)
- Remove conflict markers
- Test the resolved code to ensure it still works

4. **Complete the merge/rebase:**
```bash
# If you merged:
git add .
git commit -m "Merge {{MAIN_BRANCH}} into feature/your-branch to resolve conflicts"

# If you rebased:
git add .
git rebase --continue
```

5. **Push the resolved conflicts:**
```bash
# Normal push after merge:
git push

# Force push after rebase (use with caution):
git push --force-with-lease
```

6. **Re-run tests and verify:**
```bash
{{RUN_ALL_TESTS_COMMAND}}
```

7. **Comment on PR:**
```bash
gh pr comment <number> --body "Resolved merge conflicts with {{MAIN_BRANCH}}. All tests passing."
```

**Important notes:**
- **Always test after resolving conflicts**
- **Never force push without `--force-with-lease`**
- **If you rebased, notify the reviewer**
- **Ask for help if conflicts are complex**

## Reference Docs (for deeper detail)

**Workflow & Standards:**
- `{{CONTRIBUTING_DOC}}` - Full workflow details
- `{{CODING_GUIDELINES_DOC}}` - Code style and boundaries
- `{{TESTING_POLICY_DOC}}` - Testing requirements
- [PR_REVIEW_START.md](PR_REVIEW_START.md) - Review workflow

**Architecture & Design:**
- `{{DEVELOPMENT_DOC}}` - Technical architecture reference
- `{{PROJECT_DESIGN_DOCS}}` - Design documentation

---

**Ready?** Tell the requester you've read this document and are ready for their feature request OR to address PR review feedback. Then begin with **Step 1: Codebase Survey**.

## Customization for Your Project

Replace these placeholders:

- `{{PROJECT_NAME}}` → Your project name
- `{{TECH_STACK}}` → "Node.js 20 + TypeScript 5", "Python 3.11 + FastAPI", "Rust + Actix"
- `{{MAIN_BRANCH}}` → "main", "master", "develop"
- `{{PROJECT_DOMAIN}}` → "example.com", "mycompany.dev"
- `{{IMPLEMENTATION_STATUS_DOC}}` → "docs/IMPLEMENTATION_STATUS.md"
- `{{PROJECT_DESIGN_DOCS}}` → "docs/design/", "docs/specs/", "docs/adr/"
- `{{DEVELOPMENT_DOC}}` → "docs/DEVELOPMENT.md", "docs/ARCHITECTURE.md"
- `{{CODING_GUIDELINES_DOC}}` → "docs/CODING_GUIDELINES.md"
- `{{TESTING_POLICY_DOC}}` → "docs/TESTING_POLICY.md"
- `{{CONTRIBUTING_DOC}}` → "docs/CONTRIBUTING.md"
- `{{SYSTEM_1/2/3}}` → Your key systems/modules
- `{{UNIT_TEST_TYPE}}` → "Jest unit tests", "pytest tests", "cargo tests"
- `{{INTEGRATION_TEST_TYPE}}` → "Playwright e2e tests", "integration tests"
- `{{RUN_ALL_TESTS_COMMAND}}` → "npm test", "pytest", "cargo test"
- `{{RUN_UNIT_TESTS_COMMAND}}` → "npm run test:unit", "pytest tests/unit"
