---
name: evolve
description: Apply the AIDE system evolution workflow to repeated mistakes. Reads SYSTEM_EVOLUTION.md and outputs a concrete proposal for turning failures into rules or automation.
---

# AIDE Evolve

Turn repeated mistakes into system improvements (constraints, docs, automation).

## Workflow

### 1. Locate repo root
Walk up from current directory until you find `AGENTS.md`.

### 2. Read the evolution guide
Read `.aide/docs/agents/SYSTEM_EVOLUTION.md` for the decision tree and trigger criteria.

### 3. Collect failure pattern inputs
Ask the user for:
- **What happened?** (Describe the failure/mistake)
- **How many times?** (Must be 2+ occurrences across sessions/PRs)
- **Evidence:** (PR/issue links or brief excerpts showing the pattern)
- **Where should it have been caught?** (Tooling? Docs? Invariant?)

### 4. Apply decision tree
Use this hierarchy (smallest effective change):

**1. Can it be automated?**
- Is it enforceable by tooling (lint, validator, CI check)?
- If YES → Propose automation (scripts, CI, pre-commit hook)

**2. Is it project-wide binding?**
- Does it apply to ALL code/features?
- Is violating it a critical error?
- If YES → Tier 1 constraint (AGENTS.md)

**3. Is it system-specific guidance?**
- Does it apply to a specific subsystem/pattern?
- Is it helpful but not critical?
- If YES → Tier 2 guidance (docs/[system].md)

**4. Is it informational only?**
- Is it a best practice but not enforceable?
- If YES → Reference-only (docs/reference/ or comments)

### 5. Output concrete proposal
```markdown
## System Evolution Proposal

### Failure Pattern
**What:** [Clear description]
**Frequency:** [X times across Y PRs/sessions]
**Evidence:**
- [PR/issue link or excerpt 1]
- [PR/issue link or excerpt 2]

### Analysis
**Where it should be caught:** [Tooling/Docs/Invariant]
**Impact if violated:** [Low/Medium/High]
**Enforceable by automation:** [Yes/No]

### Decision: [AUTOMATION | TIER 1 | TIER 2 | REFERENCE]

**Rationale:** [1-2 sentences explaining why this tier/approach]

### Proposed Change

**Location:** [Exact file path + section heading]

**Current state:** [What exists now, if anything]

**Proposed addition:**
```
[Exact text to add - use positive constraints, not negative]
```

**Example in practice:**
```
[Show how this rule/check would prevent the failure]
```

### Implementation Steps
1. [What to modify/add]
2. [Testing/validation needed]
3. [PR creation]

### Next Action
[Create PR? Add to automation? Update docs?]
```

### 6. Important constraints
- Use positive language ("Do X" not "Don't do Y")
- Be specific and measurable
- Include examples showing correct behavior
- If automation: specify exact tool/command
- If Tier 1: must be universally applicable

### 7. Get approval before implementing
After proposing the change:
- Ask if the user agrees with the tier/approach
- Confirm the proposed wording is clear
- Get approval before creating PR or modifying files

## Examples

**Automation example:**
```
Decision: AUTOMATION
Location: .github/workflows/pr-check.yml
Proposed: Add validator for PR body formatting
Rationale: Enforceable via regex, prevents recurring formatting issues
```

**Tier 1 example:**
```
Decision: TIER 1
Location: AGENTS.md → Critical Invariants
Proposed: "InventoryService is the single source of truth for item quantities"
Rationale: Project-wide invariant, violations cause data corruption
```

**Tier 2 example:**
```
Decision: TIER 2
Location: docs/UI_PATTERNS.md
Proposed: "Prefer IconButton over TextButton for toolbars (consistency)"
Rationale: UI pattern, not critical but improves UX consistency
```

## Important Notes
- Do NOT modify files until user approves
- Prefer automation when possible (enforced > documented)
- Keep constraints actionable and testable
- Link to evidence (PRs/issues where pattern occurred)
- This is about preventing future failures, not blame