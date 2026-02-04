# Codex skills (AIDE)

> **⚠️ DEPRECATED:** This directory is being phased out in favor of the unified skills system at `../../skills/`.
>
> **New location:** [../../skills/README.md](../../skills/README.md)
>
> This directory remains for backward compatibility but will be removed in a future release.

This folder contains the source for AIDE's `aide-*` Codex skills.

## Folder layout

- `src/` - skill sources (reviewable diffs)
- `dist/` - generated `.skill` packages (ignored; produced by scripts/CI)
- `scripts/` - packaging utilities

## Install

Preferred distribution is via GitHub Releases for the AIDE repo:

1. Download the desired `.skill` from the latest AIDE release assets.
2. Import it via your Codex extension UI (e.g. "Import Skill").
3. Reload VS Code / restart the extension.

## Script execution model

Skills include optional `scripts/` for deterministic execution in environments that allow running them. If scripts cannot be executed, the `SKILL.md` instructions remain the source of truth for manual or model-driven execution.

## Note on entry commands

Older versions used routing commands like `/prime` and `/role`. The unified skills system prefers role entrypoints (e.g. `/implement`, `/pr-review`, `/design`) under `.aide/skills/`.

## Build packages locally

**Recommended (new unified system):**

```powershell
powershell -ExecutionPolicy Bypass -File skills/package-codex.ps1
```

**Legacy (this directory):**

```powershell
powershell -ExecutionPolicy Bypass -File tools/codex-skills/scripts/package_all.ps1
```

