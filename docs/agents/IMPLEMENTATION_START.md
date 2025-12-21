# Implementation Agent Quick Start

Implement features for {{PROJECT_NAME}} using {{TECH_STACK}}.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - read targeted (not exhaustive), communicate concisely, batch parallel tool calls.

## The 9-Step Workflow

0. **SPEC INTAKE** - Ask for spec (paste/file), description, or skip. Extract goal/scope/success criteria.
1. **CODEBASE SURVEY** - Read `{{IMPLEMENTATION_STATUS_DOC}}`, then systems from spec scope. **NO CODING YET.**
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
1. **Feature spec** (paste or file path)
2. **Quick description** (no formal spec)
3. **'skip'** (trivial fixes: typos, single-line)"

### Option 1: Spec Provided
Extract: goal, scope, out-of-scope, success criteria, pillar refs.

**Then (before planning):** Do a brief **Spec ⇄ Codebase Alignment** pass:
- Call out spec items that conflict with known architecture/engine constraints.
- List assumptions the plan would rely on.
- Ask clarifying questions (or propose small spec edits) to preserve intent and avoid unintended behavior changes.

**Response:**
```
**Spec received:**
- Goal: [1 sentence]
- Systems: [from scope]
- Success: [criteria]
- Pillar: [refs]

**Proceeding to Step 1 (Survey + Alignment)**
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
- `{{IMPLEMENTATION_STATUS_DOC}}` → "docs/IMPLEMENTATION_STATUS.md"
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
