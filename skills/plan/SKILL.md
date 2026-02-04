---
name: plan
description: Create a two-layer AIDE implementation plan from an issue/PR spec using project constraints and placeholder mappings.
---

# AIDE Plan

Create a two-layer AIDE implementation plan from a task spec.

## Workflow

### 1. Locate repo root
Assume the current workspace is the repo root.

### 2. Get the task spec
Ask user for:
- Issue/PR description text (preferred)
- OR issue number (will fetch via `gh issue view [number]`)
- OR PR number (will fetch via `gh pr view [number]`)

If user provides a number, fetch the full spec with `gh`.

### 3. Read project constraints
Use project constraints and placeholder mappings to capture:
- Critical invariants (top section)
- Design pillars
- Architectural constraints
- Quality commands (`{{RUN_ALL_TESTS_COMMAND}}`, `{{LINT_COMMAND}}`, etc.)
- Testing policy

### 4. Produce Layer 1 Constraints
Extract project-wide rules that apply to this task:
- Which invariants apply?
- Which systems/services are authoritative?
- What boundaries must be respected?
- What patterns must be followed?

Output as short bullet list (<=8 items).

### 5. Produce Layer 2 Plan
Create ordered implementation steps with exit criteria:

Format:
```
1. [Step name] - [What to do] → Exit: [How to verify this step is done]
2. [Step name] - [What to do] → Exit: [How to verify this step is done]
...
```

Include:
- Files likely to be touched
- Testing strategy (smallest scope first)
- Validation commands to run
- Risks or unknowns

Keep plan concise (<=12 steps).

### 6. Output format
```markdown
## Layer 1: Constraints
- [Project-wide rule that applies]
- [Architectural boundary to respect]
- [Authoritative service pattern]
...

## Layer 2: Implementation Plan

**Files Likely Touched:**
- [file path] - [why]
- [file path] - [why]

**Steps:**
1. [Step] → Exit: [criteria]
2. [Step] → Exit: [criteria]
...

**Testing Strategy:**
- Unit tests: [which tests to write/modify]
- Integration tests: [if needed]
- Validation: `[project-configured command]`

**Risks/Unknowns:**
- [Any uncertainty or decision points]
- [Questions to resolve before starting]

## Draft PR Body
```markdown
Fixes #[issue-number]

**Layer 1 Constraints:**
- [List key constraints]

**Implementation:**
- [ ] [Step 1]
- [ ] [Step 2]
...

**Validation:**
- [ ] Lint passes: `[command]`
- [ ] Tests pass: `[command]`
- [ ] Smoke tests pass (if applicable): `[command]`

**Testing:**
[Description of test strategy]
```
```

### 7. Get user approval
After presenting the plan, ask:
- Does this plan look correct?
- Any missing steps or concerns?
- Ready to proceed with implementation?

**Do NOT start implementing until user approves the plan.**

## Important Notes
- Planning only - no code changes yet
- Be specific about exit criteria (measurable, verifiable)
- Prefer narrow test scope first, then broaden
- Call out any unknowns or decision points upfront
- The plan should be reviewable and adjustable before coding starts
