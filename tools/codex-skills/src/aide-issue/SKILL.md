---
name: aide-issue
description: Create a GitHub issue following AIDE label conventions. Use when the user types /issue or asks to file an out-of-scope bug, feature, or tech debt. Creates the issue via gh with required labels (type, priority, area, status).
---

# AIDE Issue

## Overview

Create issues consistently with required labels so work is trackable and automation-friendly.

## Workflow

### Inputs
- Title (required)
- Body (required; include reproduction/acceptance criteria)
- Type: `bug` | `enhancement` | `technical-debt`
- Priority: `critical` | `high` | `medium` | `low`
- Area: `area:<name>` (string)
- Status: `status:needs-spec` | `status:ready` | `status:in-progress`
- Optional repo override (`owner/repo`)

### Actions
1) Build labels list: `<type>, priority:<x>, area:<y>, status:<z>`
2) Run `gh issue create` with title/body/labels.
3) Output the created issue URL.

## Notes
- If labels are missing or differ in a repo, ask for the correct labels before creating.

