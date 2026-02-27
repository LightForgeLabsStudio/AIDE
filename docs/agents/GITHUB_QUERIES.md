# GitHub Queries Reference

Query GitHub state dynamically. CLI queries (~200 tokens) vs reading snapshot docs (~8,000+ tokens).

## Quick Reference

```bash
# Current work and pipeline
gh issue list --label "status:in-progress" --state open
gh issue list --label "status:ready" --state open
gh pr list --state open
gh pr list --state merged --limit 10

# By epic or area
gh issue list --label "Epic" --state open
gh issue list --label "area:combat" --state open

# View issue with spec + discussion
gh issue view <number> --comments
```

## Auto-Detect Owner/Repo

```bash
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
```

## Sub-Issues (Epic/Child Hierarchy)

```bash
# Get IDs for parent and child issues
gh api graphql -f query='{
  repository(owner: "OWNER", name: "REPO") {
    parent: issue(number: 116) { id }
    child: issue(number: 117) { id }
  }
}'

# Link child to parent
gh api graphql -f query='
mutation {
  addSubIssue(input: { issueId: "PARENT_ID" subIssueId: "CHILD_ID" }) {
    issue { number }
  }
}'
```

## References

- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub CLI manual](https://cli.github.com/manual/)
