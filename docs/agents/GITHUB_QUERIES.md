# GitHub Queries Reference for Agents

Query GitHub state dynamically instead of reading stale markdown files.

**Token Efficiency**: GitHub CLI queries use ~200 tokens vs reading IMPLEMENTATION_STATUS.md (~8,000+ tokens). Queries are always current.

## Quick Reference Commands

```bash
# Current work
gh issue list --label "status:in-progress" --state open

# Ready to implement
gh issue list --label "status:ready" --state open

# Active PRs
gh pr list --state open

# Recent completions
gh pr list --state merged --limit 10

# Specific epic/area
gh issue list --label "Epic" --state open
gh issue list --label "area:job-system" --state open
```

## Issue Relationships

GitHub supports native issue relationships for dependency tracking and epic structure.

### Query Relationships (GraphQL)

**Get issue with all relationships:**

```bash
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 42) {
      number
      title
      state

      # Child issues / tracked work
      trackedIssues(first: 20) {
        totalCount
        nodes {
          number
          title
          state
          labels(first: 5) {
            nodes { name }
          }
        }
      }

      # Parent issues / blocking work
      trackedInIssues(first: 10) {
        totalCount
        nodes {
          number
          title
          state
        }
      }
    }
  }
}
' --jq '.data.repository.issue'
```

**Find all epic issues with their children:**

```bash
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issues(first: 10, labels: ["Epic"], states: OPEN) {
      nodes {
        number
        title
        trackedIssues(first: 50) {
          totalCount
          nodes {
            number
            title
            state
          }
        }
      }
    }
  }
}
' --jq '.data.repository.issues.nodes[]'
```

**Find blocked issues (issues with dependencies):**

```bash
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issues(first: 20, states: OPEN) {
      nodes {
        number
        title
        trackedInIssues(first: 5) {
          totalCount
          nodes {
            number
            title
            state
          }
        }
      }
    }
  }
}
' --jq '.data.repository.issues.nodes[] | select(.trackedInIssues.totalCount > 0)'
```

### Set Relationships (GraphQL Mutations)

GitHub uses **TaskList** items to track issue relationships. You need the issue's `id` (not number) for mutations.

**Get issue ID:**

```bash
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 42) {
      id
      number
      title
    }
  }
}
' --jq '.data.repository.issue.id'
```

**Add child issue to epic (track relationship):**

```bash
# First, get the parent issue ID
PARENT_ID=$(gh api graphql -f query='{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 42) { id }
  }
}' --jq -r '.data.repository.issue.id')

# Then add the child issue as a tracked issue
gh api graphql -f query='
mutation {
  updateIssue(input: {
    id: "'"$PARENT_ID"'"
    body: "Epic body text\n\n- [ ] #45\n- [ ] #46\n- [ ] #47"
  }) {
    issue {
      id
      trackedIssues { totalCount }
    }
  }
}
' --jq '.data.updateIssue.issue'
```

**Note:** GitHub automatically detects task list items with issue references (`- [ ] #45`) and creates tracked relationships.

**Alternative: Use issue body with task lists**

```bash
# Create epic with child issues in body
gh issue create \
  --title "[Epic]: Feature Name" \
  --body "## Summary
Epic description

## Child Issues
- [ ] #101 - Subtask 1
- [ ] #102 - Subtask 2
- [ ] #103 - Subtask 3

## Success Criteria
- All child issues completed"
```

**Set blocked by relationship:**

Add to issue body using keywords:
- "Blocked by #42"
- "Depends on #42"
- "Requires #42"

```bash
gh issue edit 45 --body "$(cat <<'EOF'
## Description
Implement feature X

## Blocked by
- #42 (waiting for API refactor)
- #43 (needs design approval)

## Implementation
...
EOF
)"
```

**Query with owner/repo from current directory:**

```bash
# Auto-detect owner and repo
REPO_INFO=$(gh repo view --json owner,name -q '{owner: .owner.login, name: .name}')
OWNER=$(echo $REPO_INFO | jq -r '.owner')
REPO=$(echo $REPO_INFO | jq -r '.name')

# Use in queries
gh api graphql -f owner="$OWNER" -f repo="$REPO" -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    issues(first: 10, states: OPEN) {
      nodes { number title }
    }
  }
}
'
```

## Common Query Patterns

### Epic Progress Tracking

```bash
# Get epic progress summary
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 116) {
      title
      trackedIssues {
        totalCount
        nodes {
          state
        }
      }
    }
  }
}
' --jq '{
  epic: .data.repository.issue.title,
  total: .data.repository.issue.trackedIssues.totalCount,
  closed: [.data.repository.issue.trackedIssues.nodes[] | select(.state == "CLOSED")] | length,
  open: [.data.repository.issue.trackedIssues.nodes[] | select(.state == "OPEN")] | length
}'
```

### Find Unblocked Work

```bash
# Issues ready to implement (no blocking dependencies)
gh issue list --label "status:ready" --json number,title,body \
  --jq '.[] | select(.body | test("(Blocked by|Depends on|Requires) #[0-9]+") | not)'
```

### Find Critical Path

```bash
# Issues that block other work
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issues(first: 50, states: OPEN, labels: ["status:in-progress"]) {
      nodes {
        number
        title
        trackedIssues(first: 10) {
          totalCount
        }
      }
    }
  }
}
' --jq '.data.repository.issues.nodes[] | select(.trackedIssues.totalCount > 0) | {number, title, blocks: .trackedIssues.totalCount}'
```

## Workflow Integration

### Step 0: Spec Intake (IMPLEMENTATION_START.md)

```bash
# Read issue spec
gh issue view <number>

# Check dependencies
gh api graphql -f query='{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: <number>) {
      trackedInIssues {
        nodes {
          number
          title
          state
        }
      }
    }
  }
}'
```

### Step 1: Codebase Survey

```bash
# Query current state
gh issue list --label "status:in-progress" --state open
gh pr list --state open

# Check for related work
gh issue list --search "sort:updated-desc <keyword>" --limit 10
```

### After PR Merge

```bash
# Issue auto-closes via "Fixes #42" in PR
# Query recent completions
gh pr list --state merged --limit 5 --json number,title,closedAt

# Check epic progress
gh api graphql -f query='{...epic query...}'
```

## Advanced: Projects V2 Integration

GitHub Projects V2 can also track issue relationships:

```bash
# List project items (issues/PRs in a project)
gh project item-list <project-number> --owner OWNER --format json

# Add issue to project
gh project item-add <project-number> --owner OWNER --url <issue-url>
```

## Token Efficiency Comparison

| Method | Tokens | Currency | Auto-Update |
|--------|--------|----------|-------------|
| Read IMPLEMENTATION_STATUS.md | ~8,000 | ❌ Stale | ❌ Manual |
| `gh issue list` query | ~200 | ✅ Current | ✅ Automatic |
| GraphQL relationships | ~300 | ✅ Current | ✅ Automatic |

## Reference

- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Issue Relationships](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-task-lists)

---

**Usage in AIDE**: Agents query GitHub state at the start of each session instead of reading snapshot documents. State is always current and auto-updates on PR merge.
