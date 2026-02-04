---
name: skill-author
description: Create or update AIDE skills in .aide/skills with valid YAML frontmatter and consistent install workflow.
---

# Skill Author

Create a new skill (or refine an existing one) in the unified AIDE skills system.

## Inputs (ask first)

- Are we **creating** a new skill or **updating** an existing one
- Desired command name (hyphenated, e.g. `skill-author`)
- 1–2 sentence goal for the skill (what user wants done)
- Trigger guidance (what should cause this skill to be chosen)
- Target tools to verify (Codex, Claude, both)

## Output contract (what to produce)

- A folder: `.aide/skills/<skill-name>/`
- A `SKILL.md` with:
  - YAML frontmatter: `name`, `description`
  - A concise, step-by-step workflow in the body
- Update `.aide/skills/README.md` to list the skill

## Workflow

1) Define scope
   - What this skill does (and what it explicitly does not do)
   - Any repo-specific invariants it must respect (link, don’t duplicate)

2) Choose metadata (frontmatter)
   - `name`: hyphenated command name
   - `description`: short, plain text, avoid extra `:` characters

3) Draft the SKILL.md body (progressive disclosure)
   - **Inputs** section (what to ask the user for)
   - **Steps** section (numbered, deterministic, minimal ambiguity)
   - **References/resources** section (only link what’s necessary)

4) Add bundled resources only if they pay for themselves
   - `scripts/` when deterministic execution is needed or repeated work appears
   - `references/` for long docs that should be loaded on-demand
   - Avoid extra docs like `README.md` inside the skill folder

5) Install and sanity check
   - Codex repo-local install: run `.aide/skills/install-codex.ps1`
   - Claude install: run `.aide/skills/install-claude.ps1` (override `-SkillsPath` if your setup is user-level)
   - Reload tool UI and confirm the new `/skill-name` appears

## Authoring checklist

- `SKILL.md` frontmatter is valid YAML
- `description` is short and avoids extra `:` characters
- Skill instructions are actionable (no “hand-wavy” steps)
- References are links, not pasted walls of text
