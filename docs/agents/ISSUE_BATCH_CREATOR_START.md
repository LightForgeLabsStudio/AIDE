# Issue Batch Creator Agent Quick Start

Batch create GitHub issues with Epic/child relationships from formatted spec files for {{PROJECT_NAME}}.

**Token Economy:** This tool exists to save agent tokens. **DO NOT read spec files.** Run the tool, handle errors from tool output, verify via GitHub API only.

**Default Behavior:** Get file path → run tool → handle errors → verify via GitHub → clean up. No validation, no spec reading.

## The Workflow

1. **SPEC INTAKE** - Get spec file path from user
2. **RUN TOOL** - Execute issue-creator.py immediately (no reading, no validation)
3. **HANDLE ERRORS** - If tool fails, fix errors (create labels, fix format issues reported by tool)
4. **VERIFY RESULTS** - Check Epic/child relationships via GitHub API, fix title formatting if needed
5. **CLEAN UP** - Remove temp files, report completion

## Spec File Format

The issue-creator tool expects markdown files with this structure:

```markdown
## [Epic]: Epic Title

### Goal
Epic description

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

---

## Issue: [TypeTag] Issue Title
priority: high|medium|low
area: system-name

### Goal
Issue description

### Scope
What this issue includes

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

---

## Issue: [TypeTag] Another Issue
priority: medium
area: system-name
blocked_by: Exact Issue Title
...
```

**Key format rules:**
- Epic heading: `## [Epic]: Title` (no type tags)
- Issue heading: `## Issue: [TypeTag] Title` (type tags like [Chore], [Refactor], [Bug] go AFTER "Issue:")
- Section separator: `---`
- Metadata on separate lines: `priority:`, `area:`, `blocked_by:`
- Success criteria: `- [ ]` checkbox format

**Common type tags:**
- `[Chore]` - Maintenance, cleanup, documentation
- `[Refactor]` - Code restructuring without behavior change
- `[Bug]` - Fix broken functionality
- `[Feature]` - New functionality
- `[Hardening]` - Improve robustness, add guardrails
- `[Cleanup]` - Remove duplication, simplify

**References:**
- See `.aide/docs/ISSUE_CREATOR_GUIDE.md` for complete format documentation
- See `.aide/tools/example-spec.md` for working examples
- See `.aide/docs/CUSTOM_GPT_SETUP.md` for Custom GPT workflow

## Step 1: Spec Intake

**Agent asks:**
"Ready to create issues. Please provide the **spec file path** (e.g., `.aide/tools/specs.md`)."

**Common locations:**
- `.aide/tools/*_specs_*.md` (user-generated, gitignored)
- `.aide/tools/aide_issue_specs_*.md` (user-generated, gitignored)
- Any path provided by user

**DO NOT read the spec file.** The Custom GPT already validated format. If format is wrong, the tool will fail with a clear error message.

**Immediately proceed to Step 2 (Run Tool).**

## Step 2: Run Tool

Execute the issue-creator tool immediately. **No pre-flight checks, no label validation.** If labels are missing, the tool will fail with a clear error message and you'll create them in Step 3.

**Command:**
```bash
python .aide/tools/issue-creator.py <spec-file-path>
```

**Tool behavior:**
- **Phase 1**: Creates all issues via `gh issue create`
- **Phase 2**: Links Epic/child relationships via GraphQL `addSubIssue` mutation
- **Phase 3**: Reports blocking dependencies (must be manually resolved)
- **Output**: Issue URLs, Epic/child relationships, blocking dependencies

**If tool succeeds**: Proceed to Step 3 (Verify Results).

**If tool fails**: See error handling below, fix errors, then re-run tool.

## Step 3: Handle Errors (if tool failed)

The tool will fail with clear error messages. Fix the error, then re-run the tool.

**Common errors and fixes:**

### Error: UnicodeDecodeError
**Symptom:** `'charmap' codec can't decode byte`

**Cause:** Spec file has Unicode characters (curly quotes from ChatGPT), Python defaulting to CP1252 on Windows.

**Fix:** Tool already handles UTF-8 encoding. If error persists:
```bash
# Convert file to UTF-8 explicitly
iconv -f UTF-16 -t UTF-8 <spec-file> -o <spec-file>.utf8
python .aide/tools/issue-creator.py <spec-file>.utf8
```

### Error: Label not found
**Symptom:** `could not add label: 'Epic' not found`

**Cause:** Missing GitHub label.

**Fix:** Create missing label, then re-run tool.

```bash
# Epic label (purple, high visibility)
gh label create "Epic" --description "Parent issue grouping related work" --color "7057ff"

# Area labels (light blue)
gh label create "area:docs" --description "Documentation" --color "c5def5"
gh label create "area:job-system" --description "Job assignment" --color "c5def5"
# ... create any area labels mentioned in error

# Priority labels (traffic light colors)
gh label create "priority:high" --description "Should address soon" --color "d93f0b"
gh label create "priority:medium" --description "Moderate importance" --color "fbca04"
gh label create "priority:low" --description "Nice to have" --color "0e8a16"

# Re-run tool
python .aide/tools/issue-creator.py <spec-file-path>
```

### Error: GitHub API rate limit
**Symptom:** `API rate limit exceeded`

**Cause:** Too many API calls in short time (rare, usually only with very large batches).

**Fix:** Wait 60 seconds, then re-run. Tool is idempotent (won't duplicate issues).

## Step 4: Verify Results

After tool completes, verify issues were created correctly.

**Check Epic created:**
```bash
# Find recently created Epic
gh issue list --label "Epic" --limit 5 --json number,title,createdAt --state all
```

**Check child issues:**
```bash
# List recent issues
gh issue list --limit 20 --json number,title,labels,createdAt --state all
```

**Check parent/child relationships:**
```bash
# View Epic to see linked children (GitHub Web UI is clearest)
gh issue view <epic-number> --web
```

**Common title formatting issues:**

If titles have `[Feature]: Issue: [TypeTag]` instead of just `[TypeTag]`, fix them:

```bash
# Fix redundant prefixes
gh issue edit <number> --title "[TypeTag] Actual Title"

# Example
gh issue edit 171 --title "[Chore] Update Documentation Policy"
gh issue edit 172 --title "[Refactor] Formalize Job record model"
```

**Verify blocking dependencies:**

The tool reports blocking dependencies but **cannot auto-link them** (GitHub limitation). You must:
1. Note which issues are blocked
2. Manually add dependency comments or use project board automation
3. Report to user for manual tracking

**Report verification:**
```markdown
**Issues created:**
- Epic #<number>: <title>
- Issue #<number>: <title> (child of Epic #<epic>)
- Issue #<number>: <title> (child of Epic #<epic>)
...

**Blocking dependencies (manual tracking needed):**
- Issue #<number> blocked by: <title>

**Title formatting:** [OK / Fixed <count> issues]
```

## Step 5: Clean Up

Remove temp files and report completion.

**Remove spec file (if in gitignored location):**
```bash
# Only delete if user confirms or if in tools/*_specs_*.md pattern
rm <spec-file-path>
```

**Verify git status clean:**
```bash
git status
```

**Report completion:**
```markdown
✅ **Batch issue creation complete**

**Created:**
- Epic #<number>: <title>
- <count> child issues (#<start>-#<end>)

**Epic URL:** <epic-url>

**Blocking dependencies:** [None / See issue comments]

**Next steps:**
- Review Epic in GitHub: <epic-url>
- Start implementation with `/implement <issue-number>`
```

## Error Recovery

If tool fails mid-execution, it's safe to re-run. The tool is **idempotent**:
- Won't duplicate issues (check by title before creating)
- Can resume linking relationships
- Will skip already-completed steps

**To resume after failure:**
1. Check what was created: `gh issue list --limit 20`
2. Identify what failed (Epic? Children? Relationships?)
3. Re-run tool with same spec file
4. Tool will skip already-created issues

**To clean up partial failures:**
```bash
# Close duplicate/failed issues
gh issue close <number> --reason "duplicate"

# Delete recently created issues (if needed)
gh issue delete <number>
```

## Reference Docs

- `.aide/docs/ISSUE_CREATOR_GUIDE.md` - Complete format documentation
- `.aide/tools/example-spec.md` - Working examples with Epic, children, dependencies
- `.aide/docs/CUSTOM_GPT_SETUP.md` - Custom GPT workflow for formatting specs
- `.aide/tools/issue-creator.py` - The tool itself (Python 3)

## Common Workflows

### Workflow 1: New Epic with Children
User provides spec file from Custom GPT:
1. Read spec file
2. Pre-flight check (labels)
3. Run tool
4. Verify Epic + children created
5. Fix title formatting if needed
6. Report results

### Workflow 2: Standalone Issues (No Epic)
Spec file has only `## Issue:` headings (no `## [Epic]:`):
1. Read spec file
2. Pre-flight check
3. Run tool
4. Verify issues created
5. Report results

### Workflow 3: Children for Existing Epic
Spec file has `## Issue:` headings referencing existing Epic:
1. Read spec file
2. Check Epic exists: `gh issue view <epic-number>`
3. Run tool with Epic number: `python .aide/tools/issue-creator.py <spec-file> --epic <epic-number>`
4. Verify children linked to Epic
5. Report results

## Critical Don'ts

- ❌ Don't manually create issues (use tool for consistency)
- ❌ Don't modify issue-creator.py without testing on example-spec.md first
- ❌ Don't delete spec files without user confirmation
- ❌ Don't skip title formatting fixes (makes issue lists hard to scan)
- ❌ Don't ignore blocking dependencies (user needs to track them)

## Customization for Your Project

Replace these placeholders with your project specifics:

- `{{PROJECT_NAME}}` → Your project name

**Project-specific labels:**
Check your project's `.aide/tools/issue-creator.config.json` for configured area labels.

Common area patterns:
- **Game projects**: `area:job-system`, `area:drone-ai`, `area:buildings`, `area:ui`
- **Web projects**: `area:frontend`, `area:backend`, `area:api`, `area:database`
- **Library projects**: `area:core`, `area:utils`, `area:docs`, `area:tests`

---

**Ready?** Begin **Step 1: Ask user for spec file path**.
