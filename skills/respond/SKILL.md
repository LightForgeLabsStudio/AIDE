---
name: respond
description: Apply findings from a /findings review to a spec or ADR and write a response file
---

# Respond

Handle the designer's side of the spec/ADR review loop. Read findings, triage them, apply agreed changes, and write a response record.

Pairs with `/findings` (reviewer writes findings) and `/design` (designer writes the spec/ADR).

## Inputs

- Path to the spec or ADR under review, or enough context to locate it
- The findings file must already exist alongside it as `<slug>.findings.md`

## Workflow

1. **Locate files** — Find the artifact in `docs/specs/`, `docs/decisions/`, or `.aide/docs/`. Look for the sibling `<slug>.findings.md`. If not found, stop and tell the user.

2. **Read both files** — Read the artifact and the findings file in full.

3. **Triage findings** — For each finding, decide:
   - **Apply** — finding is correct, change the artifact
   - **Reject** — finding is incorrect or out of scope; record reasoning
   - **Defer** — valid but out of scope for this artifact; note where it should land

4. **Apply changes** — Edit the artifact for all accepted findings. Do not change its status — the reviewer (`/findings`) owns that.

5. **Write response file** — Write `<slug>.response.md` alongside the artifact with this structure:
   ```
   # Review Response: <Title>
   ## Applied
   ## Rejected
   ## Deferred
   ```
   Each entry cites the finding and gives a one-line reason.

6. **Confirm** — Report a summary of applied / rejected / deferred counts to the user.

## Reference

- Artifact locations: `docs/specs/` (living specs), `docs/decisions/` (project ADRs), `.aide/docs/decisions/` (AIDE ADRs)
- Findings file written by: `/findings`
