# Issue Spec Writing Guide

**This document is normative.** When writing issue specs (manually or via LLM), follow these patterns for compatibility with the `issue-creator` tool and GitHub workflow.

## Table of Contents

- [Core Principles](#core-principles)
- [Epic Structure](#epic-structure)
- [Issue Structure](#issue-structure)
- [Issue Types](#issue-types)
- [Metadata Fields](#metadata-fields)
- [Dependencies](#dependencies)
- [Success Criteria Requirements](#success-criteria-requirements)
- [Sanity Checks](#sanity-checks)
- [Examples](#examples)

---

## Core Principles

### 1. Issues Are Descriptive, PRs Are Executable

- **Issues** = Intent, scope, and acceptance criteria
- **PRs** = Task checklists, implementation progress, code changes

**Never put checklists (`- [ ]`) in issue specs.** Use plain bullets (`-`).

### 2. Epic vs Issue Have Different Requirements

Epics provide context and group related work. Issues define specific, implementable units of work.

### 3. Fidelity Over Enhancement

When converting designs to specs, preserve all sections and narrative unless explicitly instructed otherwise. Default to structural transformation only—do not add, remove, or reinterpret concepts.

### 4. Example-Spec is Normative

The [example-spec.md](../tools/issue-creator/example-spec.md) file shows canonical patterns. When in doubt, match its structure.

### 5. `---` Separates Specs

Use `---` only between specs (Epic -> Issue -> Issue...). Do not use `---` inside an Epic or Issue section; use headings (`### ...`) for intra-section structure.

---

## Epic Structure

Epics group related issues and provide strategic context.

### Required Sections

- **Goals** - High-level objectives and intent
- **Success Criteria** - How we know the Epic is complete (often: "All child issues completed")

### Recommended Sections

- **Pillar References** - Which design pillars this Epic supports (if applicable)
- **Background/Context** - Problem statement, motivation, or system overview (especially for complex systems)

### Optional Sections

- **Non-Goals** - Explicit scope boundaries
- **Notes** - Implementation considerations

### Example

```markdown
## [Epic]: Job System Overhaul

Complete overhaul of the job assignment and priority system to enable more flexible drone behavior and better player control.

### Goals
- Flexible priority system for jobs
- Better drone assignment logic
- Cancellation support for in-progress jobs
- UI indicators for job status

### Success Criteria
- All child issues completed
- Performance maintained (no regression in job assignment speed)
- Backward compatible with existing save files

### Pillar References
- Pillar 2: Sector Logistics (job management is core to logistics)
```

---

## Issue Structure

Issues define specific, implementable work units.

### Required Sections

- **Goals** - What this issue aims to achieve
- **Scope** - Specific implementation details (files, methods, systems touched)
- **Success Criteria** - Testable/measurable outcomes

### Optional Sections

- **Non-Goals** - What this issue explicitly does NOT include
- **Background** - Context or rationale (if not obvious from Epic)
- **Dependencies** - Can also be expressed via `blocked_by:` metadata

### Example

```markdown
## [Feature]: Job Priority System
priority: high
area: job-system

### Goals
- Drones prioritize high-priority jobs over low-priority ones
- Buildings can mark jobs as urgent
- Priority visible in UI

### Scope
- Add `priority` enum field to Job struct (LOW, NORMAL, HIGH, URGENT)
- Update `Drone._select_next_job()` to sort by priority
- Add priority icons to job queue UI
- Update JobSystem.post_job() to accept priority parameter

### Non-Goals
- No changes to pathfinding logic
- No changes to resource requirements

### Success Criteria
- Drones claim highest priority job first when multiple available
- Priority UI indicators show correct priority level
- Tests verify priority sorting logic
- Manual test: High priority job claimed before low priority job
```

---

## Issue Types

Issue type is declared in the **heading tag**.

### Required Field

Use a typed heading for each Issue section (not Epics):

```markdown
## [Feature]: Job Priority System
priority: high
area: job-system
```

### Notes

- Use one of: `[Feature]`, `[Bug]`, `[Tech Debt]`, `[Chore]`, `[Documentation]`, `[Research]`, `[Epic]`.
- The tool maps these tags to GitHub Issue Types.
- `type: <value>` metadata is supported as an override, but the preferred format is the typed heading.

---

## Metadata Fields

Add metadata as `key: value` lines at the start of each section (after the heading).

### Available Fields

#### `type: feature|bug|technical-debt|chore|documentation|research`

Optional override for Issue type. Prefer using the typed heading tag.

```markdown
## [Feature]: Drone Pathfinding Optimization
type: feature
```

#### `priority: high|medium|low`

Maps to `priority:high`, `priority:medium`, `priority:low` labels.

**Default:** `medium`

```markdown
## [Bug]: Critical Bug Fix
priority: high
```

#### `area: system-name`

Maps to `area:system-name` labels. Comma-separated for multiple areas.

The tool also auto-infers areas from content keywords (configured in `issue-creator.config.json`).

```markdown
## [Tech Debt]: Drone Pathfinding Optimization
area: drone-ai, performance
```

#### `blocked_by: Issue Title`

Creates GitHub blocking relationship via `addBlockedBy` GraphQL mutation.

**Must match exact GitHub issue title.**

```markdown
## [Feature]: Job Cancellation
blocked_by: Job Priority System
```

This creates a blocking relationship visible in GitHub's "Relationships" dropdown and prevents closing the blocked issue until the blocker is resolved.

#### `blocks: Issue Title`

Reserved for future use (inverse of `blocked_by`).

---

## Dependencies

### When to Use `blocked_by`

Use when one issue **cannot be implemented** without another being completed first.

Examples:
- "Introduce data structure X" blocks "Use data structure X in system Y"
- "Add API endpoint" blocks "Wire endpoint to UI"
- "Implement core logic" blocks "Add tests for core logic"

### Inferring Dependencies

You **MAY** infer `blocked_by` relationships when dependency ordering is **explicitly stated** in the design.

Examples of explicit ordering:
- "After X is complete, implement Y"
- "Once the foundation is in place, add..."
- "This depends on..."

**Do not** invent dependencies based on assumptions. Only derive from explicit statements.

### Multiple Blockers

Use comma-separated values:

```markdown
blocked_by: Foundation Task, Another Prerequisite
```

### Reference Format

The `blocked_by` value must match the **exact title** from the heading:

- Heading: `## [Feature]: Foundation Task` -> Reference: `blocked_by: Foundation Task`
- Heading: `## [Tech Debt]: Foundation Task` -> Reference: `blocked_by: Foundation Task`
- Epic heading: `## [Epic]: My Epic` -> Reference: `blocked_by: [Epic]: My Epic`

### Limitation

The tool only links issues **created in the same batch**. It does not currently support referencing existing issue numbers like `blocked_by: #203`.

---

## Success Criteria Requirements

Every issue must include **testable/measurable** success criteria. This is a hard requirement.

### Acceptable Patterns

#### 1. Reference Automated Tests

```markdown
### Success Criteria
- Tests verify priority sorting logic
- Integration test confirms refund calculations
- Unit tests cover edge cases
```

#### 2. Define Measurable Outcomes

```markdown
### Success Criteria
- 50% reduction in time spent in assign_jobs() for 100+ job queues
- No regressions in assignment correctness (benchmark suite passes)
```

#### 3. Specify Manual Validation

```markdown
### Success Criteria
- Manual test: High priority job claimed before low priority job
- Manual test: Cancel job mid-execution, verify drone picks new job
```

#### 4. Combination (Recommended)

```markdown
### Success Criteria
- Drones claim highest priority job first when multiple available
- Priority UI indicators show correct priority level
- Tests verify priority sorting logic
- Manual test: High priority job claimed before low priority job
```

### Unacceptable (Too Vague)

❌ "Feature works correctly"
❌ "System is more maintainable"
❌ "Code is clean"

---

## Sanity Checks

Use these checks before submitting a spec to the `issue-creator` tool.

### ✅ Keep These Checks

| Check | Reason | Example |
|-------|--------|---------|
| **No checklists (`- [ ]`)** | Tool cannot parse checklists; use plain bullets | ❌ `- [ ] Task` -> ✅ `- Task` |
| **Success criteria are testable** | Prevents unimplementable issues | ✅ "Tests verify X" / "Manual test: Y" |
| **Scope boundaries clear** | Prevents scope bleed | Include "Non-Goals" for complex issues |
| **Dependencies identified** | Enables blocking relationships | Use `blocked_by:` when ordering matters |
| **Required sections present** | Ensures spec completeness | Epic: Goals + Success / Issue: Goals + Scope + Success |

### 🚨 Critical Rules

| Rule | Behavior |
|------|----------|
| **Fidelity-first** | Preserve all sections from input unless explicitly told to prune |
| **No silent edits** | Do not add, remove, or reinterpret concepts—format only |
| **Example-spec is normative** | Match structure from [example-spec.md](../tools/issue-creator/example-spec.md) |
| **Dependency inference allowed** | MAY infer `blocked_by` when ordering is explicit in design |

---

## Examples

### Minimal Issue

```markdown
## [Feature]: Add Health Bar to Unit
priority: medium
area: ui

### Goals
- Display unit health visually

### Scope
- Add ProgressBar to Unit scene
- Update on health change signal

### Success Criteria
- Health bar reflects current health
- Bar color changes at low health
```

### Issue with Blocker

```markdown
## [Feature]: Wire Health Bar to Combat System
priority: medium
area: ui, combat
blocked_by: Add Health Bar to Unit

### Goals
- Health bar updates during combat

### Scope
- Connect CombatSystem damage signals to health bar
- Add tests for signal connections

### Success Criteria
- Health bar updates when unit takes damage
- Tests verify signal connections
```

### Epic with Context

```markdown
## [Epic]: Combat System Overhaul

Introduce real-time combat with formations, targeting priorities, and unit abilities.

### Background
Current combat is placeholder (instant resolution). This Epic introduces the foundation for the combat pillar, enabling tactical depth and player expression.

### Goals
- Real-time combat with unit health/damage
- Formation system for unit positioning
- Targeting priorities (focus fire, spread damage)
- Basic unit abilities (special attacks, defensive stance)

### Success Criteria
- All child issues completed
- Combat is legible in play (clear feedback, no guessing)
- Performance: 100+ units in combat with no stutter

### Pillar References
- Pillar 3: Combat & Defense (this Epic implements the combat pillar)
```

---

## See Also

- [example-spec.md](../tools/issue-creator/example-spec.md) - Canonical example
- [ISSUE_CREATOR_GUIDE.md](ISSUE_CREATOR_GUIDE.md) - Tool usage and technical reference
- [issue-creator.config.json](../../issue-creator.config.json) - Label/area/type configuration
