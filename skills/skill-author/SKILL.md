---
name: skill-author
description: Create or update an AIDE skill in .aide/skills with valid frontmatter and a concise workflow.
---

# Skill Author

Create a new skill or refine an existing one. Skills are task starters, not role primers.

## Inputs

- Are you creating a new skill or updating an existing skill? Please specify which skill and what changes are needed.
- Command name (hyphenated, e.g. `skill-author`)
- 1-2 sentence goal (what the user wants done)
- What triggers this skill (when should it be chosen over others?)

## Workflow

1. **Define scope** — What this skill does and what it explicitly does not do. Link to AGENTS.md for project facts; do not duplicate them.

2. **Choose metadata** — `name`: hyphenated. `description`: short plain text, no extra `:` characters.

3. **Write SKILL.md** to `.aide/skills/<skill-name>/SKILL.md` using this sequence:
   1. Add YAML frontmatter with `name` and `description` only.
   2. Define the task clearly and avoid role framing or primer-style sections.
   3. Add an **Inputs** section describing the required inputs.
   4. Add a **Workflow** section with numbered, deterministic steps.
   5. Add a **Reference** section only when linking to a real file that must exist.
   6. Keep the file within 30-50 lines total.

4. **Add bundled resources only if they pay for themselves** — `scripts/` for deterministic execution, no extra READMEs inside the skill folder.

5. **Install** — Run `.aide/skills/install-claude.ps1`. Reload tool UI and confirm `/skill-name` appears.

## Authoring checklist

- Frontmatter is valid YAML
- `description` has no extra `:` characters
- Steps are actionable (no hand-wavy language)
- No references to deleted primer files
- File is 30-50 lines
