# Init Project Tool

Initialize AIDE framework in a new or existing project.

## Usage

```bash
bash .aide/tools/init-project/init-project.sh
```

## What It Does

The init script sets up your project with AIDE framework:

1. **Detects your tech stack** (if possible)
2. **Copies relevant templates** from `.aide/docs/examples/`
3. **Creates symlinks** to core AIDE docs
4. **Guides configuration** of placeholders

## Interactive Setup

The script will ask:

- **Project name**
- **Tech stack** (Godot, Node.js, Python, Rust, etc.)
- **Test command** (e.g., `npm test`, `cargo test`)
- **Main branch** (usually `main`)

## Project Structure After Init

```
your-project/
├── .aide/                          # AIDE submodule (or clone)
├── docs/
│   ├── DOCUMENTATION_POLICY.md     # → .aide/docs/core/DOCUMENTATION_POLICY.md
│   ├── CONTRIBUTING.md             # → .aide/docs/core/CONTRIBUTING.md
│   ├── TESTING_POLICY.md           # Copied from examples/{stack}/
│   ├── CODING_GUIDELINES.md        # Copied from examples/{stack}/
│   ├── DEVELOPMENT.md              # Copied from examples/{stack}/
│   ├── AGENTS.md                   # Configuration mappings
│   └── agents/                     # → .aide/docs/agents/
```

## Manual Setup

Prefer to set up manually? See [../../QUICK_START.md](../../QUICK_START.md) for:
- Step-by-step instructions
- Placeholder configuration
- Tech stack customization

## Customization

After running init, customize:

1. **Edit `docs/AGENTS.md`** - Map AIDE placeholders to your project values
2. **Review `docs/TESTING_POLICY.md`** - Adjust test requirements for your project
3. **Update `docs/CODING_GUIDELINES.md`** - Add project-specific style rules

## Troubleshooting

### Script fails to detect tech stack

Manually specify when prompted or edit generated files after setup.

### Symlinks not working (Windows)

Run as Administrator or use Git Bash. Alternatively, copy files instead of symlinking.

### Want different examples

Browse `.aide/docs/examples/` and copy relevant files manually.

## License

MIT License - Part of the AIDE framework
