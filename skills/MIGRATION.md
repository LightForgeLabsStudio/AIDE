# Migration: Unified AIDE Skills

This repo uses `.aide/skills/` as the single source of truth for skills across tools.

Legacy Codex-only skills and routing workflows have been removed to avoid backward-compatibility confusion.

## Current Layout

```
.aide/skills/
├── implement/
├── pr-review/
├── design/
├── codebase-review/
├── doc-review/
├── quality/
├── handoff/
├── plan/
├── issue/
├── pr-ready/
├── evolve/
├── sync/
└── dist/              # Generated packages (gitignored)
```

## Validation

- Install repo-local skills for Codex: `powershell -ExecutionPolicy Bypass -File .aide/skills/install-codex.ps1`
- Package `.skill` files: `powershell -ExecutionPolicy Bypass -File .aide/skills/package-codex.ps1`
