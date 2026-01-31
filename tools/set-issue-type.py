#!/usr/bin/env python3
"""
Set GitHub Issue Type for an existing issue.

Usage:
  python .aide/tools/set-issue-type.py --issue 123 --type bug
"""

import argparse
import json
import subprocess
from pathlib import Path


DEFAULT_CONFIG = {
    "issue_type_mapping": {
        "epic": "Epic",
        "feature": "Feature",
        "bug": "Bug",
        "technical-debt": "Technical Debt",
        "chore": "Chore",
        "documentation": "Documentation",
        "research": "Research",
    }
}


def _run_gh_graphql(query: str) -> dict:
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"],
        capture_output=True,
        text=True,
        check=True,
    )
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON from gh api graphql: {exc}") from exc

    errors = payload.get("errors")
    if errors:
        raise SystemExit(f"GraphQL errors: {errors}")

    return payload


def _resolve_repo_root() -> Path:
    """
    Resolve the repo root for gh commands.

    This script often lives inside a git submodule (e.g. `.aide/`). If it is
    executed from within the submodule directory, `gh repo view` will resolve
    the *submodule* repository instead of the superproject. We prefer the
    superproject when available.
    """
    try:
        superproject = subprocess.run(
            ["git", "rev-parse", "--show-superproject-working-tree"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if superproject:
            return Path(superproject)
    except subprocess.CalledProcessError:
        pass

    try:
        toplevel = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if toplevel:
            return Path(toplevel)
    except subprocess.CalledProcessError:
        pass

    return Path.cwd()


def load_config():
    config_paths = [
        Path("issue-creator.config.json"),
        Path(".aide/issue-creator.config.json"),
        Path(".aide/tools/issue-creator.config.json"),
    ]
    for path in config_paths:
        if path.exists():
            with open(path) as f:
                user_config = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            return config
    return DEFAULT_CONFIG


def normalize_type(raw_type: str) -> str:
    value = raw_type.strip().lower()
    allowed = {
        "feature",
        "bug",
        "technical-debt",
        "chore",
        "documentation",
        "research",
        "epic",
    }
    if value not in allowed:
        raise SystemExit(
            "Invalid issue type '{0}'. Allowed values: feature, bug, technical-debt, "
            "chore, documentation, research, epic.".format(value)
        )
    return value


def get_repo_info():
    repo_root = _resolve_repo_root()
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "owner,name"],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )
    data = json.loads(result.stdout)
    return data["owner"]["login"], data["name"]


def get_issue_id(owner: str, repo: str, issue_num: int) -> str:
    query = f'''{{
      repository(owner: "{owner}", name: "{repo}") {{
        issue(number: {issue_num}) {{
          id
        }}
      }}
    }}'''
    data = _run_gh_graphql(query)
    issue_id = data.get("data", {}).get("repository", {}).get("issue", {}).get("id")
    if not issue_id:
        raise SystemExit(f"Could not resolve issue id for #{issue_num} in {owner}/{repo}.")
    return issue_id


def get_issue_types(owner: str) -> dict:
    query = f'''{{
      organization(login: "{owner}") {{
        issueTypes(first: 25) {{
          nodes {{
            id
            name
          }}
        }}
      }}
    }}'''
    data = _run_gh_graphql(query)
    org = data.get("data", {}).get("organization")
    if not org:
        raise SystemExit(
            f"Could not query issueTypes for organization '{owner}'. "
            "Is this repository owned by an org with Issue Types enabled?"
        )
    types = org.get("issueTypes", {}).get("nodes", [])
    return {t["name"]: t["id"] for t in types}


def set_issue_type(owner: str, repo: str, issue_num: int, issue_type: str, mapping: dict):
    type_name = mapping.get(issue_type)
    if not type_name:
        raise SystemExit(
            "Unknown issue type '{0}'. Allowed values: feature, bug, technical-debt, "
            "chore, documentation, research, epic.".format(issue_type)
        )
    issue_types = get_issue_types(owner)
    type_id = issue_types.get(type_name)
    if not type_id:
        raise SystemExit(f"Issue type '{type_name}' not found in org.")
    issue_id = get_issue_id(owner, repo, issue_num)
    mutation = f'''mutation {{
      updateIssueIssueType(input: {{
        issueId: "{issue_id}"
        issueTypeId: "{type_id}"
      }}) {{
        issue {{
          number
          issueType {{ name }}
        }}
      }}
    }}'''
    data = _run_gh_graphql(mutation)
    actual_type = (
        data.get("data", {})
        .get("updateIssueIssueType", {})
        .get("issue", {})
        .get("issueType", {})
        .get("name")
    )
    if actual_type != type_name:
        raise SystemExit(
            f"Failed to set issue type on #{issue_num}: expected '{type_name}', got '{actual_type}'."
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument("--type", required=True)
    args = parser.parse_args()

    config = load_config()
    issue_type = normalize_type(args.type)
    owner, repo = get_repo_info()
    set_issue_type(owner, repo, args.issue, issue_type, config["issue_type_mapping"])


if __name__ == "__main__":
    main()
