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
├── prime/
│   ├── SKILL.md          # Skill definition (YAML + markdown)
│   └── scripts/          # Optional: tool-specific automation
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

## Installation

### Claude Code (VS Code Extension or CLI)

**Option 1: Symlink (recommended - stays in sync)**
```bash
# Windows (PowerShell as Admin)
New-Item -ItemType SymbolicLink -Path "$HOME\.claude\skills\prime" -Target "path\to\.aide\skills\prime"

# Linux/Mac
ln -s /path/to/.aide/skills/prime ~/.claude/skills/prime
```

**Option 2: Copy**
```bash
# Windows
xcopy /E /I .aide\skills\prime %USERPROFILE%\.claude\skills\prime

# Linux/Mac
cp -r .aide/skills/prime ~/.claude/skills/prime
```

**Option 3: Install Script**
```bash
# From repo root
.aide/skills/install-claude.ps1    # Windows
.aide/skills/install-claude.sh     # Linux/Mac
```

### Codex (VS Code Extension)

Codex requires packaged `.skill` files (zip archives). Use the packaging script:

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
| **prime** | `/prime` | Load AGENT_ORIENTATION.md and AGENTS.md, extract constraints |
| **quality** | `/quality` | Run lint and tests from AGENTS.md placeholders |
| **handoff** | `/handoff` | Generate session handoff note for context resets |
| **plan** | `/plan` | Create two-layer implementation plan + PR draft |
| **evolve** | `/evolve` | Turn repeated failures into rules/automation |
| **role** | `/role` | Route to correct AIDE workflow primer |
| **sync** | `/sync` | End-of-session git sync (pull, push, verify) |
| **issue** | `/issue` | Create labeled GitHub issue |
| **pr-ready** | `/pr-ready` | Validate and mark PR ready |

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
- **Respect project Tier 1 rules** - Always read AGENTS.md
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
# Share prime skill
cp -r .aide/skills/prime ~/shared-skills/
# Recipient installs to their tool's skills directory
```

### Via GitHub Releases

Packaged skills (`.skill` zips for Codex, etc.) are attached to AIDE releases:

1. Go to [AIDE Releases](https://github.com/YourOrg/AIDE/releases)
2. Download desired `.skill` files
3. Import via tool's UI

## License

Same as AIDE framework (specify license here)