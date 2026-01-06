# Beads (bd) Usage Guide for AI Agents

AI working memory and tactical task tracking alongside GitHub Issues.

**Token Economy:** Beads queries are fast (~200 tokens). Use `bd ready` to find work, not exhaustive file scanning.

## Purpose and Scope

**Mission:** Provide AI agents with fast, queryable working memory for:
- Discovered work during implementation (bugs found, TODOs identified)
- Task decomposition and dependency tracking
- Single-session execution tracking (complements TodoWrite for persistence)
- Cross-session context recovery

**Non-goals:**
- NOT a replacement for GitHub Issues (GitHub is human-facing source of truth)
- NOT for long-term roadmap (use GitHub Epics)
- NOT for PR tracking (use GitHub PRs)

## Sources of Truth

**Dual tracking system:**
- **GitHub Issues** - Strategic work (Epics, features, bugs requiring specs)
- **Beads (bd)** - Tactical work (AI-discovered tasks, decomposed subtasks, dependencies)

**Relationship:**
- GitHub Issue #98 might spawn multiple bd tasks (bd-a3f, bd-b2e, bd-c4d)
- Close GitHub Issue when Epic/Feature complete
- Close bd tasks as each tactical step finishes

## When to Use Beads

**Use bd for:**
- ✅ Discovering new work during implementation ("Found bug X while implementing Y")
- ✅ Decomposing large tasks into dependency chains
- ✅ Tracking blockers ("Can't implement auth until crypto lib is added")
- ✅ Recording TODOs that span multiple sessions
- ✅ Finding next available work (`bd ready`)

**Use TodoWrite for:**
- ✅ Single-session execution tracking (current PR checklist)
- ✅ Simple linear task lists (no dependencies)

**Use GitHub Issues for:**
- ✅ User-facing features and bugs
- ✅ Epic-level tracking with sub-issues
- ✅ Team communication and PR links

**Rule of thumb:** If it needs to survive compaction/session end and has dependencies → bd. If it's just execution tracking → TodoWrite.

## Essential Commands

### Finding Work
```bash
# Show unblocked issues ready to work
bd ready

# List all open issues
bd list --status=open

# Show active work
bd list --status=in_progress

# View issue details with dependencies
bd show <id>
```

### Creating Issues
```bash
# Create task (priority: 0-4 or P0-P4, NOT "high"/"medium"/"low")
bd create "Fix login bug" --type bug --priority 2

# Create feature
bd create "Add auth system" --type feature --priority 1

# Create with description
bd create "Write tests" --type task --priority 2 -d "Unit tests for auth module"

# Batch create (use parallel subagents for many items)
# Run multiple bd create commands concurrently
```

### Managing Work
```bash
# Claim work
bd update <id> --status in_progress

# Complete work (can close multiple at once)
bd close <id1> <id2> <id3>

# Close with reason
bd close <id> --reason "Fixed in commit abc123"
```

### Dependencies
```bash
# Add dependency (issue2 depends on issue1)
bd dep add <issue2> <issue1>

# Show all blocked issues
bd blocked

# View dependency tree
bd dep tree <id>
```

### Sync with Git
```bash
# Sync at session end (MANDATORY)
bd sync

# Check sync status
bd sync --status
```

## Workflow Integration Patterns

### Context Recovery (Starting Work)
```bash
# Check for existing beads work
bd list --status=open
bd ready  # Find unblocked work
bd prime  # Full workflow context
```

### Exploration and Survey
```bash
# Record discovered work
bd create "Refactor XYZ for cleaner integration" --type task --priority 3

# Note blockers
bd create "Add crypto library dependency" --type task --priority 1
bd dep add <auth-task-id> <crypto-lib-id>  # Auth blocked by crypto
```

### During Active Work
```bash
# Record TODOs and bugs found
bd create "Bug: Drone crashes on empty queue" --type bug --priority 0
bd create "TODO: Optimize pathfinding for large maps" --type task --priority 4

# Link related work
bd dep add <current-issue> <discovered-blocker>
```

### Session Close (CRITICAL - All Agents)
```bash
# ALWAYS run bd sync before ending session
bd sync

# Verify sync succeeded
bd sync --status
```

## Beads + GitHub Workflow

**Example: Implementing GitHub Issue #98 (Epic: Content Pipeline)**

1. **Read GitHub Issue #98** - Get spec (goal, scope, success criteria)
2. **Check beads for related work** - `bd ready`, `bd list`
3. **Decompose into bd tasks**:
   ```bash
   bd create "Parse ResourceDef JSONL schema" --type task --priority 1
   bd create "Validate ResourceDef on load" --type task --priority 1
   bd create "Integrate ResourceDef with ContentDB" --type task --priority 2
   # Add dependencies
   bd dep add <integrate-id> <validate-id>  # Integration blocked by validation
   ```
4. **Work through bd ready queue** - Claim, implement, close each task
5. **Close GitHub Issue #98** - When all bd tasks complete and spec criteria met

## Session Close Protocol

**CRITICAL:** Before ending session, ALWAYS run:

```bash
bd sync              # Commit beads changes to git
git push             # Push to remote
```

Work is NOT complete until pushed. See "Landing the Plane" section in AGENTS.md.

## Common Patterns

### Discovered Work During Implementation
```bash
# While implementing feature X, discovered bug Y
bd create "Bug: Race condition in JobSystem" --type bug --priority 1
bd create "Investigate JobSystem thread safety" --type task --priority 2
bd dep add <investigate-id> <race-condition-id>
```

### Cross-Epic Dependencies
```bash
# Epic #100 (Combat) blocked by Epic #116 (Motion)
bd create "Combat blocked: needs motion refactor" --type blocker --priority 0
bd dep add <combat-task> <motion-task>
bd blocked  # Shows all blocked work
```

### Multi-Session Implementation
```bash
# Session 1: Start work
bd create "Implement auth middleware" --type task --priority 1
bd update <id> --status in_progress
bd sync  # End session

# Session 2: Resume
bd prime  # Context recovery
bd ready  # See what's available
bd show <id>  # Review details
# Continue work...
bd close <id>
bd sync
```

## Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `bd ready` | Find unblocked work | `bd ready` |
| `bd create` | Create issue | `bd create "Title" --type task --priority 2` |
| `bd list` | List issues | `bd list --status=open` |
| `bd show` | View details | `bd show bd-a3f` |
| `bd update` | Update issue | `bd update bd-a3f --status in_progress` |
| `bd close` | Complete work | `bd close bd-a3f bd-b2e` |
| `bd dep add` | Add dependency | `bd dep add <depends-on> <blocker>` |
| `bd blocked` | Show blocked | `bd blocked` |
| `bd sync` | Sync with git | `bd sync` |
| `bd prime` | Context recovery | `bd prime` |

## Flags and Options

**Priority values:**
- `0` or `P0` - Critical (blocks everything)
- `1` or `P1` - High (this sprint)
- `2` or `P2` - Medium (next sprint)
- `3` or `P3` - Low (backlog)
- `4` or `P4` - Nice to have

**Issue types:**
- `task` - Standard work item
- `bug` - Bug fix
- `feature` - New feature
- `blocker` - Blocking issue (use with dependencies)

**Status values:**
- `open` - Available to work
- `in_progress` - Currently being worked
- `done` - Completed

## Token Economy

**Efficient usage:**
- `bd ready` (~200 tokens) beats scanning all files for TODOs
- `bd prime` (~80 lines) provides full workflow context
- `bd show <id>` gives targeted context vs reading entire codebase

**Batch operations:**
- Create multiple issues in parallel (use subagents for >5 items)
- Close multiple issues at once: `bd close bd-1 bd-2 bd-3`

## Database Location

Beads auto-discovers database:
1. `--db` flag
2. `$BEADS_DB` environment variable
3. `.beads/*.db` in current directory or ancestors
4. `~/.beads/default.db` as fallback

Current project: `.beads/beads.db` (local, gitignored for speed)

## Sync Model

**Auto-sync:**
- Changes auto-flush to JSONL after 5s debounce
- Auto-import from JSONL when newer than DB (after git pull)

**Manual sync:**
- Run `bd sync` at session end (MANDATORY)
- Commits beads changes to git
- Follows `git push` in Landing the Plane workflow

**Files:**
- `.beads/beads.db` - Local SQLite (fast queries, gitignored)
- `.beads/issues.jsonl` - Git-tracked (team sync)
- `.beads/config.yaml` - Configuration (git-tracked)

## Critical Don'ts

- ❌ Don't skip `bd sync` at session end (leaves work stranded)
- ❌ Don't use beads for long-term roadmap (use GitHub Issues)
- ❌ Don't duplicate GitHub Issues in beads (they're complementary)
- ❌ Don't use priority names like "high"/"medium"/"low" (use 0-4 or P0-P4)

## Reference Docs

- `bd prime` - Full workflow context
- `bd quickstart` - Quick start guide
- [GITHUB_QUERIES.md](GITHUB_QUERIES.md) - Query GitHub for strategic work
- [AGENT_OPERATIONAL_TOKEN_ECONOMY.md](AGENT_OPERATIONAL_TOKEN_ECONOMY.md) - Efficient operation

---

**Ready?** Run `bd ready` to find available work, or `bd prime` for full context.
