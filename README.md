# AIDE: AI-Assisted Development Environment

**A universal framework for AI-assisted software development workflows.**

AIDE provides battle-tested processes, agent primers, and documentation templates for teams building software with AI assistance. Language-agnostic, framework-agnostic, and adaptable to any project type.

## What is AIDE?

AIDE (AI-Assisted Development Environment) is a comprehensive framework that standardizes how AI agents collaborate with human developers on software projects. It provides:

- **Process Documentation**: Contribution workflows, testing policies, documentation standards
- **AI Agent Primers**: Role-specific instructions for implementation, review, design, and documentation agents
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

# Agent primers (usually symlink)
ln -s .aide/docs/agents docs/agents
```

### 4. Customize for Your Project

Replace template placeholders with your project specifics:
- `{{PROJECT_NAME}}` → Your project name
- `{{LANGUAGE}}` → Your programming language
- `{{FRAMEWORK}}` → Your framework/engine
- `{{RUN_ALL_TESTS_COMMAND}}` → Your test command

See [QUICK_START.md](QUICK_START.md) for detailed instructions.

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
│   ├── agents/                  # AI agent primers (symlink these)
│   │   ├── IMPLEMENTATION_START.md
│   │   ├── PR_REVIEW_START.md
│   │   ├── DOC_REVIEW_START.md
│   │   └── ...
│   │
│   └── examples/                # Language-specific examples
│       ├── godot-gdscript/
│       ├── nodejs-typescript/
│       ├── python/
│       └── rust/
│
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

## Agent Roles

AIDE defines specialized AI agent roles:

- **Implementation Agent**: Builds features following the 7-step workflow
- **PR Review Agent**: Reviews code for quality, architecture, and standards
- **Documentation Agent**: Reviews docs for accuracy and consistency
- **Codebase Review Agent**: Performs holistic codebase audits
- **Design Spec Agent**: Helps prioritize and spec new features
- **Design Workshop Agent**: Facilitates high-level design exploration

Each role has a dedicated primer in `docs/agents/`.

## The 7-Step Implementation Workflow

1. **Codebase Survey** - Understand current state (no coding yet)
2. **Implementation Plan** - Design approach, get approval
3. **Git-First Development** - Branch, draft PR, clean commits
4. **Testing** - Automated tests, manual verification
5. **Sanity Check** - Edge cases, gameplay/user testing
6. **PR Ready** - Complete scope, passing tests, docs updated
7. **Review & Merge** - Feedback loop, merge on approval

See [docs/agents/IMPLEMENTATION_START.md](docs/agents/IMPLEMENTATION_START.md) for full details.

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
- 7-step implementation workflow
- PR review process with inline comments
- Documentation review and accuracy checks
- Design workshop for feature planning

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
- Check `docs/agents/` for agent-specific guidance
- Open an issue for questions or suggestions
