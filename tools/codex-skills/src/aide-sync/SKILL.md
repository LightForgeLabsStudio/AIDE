---
name: aide-sync
description: Sync branch with remote and verify a clean end-of-session state. Use when the user types /sync or asks to "land the plane". Runs git pull --rebase, git push, and verifies status is clean and up to date. Refuses to run on main unless -AllowMain is provided.
---

# AIDE Sync

## Overview

Standardize the end-of-session workflow: update, push, and confirm nothing is left unpushed.

## Workflow

### Inputs
- Optional `-DryRun` to print actions only.
- Optional `-AllowMain` to permit syncing on `main`.

### Actions
1) Confirm current branch is not `main`.
2) Confirm working tree is clean (or warn and stop).
3) Run `git pull --rebase`.
4) Run `git push`.
5) Run `git status -sb` and confirm branch is up to date.

### Output
- A short summary including the final `git status -sb`.

## Notes
- If `git pull --rebase` fails, stop and request help (do not force).

