# AIDE Tools

Command-line tools for streamlining AI-assisted development workflows.

## Available Tools

### [workflow-gen](workflow-gen/)
Generate/validate workflow artifacts from a canonical manifest (prevents skill/docs drift).

### [issue-creator](issue-creator/)
Batch create GitHub issues with Epic/child relationships from formatted spec files.

**Quick Start:** [Use the Custom GPT](https://chatgpt.com/g/g-696532cabeac81918a55b5f62eb9b8fd-issue-spec-formatter-aide) to format specs, then run:
```bash
python .aide/tools/issue-creator/issue-creator.py specs.md
```

See [issue-creator/README.md](issue-creator/README.md) for details.

### [init-project](init-project/)
Initialize AIDE framework in a new or existing project.

```bash
bash .aide/tools/init-project/init-project.sh
```

See [init-project/README.md](init-project/README.md) for details.

## Tool Organization

Each tool has its own subdirectory with:
- `README.md` - Usage documentation
- Tool scripts/executables
- Configuration examples
- Example files

This structure makes it easy to extract tools into separate submodules if needed.

## Contributing Tools

When adding new tools:
1. Create subdirectory: `.aide/tools/your-tool/`
2. Add `README.md` with usage instructions
3. Add tool to this file's "Available Tools" section
4. Update `.aide/README.md` to mention the tool
5. Consider creating an agent primer in `.aide/docs/agents/`
