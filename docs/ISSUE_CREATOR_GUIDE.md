# Issue Creator Tool Guide

Batch create GitHub issues with Epic/child relationships and automatic area inference.

## Quick Start

```bash
# Setup (one-time)
cp .aide/tools/issue-creator.config.example.json issue-creator.config.json

# Make executable
chmod +x .aide/tools/issue-creator/issue-creator.py

# Create issues from file
.aide/tools/issue-creator/issue-creator.py specs.md

# Create issues from stdin (paste spec, then Ctrl+D / Ctrl+Z)
.aide/tools/issue-creator/issue-creator.py

# Pipe from clipboard (macOS)
pbpaste | .aide/tools/issue-creator/issue-creator.py

# Pipe from clipboard (Windows PowerShell)
Get-Clipboard | .aide/tools/issue-creator/issue-creator.py
```

## Spec File Format

Issues are separated by `---` or `## Issue:` markers.

### Example: Epic with Children

```markdown
## [Epic]: Job System Overhaul

Complete overhaul of job assignment and priority system.

### Goals
- Flexible priority system
- Better drone assignment logic
- Cancellation support

### Success Criteria
- [ ] All child issues completed
- [ ] Performance maintained

---

## Issue: Job Priority System
priority: high
area: job-system

### Goals
- Drones prioritize high-priority jobs
- Buildings can mark urgent jobs

### Scope
- Add priority field to Job struct
- Update drone job selection logic

### Success Criteria
- [ ] High priority jobs claimed first
- [ ] Tests verify priority sorting

---

## Issue: Job Cancellation
priority: medium
area: job-system
blocked_by: Job Priority System

### Goals
- Cancel jobs in progress
- Refund partial resources

### Success Criteria
- [ ] Jobs can be cancelled mid-execution
- [ ] Resources properly refunded
```

## Spec Fields

### Required
- **Title**: First heading in section (`## Issue: Title` or `# Title`)

### Optional Metadata
Add these as `key: value` lines at the start of each section:

- `priority: high|medium|low` (default: `medium`)
- `area: system-name` (comma-separated for multiple areas)
- `blocked_by: Issue Title` (references another issue in same batch)
- `blocks: Issue Title` (references another issue in same batch)

### Epic Marker
Use `[Epic]:` in title or `## [Epic]: Title` to create an Epic issue:
- Gets `Epic` label instead of `enhancement`
- Subsequent issues (until next Epic) become children

## Area Inference

The tool automatically infers area labels from content keywords (configured in `.aide/issue-creator.config.json`).

**Example keywords:**
- `drone`, `pathfinding` → `area:drone-ai`
- `job`, `assignment` → `area:job-system`
- `ui`, `hud`, `menu` → `area:ui`

You can override or supplement with explicit `area:` field.

## Configuration

### Project Config: `issue-creator.config.json`

```json
{
  "area_keywords": {
    "job-system": ["job", "jobs", "task", "assignment"],
    "drone-ai": ["drone", "pathfinding", "navigation", "ai"],
    "ui": ["ui", "hud", "interface", "menu", "panel"]
  },
  "default_priority": "medium",
  "default_status_ready": "status:ready",
  "default_status_blocked": "status:blocked",
  "epic_label": "Epic",
  "enhancement_label": "enhancement"
}
```

**Customize:**
- `area_keywords`: Keyword-to-area mapping for auto-inference
- `default_priority`: Priority when not specified in spec
- Label names to match your project's label system

## Output

```
✓ Loaded config from .aide/issue-creator.config.json
Creating 3 issues...

✓ Created Epic #140: Job System Overhaul
  ✓ Created #141: Job Priority System (priority: high, areas: job-system)
  ✓ Created #142: Job Cancellation (priority: medium, areas: job-system)

Setting up relationships...
  ✓ Linked #141 as child of #140
  ✓ Linked #142 as child of #140

Blocked issues (set via labels and body):
  ⚠ #142 blocked by: Job Priority System

Summary:
  Created 3 issues
  1 Epic(s) with children

Issue numbers:
  #140: Job System Overhaul
  #141: Job Priority System
  #142: Job Cancellation
```

## Features

### Parent/Child Relationships (Epics)
- Epics automatically link children via GitHub's `addSubIssue` GraphQL mutation
- Children appear in Epic's "Relationships" sidebar in GitHub UI
- Query: `gh api graphql -f query='{...see GITHUB_QUERIES.md...}'`

### Blocking Dependencies
- `blocked_by: Issue Title` adds:
  - `status:blocked` label
  - "Blocked By" section in issue body
  - Dependency tracking for queries

### Label Automation
- **Type**: `Epic` or `enhancement`
- **Priority**: `priority:high|medium|low`
- **Area**: `area:system-name` (auto-inferred + explicit)
- **Status**: `status:ready` or `status:blocked`

## Integration with AIDE Workflow

### Step 1: Design Session (ChatGPT)
Create specs in ChatGPT, export to markdown file.

### Step 2: Batch Create Issues
```bash
.aide/tools/issue-creator/issue-creator.py design-session-specs.md
```

### Step 3: Implement (Implementation Agent)
```
Implement #141
```

Agent reads issue, implements, creates PR with `Fixes #141`.

### Step 4: Review (PR Review Agent)
PR review agent reads spec from issue #141 (not PR description).

## Troubleshooting

### "No issues found"
- Check that sections are separated by `---` or `## Issue:` markers
- Ensure each section has a heading with title

### "No area inference"
- Config file not found or has invalid JSON
- Copy example: `cp .aide/tools/issue-creator.config.example.json .aide/issue-creator.config.json`

### GraphQL errors
- Ensure `gh` CLI is authenticated: `gh auth status`
- Requires `repo` scope for creating issues and setting relationships

### Parent/child linking fails
- Both parent and child must be created in same batch
- Epic must appear before children in spec file
- Use exact title match for parent reference

## Advanced Usage

### Dry Run (Preview)
Add `--dry-run` flag (future feature):
```bash
.aide/tools/issue-creator/issue-creator.py --dry-run specs.md
```

### Custom Label Prefix
For projects with different label conventions, update config:
```json
{
  "default_status_ready": "ready",
  "default_status_blocked": "blocked"
}
```

### Multiple Epics
Each `[Epic]:` starts a new epic scope. Issues belong to the most recent epic:

```markdown
## [Epic]: Backend Refactor
...

## Issue: API v2
(child of Backend Refactor)

---

## [Epic]: UI Redesign
...

## Issue: New Theme System
(child of UI Redesign)
```

## See Also

- [GITHUB_QUERIES.md](agents/GITHUB_QUERIES.md) - Query issue relationships
- [LABELS.md](../../.github/LABELS.md) - Label system reference
- [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) - Issue workflow
