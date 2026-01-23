# Implementation Agent - Step 0: Spec Intake

## Purpose
Get the spec, extract goals/scope/success criteria, and confirm the work is feasible and aligned before planning.

## Prerequisites
- Project authority mapping is loaded (project `AGENT_ORIENTATION.md` or `AGENTS.md`).
- You have the GitHub issue number containing the spec.

## Step Actions

Agent asks:
"Ready to implement. Please provide GitHub issue number containing the spec."

### Reading the Issue

Read issue:
```bash
gh issue view <number>
```

Extract: goal, scope, out-of-scope, success criteria, pillar refs from issue description.

Mark in progress:
```bash
gh issue edit <number> --add-label "status:in-progress"
```

### Spec Quality Check

Before planning, verify spec quality. If issues found, post questions to issue and wait for clarification.

Clarity checklist:
- [ ] Goal is clear and specific (not vague)?
- [ ] Success criteria are measurable (testable)?
- [ ] Scope boundaries defined (in-scope vs out-of-scope)?

Completeness checklist:
- [ ] All required sections present (Goal, Scope, Success Criteria)?
- [ ] Dependencies identified?
- [ ] Test approach mentioned or implied?

Feasibility checklist:
- [ ] Conflicts with existing architecture?
- [ ] Relies on unbuilt dependencies?
- [ ] Reasonable scope for single PR (not too large)?

If any issues found:
- Post specific questions to issue (use format below)
- Mark what's unclear and why it matters
- Suggest alternatives if applicable
- Wait for user clarification before proceeding

Example clarification comment:
```bash
gh issue comment <number> --body "**Spec Quality Check - Clarification needed:**

**Issue:** Success criteria not measurable
- Current: \"Improve performance\"
- Suggest: \"Reduce job assignment time from 50ms to <20ms\"

**Context:** Measurable criteria help verify implementation success and guide testing.

Please update spec with specific metrics or expected behavior."
```

If spec is clear: proceed to alignment check.

### Spec <-> Codebase Alignment

Before planning: do a brief alignment pass:
- Call out spec items that conflict with known architecture/engine constraints
- List assumptions the plan would rely on
- Ask clarifying questions to preserve intent

If clarifications needed:
```bash
gh issue comment <number> --body "**Clarification needed:**

<question>

**Context:** <why this matters>

**Options:** <if applicable>"
```

Wait for user response. User will answer in issue comments or update issue description.

Read updated issue:
```bash
gh issue view <number> --comments
```

Response template:
```
**Spec received (issue #<number>):**
- Goal: [1 sentence]
- Systems: [from scope]
- Success: [criteria]
- Pillar: [refs]

**Proceeding to Step 1 (Survey + Alignment)**
```

## Exit Criteria
- Issue read and distilled (goal/scope/success criteria captured).
- Issue labeled `status:in-progress` (or equivalent for the project).
- Any spec gaps/risks documented as issue comments, and you're waiting if clarification is needed.

