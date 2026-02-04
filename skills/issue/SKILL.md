---
name: issue
description: Create a GitHub issue following AIDE label conventions. Applies priority/area/status labels and sets GitHub Issue Type (no type labels).
---

# AIDE Issue

## Overview

Create issues consistently with required labels so work is trackable and automation-friendly.

## Spec Writing (recommended structure)

When the issue is a spec (feature/tech debt/chore), prefer a lean, issue-friendly structure:

- **Goals**
- **Scope**
- **Non-Goals**
- **Success Criteria** (testable/measurable)

Rules:
- Do not use checklists (`- [ ]`) in issues; use plain bullets (`-`).
- For batch epics/children, prefer the issue-creator tool spec format.

References:
- `.aide/docs/SPEC_WRITING_GUIDE.md` (normative)
- `.aide/docs/ISSUE_CREATOR_GUIDE.md`
- `.aide/tools/issue-creator/example-spec.md`

## Workflow

### Inputs
- Title (required)
- Body (required; include reproduction/acceptance criteria)
- Issue Type (GitHub Issue Types): `feature` | `bug` | `technical-debt` | `chore` | `documentation` | `research` | `epic`
- Priority: `critical` | `high` | `medium` | `low`
- Area: `area:<name>` (string)
- Status: `status:needs-spec` | `status:ready` | `status:in-progress`
- Optional repo override (`owner/repo`)

### Actions
1) Build labels list: `priority:<x>, area:<y>, status:<z>` (+ `Epic` if epic)
2) Run `gh issue create` with title/body/labels.
3) Set GitHub Issue Type via `.aide/tools/set-issue-type.py --issue <num> --type <type>`; fail if this step fails.
4) Output the created issue URL.

## Notes
- If labels are missing or differ in a repo, ask for the correct labels before creating.
