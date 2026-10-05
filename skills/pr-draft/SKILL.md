---
name: pr-draft
description: Create or update a draft PR with a validated body and issue linkage when applicable.
---

# PR Draft

Create or update a draft PR using a consistent template. Validate its body locally before publishing.

## Inputs

Read the consuming project's root AGENTS.md and any workflow document it names. Resolve the base branch from explicit input or `MAIN_BRANCH` (default `main`). Inputs also include head branch (default current), PR title, requirements or linked issue, summary bullets (between 1 and 4), implementation checklist items, and validation checklist items.

## Workflow

1. **Confirm branch state** — Verify the head differs from the resolved base branch and has commits beyond it. Use an existing PR's head when updating it. Push if needed:
   ```
   git push -u origin <branch>
   ```

   Look for an existing PR for this head and base with `gh pr list --head <head> --base <base> --state open --json number,url,isDraft`. Update that PR rather than creating a duplicate. Do not silently convert a ready PR back to draft.

2. **Build PR body** — Write a temporary markdown file:
   ```markdown
   Fixes #<number>

   ## Summary
   - <bullet>

   ## Implementation Plan
   - [ ] <step>

   ## Validation
   - [ ] <criterion>
   ```

   Include `Fixes #<number>` only when a linked issue should close on merge. For pasted requirements without an issue, omit that line and capture the requirements in the summary and checklists; do not invent an issue.

3. **Validate body** — Locate the validator from the repository root before running it. Check both the repository-level path and the AIDE-submodule path; this repository may keep it under `.aide/tools/`:
   ```
   $validator = @("tools/validate_pr_body.ps1", ".aide/tools/validate_pr_body.ps1") |
       Where-Object { Test-Path -LiteralPath $_ } |
       Select-Object -First 1
   if (-not $validator) {
       throw "Validator not found; search hidden files and inspect submodules before proceeding."
   }
   powershell -ExecutionPolicy Bypass -File $validator -Body (Get-Content -Raw <tmpfile>)
   ```
   If neither path exists, search the repository including hidden files and inspect submodules before calling the validator unavailable. Do not replace the validator with manual checks. Fix and re-run until green; if validation fails, provide the specific errors and suggest corrections.

4. **Publish** — For a new PR, run:
   ```
   gh pr create --draft --base <base> --head <head> --title "<title>" --body-file <tmpfile>
   ```

   For an existing PR, run `gh pr edit <pr> --title "<title>" --body-file <tmpfile>` instead.

5. **Verify & cleanup** — Run `gh pr view --json number,url,body`. Confirm formatting persisted. Delete the temporary body file.

## Output

PR URL, current draft/ready state, linked issue number if applicable, validation result.
