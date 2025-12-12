# Agent Token Economy Best Practices

**Purpose:** Optimize agent primer files to maximize context budget for code analysis and implementation.

Token efficiency directly impacts agent capability. A 500-token primer leaves 95% of context for actual work vs a 10,000-token primer that consumes context before coding begins.

## Core Principles

### 1. Concise Directives Over Verbose Explanations

**Bad (verbose):**
```markdown
When you are implementing a new feature, it is very important that you take the time to carefully read through all of the existing documentation so that you can understand the current state of the codebase and ensure that your implementation aligns with the established patterns and architectural decisions that have been made by the team.
```

**Good (concise):**
```markdown
- Read `IMPLEMENTATION_STATUS.md` before coding
- Extend existing patterns (don't rewrite)
- Follow architectural constraints in `DEVELOPMENT.md`
```

**Token savings:** ~70% reduction (95 tokens → 28 tokens)

### 2. Bullet Points and Checklists Over Paragraphs

**Bad (paragraph form):**
```markdown
The first step in the implementation workflow is to conduct a thorough codebase survey. During this phase, you should inspect the current branch, examine relevant modules and components, review the architecture, and identify any mismatches between the design documentation and the actual code. It is critical that you do not write any code during this phase.
```

**Good (checklist):**
```markdown
**Step 1: Codebase Survey** (NO CODING YET)
- Inspect current branch
- Review relevant modules/components
- Identify design/code mismatches
```

**Token savings:** ~65% reduction (68 tokens → 24 tokens)

### 3. Reference Instead of Duplicate

**Bad (duplicates content):**
```markdown
## Testing Requirements

All features must include:
- Unit tests for pure logic
- Integration tests for workflows
- Manual checklists only if automation is impractical
- Tests must pass before PR approval
- Use GUT framework for Godot projects
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Test edge cases and error paths
```

**Good (references authoritative source):**
```markdown
## Testing Requirements

Follow `TESTING_POLICY.md` for coverage expectations, frameworks, and commands.

**Quick reference:**
- Derive test intent from spec success criteria
- Automated tests preferred (GUT unit → integration)
- Manual checklist only if automation impractical (state why in PR)
```

**Token savings:** ~55% reduction (72 tokens → 33 tokens)

### 4. Front-Load Critical Information

**Bad (buries critical info):**
```markdown
## Implementation Process

When implementing features, there are several important steps to follow. First, you should familiarize yourself with the codebase and understand the current architecture. Then, you should create an implementation plan and get approval before proceeding. **CRITICAL: Never work directly on the main branch.** After approval, you can begin coding...
```

**Good (critical info first):**
```markdown
## Implementation Process

**CRITICAL: Never work directly on `main`. Create feature branch first.**

1. Codebase survey (no coding)
2. Implementation plan (get approval)
3. Branch + draft PR setup
4. Git-first development
```

**Token savings:** ~60% reduction + improved compliance

### 5. Use Quick Reference Documents When Available

**Instead of:**
```markdown
Reading 7 full design pillar documents (10,000+ tokens)
```

**Use:**
```markdown
Read `DESIGN_QUICK_REFERENCE.md` (500 tokens) for overview
→ Reference specific pillar sections when implementing
```

**Token savings:** 95%+ on initial context load

### 6. One Clear Example Over Multiple Similar Ones

**Bad (redundant examples):**
```markdown
## Commit Message Format

Example 1:
git commit -m "Add user authentication\n\nImplemented JWT-based auth.\n\nCo-Authored-By: Claude <claude@example.com>"

Example 2:
git commit -m "Fix navigation bug\n\nResolved race condition.\n\nCo-Authored-By: Claude <claude@example.com>"

Example 3:
git commit -m "Update documentation\n\nAdded API reference.\n\nCo-Authored-By: Claude <claude@example.com>"
```

**Good (single comprehensive example):**
```markdown
## Commit Message Format

```bash
git commit -m "Brief imperative summary

Optional detailed explanation.

Co-Authored-By: [Agent Name] <agent@example.com>"
```
```

**Token savings:** ~75% reduction (142 tokens → 36 tokens)

## Practical Application

### Example Agent Primer Refactor

**Before (verbose):**
```markdown
# Feature Implementation Agent

Welcome to the feature implementation workflow. This document will guide you through the process of implementing new features for the project. It is important that you follow these steps carefully to ensure that your implementation is consistent with the project's architecture and coding standards.

The first thing you need to do is understand the current state of the codebase. You should read through the implementation status document, which provides a comprehensive overview of what has been built so far, what is currently in progress, and what is planned for the future. This will help you understand where your feature fits into the overall project.

Next, you should familiarize yourself with the design documentation. The design pillars describe the core systems and gameplay mechanics that define the project. Your feature should align with these pillars and enhance the player experience as described in the design documentation.

Before you write any code, you need to create an implementation plan...
```
**Token count:** ~175 tokens

**After (concise):**
```markdown
# Feature Implementation Agent

Implement features for {{PROJECT_NAME}} using {{TECH_STACK}}.

## Before Coding

1. Read `IMPLEMENTATION_STATUS.md` - current state, dependencies
2. Read relevant `design/` pillar sections - authoritative requirements
3. Review `DEVELOPMENT.md` - architecture patterns

## Workflow

1. **Codebase Survey** - Identify patterns, design mismatches (NO CODING)
2. **Implementation Plan** - Extend patterns, get approval (WAIT)
3. **Branch + Draft PR** - Never on `main`, create `feature/<name>`
4. **Git-First Dev** - Clean commits, tests pass
5. **Sanity Check** - Edge cases, user workflow
6. **PR Ready** - Scope complete, tests pass, docs updated
7. **Report Back** - Summarize changes, limitations
```
**Token count:** ~52 tokens

**Token savings:** 70% reduction (123 tokens saved)

## Agent File Optimization Checklist

When creating or updating agent primer files:

- [ ] Remove unnecessary introductory paragraphs
- [ ] Convert prose to bullet points/checklists
- [ ] Replace duplicated content with references to authoritative docs
- [ ] Move critical constraints to top of file
- [ ] Use quick reference documents for broad overviews
- [ ] Limit examples to one clear, comprehensive instance per concept
- [ ] Remove filler words ("very", "carefully", "thoroughly", etc.)
- [ ] Use numbered lists for sequential workflows
- [ ] Combine related items into single bullets
- [ ] Replace "must", "should", "need to" with imperative verbs

## Measuring Token Efficiency

**Target token budgets by agent type:**
- **Implementation agents:** 300-500 tokens (complex workflows)
- **Review agents:** 200-400 tokens (structured evaluation)
- **Design agents:** 150-300 tokens (prioritization + handoff)
- **Specialized agents:** 100-200 tokens (narrow scope)

**How to measure:**
Use token counting tools (e.g., `tiktoken` for GPT models) on agent primer markdown files.

**Red flags:**
- Agent primer >1000 tokens → likely contains duplicated content
- Multiple paragraphs of prose → convert to bullets
- Repeated phrases across sections → consolidate

## Maintenance

**When updating agent primers:**
1. Review token count before and after changes
2. Ensure no content duplication with authoritative docs
3. Verify critical constraints remain front-loaded
4. Test agent behavior with updated primer (does it still work?)
5. Update `DOCUMENTATION_POLICY.md` if new patterns emerge

**Synchronization requirements:**
- When authoritative docs change, update references (not duplicated content)
- When workflow changes, update checklist steps (keep concise)
- When new constraints added, front-load them (remove less critical items if needed)

## Trade-offs and Exceptions

**When verbosity is acceptable:**
- **Safety-critical constraints** (e.g., "Never modify tests without approval") → repeat in multiple sections if needed
- **Complex examples** requiring context (limit to 1-2 per primer)
- **Project-specific gotchas** not documented elsewhere

**When to add content despite token cost:**
- New agent types with novel workflows (document once, reuse pattern)
- Critical failures traced to missing primer guidance
- User-requested clarifications that prevent repeated questions

Token efficiency is a means to an end: maximizing agent capability. Optimize ruthlessly, but prioritize clarity and correctness over extreme compression.
