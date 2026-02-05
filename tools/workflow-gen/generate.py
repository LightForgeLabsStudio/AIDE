from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]

ONE_PAGER_STEPS_START = "<!-- AIDE-GEN:IMPLEMENTATION_STEPS_START -->"
ONE_PAGER_STEPS_END = "<!-- AIDE-GEN:IMPLEMENTATION_STEPS_END -->"

SKILL_WORKFLOW_START = "<!-- AIDE-GEN:IMPLEMENT_WORKFLOW_START -->"
SKILL_WORKFLOW_END = "<!-- AIDE-GEN:IMPLEMENT_WORKFLOW_END -->"


@dataclass(frozen=True)
class Step:
    number: int
    title: str
    summary: str
    doc: str


def _load_manifest(path: Path) -> tuple[dict, list[Step]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    steps = [
        Step(
            number=int(step["number"]),
            title=str(step["title"]),
            summary=str(step["summary"]),
            doc=str(step["doc"]),
        )
        for step in data["steps"]
    ]
    steps_sorted = sorted(steps, key=lambda s: s.number)
    expected_numbers = list(range(len(steps_sorted)))
    actual_numbers = [s.number for s in steps_sorted]
    if actual_numbers != expected_numbers:
        raise ValueError(
            f"Manifest steps must be contiguous 0..{len(steps_sorted)-1}; got {actual_numbers}"
        )
    return data, steps_sorted


def _replace_block(text: str, start: str, end: str, replacement: str) -> str:
    start_idx = text.find(start)
    end_idx = text.find(end)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise ValueError(f"Missing or invalid markers: {start} / {end}")
    before = text[: start_idx + len(start)]
    after = text[end_idx:]
    return f"{before}\n{replacement}\n{after}"


def _relpath(from_path: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, start=from_path.parent).replace("\\", "/")


def _render_one_pager_steps(one_pager_path: Path, steps: Iterable[Step]) -> str:
    lines: list[str] = []
    for step in steps:
        doc_path = (REPO_ROOT / step.doc).resolve()
        rel = _relpath(one_pager_path, doc_path)
        # One-pager lives under docs/agents/, so this should be `implementation/STEP_*.md`.
        lines.append(
            f"{step.number}. **{step.title}** -> {step.summary} (`{rel}`)"
        )
    return "\n".join(lines)


def _render_skill_workflow(manifest: dict, steps: Iterable[Step]) -> str:
    prefix = str(manifest.get("skill_consumer_prefix", ""))
    lines: list[str] = []
    lines.append(
        f"Canonical workflow (also see: `{prefix}docs/agents/IMPLEMENTATION_ONE_PAGER.md`)."
    )
    lines.append("")
    for step in steps:
        lines.append(
            f"{step.number}) **{step.title}** -> {step.summary} (`{prefix}{step.doc}`)"
        )
    return "\n".join(lines)


def _build_step_filename(step_number: int) -> str:
    return f"STEP_{step_number}_"


def _check_step_navs(steps: list[Step]) -> list[str]:
    issues: list[str] = []
    total = len(steps)
    impl_dir = REPO_ROOT / "docs/agents/implementation"
    for step in steps:
        step_doc = REPO_ROOT / step.doc
        if not step_doc.exists():
            issues.append(f"Missing step doc: {step.doc}")
            continue
        lines = step_doc.read_text(encoding="utf-8").splitlines()
        if len(lines) < 3:
            issues.append(f"{step.doc}: too short to contain nav line")
            continue
        nav_line = lines[2].strip()
        if not nav_line.startswith("**Navigation:**"):
            issues.append(f"{step.doc}: missing navigation line at line 3")
            continue
        # Validate that prev/next step links exist in the text (best-effort, filename varies for step 10).
        if step.number > 0 and f"Step {step.number - 1}" not in nav_line:
            issues.append(f"{step.doc}: nav line missing prev Step {step.number - 1}")
        if step.number < total - 1 and f"Step {step.number + 1}" not in nav_line:
            issues.append(f"{step.doc}: nav line missing next Step {step.number + 1}")
        # Validate referenced filenames exist (glob-style check).
        for neighbor in (step.number - 1, step.number + 1):
            if neighbor < 0 or neighbor >= total:
                continue
            prefix = _build_step_filename(neighbor)
            matches = list(impl_dir.glob(f"{prefix}*.md"))
            if not matches:
                issues.append(
                    f"{step.doc}: expected step file for {neighbor} under docs/agents/implementation"
                )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="manifests/implementation.json",
        help="Path to workflow manifest (repo-relative).",
    )
    parser.add_argument("--write", action="store_true", help="Update files in place.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if updates would be made.",
    )
    args = parser.parse_args()
    if args.write and args.check:
        print("Use only one of --write or --check", file=sys.stderr)
        return 2
    mode = "check" if args.check else "write"

    manifest_path = REPO_ROOT / args.manifest
    manifest, steps = _load_manifest(manifest_path)

    one_pager_path = REPO_ROOT / manifest["one_pager"]
    one_pager_text = one_pager_path.read_text(encoding="utf-8")
    expected_steps_block = _render_one_pager_steps(one_pager_path, steps)
    updated_one_pager = _replace_block(
        one_pager_text, ONE_PAGER_STEPS_START, ONE_PAGER_STEPS_END, expected_steps_block
    )

    skill_path = REPO_ROOT / manifest["skill"]
    skill_text = skill_path.read_text(encoding="utf-8")
    expected_skill_block = _render_skill_workflow(manifest, steps)
    updated_skill = _replace_block(
        skill_text, SKILL_WORKFLOW_START, SKILL_WORKFLOW_END, expected_skill_block
    )

    nav_issues = _check_step_navs(steps)

    changed = []
    if updated_one_pager != one_pager_text:
        changed.append(manifest["one_pager"])
    if updated_skill != skill_text:
        changed.append(manifest["skill"])
    if nav_issues:
        changed.append("docs/agents/implementation/STEP_*.md (nav)")

    if mode == "check":
        if changed:
            print("workflow-gen check failed. Updates required:")
            for path in changed:
                print(f"- {path}")
            if nav_issues:
                print("\nNavigation issues:")
                for issue in nav_issues:
                    print(f"- {issue}")
            return 1
        return 0

    # write mode
    one_pager_path.write_text(updated_one_pager, encoding="utf-8", newline="\n")
    skill_path.write_text(updated_skill, encoding="utf-8", newline="\n")
    if nav_issues:
        print("Warning: navigation issues detected (not auto-fixed):")
        for issue in nav_issues:
            print(f"- {issue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
