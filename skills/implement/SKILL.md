---
name: implement
description: Implement a ticket, validate, and deliver a draft PR for review. Apply accepted PR findings on the same branch.
---

# Implement

Read the consuming project's root AGENTS.md and any workflow document it names (convention: `docs/agents/workflow.md`, relative to the project root). Resolve required commands there before acting; report missing configuration instead of guessing or skipping a gate. User instructions and project constraints govern the workflow. Resolve `MAIN_BRANCH` (default `main`), the full validation command (`VALIDATE_COMMAND` or `RUN_ALL_TESTS_COMMAND`), and `REVIEW_MODE` (`external` by default; `independent-agent` only when selected by the project or user).

## Inputs

A ticket, pasted requirements, or an existing PR with accepted findings. Tickets can be the complete decision source; create a spec only when the project requires one. Read the ticket and its comments, plus any existing findings file.

## Before code

1. Confirm goal, success criteria and scope from the available requirements. Ask only for missing decisions.
2. State a narrow two-layer plan: applicable project constraints (at most eight bullets), then steps with checkable exit criteria. Name the files to inspect.
3. Record the base branch and starting commit. Create a feature branch before implementation when currently on the base branch; use an isolated worktree if another task owns the checkout. Preserve unrelated changes. For an existing PR, use its head branch. Explicit user authorization or a project path-specific exception can allow work on the base branch; a notes-only exception never applies to code.

## Implement and validate

- Keep the diff within the accepted scope. Follow the project's test policy, including any approval requirement for changing existing tests. Without a project test policy, do not modify existing tests without explicit user approval.
- Run focused checks as needed, then the configured full validation command once on the final implementation. Run a separate lint command only when full validation does not include it.
- If validation fails, compare with the base branch and inspect the full PR range before attributing it. Fix branch-owned failures; report proven baseline failures precisely.
- Re-read the current ticket and comments before delivery. Account for every acceptance criterion with implementation and evidence, or mark it unresolved. Automated checks, inspected visual evidence and human play acceptance are distinct results.

## Deliver for review

1. Inspect the final diff and status, then commit only this task's changes. Review tools comparing committed HEAD must run after this commit.
2. Push the feature branch and follow [pr-draft](../pr-draft/SKILL.md) to create or update its draft PR. Keep the description aligned with the current scope and outstanding acceptance work. Do not close the ticket or merge the PR as part of implementation.
3. Record the PR URL, head SHA and current CI status. In **external** review mode, return this handoff:

   ```text
   Review <PR URL> at head <full SHA> against <ticket(s)> using pr-review.
   Read the project root AGENTS.md and its linked workflow document; post findings through the configured review command.
   If the head changed, review the new complete head and state its SHA.
   ```

   The configured external reviewer (for example Claude) owns that pass. Do not substitute the implementation agent's own review or wait indefinitely for another session. In **independent-agent** mode, use a separate review agent only when configured or requested; include the pinned head and ticket. A report is not a submitted GitHub review.
4. Report what was delivered, acceptance gaps, CI status and the review handoff. Green checks alone do not imply approval.

## Accepted review findings

When asked to address a PR's findings, read all reviews, threads and relevant comments at its current head. Resolve the accepted items on the same branch, preserve behavioral coverage, revalidate, commit and push. Update the PR description and return a fresh head-specific handoff. Previous approval does not establish review of new commits. Merge only on explicit user instruction after checking the current head, CI and review state.
