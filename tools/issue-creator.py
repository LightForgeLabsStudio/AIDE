#!/usr/bin/env python3
"""
Issue Creator - Batch create GitHub issues with Epic/child relationships

Part of the AIDE framework. Project-specific config in issue-creator.config.json

Usage:
    ./issue-creator.py spec.md
    ./issue-creator.py < spec.md
    cat spec.md | ./issue-creator.py
"""

import sys
import os
import json
import re
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class IssueSpec:
    title: str
    body: str
    priority: str = "medium"
    areas: List[str] = field(default_factory=list)
    is_epic: bool = False
    parent_title: Optional[str] = None
    blocks: List[str] = field(default_factory=list)
    blocked_by: List[str] = field(default_factory=list)

class IssueCreator:
    DEFAULT_CONFIG = {
        "area_keywords": {},
        "default_priority": "medium",
        "default_status_ready": "status:ready",
        "default_status_blocked": "status:blocked",
        "epic_label": "Epic",
        "enhancement_label": "enhancement"
    }

    def __init__(self):
        self.config = self._load_config()
        self.repo_info = self._get_repo_info()
        self.created_issues = {}

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
                    print(f"✓ Loaded config from {path}", file=sys.stderr)
                    return config

        print("⚠ No config found, using defaults (no area inference)", file=sys.stderr)
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

    def parse_spec_file(self, content: str) -> List[IssueSpec]:
        """Parse spec file into IssueSpec objects"""
        specs = []
        sections = re.split(r'\n(?:---+|##\s+Issue:)\s*\n', content)
        current_epic = None

        for section in sections:
            if not section.strip():
                continue

            is_epic = '[Epic]' in section or 'Epic:' in section

            title_match = re.search(r'^#+\s*(?:\[Epic\]:?\s*)?(.+?)$', section, re.MULTILINE)
            if not title_match:
                continue

            title = title_match.group(1).strip()

            # Extract fields
            priority_match = re.search(r'^priority:\s*(\w+)', section, re.MULTILINE | re.IGNORECASE)
            priority = priority_match.group(1) if priority_match else self.config['default_priority']

            area_match = re.search(r'^area:\s*(.+?)$', section, re.MULTILINE | re.IGNORECASE)
            explicit_areas = [a.strip() for a in area_match.group(1).split(',')] if area_match else []

            blocks_match = re.search(r'^blocks:\s*(.+?)$', section, re.MULTILINE | re.IGNORECASE)
            blocks = [b.strip() for b in blocks_match.group(1).split(',')] if blocks_match else []

            blocked_match = re.search(r'^blocked_by:\s*(.+?)$', section, re.MULTILINE | re.IGNORECASE)
            blocked_by = [b.strip() for b in blocked_match.group(1).split(',')] if blocked_match else []

            # Infer areas from content
            inferred_areas = self.infer_areas(section)
            areas = list(set(explicit_areas + inferred_areas))

            if is_epic:
                current_epic = title

            spec = IssueSpec(
                title=title,
                body=section,
                priority=priority,
                areas=areas,
                is_epic=is_epic,
                parent_title=current_epic if not is_epic else None,
                blocks=blocks,
                blocked_by=blocked_by
            )

            specs.append(spec)

        return specs

    def create_issue(self, spec: IssueSpec) -> int:
        """Create single GitHub issue, returns issue number"""
        labels = []

        # Type label
        if spec.is_epic:
            labels.append(self.config['epic_label'])
        else:
            labels.append(self.config['enhancement_label'])

        # Priority
        labels.append(f'priority:{spec.priority}')

        # Areas
        for area in spec.areas:
            labels.append(f'area:{area}')

        # Status
        if spec.blocked_by:
            labels.append(self.config['default_status_blocked'])
        else:
            labels.append(self.config['default_status_ready'])

        # Add blocked-by section to body if needed
        body = spec.body
        if spec.blocked_by:
            blocked_section = "\n\n## Blocked By\n" + "\n".join(
                f"- {dep}" for dep in spec.blocked_by
            )
            body += blocked_section

        # Build title
        if spec.is_epic:
            title = f"[Epic]: {spec.title}"
        else:
            title = f"[Feature]: {spec.title}"

        # Create issue via gh CLI
        cmd = [
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
            '--label', ','.join(labels)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Extract issue number from URL
        url = result.stdout.strip()
        issue_num = int(url.split('/')[-1])

        return issue_num

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

        subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={mutation}'],
            capture_output=True, text=True, check=True
        )

    def process_specs(self, specs: List[IssueSpec]):
        """Create all issues and set up relationships"""
        print(f"Creating {len(specs)} issues...")
        print()

        # Phase 1: Create all issues
        for spec in specs:
            issue_num = self.create_issue(spec)
            self.created_issues[spec.title] = issue_num

            if spec.is_epic:
                print(f"✓ Created Epic #{issue_num}: {spec.title}")
            else:
                areas_str = ', '.join(spec.areas) if spec.areas else 'none'
                print(f"  ✓ Created #{issue_num}: {spec.title} (priority: {spec.priority}, areas: {areas_str})")

        print()

        # Phase 2: Link parent/child relationships
        if any(s.parent_title for s in specs):
            print("Setting up relationships...")
            for spec in specs:
                if spec.parent_title and spec.parent_title in self.created_issues:
                    parent_num = self.created_issues[spec.parent_title]
                    child_num = self.created_issues[spec.title]

                    self.add_child_to_parent(parent_num, child_num)
                    print(f"  ✓ Linked #{child_num} as child of #{parent_num}")
            print()

        # Phase 3: Report blocking relationships
        blocked_issues = [s for s in specs if s.blocked_by]
        if blocked_issues:
            print("Blocked issues (set via labels and body):")
            for spec in blocked_issues:
                issue_num = self.created_issues[spec.title]
                blockers = ', '.join(spec.blocked_by)
                print(f"  ⚠ #{issue_num} blocked by: {blockers}")
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
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    creator = IssueCreator()
    specs = creator.parse_spec_file(content)

    if not specs:
        print("No issues found in spec file", file=sys.stderr)
        sys.exit(1)

    creator.process_specs(specs)

if __name__ == '__main__':
    main()
