# workflow-gen

Generate and validate workflow artifacts from a canonical manifest.

## Purpose

Avoid drift between:
- `docs/agents/IMPLEMENTATION_ONE_PAGER.md`
- `skills/implement/SKILL.md`
- `docs/agents/implementation/STEP_*.md` navigation headers

## Usage

From repo root:

```bash
python tools/workflow-gen/generate.py --write
python tools/workflow-gen/generate.py --check
```

`--write` updates files in place. `--check` exits non-zero if updates are required.

