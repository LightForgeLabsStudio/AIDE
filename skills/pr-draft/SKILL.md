---
name: pr-draft
description: Create a draft PR with a validated body template and issue linkage.
---

# PR Draft

Create a draft PR using a consistent template. Validate body locally before opening.

## Inputs

Base branch (default `main`), head branch (default current), PR title, issue number, summary bullets (between 1 and 4), implementation checklist items, validation checklist items.

## Workflow

1. **Confirm branch state** — Verify not on `main`. Verify at least one commit exists. Push if needed:
   ```
   git push -u origin <branch>
   ```

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

4. **Create draft PR** — Run:
   ```
   gh pr create --draft --base <base> --head <head> --title "<title>" --body-file <tmpfile>
   ```

5. **Verify & cleanup** — Run `gh pr view --json number,url,body`. Confirm formatting persisted. Delete the temporary body file.

## Output

PR URL, linked issue number, validation result.
