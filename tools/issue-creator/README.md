# Issue Creator Tool

Batch create GitHub issues with Epic/child relationships from formatted spec files.

**Saves agent tokens** by keeping spec content out of conversation context.

## Quick Start

**Option A: Use the Custom GPT (Recommended)**

1. [Use the official Custom GPT](https://chatgpt.com/g/g-696532cabeac81918a55b5f62eb9b8fd-issue-spec-formatter-aide) (requires ChatGPT Plus)
2. Generate specs in design session
3. Custom GPT formats as markdown -> download Canvas as `specs.md`
4. Run tool:
   ```bash
   python .aide/tools/issue-creator/issue-creator.py specs.md
   ```

**Option B: Manual spec creation**

1. Write spec file following format in [example-spec.md](example-spec.md)
2. Run tool (same as above)

## Features

- ✅ Creates Epic + child issues in one batch
- ✅ Links Epic/child relationships via GitHub GraphQL API
- ✅ Infers labels from metadata (priority, area)
- ✅ Reports blocking dependencies
- ✅ Idempotent reruns (updates existing issues, and `--update-blockers` reapplies dependencies)
- ✅ Preflights and creates missing labels needed by specs
- ✅ Normalizes redundant “Issue:” title prefixes
- ✅ UTF-8 support (handles curly quotes from ChatGPT)
- ✅ Windows + Mac + Linux compatible

## Manual Links

```bash
# Link existing issues via CLI without rerunning specs
python .aide/tools/issue-creator/issue-creator.py --link-blocker 232:231
python .aide/tools/issue-creator/issue-creator.py --link-child 227:232
```

Use `PARENT:CHILD` to call the GraphQL `addSubIssue` mutation or `BLOCKED:BLOCKER` for `addBlockedBy`.

## Spec File Format

```markdown
## [Epic]: Epic Title

### Goal
Epic description

### Success Criteria
- Criterion 1

---

## Issue: Issue Title
type: feature|bug|technical-debt|chore|documentation|research
priority: high|medium|low
area: system-name

### Goal
Issue description

### Success Criteria
- Criterion 1

---
```

**Key format rules:**
- Epic: `## [Epic]: Title` (only Epics use a title prefix)
- Issue: `## Issue: Title` (no type tags)
- Section separator: `---`
- Metadata: `type:`, `priority:`, `area:`, `blocked_by:` on separate lines
- Success criteria: Plain bullets `- item` (NO checklists - those belong in PRs)

## Setup

### Prerequisites

- Python 3.7+
- GitHub CLI (`gh`) installed and authenticated
- GitHub repository with issues enabled

### Configuration

Create `.aide/tools/issue-creator/issue-creator.config.json` (optional):

```json
{
  "area_labels": {
    "job-system": "area:job-system",
    "drone-ai": "area:drone-ai",
    "ui": "area:ui"
  },
  "priority_labels": {
    "high": "priority:high",
    "medium": "priority:medium",
    "low": "priority:low"
  }
}
```

See [issue-creator.config.example.json](issue-creator.config.example.json) for full example.

## Usage

### Create Mode (Default)

```bash
# Create issues from spec file
python .aide/tools/issue-creator/issue-creator.py specs.md

# Read from stdin
cat specs.md | python .aide/tools/issue-creator/issue-creator.py

# Show help
python .aide/tools/issue-creator/issue-creator.py --help
```

### Update Mode

Update existing issues instead of creating new ones.

**Update single issue:**

```bash
# Update issue #171 with first spec in file
python .aide/tools/issue-creator/issue-creator.py specs.md --update 171
```

**Update Epic + children:**

```bash
# Update Epic #170 and all children (matches by order)
python .aide/tools/issue-creator/issue-creator.py specs.md --update-epic 170
```

**Auto-update with metadata:**

```bash
# Update issues based on issue_number field in specs
python .aide/tools/issue-creator/issue-creator.py specs.md --update-auto
```

**Spec file for auto-update:**

```markdown
## Issue: Updated Title
type: chore
issue_number: 171
priority: high
area: docs

### Goal
Updated description
```

The `issue_number: N` field tells the tool which issue to update.

### Reapply blockers

```bash
# Reapply blocked_by relationships defined in the spec to existing issues
python .aide/tools/issue-creator/issue-creator.py specs.md --update-blockers
```

Ensure each `blocked_by` entry uses the final issue titles (no type tags) so the tool can locate the blocker automatically.

### With Agent

Use the Issue Batch Creator agent:

```bash
# In Claude Code / other AI assistant
/agent .aide/docs/agents/ISSUE_BATCH_CREATOR_START.md
```

Agent workflow:
1. Get spec file path from user
2. Run tool immediately (no reading/validation)
3. Handle errors (create missing labels)
4. Verify results via GitHub API
5. Clean up temp files

## Tool Behavior

**Phase 1: Create Issues**
- Parses spec file for Epic and Issue headings
- Creates all issues via `gh issue create`
- Applies labels from metadata (priority, area)

**Phase 2: Link Relationships**
- Links child issues to Epic via GraphQL `addSubIssue` mutation
- Epic URL is added to each child's description

**Phase 3: Apply Dependencies**
- Reads `blocked_by` metadata and invokes the `addBlockedBy` GraphQL mutation
- Adds a “Blocked by” section in the issue body
- Re-run with `--update-blockers` to refresh these relationships on existing issues

## Common Errors

### Error: Label not found

**Symptom:** `could not add label: 'Epic' not found`

**Fix:** Create missing label, then re-run:

```bash
# Epic label
gh label create "Epic" --description "Parent issue grouping related work" --color "7057ff"

# Area labels
gh label create "area:docs" --description "Documentation" --color "c5def5"

# Priority labels
gh label create "priority:high" --description "Should address soon" --color "d93f0b"
gh label create "priority:medium" --description "Moderate importance" --color "fbca04"
gh label create "priority:low" --description "Nice to have" --color "0e8a16"

# Re-run tool
python .aide/tools/issue-creator/issue-creator.py specs.md
```

### Error: UnicodeDecodeError

**Symptom:** `'charmap' codec can't decode byte`

**Cause:** Spec file has Unicode (curly quotes from ChatGPT), Python defaulting to CP1252 on Windows.

**Fix:** Tool already handles UTF-8. If error persists, convert file:

```bash
iconv -f UTF-16 -t UTF-8 specs.md -o specs-utf8.md
python .aide/tools/issue-creator/issue-creator.py specs-utf8.md
```

### Error: Title formatting

If created issues have redundant `Issue:` prefixes, fix manually:

```bash
gh issue edit 171 --title "Update Documentation Policy"
gh issue edit 172 --title "Formalize Job record model"
```

## Customization

### Custom GPT Setup

Want to customize the Custom GPT for your project?

See [../../docs/CUSTOM_GPT_SETUP.md](../../docs/CUSTOM_GPT_SETUP.md) for:
- Full GPT configuration
- Knowledge base files to upload
- Custom instructions
- Conversation starters

### Extending the Tool

The tool is designed to be extended:
- `parse_spec(content)` - Parses markdown into Epic/Issue structures
- `create_issue(data)` - Creates single issue via `gh`
- `link_child_to_epic(child_num, epic_num)` - Links via GraphQL

Fork and customize for your workflow!

## Documentation

- [ISSUE_CREATOR_GUIDE.md](../../docs/ISSUE_CREATOR_GUIDE.md) - Complete format specification
- [CUSTOM_GPT_SETUP.md](../../docs/CUSTOM_GPT_SETUP.md) - Custom GPT configuration
- [example-spec.md](example-spec.md) - Working example with Epic + 5 children
- [ISSUE_BATCH_CREATOR_START.md](../../docs/agents/ISSUE_BATCH_CREATOR_START.md) - Agent primer

## Philosophy

This tool exists to **save agent tokens**. Instead of having AI agents read/write large spec files (consuming context budget), we:

1. Use Custom GPT to format specs (cheap, included in ChatGPT Plus)
2. Run CLI tool to create issues (free, local, fast)
3. Agent only verifies via GitHub API (small JSON responses)

Result: **Zero additional token cost** for batch issue creation.

## License

MIT License - Part of the AIDE framework
