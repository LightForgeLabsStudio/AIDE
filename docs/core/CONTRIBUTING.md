# Contributing / Working Agreement

Minimal, repeatable workflow to keep changes consistent and documented.

## Official Workflow

**All contributors and agents must follow the 7-Step Workflow documented in [agents/IMPLEMENTATION_START.md](../agents/IMPLEMENTATION_START.md).**

The workflow ensures consistent, reviewable changes:
1. Codebase Survey → 2. Implementation Plan → 3. Git-First Development → 4. Sanity Check → 5. PR Draft → 6. Update Docs → 7. Report Back

See [agents/IMPLEMENTATION_START.md](../agents/IMPLEMENTATION_START.md) for complete details.

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

Keep specs in PR/commit descriptions or a short note; create `{{SPECS_DIRECTORY}}/<feature>.md` only for bigger features when requested.

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

## Code Standards

See [CODING_GUIDELINES.md](CODING_GUIDELINES.md) for complete coding standards.

**Summary:**
- Follow {{LANGUAGE}} style conventions and {{FRAMEWORK}} patterns
- Implement systems according to design docs (see `{{PROJECT_DESIGN_DOCS}}`)
- Keep commits small, focused, and single-purpose

---

## Reference Documentation

**Workflow & Process:**
- [agents/IMPLEMENTATION_START.md](../agents/IMPLEMENTATION_START.md) - 7-Step implementation workflow
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

- `{{MAIN_BRANCH}}` → `main`, `master`, `develop`
- `{{LANGUAGE}}` → `TypeScript`, `Python`, `Rust`, `GDScript`
- `{{FRAMEWORK}}` → `React`, `Django`, `Actix`, `Godot`
- `{{DEVELOPMENT_DOC}}` → `docs/DEVELOPMENT.md`, `docs/ARCHITECTURE.md`
- `{{SPECS_DIRECTORY}}` → `docs/specs/`, `docs/rfcs/`, `docs/adr/`
- `{{PROJECT_DESIGN_DOCS}}` → `docs/design/`, `docs/specs/`, `docs/architecture/`
