# aide-sync

`scripts/sync.ps1` runs the end-of-session "land the plane" git sequence from the repo root:

- Finds repo root by walking up to `AGENTS.md`
- Refuses to run on `main` unless `-AllowMain` is provided
- Requires a clean working tree (`git status --porcelain` empty)
- Requires an upstream (`@{u}`) so `git push` is unambiguous
- Runs: `git pull --rebase`, then `git push`, then prints `git status -sb`

Options:
- `-DryRun`: print the steps without executing them
- `-AllowMain`: allow running on `main` (default is refuse)

