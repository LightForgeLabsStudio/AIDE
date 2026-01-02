# Implementation Agent Quick Start

Implement features for {{PROJECT_NAME}} using {{TECH_STACK}}.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - read targeted (not exhaustive), communicate concisely, batch parallel tool calls.

**Default Behavior:** For implementation work, complete the full workflow (branch, tests, draft PR, ready PR) unless the user explicitly opts out of any step.

## The 9-Step Workflow

0. **SPEC INTAKE** - Ask for spec (paste/file), description, or skip. Extract goal/scope/success criteria.
1. **CODEBASE SURVEY** - Query GitHub for related issues/epics, then read systems from spec scope. **NO CODING YET.**
   - **Spec ⇄ Codebase Alignment:** Identify constraints/mismatches, list assumptions, and ask clarifying questions before planning.
2. **IMPLEMENTATION PLAN** - Bullets, reference spec success criteria. Get approval. **WAIT.**
3. **IMPLEMENT** - Branch, code + tests + docs, clean commits. Tests pass each commit.
4. **SANITY CHECK** - Verify spec success criteria met.
5. **CODE REFINEMENT** - Cleanup, simplify, align with best practices. Check scalability.
6. **DRAFT PR** - Push branch, `gh pr create --draft`, spec in description.
7. **PR READY** - Scope complete, flip to ready.
8. **REPORT BACK** - Summarize vs spec, note deviations.

## Step 0: Spec Intake

**Agent asks:**
"Ready to implement. Please provide:
1. **GitHub issue number** (spec in issue)
2. **Spec or batch of specs** (I'll create issue(s) for tracking)
3. **'skip'** (trivial fixes: typos, single-line)"

Also ask: "Proceed with full workflow (branch/tests/PR)? Say 'skip git', 'skip tests', or 'skip PR' to opt out."

### Option 1: Issue Number Provided

**Read issue:**
```bash
gh issue view <number>
```

Extract: goal, scope, out-of-scope, success criteria, pillar refs from issue description.

**Mark in progress:**
```bash
gh issue edit <number> --add-label "status: in-progress"
```

### Option 2: Spec or Batch of Specs Provided

**Single spec:** Create one tracking issue.
**Batch of specs:** Iterate through list (markdown sections, numbered, etc.), create issue for each.

**For each spec:**
```bash
gh issue create \
  --title "[Feature]: <brief title>" \
  --body "<full spec>" \
  --label "enhancement,priority: <level>,area: <system>,status: ready"
```

**If batch, output table:**
```
Created 5 issues:
- #42: Job Priority System (priority: high, area: job-system)
- #43: Drone Cargo Visualization (priority: medium, area: drone-ai, ui)
- #44: Building Health Indicators (priority: low, area: buildings, ui)
```

**If batch, ask:** "Which issue would you like to implement first?"

**Extract from issue:** goal, scope, out-of-scope, success criteria, pillar refs.

**Continue with Option 1** workflow (mark in-progress, alignment, etc.).

### Spec ⇄ Codebase Alignment (All Options)

**Before planning:** Do a brief alignment pass:
- Call out spec items that conflict with known architecture/engine constraints
- List assumptions the plan would rely on
- Ask clarifying questions to preserve intent

**If clarifications needed:**
```bash
# Post question to issue
gh issue comment <number> --body "**Clarification needed:**

<question>

**Context:** <why this matters>

**Options:** <if applicable>"
```

**Wait for user response.** User will answer in issue comments or update issue description.

**Read updated issue:**
```bash
gh issue view <number> --comments
```

**Response:**
```
**Spec received (issue #<number>):**
- Goal: [1 sentence]
- Systems: [from scope]
- Success: [criteria]
- Pillar: [refs]

**Proceeding to Step 1 (Survey + Alignment)**
```

### Option 3: Skip Requested
Confirm trivial (single file/line), proceed with description only.

## Before Survey - Read Targeted

- `{{GITHUB_QUERIES_DOC}}` - Query GitHub for related issues/epics and implementation status
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

## Step 5: Code Refinement

After implementation complete + spec verified, refine before PR:

**Checklist:**
- [ ] **Remove dead code** - Unused functions, commented blocks, debug prints
- [ ] **Simplify** - Reduce nesting, extract complex logic to functions, eliminate duplication
- [ ] **Best practices** - Follow `{{BEST_PRACTICES_DOC}}` (technology-specific patterns)
- [ ] **Scalability** - Abstract where extension likely (multiple similar entities → data-driven)
- [ ] **Clarity** - Self-documenting names, minimal comments (explain why, not what)

**Output (concise):**
```markdown
**Code Refinement:**
- Removed: [dead code items]
- Simplified: [what was refactored]
- Abstracted: [scalability improvements]
- No changes needed (already clean)
```

**Skip if:** Trivial changes (Step 0: skip), refactoring would exceed spec scope.

## Handling Out-of-Scope Work

**If you discover bugs or issues outside the current spec:**

1. **Document** the problem clearly
2. **Create GitHub issue** to track it:
   ```bash
   gh issue create \
     --title "[Bug]: Brief description" \
     --body "Description, reproduction steps, code location" \
     --label "bug,priority: [level],area: [system]"
   ```
3. **Comment in PR** that issue was discovered and tracked
4. **Continue** with current implementation (don't expand scope)

**Example:**
> Note: Discovered pathfinding issue with diagonal obstacles during testing. Created #42 to track. Out of scope for this PR.

**Don't:**
- ❌ Fix out-of-scope bugs in current PR (expands scope)
- ❌ Ignore problems without tracking them
- ❌ Let technical debt accumulate silently

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
- **Issue reference:** `Fixes #<number>` (auto-closes issue on merge)
- Agent signature: `⚙️ [Agent Name] Implementation`

**Commit messages:** Reference issue number for traceability:
```bash
git commit -m "Add job prioritization (refs #42)"
```

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

- `{{GITHUB_QUERIES_DOC}}` - GitHub queries for implementation status
- `{{CONTRIBUTING_DOC}}` - Full workflow
- `{{CODING_GUIDELINES_DOC}}` - Code style
- `{{TESTING_POLICY_DOC}}` - Testing requirements
- `{{DEVELOPMENT_DOC}}` - Architecture
- `{{BEST_PRACTICES_DOC}}` - Technology-specific patterns (e.g., Godot, React, Rust)
- `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - Efficient operation

---

**Ready?** Begin **Step 0: Ask user for spec**.

## Customization for Your Project

Replace these placeholders with your project specifics:

- `{{PROJECT_NAME}}` → Your project name
- `{{TECH_STACK}}` → "Godot 4.5 + GDScript", "Node.js + TypeScript", "Rust + Actix"
- `{{MAIN_BRANCH}}` → "main", "master", "develop"
- `{{PROJECT_DOMAIN}}` → "example.com", "yourproject.dev"
- `{{GITHUB_QUERIES_DOC}}` → ".aide/docs/agents/GITHUB_QUERIES.md" (reference for querying implementation status)
- `{{PROJECT_DESIGN_DOCS}}` → "design/", "docs/specs/", "docs/adr/"
- `{{DEVELOPMENT_DOC}}` → "docs/DEVELOPMENT.md", "docs/ARCHITECTURE.md"
- `{{CODING_GUIDELINES_DOC}}` → "docs/CODING_GUIDELINES.md"
- `{{TESTING_POLICY_DOC}}` → "docs/TESTING_POLICY.md"
- `{{CONTRIBUTING_DOC}}` → "docs/CONTRIBUTING.md"
- `{{BEST_PRACTICES_DOC}}` → "docs/GODOT_BEST_PRACTICES.md", "docs/REACT_PATTERNS.md"
- `{{UNIT_TEST_TYPE}}` → "GUT unit tests", "Jest tests", "pytest"
- `{{INTEGRATION_TEST_TYPE}}` → "GUT integration tests", "Playwright e2e"
- `{{RUN_ALL_TESTS_COMMAND}}` → "cmd /c run_tests.bat", "npm test", "cargo test"
- `{{RUN_UNIT_TESTS_COMMAND}}` → "Godot_v4.5.1_console.exe --headless -s addons/gut/gut_cmdln.gd"
