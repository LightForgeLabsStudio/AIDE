# GitHub Label Taxonomy

**Purpose:** Standard labels for issue/PR categorization, filtering, and automation.

## Label Categories

### General Labels

| Label | Color | Description | Usage |
|-------|-------|-------------|-------|
| `documentation` | #0075ca | Improvements or additions to documentation | Docs updates, guides |
| `question` | #d876e3 | Further information is requested | Clarifications, discussions |
| `duplicate` | #cfd3d7 | This issue or pull request already exists | Duplicate of existing issue |
| `invalid` | #e4e669 | This doesn't seem right | Invalid/incorrect issues |
| `wontfix` | #ffffff | This will not be worked on | Rejected features, won't address |

### Area Labels (System Scope)

| Label | Color | Description |
|-------|-------|-------------|
| `area: drone-ai` | #c5def5 | Drone behavior, pathfinding, state machine |
| `area: job-system` | #c5def5 | Job assignment, priority, scheduling |
| `area: buildings` | #c5def5 | Building system, construction, upgrades |
| `area: resources` | #c5def5 | Resource management, harvesting, storage |
| `area: ui` | #c5def5 | User interface, HUD, menus |
| `area: combat` | #c5def5 | Combat mechanics, weapons, enemies |
| `area: testing` | #c5def5 | Test infrastructure, test cases |
| `area: tooling` | #c5def5 | Dev tools, build scripts, CI/CD |
| `area: multiple-systems` | #1d76db | Cross-cutting changes across multiple systems |

**Usage:** Every issue should have at least one `area:` label.

### Priority Labels

| Label | Color | Description | Response Time |
|-------|-------|-------------|---------------|
| `priority: critical` | #b60205 | Blocks development | Immediate |
| `priority: high` | #d93f0b | Should address soon | This sprint/week |
| `priority: medium` | #fbca04 | Moderate importance | Next sprint |
| `priority: low` | #0e8a16 | Nice to have | Backlog |

**Usage:** Assign based on impact and urgency.

### Status Labels

| Label | Color | Description | Workflow State |
|-------|-------|-------------|----------------|
| `status: needs-spec` | #ededed | Needs specification | Pre-implementation |
| `status: ready` | #0e8a16 | Ready for implementation | Step 0: Spec Intake |
| `status: in-progress` | #fbca04 | Currently being worked on | Step 2-7: Implementation |
| `status: needs-review` | #8B4513 | Awaiting code review | Step 7: PR Ready |

**Status Workflow:**
```
needs-spec -> ready -> in-progress -> needs-review -> (merged/closed)
```

### Community Labels

| Label | Color | Description |
|-------|-------|-------------|
| `good first issue` | #7057ff | Good for newcomers |
| `help wanted` | #008672 | Extra attention is needed |

## Label Application

### On Issue Creation

**Required:**
- Issue Type is set via GitHub Issue Types (no type labels).
- Area label: `area: <system>`
- Priority label: `priority: <level>`
- Status label: `status: needs-spec` or `status: ready`

**Example:**
```bash
gh issue create \
  --title "Drone crashes on empty queue" \
  --body "..." \
  --label "area: drone-ai,priority: high,status: ready"
```

### During Implementation

**Update status as work progresses:**

```bash
# Starting work (Step 2)
gh issue edit 42 --add-label "status: in-progress" --remove-label "status: ready"

# PR ready for review (Step 6)
gh issue edit 42 --add-label "status: needs-review" --remove-label "status: in-progress"

```

### On PR Creation

**PRs inherit labels from linked issue** (via `Fixes #42`), but can also have:
- Review status: `status: needs-review`
- Area labels: Same as linked issue

## Querying by Labels

### Find work to do

```bash
# Ready for implementation
gh issue list --label "status: ready" --state open

# High priority work
gh issue list --label "priority: high" --state open

# My area of work
gh issue list --label "area: drone-ai" --state open
```

### Check current work

```bash
# What's in progress?
gh issue list --label "status: in-progress" --state open


# What needs review?
gh issue list --label "status: needs-review" --state open
```

### Filter by Epic

```bash
# All issues for Epic #100 (using parent/child)
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 100) {
      subIssues(first: 50, states: OPEN) {
        nodes {
          number
          title
          labels(first: 10) { nodes { name } }
        }
      }
    }
  }
}
'
```

## Label Automation Opportunities

**Potential automations:**
- Auto-apply `area:` based on files changed
- Auto-apply `status: needs-review` when PR marked ready

*Note: Not currently implemented, but available via GitHub Actions.*

## Label Management

### Adding New Labels

```bash
# Create new area label
gh label create "area: new-system" \
  --description "New system description" \
  --color "c5def5"

# Create new priority/status label
gh label create "priority: urgent" \
  --description "Drop everything" \
  --color "ff0000"
```

### Updating Labels

```bash
# Rename label
gh label edit "old-name" --name "new-name"

# Update description/color
gh label edit "priority: high" --description "Updated description" --color "ff0000"
```

### Deleting Labels

```bash
gh label delete "deprecated-label"
```

## Best Practices

1. **Every issue gets labels** - Area, Priority, Status
2. **Update status labels** as work progresses
3. **Use `area:` for filtering** work by system
4. **Use `priority:` for triage** and sprint planning
5. **Use GitHub blocking relationships** to surface dependencies
6. **Keep labels synchronized** between issue and PR
7. **Query by labels** to find relevant work (see GITHUB_QUERIES.md)

## Reference

See [GITHUB_QUERIES.md](GITHUB_QUERIES.md) for label-based queries.
