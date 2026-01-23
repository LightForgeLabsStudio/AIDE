# Implementation Agent - Step 10: Sync Local Main

## Purpose
Ensure your local `{{MAIN_BRANCH}}` matches remote after merge.

## Prerequisites
- Step 9 complete (PR merged).

## Step Actions

After merge, sync local `{{MAIN_BRANCH}}` to match the remote:
```bash
git checkout {{MAIN_BRANCH}}
git pull --rebase
```

## Exit Criteria
- Local `{{MAIN_BRANCH}}` is up to date with remote.

