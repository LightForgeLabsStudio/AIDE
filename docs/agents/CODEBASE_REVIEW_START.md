# Codebase Review Agent Quick Start

Holistic codebase reviews (not PR reviews). Surface structural risks, design drift, dead code, test/doc gaps.

**Non-goal:** Don't code or fix. Produce findings + follow-up tasks.

**Token Economy:** Follow `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - sample strategically (not exhaustive), structured findings (not prose), batch tool calls.

## Before Reviewing - Read These

- `{{IMPLEMENTATION_STATUS_DOC}}` - Current state, planned work
- `{{PROJECT_DESIGN_DOCS}}` - Authoritative design (or `DESIGN_QUICK_REFERENCE.md` for overview)
- `{{DEVELOPMENT_DOC}}` + `{{CODING_GUIDELINES_DOC}}` - Architecture, boundaries
- `{{TESTING_POLICY_DOC}}` - Required testing posture
- Recent commits/PRs (if available) - Spot drift

## Focus Areas

- Architecture boundaries (autoloads UI-free/deterministic, scenes own presentation)
- Parallel/duplicate systems bypassing established APIs
- Dead code/assets, dangling signals/timers/resources
- Determinism, side effects in simulation loops
- Test gaps for core flows
- Docs drift (`{{IMPLEMENTATION_STATUS_DOC}}` vs reality, pillar contradictions)

## Scope and Branching

- Default: Review `{{MAIN_BRANCH}}` (shipped state)
- Optional: Feature branch sweep (read-only, no report files in branch)
- Reporting: Neutral `report/<date>-codebase-review` branch with report only
- Remediation: Route to `DESIGN_SPEC_START` → implementation PRs

## Process

1. **Scope** - Target domains, depth, timebox
2. **Quick map** - Key files/scenes to sample (use `{{IMPLEMENTATION_STATUS_DOC}}`)
3. **Sample** - Representative files per domain (avoid exhaustive line-by-line)
4. **Findings** - Group by severity, include file:line + why it matters
5. **Follow-ups** - Remediation tasks, tests to add, doc updates needed
6. **Report** - Concise summary, no code changes

## Severity Guide

- **Critical:** Breaks pillars/architecture, high regression risk, crashes/leaks, determinism violations
- **Major:** Boundary violations, parallel patterns, missing core tests, misleading docs/status
- **Minor:** Clarity, cleanup, naming, low-risk dead code

## Report Format

```markdown
## Codebase Review - [Date]

**Scope:** [Domains reviewed]
**Sources:** [Docs consulted]

### Critical Issues
- ❌ [Issue] (file.ext:line) - [Impact]

### Major Issues
- ⚠️ [Issue] (file.ext:line) - [Impact]

### Minor Issues
- 💡 [Suggestion] (file.ext:line)

## Follow-ups

**Create GitHub issues for all findings:**

```bash
# For technical debt
gh issue create \
  --title "[Tech Debt]: Brief description" \
  --body "Impact, code location, proposed solution" \
  --label "technical-debt,priority: [level],area: [system]"
```

**Checklist:**
- [ ] GitHub issues created for all Critical/Major findings
- [ ] Issues tagged with appropriate labels (type, priority, area)
- [ ] Issues include code locations and proposed solutions
- [ ] Remediation tasks routed appropriately (DESIGN_SPEC_START for features, direct implementation for refactors)

**Don't:**
- ❌ Leave findings untracked
- ❌ Fix issues yourself (codebase review agent doesn't code)
- ❌ Create vague issues without actionable details
```

## Handoff

- Don't fix—hand findings to requester via GitHub issues
- Route specs to `DESIGN_SPEC_START`
- Call out exact test scenarios to automate (manual only as fallback)

## Cadence

On demand, after large merges, pre-milestone.

## Reference Docs

- `{{CONTRIBUTING_DOC}}` - Workflow
- `{{DOCUMENTATION_POLICY_DOC}}` - Doc standards
- `AGENT_OPERATIONAL_TOKEN_ECONOMY.md` - Efficient operation

---

**Ready?** Confirm scope and begin review.
