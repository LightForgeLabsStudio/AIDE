---
name: pr-draft
description: Create a draft PR with a validated body template and issue linkage for AIDE repos.
---

# PR Draft

Create a draft PR using a consistent template and validate body formatting locally before opening.

## Inputs (ask first)

- Base branch (default `main`)
- Head branch (current branch if omitted)
- PR title
- Issue number to link (`Fixes #<number>`)
- Summary bullets (1-4)
- Plan checklist items
- Validation checklist items
- Keep as draft or mark ready (default draft)

## Workflow

1) Confirm branch state
   - Verify not on `main`.
   - Verify there is at least one commit on the branch.
   - Push branch if needed: `git push -u origin <branch>`.

2) Build PR body from template
   - Write a temporary markdown file with:
   - `Fixes #<number>`
   - `## Summary`
   - `## Implementation Plan` with `- [ ]` checklist
   - `## Validation` with `- [ ]` checklist
   - Optional `## Notes`

3) Validate PR body locally before creating PR
   - Run: `powershell -ExecutionPolicy Bypass -File tools/validate_pr_body.ps1 -Body (Get-Content -Raw <tmpfile>)`
   - If validation fails, fix template/body and re-run until green.

4) Create draft PR using body file
   - Run: `gh pr create --draft --base <base> --head <head> --title "<title>" --body-file <tmpfile>`
   - Do not use inline escaped `--body` strings.

5) Post-create verification
   - Run: `gh pr view --json number,url,body`
   - Re-run local validator against returned `body` text to confirm persisted formatting.

6) Cleanup
   - Delete the temporary body file.

## Output

- PR URL
- Linked issue number
- Validation result (pass/fail)

## Notes

- Prefer this skill from `/implement` Step 2 for all draft PR creation.
- Keep body path references inside backticks to satisfy PR body check.
