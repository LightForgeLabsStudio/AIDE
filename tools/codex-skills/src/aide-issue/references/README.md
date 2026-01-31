# AIDE Issue Skill References

Creates issues via `gh issue create` using standard label fields:

- Issue Type is set via GitHub Issue Types (not labels): `feature` | `bug` | `technical-debt` | `chore` | `documentation` | `research` | `epic`
- Priority: `priority:critical|high|medium|low`
- Area: `area:<name>`
- Status: `status:needs-spec|status:ready|status:in-progress`

If the target repo uses different label naming, adjust before using.

