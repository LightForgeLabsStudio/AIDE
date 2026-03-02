# AIDE Skills (Agent-Agnostic)

This directory contains AIDE skills in a **tool-agnostic format** compatible with multiple AI coding assistants.

## Supported Tools

- **Claude Code** (VS Code Extension & CLI)
- **Codex** (VS Code Extension)
- **Cursor** (with AIDE plugin)
- **Windsurf** (with skill support)

## Skill Format

Each skill is a directory with a `SKILL.md` file:

```
skills/
├── implement/
│   └── SKILL.md
├── quality/
│   └── SKILL.md
...
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Brief description of what this skill does
---

# Skill Title

Detailed instructions for the AI agent...
```

The YAML frontmatter is **required**. The markdown content provides instructions.

### YAML Frontmatter Best Practices

**Avoid colons in `description` values.** Some skill loaders (Codex) may mis-parse frontmatter when `description:` contains additional `:`.

❌ Bad:
```yaml
description: Review PRs (no fixes): spec alignment, tests, docs
```

✅ Good:
```yaml
description: Review PRs (no fixes) covering spec alignment, tests, and docs
```

Practical tips:
- Prefer words like `covering`, `including`, `to`, `and` instead of `:`.
- Keep `description` short and plain-text (aim for <120 chars).

## Installation

### Claude Code (VS Code Extension or CLI)

**Option 0: Repo-local install (recommended for teams)**
```bash
# From repo root (Windows PowerShell)
.aide/skills/install-claude.ps1

# Installs skills into: .claude/skills/
# Reload VS Code / restart Claude Code to pick up changes
```

**Option 1: Symlink (recommended - stays in sync)**
```bash
# Windows (PowerShell as Admin)
New-Item -ItemType SymbolicLink -Path "$HOME\.claude\skills\implement" -Target "path\to\.aide\skills\implement"

# Linux/Mac
ln -s /path/to/.aide/skills/implement ~/.claude/skills/implement
```

**Option 2: Copy**
```bash
# Windows
xcopy /E /I .aide\skills\implement %USERPROFILE%\.claude\skills\implement

# Linux/Mac
cp -r .aide/skills/implement ~/.claude/skills/implement
```

**Option 3: Install Script**
```bash
# From repo root
.aide/skills/install-claude.ps1    # Windows (defaults to .claude/skills)
.aide/skills/install-claude.sh     # Linux/Mac
```

To install to a user-level directory instead:
```bash
.aide/skills/install-claude.ps1 -SkillsPath "$HOME\\.claude\\skills"
```

### Codex (VS Code Extension)

Codex can use either packaged `.skill` files or repo-local skills.

**Option 1: Repo-local install (recommended for teams)**
```bash
# From repo root
.aide/skills/install-codex.ps1

# Installs skills into: .codex/skills/
# Reload VS Code / restart Codex to pick up changes
```

**Option 2: Packaged `.skill` import (for distribution)**

```bash
# From repo root
.aide/skills/package-codex.ps1

# Generates .aide/skills/dist/*.skill files
# Import via Codex extension UI: "Import Skill"
```

### Cursor / Windsurf

Check tool documentation for skill installation. Most support the same `SKILL.md` format.

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **implement** | `/implement` | Execute a GitHub issue or spec end-to-end. Inline two-layer plan, code, verify. |
| **design** | `/design` | Design a feature or change into a reviewed ADR. Outputs a decision record ready for /scope. |
| **scope** | `/scope` | Decompose an accepted ADR into GitHub issues using the issue-creator tool. |
| **findings** | `/findings` | Write reviewer findings to a `<slug>.findings.md` file for any scoped review target. |
| **pr-review** | `/pr-review` | Review a PR for spec alignment, architecture, tests, and docs. No code changes. |
| **pr-draft** | `/pr-draft` | Create a draft PR with a validated body template and issue linkage. |
| **pr-ready** | `/pr-ready` | Run validation, post a summary, and flip a PR from draft to ready. |
| **codebase-review** | `/codebase-review` | Holistic read-only codebase health review to find drift, dead code, and test gaps. |
| **doc-review** | `/doc-review` | Review documentation for accuracy, drift, and duplication. No code changes. |
| **quality** | `/quality` | Run project quality gates from project placeholder mappings. |
| **handoff** | `/handoff` | Generate a session handoff note for context resets or multi-day work. |
| **sync** | `/sync` | Sync branch with remote and confirm a clean end-of-session state. |
| **issue** | `/issue` | Create a GitHub issue with AIDE label conventions and GitHub Issue Type. |
| **evolve** | `/evolve` | Turn a repeated failure pattern into a concrete system improvement proposal. |
| **skill-author** | `/skill-author` | Create or update an AIDE skill with valid frontmatter and a concise workflow. |

## Development

### Adding a New Skill

1. Create directory: `.aide/skills/my-skill/`
2. Create `SKILL.md` with YAML frontmatter + instructions
3. Test in your preferred tool
4. Run install/package scripts to distribute
5. Update this README

### Skill Design Principles

From `COMMAND_CATALOG.md`:
- **Reduce "agent parses prose" variability** - Clear, structured instructions
- **Keep default context lean** - Link to docs, don't preload everything
- **Respect project Tier 1 rules** - Use the project's constraints and authoritative docs
- **Be composable** - Small commands that chain together

### Syncing with Codex Skills

The `.aide/tools/codex-skills/` directory is the **old location** for Codex-specific packaging. It will be deprecated in favor of this unified structure.

**Migration plan:**
1. Use `.aide/skills/` as single source of truth
2. Generate Codex packages from `.aide/skills/` via script
3. Remove `.aide/tools/codex-skills/src/` duplicates

## Distribution

### For AIDE Framework Users

Skills are included in the AIDE framework. After cloning:

```bash
git clone https://github.com/YourOrg/AIDE .aide
cd .aide
./skills/install-claude.ps1    # or install-codex.ps1, etc.
```

### For Standalone Use

Individual skills can be shared by copying the skill directory:

```bash
# Share implement skill
cp -r .aide/skills/implement ~/shared-skills/
# Recipient installs to their tool's skills directory
```

### Via GitHub Releases

Packaged skills (`.skill` zips for Codex, etc.) are attached to AIDE releases:

1. Go to [AIDE Releases](https://github.com/YourOrg/AIDE/releases)
2. Download desired `.skill` files
3. Import via tool's UI

## License

Same as AIDE framework (specify license here)
