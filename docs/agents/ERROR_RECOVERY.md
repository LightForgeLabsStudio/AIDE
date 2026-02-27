# Error Recovery Playbook

Use when implementation hits a failure mode: tests failing, git conflicts, CI breakage, or scope pivots.

**Goals:** restore a known-good state quickly; keep changes reviewable; escalate when the decision is ambiguous.

## Default Recovery Loop

1. **Stop the bleed** — pause new coding; capture failing command + exact error text + current branch/commit.
2. **Return to stable base** — choose: fix forward, revert, or stash and branch. Prefer the smallest restoring change.
3. **Reduce to a minimal reproducer** — isolate the failing test/command before running full suites.
4. **Fix systematically** — one hypothesis at a time; keep commits small; don't mix refactors with fixes.
5. **Re-validate** — re-run the minimal reproducer, then the project's standard quality gates.

## When to Escalate

Pause and ask the user when any of these are true:

- Multiple plausible approaches with real tradeoffs (architecture/UX decisions)
- Fix requires changing Tier 1 rules, public APIs, or core workflow expectations
- Fix would modify existing tests
- The failure suggests the spec is wrong or success criteria changed
- The change would touch many files, introduce a new pattern, or expand scope

Do **not** escalate for mechanical tasks (formatting, obvious typos, trivial conflicts).

## Failure Mode Quick Reference

**Tests fail locally:** Run smallest scope first; copy only the *first* failure. Escalate if fix requires changing existing tests.

**CI fails, local passes:** Compare CI command vs local (versions, OS, paths, flags). Escalate if fix changes CI policy or project-wide tooling.

**Git conflicts:** Identify cause (upstream refactor, concurrent edits); rebase frequently rather than accumulating. Escalate if correct merge behavior for spec-critical areas is unclear.

**Scope pivot:** Restate new goal/scope/criteria; choose extend PR or new branch. Escalate if pivot contradicts design pillars or Tier 1 rules.

**Spec gap mid-implementation:** Use `AGENT_COLLABORATION.md` decision tree. Escalate (Scenario A) if spec is unimplementable without a design decision.

## Handy Commands

```bash
git status -sb          # Current state
git log -1 --oneline    # Last commit
git diff                # What changed
git rebase --continue   # After resolving conflict
git rebase --abort      # To abandon rebase
```
