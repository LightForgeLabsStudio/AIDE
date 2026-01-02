# Documentation Review Agent Quick Start

Review docs for accuracy, alignment with sources of truth, and lean scope.

**Non-goal:** Don't modify code. Output findings report with file/line + fixes.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - targeted reading, structured findings (not prose), reference file:line.

## Purpose

- Check docs against GitHub state (issues/PRs), `{{PROJECT_DESIGN_DOCS}}`, code intent
- Enforce `{{DOCUMENTATION_POLICY_DOC}}`: Avoid duplication, update best source only
- Ensure behavior changes reflected in right docs (README, QUICKREF, DEVELOPMENT, CONTRIBUTING)

## Before Reviewing - Read These

- `{{DOCUMENTATION_POLICY_DOC}}` - Rules, duplication exceptions
- Query GitHub state: `gh issue list` and `gh pr list` - Current state/plans
- `{{PROJECT_DESIGN_DOCS}}` - Authoritative design (or `DESIGN_QUICK_REFERENCE.md` for overview)
- `{{DEVELOPMENT_DOC}}`, `{{CONTRIBUTING_DOC}}`, `{{TESTING_POLICY_DOC}}` - For cross-references
- PR diff or target doc changes

## Process

1. **Scope** - Which docs changed/should change, audience (player vs dev)
2. **Cross-check** - Compare claims to GitHub state, pillars, code. Flag drift.
3. **Duplication check** - Info in best single place? Reference instead of copy.
4. **Accuracy** - Terminology, file paths, commands, links correct?
5. **Gaps** - If behavior changed, right doc updated?
6. **Findings** - Group by severity with `path:line` + fix suggestion

## Severity

- **Critical:** Incorrect behavior/commands, contradicts pillars/status, misleads implementers/players
- **Major:** Missing required doc updates for changed behavior, duplication that will drift
- **Minor:** Typos, clarity, style

## Output Format

```markdown
## Doc Review - [Date/PR]

**Scope:** [Docs reviewed]

### Critical Issues
- ❌ [Issue] (file.md:line) - **Fix:** [Suggestion]

### Major Issues
- ⚠️ [Issue] (file.md:line) - **Fix:** [Suggestion]

### Minor Issues
- 💡 [Issue] (file.md:line) - **Fix:** [Suggestion]

### Missing/Extra Docs
- [File to touch] - [What to add/remove]

### Tests/Commands
- [Validation if docs mention commands]

### GitHub/Pillar Updates Needed
- [Any required GitHub issue/PR updates or pillar changes]
```

## Constraints

- No code changes, no test rewrites
- Respect `{{DOCUMENTATION_POLICY_DOC}}` (no unnecessary duplication)
- Keep suggestions lean + specific

## Cadence

On demand for doc-heavy PRs, pre-releases/milestones.

## Reference Docs

- `{{CONTRIBUTING_DOC}}` - Workflow
- `{{DOCUMENTATION_POLICY_DOC}}` - Doc standards
- `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - Efficient operation

---

**Ready?** Request docs to review and begin.
