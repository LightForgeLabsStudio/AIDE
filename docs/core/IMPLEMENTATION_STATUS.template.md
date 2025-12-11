# Implementation Status

**Last Updated:** {{YYYY-MM-DD}}

This document tracks what's been implemented, what's in progress, and what's planned next. It helps agents understand the current state and design coherent next steps.

---

## Completed Systems

### ✅ {{Feature Name}} ({{Version}} - {{PR/Branch}})

**{{Component Category}}:**
- {{Specific implementation detail 1}}
- {{Specific implementation detail 2}}
- {{Specific implementation detail 3}}

**Tests:**
- {{Test coverage summary}}

**Key Files:**
- `{{path/to/file1}}` - {{Brief description}}
- `{{path/to/file2}}` - {{Brief description}}

---

## In Progress

- {{Feature currently being implemented}}

---

## Planned Next Steps

Priority order based on {{design pillar/roadmap}} dependencies and coherent feature progression.

### 🔷 High Priority: {{Feature Name}} ({{Design Pillar/Epic}})

**Why:** {{Strategic rationale}}

**Dependencies:**
- ✅ {{Completed dependency}}
- ⚠️ {{Missing dependency}}

**Blocks:**
- {{What this unblocks}}

**Scope:**
- {{Implementation detail 1}}
- {{Implementation detail 2}}

**References:**
- `{{path/to/design/doc}}` - {{Design doc name}}
- `{{path/to/related/code}}` - {{Current implementation}}

---

### 🔶 Medium Priority: {{Feature Name}}

(Same structure as above)

---

### 🔶 Low Priority: {{Feature Name}}

(Same structure as above)

---

## Architecture Patterns Established

These patterns should be followed in new implementations:

### {{Pattern Name}}

- **{{Principle}}:** {{Description}}
- **Example:** {{Code example or file reference}}

---

## Open Questions / Technical Debt

Track known issues or decisions that need revisiting:

### High-Priority Technical Debt

- {{Item with file:line reference}}

### Lower-Priority Technical Debt

- {{Item with rationale for deferral}}

---

## How to Update This Document

**When merging a PR:**
1. Move completed items from "Planned" to "Completed"
2. Update "Last Updated" date
3. Add new patterns/conventions discovered during implementation
4. Revise "Planned" section based on what makes sense next
5. Note any new technical debt or open questions

**When planning a new feature:**
1. Read this doc + relevant design docs
2. Check dependencies (what's ✅ vs ⚠️)
3. Draft spec referencing completed systems
4. Get approval before implementing
