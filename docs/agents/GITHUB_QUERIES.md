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

GitHub has two types of relationships:
1. **Parent/Child (Sub-issues)** - Proper hierarchical Epic structure (`addSubIssue` mutation)
2. **Tracked issues** - Task list dependencies (`trackedIssues` via task lists in body)

#### Add Sub-Issue (Parent/Child) - RECOMMENDED

This is what the GitHub web UI "Relationships" sidebar uses:

```bash
# Get issue IDs
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    parent: issue(number: 116) { id }
    child: issue(number: 117) { id }
  }
}
'

# Add child to parent
gh api graphql -f query='
mutation {
  addSubIssue(input: {
    issueId: "PARENT_ID"
    subIssueId: "CHILD_ID"
  }) {
    issue {
      number
      subIssues(first: 10) {
        totalCount
        nodes { number title state }
      }
    }
  }
}
'
```

**Query parent/child relationships:**

```bash
# From parent (Epic) - show all children
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 116) {
      number
      title
      subIssues(first: 50) {
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
'

# From child - show parent
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 117) {
      number
      title
      parent {
        number
        title
      }
    }
  }
}
'
```

#### Task List Dependencies (Tracked Issues)

Task lists in issue body create `trackedIssues` relationships (different from parent/child).

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

### Blocked Dependencies

GitHub supports dependency tracking via:
1. **`status: blocked` label** (for queries/filtering)
2. **Issue body** (for visibility and context)
3. **Task lists** (for auto-linking)

#### Method 1: Label + Body (Recommended)

```bash
# Mark issue as blocked
gh issue edit 45 \
  --add-label "status: blocked" \
  --body "$(cat <<'EOF'
## Description
Implement feature X

## Blocked By
- #42 - API refactor must complete first
- #43 - Awaiting design approval

## Implementation
Once unblocked:
1. Step 1
2. Step 2
EOF
)"
```

**Query blocked issues:**
```bash
# Find all blocked work
gh issue list --label "status: blocked" --state open

# Blocked issues by area
gh issue list --label "status: blocked,area: drone-ai" --state open
```

#### Method 2: Task List Dependencies

Use task lists to create `trackedIssues` relationships:

```bash
gh issue edit 100 --body "## Epic

- [ ] #101 - Prerequisite (must complete first)
- [ ] #102 - Can start in parallel
- [ ] #103 - Depends on #101 and #102
"
```

**Check if dependency resolved:**
```bash
# Check if blocking issue is closed
gh issue view 42 --json state --jq '.state'  # "OPEN" or "CLOSED"
```

#### Method 3: Unblock Workflow

When blocking issue closes, unblock dependent issues:

```bash
# Remove blocked status when dependency closes
gh issue edit 45 --remove-label "status: blocked" --add-label "status: ready"

# Update issue body to remove "Blocked by" section
gh issue edit 45 --body "$(cat <<'EOF'
## Description
Implement feature X

~~## Blocked By~~
~~- #42 - API refactor (RESOLVED)~~

## Implementation
1. Step 1
2. Step 2
EOF
)"
```

**Auto-detect blockers in comments:**
```bash
# Search for "blocked by" in issue comments
gh issue view 45 --comments | grep -i "blocked by"
```

#### Finding Cross-Epic Dependencies

```bash
# Epic #100 blocks Epic #90
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    epic100: issue(number: 100) {
      number
      title
      state
      subIssues(first: 50) {
        nodes {
          number
          title
          state
          labels(first: 10) {
            nodes { name }
          }
        }
      }
    }
    epic90: issue(number: 90) {
      number
      title
      state
      labels(first: 10) { nodes { name } }
      body
    }
  }
}
' --jq '
  if .data.repository.epic90.labels.nodes | map(.name) | contains(["status: blocked"])
  then "Epic #90 is blocked. Check body for dependencies."
  else "Epic #90 is not blocked."
  end
'
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

### Step 0: Spec Intake (`implementation/STEP_0_SPEC_INTAKE.md`)

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
