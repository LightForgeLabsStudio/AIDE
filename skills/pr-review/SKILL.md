---
name: pr-review
description: Review a PR against its current ticket and project constraints, then submit findings for the reviewed commit. No code changes.
---

# PR Review

Read the consuming project's root AGENTS.md and any workflow document it names (convention: `docs/agents/workflow.md`, relative to the project root). Resolve required commands there before acting; report missing configuration instead of guessing or skipping a gate. User instructions and project constraints govern the workflow. Resolve the reviewer identity and `REVIEW_COMMAND` from those sources. The reviewer can run in a different tool or session from the implementer; GitHub holds the shared review record.

## Inputs

A PR URL or number, optionally an expected head SHA and particular concerns. Respect any user request to discuss findings before submitting.

## Workflow

1. **Pin the head.** Load the PR's URL, author, base/head SHAs, draft state, checks and review decision. Compare with the handoff's expected SHA. If it changed, review the complete new head and clearly report that SHA. Inspect the full diff against the base; on re-review, recheck original findings and all new changes.
2. **Load requirements.** Read linked tickets and their current comments, project constraints and the test policy. Tickets may be the entire decision source; a separate spec is not required unless the project requires it.
3. **Review.** Account for every acceptance criterion. Identify missing behavior, wrong behavior, scope creep, architecture violations and weak evidence. Check that tests exercise the intended behavior and that claimed visual evidence was inspected. Separate mechanical checks from judgment calls. Compare red checks with the base and the full PR range before calling a failure pre-existing.
4. **Report.** Group findings by severity with file/line references and supporting requirement or observed behavior. State approve, request changes, or comment, and include the reviewed full SHA. Discuss uncertain evidence or disputed scope when user input could change the decision; routine reviews and re-reviews with a clear decision proceed to submission without another confirmation. Distinguish automation from visual inspection and human acceptance.
5. **Submit.** Recheck the head immediately before posting. If it changed, refresh the review; never approve an unreviewed head. Use the project's configured review command and a body file. Pass the reviewed SHA when the command supports it. Verify the resulting review's author, commit and decision. The reviewer must not be the PR author. Leave the shared machine's active GitHub account unchanged: use a process-scoped reviewer credential or configured wrapper. If neither is available, report the missing setup without switching the shared account.
6. **Return the handoff.** Give the review URL, reviewed SHA, decision and unresolved findings. Make no code changes and do not merge. The implementer can read the posted review in another session and return a new head for re-review.
