# Migration: Codex Skills → Unified AIDE Skills

## Old Structure (Deprecated)

```
.aide/tools/codex-skills/
├── src/
│   ├── aide-prime/
│   │   ├── SKILL.md
│   │   ├── scripts/prime.ps1
│   │   └── references/README.md
│   ├── aide-quality/
│   └── ...
├── dist/               # Generated .skill packages
├── scripts/
│   └── package_all.ps1
└── README.md
```

**Issues:**
- Codex-specific (not usable with Claude Code, Cursor, etc.)
- Separate from unified AIDE skills location
- Duplication with Claude Code skills
- Packaging script tightly coupled to Codex

## New Structure (Unified)

```
.aide/skills/
├── prime/
│   ├── SKILL.md        # Agent-agnostic skill definition
│   └── scripts/        # Optional: tool-specific helpers
├── quality/
│   └── SKILL.md
├── handoff/
│   └── SKILL.md
├── plan/
│   └── SKILL.md
├── evolve/
│   └── SKILL.md
├── dist/               # Generated packages (gitignored)
├── install-claude.ps1  # Install for Claude Code
├── package-codex.ps1   # Package for Codex
└── README.md           # Installation docs
```

**Benefits:**
- **Single source of truth** - One skill definition works across tools
- **Easy distribution** - Scripts handle tool-specific formatting
- **Maintainable** - Update once, distribute to all tools
- **Version controlled** - Skills in repo, not user config

## Migration Steps

### Step 1: Copy Skills to New Location

```bash
# Already done - skills copied from ~/.claude/skills/ to .aide/skills/
```

### Step 2: Verify Skills Work

```bash
# Test Claude Code installation
.aide/skills/install-claude.ps1

# Test Codex packaging
.aide/skills/package-codex.ps1
```

### Step 3: Update CI Workflow

Replace `.github/workflows/codex-skills.yml` reference:

**Old:**
```yaml
run: ./tools/codex-skills/scripts/package_all.ps1
path: tools/codex-skills/dist/*.skill
```

**New:**
```yaml
run: ./.aide/skills/package-codex.ps1
path: .aide/skills/dist/*.skill
```

### Step 4: Deprecate Old Location

Add deprecation notice to `tools/codex-skills/README.md`:

```markdown
# DEPRECATED

This directory is deprecated. Skills have moved to `.aide/skills/`.

See: [.aide/skills/README.md](../../.aide/skills/README.md)
```

### Step 5: Update Documentation

- Update COMMAND_CATALOG.md to reference `.aide/skills/`
- Update AGENT_ORIENTATION.md with new skill installation instructions
- Update project README with skill links

## Compatibility

### Codex Users

**Before:**
- Download `.skill` from GitHub Releases
- Import via Codex UI

**After:**
- Same process! `.skill` files generated from unified source
- OR: Clone repo and run `.aide/skills/install-codex.ps1` (future enhancement)

### Claude Code Users

**Before:**
- No official skills (manual copy or custom)

**After:**
- Run `.aide/skills/install-claude.ps1`
- Skills install to `~/.claude/skills/`
- Auto-discovered by extension

### Other Tools (Cursor, Windsurf)

**Before:**
- Not supported

**After:**
- Check tool docs for skill installation
- Most support `SKILL.md` format
- May need tool-specific install script

## Rollout Plan

### Phase 1: Parallel Support (Current)
- Keep both `.aide/tools/codex-skills/` and `.aide/skills/`
- Generate Codex packages from new location
- Test with multiple tools

### Phase 2: Deprecation Notice
- Add warnings to old location
- Update all docs to reference new location
- Keep old location functional

### Phase 3: Full Migration
- Remove `.aide/tools/codex-skills/src/` (keep only as archive)
- All packaging from `.aide/skills/`
- Single source of truth established

## Tool-Specific Notes

### Scripts Directory

Some skills have a `scripts/` subdirectory with PowerShell files:
- **Codex:** May execute these scripts (needs verification)
- **Claude Code:** Ignores scripts, uses only SKILL.md instructions
- **Decision:** Keep scripts for backward compatibility, mark as optional

### YAML Frontmatter

All tools support the format:
```markdown
---
name: skill-name
description: Brief description
---
```

This is the common denominator and should be mandatory.

### References Directory

Old Codex skills had `references/README.md`:
- Not used by Claude Code
- Can be removed or moved to comments in SKILL.md

## Testing Checklist

- [ ] Claude Code: Install script works, skills appear in `/` menu
- [ ] Codex: Package script works, `.skill` imports successfully
- [ ] CI: Workflow packages and uploads to releases
- [ ] Docs: README.md has clear install instructions for each tool
- [ ] Migration: Old location marked deprecated
- [ ] Skills work identically across tools
