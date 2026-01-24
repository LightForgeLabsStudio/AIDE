# Contributing / Working Agreement

Minimal, repeatable workflow to keep changes consistent and documented.

## Official Workflow

**All contributors and agents must follow the implementation workflow (Steps 0-10) documented in [agents/IMPLEMENTATION_START.md](../agents/IMPLEMENTATION_START.md).**

To reduce duplication and drift, this file does not restate the step-by-step workflow. Use the primer index as the single source of truth, and load only the step document for the stage you are currently executing.

See [agents/IMPLEMENTATION_START.md](../agents/IMPLEMENTATION_START.md) (index) and [agents/implementation/](../agents/implementation/) (step docs) for complete details.

---

## Contribution Process Summary

1. **Branch:** Create a feature branch for the work (one feature/bugfix per branch)
2. **Plan & Approve:** Write brief spec, share implementation plan, wait for approval
3. **Implement:** Follow [agents/IMPLEMENTATION_START.md](../agents/IMPLEMENTATION_START.md) workflow
4. **Test:** Run tests per [TESTING_POLICY.md](TESTING_POLICY.md)
5. **Document:** Update docs per [DOCUMENTATION_POLICY.md](DOCUMENTATION_POLICY.md)
6. **Review:** Open PR for review per [agents/PR_REVIEW_START.md](../agents/PR_REVIEW_START.md)
7. **Merge:** Address feedback, then implementer merges when approved by reviewer

**Important Constraints:**
- Do not modify existing tests without explicit approval and justification
- Confirm with requester before large refactors or cross-cutting architectural changes
- Align on approach/testing intent before committing significant changes

## PR Review Process

All PRs require review before merging. See [agents/PR_REVIEW_START.md](../agents/PR_REVIEW_START.md) for the complete review workflow.

**Review Expectations:**
- Reviewer inspects: scope, changes, architecture compliance, test results
- Reviewer posts: inline comments on specific lines + summary review
- Findings categorized: Critical (block), Major (request changes), Minor (comment)
- Implementer addresses findings before merge
- **Implementer merges after reviewer approval** (separation of duties: reviewer approves, implementer merges)

### Addressing PR Review Feedback

**Who addresses feedback:** The original implementation agent (or contributor) who created the PR.

**Process:**
1. Read the PR review summary and all inline comments
2. Address each issue systematically:
   - **Critical issues:** Must be fixed before merge (blocking)
   - **Major issues:** Should be fixed or discussed with reviewer
   - **Minor issues/suggestions:** Address if straightforward, or defer to follow-up PR
3. Make focused commits addressing the feedback
4. Re-run all tests to ensure changes don't break existing functionality
5. Push changes and comment on the PR indicating what was addressed
6. Request re-review if critical/major issues were fixed

**Do NOT:**
- Have the review agent fix their own findings (separation of concerns)
- Ignore critical issues and merge anyway
- Make changes without re-testing
- Bundle unrelated improvements with feedback fixes

## Branch and Commit Cadence

- Branch off `{{MAIN_BRANCH}}` for every feature/bugfix; keep one concern per branch
- Make small, reviewable commits that match logical steps: spec/plan written, tests added/updated, feature implemented, docs/changelog updated, final verification
- Avoid combining unrelated changes in the same commit; keep diffs focused and easy to revert
- Use short, descriptive messages that state the change and intent (e.g., "Add user authentication middleware")
- Rebase/merge {{MAIN_BRANCH}} regularly to avoid drift; resolve conflicts on the feature branch before PR

## Spec Template (lightweight)

- Summary: 2-3 sentences on what the feature is
- Goal: what you want to achieve
- Scope: what you will touch/change (modules, components, files)
- Out of scope: what you're not addressing
- Success criteria: bullet list of observable outcomes (and tests)
- Implementation approach: brief outline (systems touched, data/flows, tests to add)
- Impacted files: key modules/components/scripts

Specs live in GitHub Epics + child Issues. PR descriptions summarize the implementation approach and link to the issue.

## Testing Requirements

See [TESTING_POLICY.md](TESTING_POLICY.md) for complete testing requirements.

**Summary:**
- Add deterministic tests for new logic
- Run relevant test suites before opening PR
- Do not modify existing tests without approval

## Documentation Requirements

See [DOCUMENTATION_POLICY.md](DOCUMENTATION_POLICY.md) for complete documentation standards.

**Summary:**
- Update relevant docs when behavior changes (README, {{DEVELOPMENT_DOC}}, design docs)
- Avoid duplicating information across files; use references
- Only create new spec files when explicitly requested
- System invariants live in {{CONTRACTS_DIRECTORY}} (if used); avoid restating them elsewhere

## Code Standards

See [CODING_GUIDELINES.md](CODING_GUIDELINES.md) for complete coding standards.

**Summary:**
- Follow {{LANGUAGE}} style conventions and {{FRAMEWORK}} patterns
- Implement systems according to design docs (see `{{PROJECT_DESIGN_DOCS}}`)
- Keep commits small, focused, and single-purpose

---

## Reference Documentation

**Workflow & Process:**
- [agents/IMPLEMENTATION_START.md](../agents/IMPLEMENTATION_START.md) - Implementation workflow (index)
- [agents/PR_REVIEW_START.md](../agents/PR_REVIEW_START.md) - PR review workflow
- [TESTING_POLICY.md](TESTING_POLICY.md) - Testing requirements and standards
- [DOCUMENTATION_POLICY.md](DOCUMENTATION_POLICY.md) - Documentation standards

**Technical Standards:**
- [CODING_GUIDELINES.md](CODING_GUIDELINES.md) - Code style and architecture standards
- [{{DEVELOPMENT_DOC}}]({{DEVELOPMENT_DOC}}) - Technical architecture reference

**Design Documentation:**
- `{{PROJECT_DESIGN_DOCS}}` - Complete design documentation

## Customization for Your Project

Replace these placeholders:

- `{{MAIN_BRANCH}}` -> `main`, `master`, `develop`
- `{{LANGUAGE}}` -> `TypeScript`, `Python`, `Rust`, `GDScript`
- `{{FRAMEWORK}}` -> `React`, `Django`, `Actix`, `Godot`
- `{{DEVELOPMENT_DOC}}` -> `docs/DEVELOPMENT.md`, `docs/ARCHITECTURE.md`
- `{{CONTRACTS_DIRECTORY}}` -> `docs/contracts/`
- `{{PROJECT_DESIGN_DOCS}}` -> `docs/design/`, `docs/architecture/`
