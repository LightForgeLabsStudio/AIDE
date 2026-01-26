# Codex skills (AIDE)

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

## Build packages locally

From the AIDE repo root:

```powershell
powershell -ExecutionPolicy Bypass -File tools/codex-skills/scripts/package_all.ps1
```

