# Issue Creator Reference

Batch-create GitHub issues from formatted spec files.
Tool: `.aide/tools/issue-creator/issue-creator.py` | Full docs: `.aide/tools/issue-creator/README.md`

## Spec File Format

```markdown
## [Epic]: Epic Title
### Goal
Description
### Success Criteria
- Criterion 1
---
## [Feature]: Issue Title
priority: high|medium|low
area: system-name
blocked_by: Other Issue Title
### Goal
What this delivers
### Success Criteria
- Measurable criterion
---
```

**Types:** `[Epic]` `[Feature]` `[Bug]` `[Tech Debt]` `[Documentation]` `[Chore]`
**Rules:** `---` is section separator only (not inside sections). Success criteria = plain `- bullets` (no checklists).

## Commands

```bash
python .aide/tools/issue-creator/issue-creator.py specs.md            # create
python .aide/tools/issue-creator/issue-creator.py specs.md --update 171       # update single
python .aide/tools/issue-creator/issue-creator.py specs.md --update-epic 170  # update epic+children
python .aide/tools/issue-creator/issue-creator.py specs.md --update-auto      # via issue_number field
python .aide/tools/issue-creator/issue-creator.py --link-child 227:232        # PARENT:CHILD
python .aide/tools/issue-creator/issue-creator.py --link-blocker 232:231      # BLOCKED:BLOCKER
```

## Common Errors

**Label not found**: Create missing label then re-run:
```bash
gh label create "Epic" --description "Parent issue" --color "7057ff"
gh label create "area:combat" --description "Combat" --color "c5def5"
```

**UnicodeDecodeError** (curly quotes from ChatGPT):
```bash
iconv -f UTF-16 -t UTF-8 specs.md -o specs-utf8.md
```
