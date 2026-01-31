#!/usr/bin/env python3
"""
Issue Creator - Batch create GitHub issues with Epic/child relationships

Part of the AIDE framework. Project-specific config in issue-creator.config.json

Usage:
    ./issue-creator.py spec.md                    # Create new issues
    ./issue-creator.py spec.md --update 171       # Update issue #171
    ./issue-creator.py spec.md --update-epic 170  # Update Epic #170 + children
    ./issue-creator.py --help                     # Show help
"""

import sys
import os
import json
import re
import subprocess
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class IssueSpec:
    title: str
    body: str
    priority: str = "medium"
    areas: List[str] = field(default_factory=list)
    is_epic: bool = False
    issue_type: str = "feature"  # epic, feature, bug, technical-debt, chore, documentation, research
    parent_title: Optional[str] = None
    blocks: List[str] = field(default_factory=list)
    blocked_by: List[str] = field(default_factory=list)
    issue_number: Optional[int] = None  # For update mode

class IssueCreator:
    DEFAULT_CONFIG = {
        "area_keywords": {},
        "default_priority": "medium",
        "default_status_ready": "status:ready",
        "epic_label": "Epic",
        "issue_type_mapping": {
            "epic": "Epic",
            "feature": "Feature",
            "bug": "Bug",
            "technical-debt": "Technical Debt",
            "chore": "Chore",
            "documentation": "Documentation",
            "research": "Research"
        }
    }

    def __init__(self):
        self.config = self._load_config()
        self.repo_info = self._get_repo_info()
        self.issue_types = self._get_issue_types()
        self.created_issues = {}

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Normalize headings like 'Issue: [Feature] Foo' to '[Feature] Foo'."""
        value = title.strip()
        if value.lower().startswith("issue:"):
            value = value[6:].lstrip()
        if value.startswith("[") and "]:" in value:
            tag, rest = value.split("]:", 1)
            value = f"{tag}]{rest}".strip()
        return value

    def _format_title(self, title: str, issue_type: str) -> str:
        """Return the final GitHub title (epics get the prefix)."""
        return f"[Epic]: {title}" if issue_type == "epic" else title

    def format_issue_title(self, spec: IssueSpec) -> str:
        """Return the formatted title for a spec."""
        return self._format_title(spec.title, spec.issue_type)

    def find_issue_by_title(self, title: str) -> Optional[int]:
        """Return an existing issue number by exact title (searches open+closed)."""
        if not title:
            return None

        result = subprocess.run(
            ['gh', 'issue', 'list', '--state', 'all', '--search', title,
             '--json', 'number,title', '--limit', '100'],
            capture_output=True, text=True, encoding='utf-8', check=True
        )
        issues = json.loads(result.stdout)

        normalized = title.strip()
        for issue in issues:
            if issue['title'].strip() == normalized:
                return issue['number']
        return None

    def ensure_labels(self, labels: List[str]):
        """Ensure labels exist in the repo before creating issues."""
        result = subprocess.run(
            ['gh', 'label', 'list', '--json', 'name'],
            capture_output=True, text=True, check=True
        )
        existing = {label['name'] for label in json.loads(result.stdout)}
        missing = [label for label in labels if label not in existing]

        for label in missing:
            description = "Auto-created by issue-creator"
            color = "c5def5"
            if label == self.config.get('epic_label'):
                description = "Parent issue grouping related work"
                color = "7057ff"
            elif label.startswith("priority:"):
                color = "fbca04"
            elif label.startswith("status:"):
                color = "0e8a16"

            subprocess.run(
                ['gh', 'label', 'create', label, '--description', description, '--color', color],
                capture_output=True, text=True
            )

    def labels_for_spec(self, spec: IssueSpec) -> List[str]:
        """Compute labels the tool will apply for a spec."""
        labels = []
        if spec.issue_type == "epic":
            labels.append(self.config['epic_label'])
        labels.append(f'priority:{spec.priority}')
        for area in spec.areas:
            labels.append(f'area:{area}')
        labels.append(self.config['default_status_ready'])
        return labels

    def ensure_labels_for_specs(self, specs: List[IssueSpec]):
        """Preflight and create any labels needed for specs."""
        label_set = set()
        for spec in specs:
            label_set.update(self.labels_for_spec(spec))
        self.ensure_labels(sorted(label_set))

    def _load_config(self) -> Dict:
        """Load project-specific config, fall back to defaults"""
        # Look for config in project root, then .aide/ directory
        config_paths = [
            Path('issue-creator.config.json'),  # Project root (recommended)
            Path('.aide/issue-creator.config.json'),
            Path('.aide/tools/issue-creator.config.json'),
        ]

        for path in config_paths:
            if path.exists():
                with open(path) as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(user_config)
                    print(f"[OK] Loaded config from {path}", file=sys.stderr)
                    return config

        print("[WARN] No config found, using defaults (no area inference)", file=sys.stderr)
        print("  Create issue-creator.config.json in project root to customize", file=sys.stderr)
        return self.DEFAULT_CONFIG

    def _get_repo_info(self) -> Dict[str, str]:
        """Get owner and repo from gh CLI"""
        result = subprocess.run(
            ['gh', 'repo', 'view', '--json', 'owner,name'],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        return {
            'owner': data['owner']['login'],
            'repo': data['name']
        }

    def _get_issue_types(self) -> Dict[str, str]:
        """Query org issue types and return name->ID mapping"""
        query = f'''{{
          organization(login: "{self.repo_info['owner']}") {{
            issueTypes(first: 100) {{
              nodes {{
                id
                name
              }}
            }}
          }}
        }}'''

        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={query}'],
            capture_output=True, text=True, check=True
        )

        data = json.loads(result.stdout)
        types = data['data']['organization']['issueTypes']['nodes']
        return {t['name']: t['id'] for t in types}

    def infer_areas(self, text: str) -> List[str]:
        """Infer area labels from content using config keywords"""
        if not self.config.get('area_keywords'):
            return []

        text_lower = text.lower()
        areas = set()

        for area, keywords in self.config['area_keywords'].items():
            if any(kw in text_lower for kw in keywords):
                areas.add(area)

        return sorted(areas)

    def check_for_checklists(self, content: str) -> List[str]:
        """Check for checklist patterns and return warnings"""
        warnings = []
        checklist_pattern = re.compile(r'^(\s*)-\s*\[\s*\]', re.MULTILINE)
        matches = checklist_pattern.findall(content)

        if matches:
            count = len(re.findall(r'-\s*\[\s*\]', content))
            warnings.append(
                f"[WARN] Found {count} checklist item(s) '- [ ]' in spec.\n"
                f"       Issues should use plain bullets '- item', not checklists.\n"
                f"       Checklists belong in PRs (progress tracking), not Issues (descriptive).\n"
                f"       The tool will proceed, but consider fixing the spec format."
            )
        return warnings

    def parse_spec_file(self, content: str) -> List[IssueSpec]:
        """Parse spec file into IssueSpec objects"""
        specs = []
        sections = re.split(r'\n(?:---+|##\s+Issue:)\s*\n', content)
        current_epic = None

        for section in sections:
            if not section.strip():
                continue

            is_epic = '[Epic]' in section or 'Epic:' in section
            if not is_epic:
                if re.search(r'\[(Bug|Feature|Tech Debt|Technical Debt|Chore|Documentation|Docs|Research)\]', section):
                    raise ValueError("Non-epic title markers are not allowed. Use 'type: <value>' metadata instead.")

            issue_type = "feature"  # default
            type_match = re.search(r'^type:\s*(.+?)$', section, re.MULTILINE | re.IGNORECASE)
            if type_match:
                raw_type = type_match.group(1).strip().lower()
                type_map = {
                    "feature": "feature",
                    "bug": "bug",
                    "technical-debt": "technical-debt",
                    "chore": "chore",
                    "documentation": "documentation",
                    "research": "research",
                }
                issue_type = type_map.get(raw_type, raw_type)

            title_match = re.search(
                r'^#+\s*(?:\[(?:Epic|Bug|Tech Debt|Technical Debt|Feature|Chore|Documentation|Docs|Research)\]:?\s*)?(.+?)$',
                section, re.MULTILINE
            )
            if not title_match:
                continue

            title = self._normalize_title(title_match.group(1).strip())
            if is_epic:
                issue_type = "epic"
            elif not type_match:
                raise ValueError(f"Missing required type for issue '{title}'. Add 'type: <value>' metadata.")
            elif issue_type not in (
                "feature", "bug", "technical-debt", "chore", "documentation", "research"
            ):
                raise ValueError(
                    f"Invalid issue type '{issue_type}' for '{title}'. "
                    "Allowed values: feature, bug, technical-debt, chore, documentation, research."
                )

            # Extract fields
            priority_match = re.search(r'^priority:\s*(\w+)', section, re.MULTILINE | re.IGNORECASE)
            priority = priority_match.group(1) if priority_match else self.config['default_priority']

            area_match = re.search(r'^area:\s*(.+?)$', section, re.MULTILINE | re.IGNORECASE)
            explicit_areas = [a.strip() for a in area_match.group(1).split(',')] if area_match else []

            blocks_match = re.search(r'^blocks:\s*(.+?)$', section, re.MULTILINE | re.IGNORECASE)
            blocks = [b.strip() for b in blocks_match.group(1).split(',')] if blocks_match else []

            blocked_match = re.search(r'^blocked_by:\s*(.+?)$', section, re.MULTILINE | re.IGNORECASE)
            blocked_by = [b.strip() for b in blocked_match.group(1).split(',')] if blocked_match else []

            issue_num_match = re.search(r'^issue_number:\s*(\d+)', section, re.MULTILINE | re.IGNORECASE)
            issue_number = int(issue_num_match.group(1)) if issue_num_match else None

            # Infer areas from content
            inferred_areas = self.infer_areas(section)
            areas = list(set(explicit_areas + inferred_areas))

            if is_epic:
                current_epic = self._format_title(title, issue_type)

            spec = IssueSpec(
                title=title,
                body=section,
                priority=priority,
                areas=areas,
                is_epic=is_epic,
                issue_type=issue_type,
                parent_title=current_epic if not is_epic else None,
                blocks=blocks,
                blocked_by=blocked_by,
                issue_number=issue_number
            )

            specs.append(spec)

        return specs

    def create_issue(self, spec: IssueSpec) -> int:
        """Create single GitHub issue, returns issue number"""
        labels = []

        if spec.issue_type == "epic":
            labels.append(self.config['epic_label'])

        # Priority
        labels.append(f'priority:{spec.priority}')

        # Areas
        for area in spec.areas:
            labels.append(f'area:{area}')

        # Status
        labels.append(self.config['default_status_ready'])

        # Build title (only Epic gets prefix, others use labels)
        body = spec.body
        title = self.format_issue_title(spec)

        # Create issue via gh CLI
        cmd = [
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
        ]

        for label in labels:
            cmd.extend(['--label', label])

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            print(f"Error creating issue: {result.stderr}", file=sys.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

        # Extract issue number from URL
        url = result.stdout.strip()
        issue_num = int(url.split('/')[-1])

        # Set GitHub issue type
        self.set_issue_type(issue_num, spec.issue_type)

        return issue_num

    def ensure_issue_for_spec(self, spec: IssueSpec) -> Tuple[int, bool]:
        """Create the issue unless it already exists, returning (number, created)."""
        formatted_title = self.format_issue_title(spec)

        if spec.issue_number:
            self.update_issue(spec.issue_number, spec)
            return spec.issue_number, False

        existing = self.find_issue_by_title(formatted_title)
        if existing:
            print(f"[WARN] Issue '{formatted_title}' already exists as #{existing}; updating instead of creating.", file=sys.stderr)
            self.update_issue(existing, spec)
            return existing, False

        issue_num = self.create_issue(spec)
        return issue_num, True

    def get_issue_id(self, issue_num: int) -> str:
        """Get GraphQL node ID for issue number"""
        query = f'''{{
          repository(owner: "{self.repo_info['owner']}", name: "{self.repo_info['repo']}") {{
            issue(number: {issue_num}) {{
              id
            }}
          }}
        }}'''

        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={query}'],
            capture_output=True, text=True, check=True
        )

        data = json.loads(result.stdout)
        return data['data']['repository']['issue']['id']

    def add_child_to_parent(self, parent_num: int, child_num: int):
        """Link child issue to parent epic via addSubIssue mutation"""
        parent_id = self.get_issue_id(parent_num)
        child_id = self.get_issue_id(child_num)

        mutation = f'''mutation {{
          addSubIssue(input: {{
            issueId: "{parent_id}"
            subIssueId: "{child_id}"
          }}) {{
            issue {{
              number
              title
            }}
          }}
        }}'''

        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={mutation}'],
            capture_output=True, text=True, check=False
        )

        if result.returncode != 0:
            print(f"[WARN] Unable to link #{child_num} to #{parent_num}: {result.stderr}", file=sys.stderr)

    def add_blocking_relationship(self, blocked_issue_num: int, blocking_issue_num: int):
        """Add 'blocked by' relationship via addBlockedBy mutation"""
        blocked_id = self.get_issue_id(blocked_issue_num)
        blocking_id = self.get_issue_id(blocking_issue_num)

        mutation = f'''mutation {{
          addBlockedBy(input: {{
            issueId: "{blocked_id}"
            blockingIssueId: "{blocking_id}"
          }}) {{
            issue {{
              number
            }}
            blockingIssue {{
              number
            }}
          }}
        }}'''

        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={mutation}'],
            capture_output=True, text=True, check=False
        )

        if result.returncode != 0:
            print(f"[WARN] Unable to add blocker #{blocking_issue_num} -> #{blocked_issue_num}: {result.stderr}", file=sys.stderr)

    def link_blocker_pair(self, blocked_num: int, blocking_num: int):
        """Explicitly link blocked -> blocking issues."""
        try:
            self.add_blocking_relationship(blocked_num, blocking_num)
            print(f"[OK] Linked #{blocking_num} as blocker of #{blocked_num}")
        except subprocess.CalledProcessError as exc:
            print(f"[ERROR] Failed to link blocker #{blocking_num} -> #{blocked_num}: {exc.stderr}", file=sys.stderr)

    def link_child_pair(self, parent_num: int, child_num: int):
        """Explicitly link child to epic."""
        try:
            self.add_child_to_parent(parent_num, child_num)
            print(f"[OK] Linked #{child_num} as child of Epic #{parent_num}")
        except subprocess.CalledProcessError as exc:
            print(f"[ERROR] Failed to link child #{child_num} to Epic #{parent_num}: {exc.stderr}", file=sys.stderr)

    @staticmethod
    def parse_link_arg(value: str) -> Tuple[int, int]:
        """Parse LINK text 'A:B' into ints."""
        if ':' not in value:
            raise ValueError("Link arguments must use the format A:B")
        left, right = value.split(':', 1)
        return int(left), int(right)

    def set_issue_type(self, issue_num: int, issue_type: str):
        """Set GitHub issue type via updateIssueIssueType mutation"""
        # Get mapped type name from config
        type_name = self.config['issue_type_mapping'].get(issue_type)
        if not type_name:
            return  # No type mapping configured

        # Get type ID from cached org types
        type_id = self.issue_types.get(type_name)
        if not type_id:
            print(f"[WARN] Issue type '{type_name}' not found in org", file=sys.stderr)
            return

        # Get issue GraphQL ID
        issue_id = self.get_issue_id(issue_num)

        mutation = f'''mutation {{
          updateIssueIssueType(input: {{
            issueId: "{issue_id}"
            issueTypeId: "{type_id}"
          }}) {{
            issue {{
              number
              issueType {{
                name
              }}
            }}
          }}
        }}'''

        subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={mutation}'],
            capture_output=True, text=True, check=True
        )

    def infer_type_from_labels(self, labels: List[str]) -> str:
        """Infer issue_type from labels"""
        return 'epic' if self.config['epic_label'] in labels else 'feature'

    def sync_types(self, issue_numbers: List[int]):
        """Sync GitHub issue types based on labels for given issues"""
        print(f"Syncing types for {len(issue_numbers)} issue(s)...")
        print()

        synced_count = 0
        skipped_count = 0

        for issue_num in issue_numbers:
            try:
                # Get current labels
                labels = self.get_current_labels(issue_num)

                # Infer type from labels
                issue_type = self.infer_type_from_labels(labels)
                type_name = self.config['issue_type_mapping'].get(issue_type)

                # Set GitHub issue type
                print(f"#{issue_num}: Setting type to '{type_name}' (from labels: {', '.join(labels)})")
                self.set_issue_type(issue_num, issue_type)
                synced_count += 1

            except Exception as e:
                print(f"[ERROR] Failed to sync #{issue_num}: {e}", file=sys.stderr)
                skipped_count += 1

        print()
        print(f"Summary: Synced {synced_count} issue(s), skipped {skipped_count}")

    def get_current_labels(self, issue_num: int) -> List[str]:
        """Get current labels for an issue"""
        result = subprocess.run(
            ['gh', 'issue', 'view', str(issue_num), '--json', 'labels'],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        return [label['name'] for label in data.get('labels', [])]

    def update_issue(self, issue_num: int, spec: IssueSpec):
        """Update existing GitHub issue"""
        labels = []

        if spec.issue_type == "epic":
            labels.append(self.config['epic_label'])

        # Priority
        labels.append(f'priority:{spec.priority}')

        # Areas
        for area in spec.areas:
            labels.append(f'area:{area}')

        # Status
        labels.append(self.config['default_status_ready'])

        # Build title (only Epic gets prefix, others use labels)
        body = spec.body
        if spec.issue_type == "epic":
            title = f"[Epic]: {spec.title}"
        else:
            title = spec.title

        # Get current labels and preserve custom ones
        current_labels = self.get_current_labels(issue_num)
        managed_prefixes = ('priority:', 'area:', 'status:', 'Epic')
        custom_labels = [l for l in current_labels
                        if not any(l.startswith(p) or l == p
                                  for p in managed_prefixes)]

        # Combine managed labels with custom labels
        all_labels = labels + custom_labels

        # Update issue via gh CLI
        cmd = [
            'gh', 'issue', 'edit', str(issue_num),
            '--title', title,
            '--body', body,
        ]

        # Remove all existing managed labels, then add all labels
        for label in current_labels:
            if any(label.startswith(p) or label == p for p in managed_prefixes):
                cmd.extend(['--remove-label', label])

        for label in all_labels:
            cmd.extend(['--add-label', label])

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            print(f"Error updating issue #{issue_num}: {result.stderr}", file=sys.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

        # Set GitHub issue type
        self.set_issue_type(issue_num, spec.issue_type)

    def get_epic_children(self, epic_num: int) -> List[int]:
        """Get child issue numbers for an Epic"""
        query = f'''{{
          repository(owner: "{self.repo_info['owner']}", name: "{self.repo_info['repo']}") {{
            issue(number: {epic_num}) {{
              trackedIssues(first: 100) {{
                nodes {{
                  number
                }}
              }}
            }}
          }}
        }}'''

        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={query}'],
            capture_output=True, text=True, check=True
        )

        data = json.loads(result.stdout)
        tracked_issues = data['data']['repository']['issue'].get('trackedIssues', {}).get('nodes', [])
        return [issue['number'] for issue in tracked_issues]

    def process_updates(self, specs: List[IssueSpec], update_mode: str, target_issue: Optional[int] = None):
        """Update existing issues"""
        if update_mode == 'single' and target_issue:
            # Update single issue
            spec = specs[0] if specs else None
            if not spec:
                print("No issue spec found in file", file=sys.stderr)
                sys.exit(1)

            print(f"Updating issue #{target_issue}...")
            self.update_issue(target_issue, spec)
            print(f"[OK] Updated #{target_issue}: {spec.title}")

        elif update_mode == 'epic' and target_issue:
            # Update Epic + all children
            epic_spec = next((s for s in specs if s.is_epic), None)
            if not epic_spec:
                print("No Epic found in spec file", file=sys.stderr)
                sys.exit(1)

            print(f"Updating Epic #{target_issue}...")
            self.update_issue(target_issue, epic_spec)
            print(f"[OK] Updated Epic #{target_issue}: {epic_spec.title}")
            print()

            # Get existing children
            children = self.get_epic_children(target_issue)
            child_specs = [s for s in specs if not s.is_epic]

            if len(child_specs) != len(children):
                print(f"[WARN] Spec has {len(child_specs)} children, Epic #{target_issue} has {len(children)} children")
                print(f"  Will update first {min(len(child_specs), len(children))} children")

            # Update children (match by order)
            for i, child_num in enumerate(children):
                if i < len(child_specs):
                    spec = child_specs[i]
                    print(f"Updating child #{child_num}...")
                    self.update_issue(child_num, spec)
                    print(f"  [OK] Updated #{child_num}: {spec.title}")

        elif update_mode == 'auto':
            # Update/create issues based on issue_number field in specs
            updated_count = 0
            created_count = 0
            epic_spec = next((s for s in specs if s.is_epic), None)
            epic_num = epic_spec.issue_number if epic_spec else None

            # First, update Epic if present
            if epic_spec and epic_spec.issue_number:
                print(f"Updating Epic #{epic_spec.issue_number}...")
                self.update_issue(epic_spec.issue_number, epic_spec)
                print(f"[OK] Updated Epic #{epic_spec.issue_number}: {epic_spec.title}")
                print()

            # Then process children
            for spec in specs:
                if spec.is_epic:
                    continue  # Already handled above

                if spec.issue_number:
                    # Update existing issue
                    print(f"Updating issue #{spec.issue_number}...")
                    self.update_issue(spec.issue_number, spec)
                    print(f"[OK] Updated #{spec.issue_number}: {spec.title}")
                    updated_count += 1
                else:
                    # Create new issue
                    print(f"Creating new issue: {spec.title}...")
                    issue_num = self.create_issue(spec)
                    self.created_issues[spec.title] = issue_num
                    print(f"[OK] Created #{issue_num}: {spec.title}")

                    # Link to Epic if present
                    if epic_num:
                        self.add_child_to_parent(epic_num, issue_num)
                        print(f"  [OK] Linked #{issue_num} to Epic #{epic_num}")

                    created_count += 1

            if updated_count == 0 and created_count == 0:
                print("No issues updated or created.", file=sys.stderr)
                sys.exit(1)

            print()
            print(f"Summary: Updated {updated_count}, Created {created_count} issue(s)")

    def process_blockers(self, specs: List[IssueSpec]):
        """Apply blocked_by relationships for existing issues"""
        blocked_specs = [s for s in specs if s.blocked_by]
        if not blocked_specs:
            print("No blocked_by entries found in spec.", file=sys.stderr)
            return

        for spec in blocked_specs:
            formatted_title = self.format_issue_title(spec)
            issue_num = spec.issue_number or self.find_issue_by_title(formatted_title)
            if not issue_num:
                print(f"[WARN] Could not find issue '{formatted_title}' to update blockers.", file=sys.stderr)
                continue

            self.update_issue(issue_num, spec)
            for blocker_title in spec.blocked_by:
                blocking_num = self.find_issue_by_title(blocker_title)
                if not blocking_num:
                    print(f"[WARN] Could not resolve blocker '{blocker_title}' for #{issue_num}", file=sys.stderr)
                    continue
                self.add_blocking_relationship(issue_num, blocking_num)
                print(f"  [OK] #{issue_num} blocked by #{blocking_num}")

    def process_specs(self, specs: List[IssueSpec]):
        """Create all issues and set up relationships"""
        print(f"Creating {len(specs)} issues...")
        print()

        # Phase 1: Create all issues
        for spec in specs:
            formatted_title = self.format_issue_title(spec)
            issue_num, created = self.ensure_issue_for_spec(spec)
            self.created_issues[formatted_title] = issue_num

            if spec.is_epic:
                action = "Created" if created else "Updated"
                print(f"[OK] {action} Epic #{issue_num}: {formatted_title}")
            else:
                areas_str = ', '.join(spec.areas) if spec.areas else 'none'
                action = "Created" if created else "Updated"
                print(f"  [OK] {action} #{issue_num}: {formatted_title} (priority: {spec.priority}, areas: {areas_str})")

        print()

        # Phase 2: Link parent/child relationships
        if any(s.parent_title for s in specs):
            print("Setting up relationships...")
            for spec in specs:
                if spec.parent_title and spec.parent_title in self.created_issues:
                    parent_num = self.created_issues[spec.parent_title]
                    child_title = self.format_issue_title(spec)
                    child_num = self.created_issues.get(child_title)
                    if child_num is None:
                        continue

                    self.add_child_to_parent(parent_num, child_num)
                    print(f"  [OK] Linked #{child_num} as child of #{parent_num}")
            print()

        # Phase 3: Set blocking relationships
        blocked_issues = [s for s in specs if s.blocked_by]
        if blocked_issues:
            print("Setting up blocking relationships...")
            for spec in blocked_issues:
                blocked_title = self.format_issue_title(spec)
                blocked_issue_num = self.created_issues.get(blocked_title)
                if blocked_issue_num is None:
                    continue
                for blocker_title in spec.blocked_by:
                    if blocker_title in self.created_issues:
                        blocking_issue_num = self.created_issues[blocker_title]
                        self.add_blocking_relationship(blocked_issue_num, blocking_issue_num)
                        print(f"  [OK] #{blocked_issue_num} blocked by #{blocking_issue_num}")
                    else:
                        print(f"  [WARN] #{blocked_issue_num} blocker not found: {blocker_title}", file=sys.stderr)
            print()

        print("Summary:")
        print(f"  Created {len(specs)} issues")
        epics = [s for s in specs if s.is_epic]
        if epics:
            print(f"  {len(epics)} Epic(s) with children")

        print()
        print("Issue numbers:")
        for title, num in self.created_issues.items():
            print(f"  #{num}: {title}")

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    parser = argparse.ArgumentParser(
        description='Batch create or update GitHub issues with Epic/child relationships',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Create new issues from spec file
  %(prog)s specs.md

  # Update single issue
  %(prog)s specs.md --update 171

  # Update Epic and all children (matches by order)
  %(prog)s specs.md --update-epic 170

  # Auto-update issues (requires issue_number: N in spec)
  %(prog)s specs.md --update-auto

  # Update blocking relationships without creating issues
  %(prog)s specs.md --update-blockers

  # Create new issue and add to Epic #170
  %(prog)s new_child.md --add-child 170

  # Read from stdin
  cat specs.md | %(prog)s

Spec file format:
  See .aide/docs/ISSUE_CREATOR_GUIDE.md for complete documentation.
  See .aide/tools/issue-creator/example-spec.md for examples.

Update mode metadata:
  Add to any issue section in spec file:
    issue_number: 171

  Then run: %(prog)s specs.md --update-auto
        '''
    )

    parser.add_argument('spec_file', nargs='?', help='Spec file path (or read from stdin)')
    parser.add_argument('--update', type=int, metavar='NUM', help='Update single issue NUM with first spec in file')
    parser.add_argument('--update-epic', type=int, metavar='NUM', help='Update Epic NUM and all children (matches by order)')
    parser.add_argument('--update-auto', action='store_true', help='Update issues based on issue_number metadata in specs')
    parser.add_argument('--add-child', type=int, metavar='EPIC_NUM', help='Create new issue from spec and link to Epic EPIC_NUM')
    parser.add_argument(
        '--sync-types',
        type=str,
        metavar='NUMS',
        help='Migration helper: sync GitHub Issue Types from legacy type labels for comma-separated issue numbers (e.g. 42,43,44)',
    )
    parser.add_argument('--update-blockers', action='store_true', help='Update blocked_by relationships for issues described in the spec')
    parser.add_argument('--link-blocker', action='append', metavar='BLOCKED:BLOCKER', help='Explicitly link two existing issues via blocking (can be repeated)')
    parser.add_argument('--link-child', action='append', metavar='PARENT:CHILD', help='Explicitly link an existing child to an Epic (can be repeated)')

    args = parser.parse_args()

    # Initialize creator
    creator = IssueCreator()

    # Handle --sync-types mode (doesn't require spec file)
    if args.sync_types:
        try:
            issue_numbers = [int(n.strip()) for n in args.sync_types.split(',')]
        except ValueError:
            print("Error: --sync-types requires comma-separated issue numbers (e.g. 42,43,44)", file=sys.stderr)
            sys.exit(1)

        creator.sync_types(issue_numbers)
        sys.exit(0)

    # Handle explicit linking
    if args.link_blocker or args.link_child:
        if args.link_blocker:
            for value in args.link_blocker:
                try:
                    blocked, blocker = creator.parse_link_arg(value)
                    creator.link_blocker_pair(blocked, blocker)
                except ValueError as exc:
                    print(f"[ERROR] Invalid --link-blocker value '{value}': {exc}", file=sys.stderr)
        if args.link_child:
            for value in args.link_child:
                try:
                    parent, child = creator.parse_link_arg(value)
                    creator.link_child_pair(parent, child)
                except ValueError as exc:
                    print(f"[ERROR] Invalid --link-child value '{value}': {exc}", file=sys.stderr)
        sys.exit(0)

    # Read spec file
    if args.spec_file:
        with open(args.spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(0)
        content = sys.stdin.read()

    # Parse specs
    specs = creator.parse_spec_file(content)

    if not specs:
        print("No issues found in spec file", file=sys.stderr)
        sys.exit(1)

    # Check for checklists (warning only)
    checklist_warnings = creator.check_for_checklists(content)
    for warning in checklist_warnings:
        print(warning, file=sys.stderr)
        print()

    # Preflight labels for spec-driven runs
    if not (args.sync_types or args.link_blocker or args.link_child):
        creator.ensure_labels_for_specs(specs)

    # Determine mode
    if args.update:
        creator.process_updates(specs, 'single', args.update)
    elif args.update_epic:
        creator.process_updates(specs, 'epic', args.update_epic)
    elif args.update_auto:
        creator.process_updates(specs, 'auto')
    elif args.update_blockers:
        creator.process_blockers(specs)
    elif args.add_child:
        # Add child to existing Epic
        spec = specs[0] if specs else None
        if not spec:
            print("No issue spec found in file", file=sys.stderr)
            sys.exit(1)
        if spec.is_epic:
            print("Error: Spec is an Epic, expected a regular issue", file=sys.stderr)
            sys.exit(1)

        print(f"Creating new issue...")
        issue_num = creator.create_issue(spec)
        print(f"[OK] Created #{issue_num}: {spec.title}")

        print(f"Linking to Epic #{args.add_child}...")
        creator.add_child_to_parent(args.add_child, issue_num)
        print(f"[OK] Linked #{issue_num} to Epic #{args.add_child}")
    else:
        # Create mode (default)
        creator.process_specs(specs)

if __name__ == '__main__':
    main()
