# GitHub Labels (Project-Defined)

This AIDE framework doc is intentionally **generic**.

Projects should maintain their **canonical label list** in the project repo (for example: `.github/LABELS.md`) and keep it aligned with AIDE expectations.

## Minimum Conventions

- **Issue Type**: use **GitHub Issue Types** (avoid type labels like `bug`, `enhancement`, etc.).
- **Status labels**: use `status:*` to represent workflow state (e.g., `status:ready`, `status:in-progress`, `status:needs-review`).
- **Area labels**: use `area:*` to represent system/component ownership (at least one per issue).
- **Priority labels**: use `priority:*` to represent urgency/impact.

## How to discover actual labels

- Project doc: `.github/LABELS.md` (if present)
- GitHub CLI: `gh label list`

## References

- Placeholder contract: `PLACEHOLDER_CONTRACTS.md` (required label conventions)
- Query patterns: `GITHUB_QUERIES.md`
