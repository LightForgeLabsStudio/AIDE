# AIDE: AI-Assisted Development Environment

> **AI Agents:** Start with [AGENT_ORIENTATION.md](AGENT_ORIENTATION.md) for roles, authority hierarchy, and entry workflow.

**A universal framework for AI-assisted software development workflows.**

AIDE provides battle-tested processes, agent primers, and documentation templates for teams building software with AI assistance. Language-agnostic, framework-agnostic, and adaptable to any project type.

## What is AIDE?

AIDE (AI-Assisted Development Environment) is a comprehensive framework that standardizes how AI agents collaborate with human developers on software projects. It provides:

- **Process Documentation**: Contribution workflows, testing policies, documentation standards
- **AI Skills**: Self-contained task workflows for implementation, review, design, and documentation
- **Language-Agnostic Templates**: Customizable standards for any tech stack
- **Battle-Tested Patterns**: Proven workflows from real-world AI-assisted development

## Key Features

### For Any Project Type
- Web applications (React, Vue, Angular, etc.)
- Backend services (Node.js, Python, Rust, Go, etc.)
- Mobile apps (React Native, Flutter, Swift, Kotlin, etc.)
- Desktop applications (Electron, Tauri, Qt, etc.)
- Game development (Unity, Godot, Unreal, etc.)
- CLI tools, libraries, frameworks, and more

### For Any Team Size
- Solo developers with AI assistants
- Small teams (2-10 developers)
- Growing teams (10-50 developers)
- Enterprise teams (50+ developers)

### Language & Framework Agnostic
AIDE works with any programming language and technology stack. Examples provided for:
- Godot/GDScript (game development)
- Node.js/TypeScript (web/backend)
- Python (ML/backend/scripting)
- Rust (systems/performance)

## Quick Start

### 1. Clone or Download AIDE

```bash
# Option A: Clone as standalone repo
git clone <your-aide-repo-url> aide-framework

# Option B: Add as git submodule to existing project
cd your-project
git submodule add <your-aide-repo-url> .aide
```

### 2. Choose Your Tech Stack Example

Browse `docs/examples/` for your stack:
- `godot-gdscript/` - Game development with Godot
- `nodejs-typescript/` - Web/backend with Node.js
- `python/` - Backend/ML with Python
- `rust/` - Systems programming with Rust

### 3. Instantiate Templates

Copy relevant templates to your project:

```bash
# Core process docs (usually symlink these)
ln -s .aide/docs/core/DOCUMENTATION_POLICY.md docs/DOCUMENTATION_POLICY.md
ln -s .aide/docs/core/CONTRIBUTING.md docs/CONTRIBUTING.md

# Tech-specific standards (copy and customize)
cp .aide/docs/examples/nodejs-typescript/TESTING_POLICY.md docs/TESTING_POLICY.md
cp .aide/docs/examples/nodejs-typescript/CODING_GUIDELINES.md docs/CODING_GUIDELINES.md

# Install skills into your AI tool
powershell -ExecutionPolicy Bypass -File .aide/skills/install-claude.ps1
# or: .aide/skills/install-codex.ps1
```

### 4. Configure AIDE for Your Project

**Recommended:** Create a configuration mapping table in `docs/AGENTS.md` (or equivalent):

```markdown
## AIDE Configuration (Placeholder Mappings)

| AIDE Placeholder | Project Value |
|-----------------|---------------|
| `{{PROJECT_NAME}}` | YourProjectName |
| `{{TECH_STACK}}` | Your stack (e.g., "Node.js + TypeScript") |
| `{{IMPLEMENTATION_STATUS_QUERY}}` | `gh issue list --label "status:in-progress"` (see [GITHUB_QUERIES.md](docs/agents/GITHUB_QUERIES.md)) |
| `{{RUN_ALL_TESTS_COMMAND}}` | npm test |
...
```

This keeps AIDE generic while your project config defines the mappings. Agents resolve placeholders by reading your config first.

**Alternative:** Copy templates and replace `{{PLACEHOLDERS}}` directly (see legacy approach in [QUICK_START.md](QUICK_START.md)).

See [QUICK_START.md](QUICK_START.md) for detailed configuration instructions.

## Documentation Structure

```
AIDE/
├── docs/
│   ├── core/                    # Universal process docs (symlink these)
│   │   ├── DOCUMENTATION_POLICY.md
│   │   ├── CONTRIBUTING.md
│   │   └── *.template.md        # Project-specific templates
│   │
│   ├── standards/               # Customizable standard templates
│   │   ├── TESTING_POLICY.template.md
│   │   ├── CODING_GUIDELINES.template.md
│   │   └── DEVELOPMENT.template.md
│   │
│   ├── agents/                  # Compact Tier 2 reference files (on-demand)
│   │   ├── COMMAND_CATALOG.md
│   │   ├── GITHUB_QUERIES.md
│   │   ├── ERROR_RECOVERY.md
│   │   └── ...
│   │
│   └── examples/                # Language-specific examples
│       ├── godot-gdscript/
│       ├── nodejs-typescript/
│       ├── python/
│       └── rust/
│
├── skills/                      # AIDE skills (install via install-claude.ps1)
│   ├── implement/
│   ├── pr-review/
│   ├── design/
│   └── ...
└── tools/                       # Setup automation scripts
    ├── init-project.sh
    └── init-project.bat
```

## Core Principles

### 1. Process Over Tools
AIDE focuses on **how** teams work together, not which tools they use. The framework adapts to your stack.

### 2. AI as Collaborator
AI agents are treated as team members with specific roles, responsibilities, and boundaries.

### 3. Deterministic Workflows
Every process is documented, repeatable, and produces consistent results.

### 4. Lean Documentation
Document once in the best place. Reference, don't duplicate.

### 5. Test-Driven Development
All changes require tests. No exceptions (unless you document why).

## Skills

AIDE provides self-contained skills that define what the agent is doing, not who it is:

- **`/implement`** — Build features end-to-end: spec intake, code, tests, verify, push
- **`/pr-review`** — Review code for quality, architecture, and standards
- **`/design`** — Design exploration → Architecture Decision Record (ADR)
- **`/scope`** — Decompose an ADR into GitHub issues via issue-creator
- **`/codebase-review`** — Holistic codebase health audit
- **`/doc-review`** — Documentation accuracy review
- **`/findings`** — Cross-cutting review protocol that writes reviewer output to `<slug>.findings.md`
- **`/pr-draft`, `/pr-ready`** — PR lifecycle management
- **`/quality`, `/handoff`, `/sync`, `/issue`, `/evolve`, `/skill-author`** — Utilities

**Token Optimization**: Skills follow token economy best practices (see `docs/agents/TOKEN_ECONOMY.md`). Each skill is 30-50 lines and self-contained — no preloading required.

## Implementation Workflow

The canonical implementation workflow is inlined in the `/implement` skill:

- `skills/implement/SKILL.md` — two-layer plan (constraint check + ordered steps), code, verify

Start by invoking `/implement` in your AI chat session and providing a GitHub issue number or spec.

## Philosophy

AIDE emerged from real-world experience building software with AI agents. Key insights:

- **Structured processes** prevent AI drift and scope creep
- **Clear boundaries** (what agents can/cannot do) improve reliability
- **Explicit approval gates** maintain human control
- **Documentation templates** ensure consistency across projects
- **Language-agnostic patterns** allow framework reuse

## Examples & Case Studies

### Lightborn Exile: Divinity Engine (Godot/GDScript)
A roguelike factory survival game built entirely with AI-assisted development using AIDE workflows. Demonstrates:

- Skill-based implementation workflow (`/implement`, `/pr-draft`, `/pr-ready`)
- PR review process with inline comments (`/pr-review`)
- Documentation review and accuracy checks (`/doc-review`)
- Design sessions producing ADRs (`/design`, `/scope`)

See `docs/examples/godot-gdscript/` for implementation details.

## Contributing to AIDE

We welcome contributions! See [CONTRIBUTING.md](docs/core/CONTRIBUTING.md) for:
- How to suggest new agent roles
- Language/framework example additions
- Template improvements
- Process refinements

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Created by LightForge Labs as a distillation of AI-assisted development best practices.

## Getting Help

- Read [QUICK_START.md](QUICK_START.md) for setup instructions
- Browse `docs/examples/` for your tech stack
- Check `docs/agents/COMMAND_CATALOG.md` for the full skill catalog
- Open an issue for questions or suggestions
