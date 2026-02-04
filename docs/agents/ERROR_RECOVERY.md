# Error Recovery Playbook

Use this playbook when an implementation session hits a failure mode (tests failing, git conflicts, CI breakage, or scope pivots).

Goals:
- Restore a **known-good** state quickly.
- Keep changes **reviewable** and aligned with the spec.
- Escalate to the user when the decision is ambiguous, risky, or non-mechanical.

## Default Recovery Loop (Works for Most Cases)

1) **Stop the bleed**
- Pause new coding.
- Capture context: failing command + exact error text + current branch/commit.

2) **Return to a stable base**
- Decide whether to: fix forward, revert, or stash and branch.
- Prefer the smallest change that restores correctness.

3) **Reduce to a minimal reproducer**
- Isolate the failing test / command.
- If possible, reproduce locally with the smallest scope before running full suites.

4) **Fix systematically**
- One hypothesis at a time.
- Keep commits small; avoid mixing refactors with fixes.

5) **Re-validate**
- Re-run the minimal reproducer.
- Then run the project’s standard quality gates (lint/tests).

## When to Escalate to the User

Escalate (pause and ask) when any of these are true:
- Multiple plausible approaches with tradeoffs (design/architecture/UX decisions).
- Fix requires changing Tier 1 rules, public APIs, or core workflow expectations.
- Fix would modify existing tests (unless the project explicitly allows it).
- The failure suggests the spec is wrong/incomplete or the success criteria changed.
- The change would touch many files, introduce a new pattern, or expand scope.

Do not escalate for mechanical tasks (formatting, trivial conflicts, obvious typos) unless the project’s rules require it.

## Failure Modes

### 1) Tests fail locally

Checklist:
- Confirm you ran the right scope (unit vs integration vs full suite).
- Copy the *first* failure and error text; ignore cascades until the first is fixed.
- Check for warnings-as-errors and type issues (common in strict pipelines).

Fix approach:
- Make the smallest change to restore correctness.
- If the failure is unrelated to your changes, document it and ask whether to proceed or file a follow-up issue.

Escalate if:
- The fix requires changing existing tests or changing behavior beyond the spec.

### 2) CI fails but local passes

Checklist:
- Identify the CI job and its exact command (version, OS, environment).
- Look for: line endings, path case-sensitivity, missing generated files, tool version mismatches.
- Compare what CI runs vs what you ran locally (scripts, flags, working directory).

Fix approach:
- Prefer changes that improve determinism (pin versions, use repo-root paths, avoid environment assumptions).
- If CI uses a stricter configuration, align local reproduction to that strict mode first.

Escalate if:
- Fix requires changing CI policy or project-wide tooling expectations.

### 3) Git conflicts / rebase pain

Checklist:
- Identify conflict cause: upstream refactor, file moves, or concurrent edits.
- Prefer rebasing frequently rather than resolving one massive conflict at the end.

Fix approach:
- Resolve conflicts by preserving intended behavior, not by “making it compile”.
- After resolving, re-run the smallest relevant tests to ensure no silent behavior drift.

Escalate if:
- Conflicts affect spec-critical areas and the correct merge behavior is unclear.

### 4) Mid-implementation scope pivot

Checklist:
- Restate new request in terms of: goal, scope, success criteria.
- Determine whether it is: (a) same feature extension, (b) new feature, (c) separate bugfix.

Fix approach:
- If it increases review complexity, split into a follow-up issue/PR.
- Update plan/checklist to reflect the new scope.

Escalate if:
- The pivot contradicts design pillars, Tier 1 rules, or requires a new architecture decision.

## Handy Commands (Generic)

- Show current state: `git status -sb`, `git log -1 --oneline`
- Find regressions: `git diff`, `git show`, `git blame`
- Conflict help: `git rebase --continue`, `git rebase --abort`, `git mergetool` (if configured)

