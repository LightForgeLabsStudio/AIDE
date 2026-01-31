#!/usr/bin/env python3
"""
Migrate away from legacy label-based issue "type" labels by:
1) Setting GitHub Issue Type (if missing) based on legacy type labels
2) Removing legacy type labels from issues

This tool is intentionally explicit: it defaults to dry-run and requires --apply.

Usage:
  python .aide/tools/migrate-type-labels.py --state all
  python .aide/tools/migrate-type-labels.py --state all --apply
  python .aide/tools/migrate-type-labels.py --repo OWNER/REPO --state open --apply --limit 200
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_ISSUE_TYPE_MAPPING = {
    # Issue Type keys (normalized) -> GitHub Issue Type display name
    "epic": "Epic",
    "feature": "Feature",
    "bug": "Bug",
    "technical-debt": "Technical Debt",
    "chore": "Chore",
    "documentation": "Documentation",
    "research": "Research",
}

# Legacy labels that represented issue type (deprecated).
LEGACY_TYPE_LABEL_TO_ISSUE_TYPE_KEY = {
    "bug": "bug",
    "enhancement": "feature",
    "technical-debt": "technical-debt",
    "documentation": "documentation",
    "testing": "chore",
    "chore": "chore",
}


@dataclass(frozen=True)
class Issue:
    number: int
    issue_id: str
    issue_type_name: Optional[str]
    labels: Dict[str, str]  # name -> id


def _run_gh(args: List[str]) -> str:
    p = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if p.returncode != 0:
        stderr = (p.stderr or "").strip()
        stdout = (p.stdout or "").strip()
        raise RuntimeError(f"gh {' '.join(args)} failed ({p.returncode}).\n{stderr}\n{stdout}".strip())
    return p.stdout


def _get_repo_owner_and_name(repo_override: Optional[str]) -> Tuple[str, str]:
    if repo_override:
        owner, name = repo_override.split("/", 1)
        return owner, name
    out = _run_gh(["repo", "view", "--json", "owner,name"])
    data = json.loads(out)
    return data["owner"]["login"], data["name"]


def _get_issue_types(owner: str) -> Dict[str, str]:
    query = f"""
query {{
  organization(login: "{owner}") {{
    issueTypes(first: 100) {{
      nodes {{ id name }}
    }}
  }}
}}
""".strip()
    out = _run_gh(["api", "graphql", "-f", f"query={query}"])
    data = json.loads(out)
    org = data.get("data", {}).get("organization")
    if not org:
        raise RuntimeError(
            f"Failed to query organization issue types for owner '{owner}'. "
            "Ensure the repo owner is an organization and Issue Types are enabled."
        )
    nodes = org["issueTypes"]["nodes"]
    return {n["name"]: n["id"] for n in nodes}


def _iter_issues(owner: str, repo: str, state: str) -> Iterable[Issue]:
    states = {"open": ["OPEN"], "closed": ["CLOSED"], "all": ["OPEN", "CLOSED"]}[state]
    cursor: Optional[str] = None

    while True:
        after = f', after: "{cursor}"' if cursor else ""
        query = f"""
query {{
  repository(owner: "{owner}", name: "{repo}") {{
    issues(first: 100{after}, states: [{", ".join(states)}], orderBy: {{field: CREATED_AT, direction: ASC}}) {{
      nodes {{
        number
        id
        issueType {{ name }}
        labels(first: 100) {{ nodes {{ id name }} }}
      }}
      pageInfo {{ hasNextPage endCursor }}
    }}
  }}
}}
""".strip()
        out = _run_gh(["api", "graphql", "-f", f"query={query}"])
        data = json.loads(out)
        conn = data["data"]["repository"]["issues"]

        for n in conn["nodes"]:
            labels = {ln["name"]: ln["id"] for ln in n["labels"]["nodes"]}
            issue_type = n["issueType"]["name"] if n.get("issueType") else None
            yield Issue(
                number=int(n["number"]),
                issue_id=n["id"],
                issue_type_name=issue_type,
                labels=labels,
            )

        page = conn["pageInfo"]
        if not page["hasNextPage"]:
            return
        cursor = page["endCursor"]


def _set_issue_type(issue_id: str, issue_type_id: str) -> None:
    mutation = f"""
mutation {{
  updateIssueIssueType(input: {{
    issueId: "{issue_id}",
    issueTypeId: "{issue_type_id}"
  }}) {{
    issue {{ number issueType {{ name }} }}
  }}
}}
""".strip()
    _run_gh(["api", "graphql", "-f", f"query={mutation}"])


def _remove_labels(issue_id: str, label_ids: List[str]) -> None:
    if not label_ids:
        return
    label_list = ", ".join([f"\"{lid}\"" for lid in label_ids])
    mutation = f"""
mutation {{
  removeLabelsFromLabelable(input: {{
    labelableId: "{issue_id}",
    labelIds: [{label_list}]
  }}) {{
    clientMutationId
  }}
}}
""".strip()
    _run_gh(["api", "graphql", "-f", f"query={mutation}"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="owner/repo override (default: current repo)")
    parser.add_argument("--state", choices=["open", "closed", "all"], default="all")
    parser.add_argument("--limit", type=int, default=0, help="Max issues to process (0 = no limit)")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    args = parser.parse_args()

    owner, repo = _get_repo_owner_and_name(args.repo)
    issue_types = _get_issue_types(owner)

    # Build mapping from Issue Type key -> ID, based on display names.
    issue_type_key_to_id: Dict[str, str] = {}
    for key, display_name in DEFAULT_ISSUE_TYPE_MAPPING.items():
        if display_name in issue_types:
            issue_type_key_to_id[key] = issue_types[display_name]

    missing_types = [k for k, v in DEFAULT_ISSUE_TYPE_MAPPING.items() if v not in issue_types]
    if missing_types:
        print(
            "[WARN] Missing configured Issue Types in org: "
            + ", ".join([DEFAULT_ISSUE_TYPE_MAPPING[k] for k in missing_types]),
            file=sys.stderr,
        )

    planned_set = 0
    planned_remove = 0
    skipped_multi = 0
    processed = 0

    for issue in _iter_issues(owner, repo, args.state):
        processed += 1
        if args.limit and processed > args.limit:
            break

        legacy_labels = [name for name in issue.labels.keys() if name in LEGACY_TYPE_LABEL_TO_ISSUE_TYPE_KEY]
        if not legacy_labels:
            continue

        # Remove all legacy type labels regardless (post-migration policy).
        remove_label_ids = [issue.labels[name] for name in legacy_labels]

        # Set issue type only if missing.
        desired_key: Optional[str] = None
        if issue.issue_type_name is None:
            if len(legacy_labels) != 1:
                skipped_multi += 1
                print(
                    f"[SKIP] #{issue.number}: multiple legacy type labels present: {', '.join(legacy_labels)}",
                    file=sys.stderr,
                )
            else:
                desired_key = LEGACY_TYPE_LABEL_TO_ISSUE_TYPE_KEY[legacy_labels[0]]

        do_set = desired_key is not None and desired_key in issue_type_key_to_id
        do_remove = len(remove_label_ids) > 0

        if do_set:
            planned_set += 1
        if do_remove:
            planned_remove += 1

        if not args.apply:
            parts: List[str] = []
            if do_set:
                parts.append(f"set Issue Type -> {DEFAULT_ISSUE_TYPE_MAPPING[desired_key]}")
            parts.append(f"remove labels -> {', '.join(legacy_labels)}")
            print(f"[DRY-RUN] #{issue.number}: " + "; ".join(parts))
            continue

        if do_set:
            _set_issue_type(issue.issue_id, issue_type_key_to_id[desired_key])
            print(f"[OK] #{issue.number}: set Issue Type -> {DEFAULT_ISSUE_TYPE_MAPPING[desired_key]}")

        _remove_labels(issue.issue_id, remove_label_ids)
        print(f"[OK] #{issue.number}: removed labels -> {', '.join(legacy_labels)}")

    if not args.apply:
        print(
            f"[DRY-RUN] Planned: set issue types={planned_set}, remove legacy labels={planned_remove}, "
            f"skipped_multi_label={skipped_multi}",
            file=sys.stderr,
        )
        print("[DRY-RUN] Re-run with --apply to execute.", file=sys.stderr)
    else:
        print(
            f"[DONE] Updated issues: set issue types={planned_set}, removed legacy labels={planned_remove}, "
            f"skipped_multi_label={skipped_multi}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

