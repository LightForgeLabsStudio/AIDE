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
    issue_number: Optional[int] = None  # For update mode

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

            issue_num_match = re.search(r'^issue_number:\s*(\d+)', section, re.MULTILINE | re.IGNORECASE)
            issue_number = int(issue_num_match.group(1)) if issue_num_match else None

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
                blocked_by=blocked_by,
                issue_number=issue_number
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

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            print(f"Error creating issue: {result.stderr}", file=sys.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

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

    def update_issue(self, issue_num: int, spec: IssueSpec):
        """Update existing GitHub issue"""
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

        # Build title (preserve existing title prefix if it exists)
        if spec.is_epic and not spec.title.startswith('[Epic]'):
            title = f"[Epic]: {spec.title}"
        elif not spec.is_epic and not spec.title.startswith('['):
            title = f"[Feature]: {spec.title}"
        else:
            title = spec.title

        # Update issue via gh CLI
        cmd = [
            'gh', 'issue', 'edit', str(issue_num),
            '--title', title,
            '--body', body,
        ]

        # Remove all existing labels and add new ones
        # Note: gh doesn't have a --set-labels, so we use --add-label for new labels
        # The user should manually remove old labels if needed, or we could query first
        for label in labels:
            cmd.extend(['--add-label', label])

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            print(f"Error updating issue #{issue_num}: {result.stderr}", file=sys.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

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

    def process_specs(self, specs: List[IssueSpec]):
        """Create all issues and set up relationships"""
        print(f"Creating {len(specs)} issues...")
        print()

        # Phase 1: Create all issues
        for spec in specs:
            issue_num = self.create_issue(spec)
            self.created_issues[spec.title] = issue_num

            if spec.is_epic:
                print(f"[OK] Created Epic #{issue_num}: {spec.title}")
            else:
                areas_str = ', '.join(spec.areas) if spec.areas else 'none'
                print(f"  [OK] Created #{issue_num}: {spec.title} (priority: {spec.priority}, areas: {areas_str})")

        print()

        # Phase 2: Link parent/child relationships
        if any(s.parent_title for s in specs):
            print("Setting up relationships...")
            for spec in specs:
                if spec.parent_title and spec.parent_title in self.created_issues:
                    parent_num = self.created_issues[spec.parent_title]
                    child_num = self.created_issues[spec.title]

                    self.add_child_to_parent(parent_num, child_num)
                    print(f"  [OK] Linked #{child_num} as child of #{parent_num}")
            print()

        # Phase 3: Report blocking relationships
        blocked_issues = [s for s in specs if s.blocked_by]
        if blocked_issues:
            print("Blocked issues (set via labels and body):")
            for spec in blocked_issues:
                issue_num = self.created_issues[spec.title]
                blockers = ', '.join(spec.blocked_by)
                print(f"  [WARN] #{issue_num} blocked by: {blockers}")
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

    args = parser.parse_args()

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
    creator = IssueCreator()
    specs = creator.parse_spec_file(content)

    if not specs:
        print("No issues found in spec file", file=sys.stderr)
        sys.exit(1)

    # Determine mode
    if args.update:
        creator.process_updates(specs, 'single', args.update)
    elif args.update_epic:
        creator.process_updates(specs, 'epic', args.update_epic)
    elif args.update_auto:
        creator.process_updates(specs, 'auto')
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
