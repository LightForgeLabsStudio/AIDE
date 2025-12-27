# AIDE Quick Start Guide

Get AIDE integrated into your project in under 10 minutes.

## Prerequisites

- Git installed
- Existing software project (or starting a new one)
- AI assistant with file access (Claude, GPT-4, etc.)

## Installation Options

### Option A: Git Submodule (Recommended)

Add AIDE as a submodule to get automatic updates:

```bash
cd your-project
git submodule add <aide-repo-url> .aide
git submodule update --init --recursive
```

### Option B: Direct Copy

Copy AIDE files directly into your project:

```bash
cp -r /path/to/AIDE/ your-project/.aide/
```

### Option C: Project Template

Start a new project with AIDE pre-configured:

```bash
./AIDE/tools/init-project.sh my-new-project nodejs-typescript
```

## Step-by-Step Setup

### 1. Choose Your Tech Stack

Browse `docs/examples/` and find the closest match to your stack:

```bash
ls .aide/docs/examples/
# godot-gdscript/
# nodejs-typescript/
# python/
# rust/
```

If your stack isn't listed, start with the closest example and customize.

### 2. Copy Core Documentation

Create a `docs/` directory in your project and link/copy core files:

```bash
mkdir -p docs/agents

# Symlink universal process docs (recommended - get updates automatically)
ln -s ../.aide/docs/core/DOCUMENTATION_POLICY.md docs/DOCUMENTATION_POLICY.md
ln -s ../.aide/docs/core/CONTRIBUTING.md docs/CONTRIBUTING.md

# Or copy if you prefer (won't get updates)
cp .aide/docs/core/DOCUMENTATION_POLICY.md docs/
cp .aide/docs/core/CONTRIBUTING.md docs/
```

### 3. Copy Tech-Specific Standards

Copy and customize standards for your stack:

```bash
# Example: Node.js/TypeScript project
cp .aide/docs/examples/nodejs-typescript/TESTING_POLICY.md docs/
cp .aide/docs/examples/nodejs-typescript/CODING_GUIDELINES.md docs/
cp .aide/docs/examples/nodejs-typescript/DEVELOPMENT.md docs/

# Then customize these files for your project
```

### 4. Link Agent Primers

Agent primers are usually symlinked (universal across projects):

```bash
# Symlink entire agents directory
ln -s ../.aide/docs/agents docs/agents

# Or symlink individual primers
ln -s ../../.aide/docs/agents/IMPLEMENTATION_START.md docs/agents/
ln -s ../../.aide/docs/agents/PR_REVIEW_START.md docs/agents/
ln -s ../../.aide/docs/agents/DOC_REVIEW_START.md docs/agents/
# ... etc
```

### 5. Instantiate Templates

Create project-specific docs from templates:

```bash
# Implementation status tracker
cp .aide/docs/core/IMPLEMENTATION_STATUS.template.md docs/IMPLEMENTATION_STATUS.md

# Project summary
cp .aide/docs/core/PROJECT_SUMMARY.template.md docs/PROJECT_SUMMARY.md

# README
cp .aide/docs/core/README.template.md README.md
```

### 6. Configure AIDE Placeholders

**Recommended: Configuration Mapping Pattern**

Instead of copying AIDE files and manually replacing placeholders, keep AIDE generic and define mappings in your project's agent instructions:

```markdown
# Create/edit docs/AGENTS.md (or equivalent agent config file)

## AIDE Configuration (Placeholder Mappings)

This project uses the AIDE framework with the following constant mappings.
When reading AIDE primers (prefixed with `@`), mentally substitute these
values for `{{PLACEHOLDERS}}`:

### Project Identity
| AIDE Placeholder | Project Value |
|-----------------|---------------|
| `{{PROJECT_NAME}}` | MyAwesomeApp |
| `{{TECH_STACK}}` | Node.js 20, TypeScript 5.3, React 18 |
| `{{PROJECT_DOMAIN}}` | myawesomeapp.com |
| `{{MAIN_BRANCH}}` | main |

### Documentation Files
| AIDE Placeholder | Project File |
|-----------------|--------------|
| `{{IMPLEMENTATION_STATUS_DOC}}` | docs/IMPLEMENTATION_STATUS.md |
| `{{DEVELOPMENT_DOC}}` | docs/DEVELOPMENT.md |
| `{{CODING_GUIDELINES_DOC}}` | docs/CODING_GUIDELINES.md |
| `{{TESTING_POLICY_DOC}}` | docs/TESTING_POLICY.md |
| `{{CONTRIBUTING_DOC}}` | docs/CONTRIBUTING.md |
| `{{DOCUMENTATION_POLICY_DOC}}` | docs/DOCUMENTATION_POLICY.md |
| `{{BEST_PRACTICES_DOC}}` | docs/REACT_PATTERNS.md |
| `{{HIGH_LEVEL_VISION_DOC}}` | docs/VISION.md |
| `{{PROJECT_DESIGN_DOCS}}` | docs/architecture/ |

### Testing
| AIDE Placeholder | Project Value |
|-----------------|---------------|
| `{{UNIT_TEST_TYPE}}` | Jest unit tests |
| `{{INTEGRATION_TEST_TYPE}}` | Playwright e2e tests |
| `{{RUN_ALL_TESTS_COMMAND}}` | npm test |
| `{{RUN_UNIT_TESTS_COMMAND}}` | npm run test:unit |

## Agent Workflows (AIDE Framework)

@.aide/docs/agents/IMPLEMENTATION_START.md
@.aide/docs/agents/PR_REVIEW_START.md
...
```

**Benefits:**
- AIDE framework stays reusable (no project-specific content)
- AIDE updates propagate automatically (if using git submodule)
- Single source of truth for project paths
- DRY principle - no duplicating/replacing in multiple files
- Agents resolve placeholders by reading config first

**Alternative: Direct Replacement (Legacy)**

If you prefer, you can copy AIDE templates and manually replace placeholders:

1. Copy tech-specific files: `cp .aide/docs/examples/nodejs-typescript/*.md docs/`
2. Edit each file and find-replace `{{PLACEHOLDERS}}` with actual values
3. Commit modified copies to your repo

**Note:** This approach duplicates AIDE content and won't receive framework updates automatically.

### 7. Initialize Implementation Status

Edit `docs/IMPLEMENTATION_STATUS.md` to reflect your current project state:

```markdown
# Implementation Status

**Last Updated:** 2025-12-11

## Completed Systems
- Authentication (v1.0)
- User profiles (v1.0)

## In Progress
- Payment integration (Stripe)

## Planned Next Steps
- Admin dashboard
- Analytics integration
```

### 8. Commit Initial Setup

```bash
git add .aide/ docs/ README.md
git commit -m "Add AIDE framework for AI-assisted development

- Add AIDE as submodule
- Copy tech stack templates (Node.js/TypeScript)
- Initialize IMPLEMENTATION_STATUS and PROJECT_SUMMARY
- Configure agent primers

Framework provides:
- 7-step implementation workflow
- PR review process
- Documentation standards
- Testing policy"
```

## Onboarding Your AI Agent

Once setup is complete, share this with your AI assistant:

```
I've integrated the AIDE framework into this project. Please read:

1. docs/agents/IMPLEMENTATION_START.md - For implementing features
2. docs/agents/PR_REVIEW_START.md - For reviewing PRs
3. docs/IMPLEMENTATION_STATUS.md - Current project state
4. docs/CONTRIBUTING.md - Our workflow

Follow the 7-step implementation workflow for all changes.
```

## Verification Checklist

Ensure you have:

- [ ] `docs/DOCUMENTATION_POLICY.md` (symlinked or copied)
- [ ] `docs/CONTRIBUTING.md` (symlinked or copied)
- [ ] `docs/TESTING_POLICY.md` (copied and customized for your stack)
- [ ] `docs/CODING_GUIDELINES.md` (copied and customized for your stack)
- [ ] `docs/DEVELOPMENT.md` (copied and customized for your architecture)
- [ ] `docs/agents/` (symlinked directory or individual primer symlinks)
- [ ] `docs/IMPLEMENTATION_STATUS.md` (instantiated from template)
- [ ] `docs/PROJECT_SUMMARY.md` (instantiated from template)
- [ ] `README.md` (updated with project info)
- [ ] All `{{PLACEHOLDERS}}` replaced with actual values

## Common Customizations

### Using a Different Testing Framework

Edit `docs/TESTING_POLICY.md` and update:
- Framework name (Jest → Vitest, pytest → unittest, etc.)
- Test commands
- Test file locations
- Example test structure

### Using a Different Style Guide

Edit `docs/CODING_GUIDELINES.md` and update:
- Style guide reference link
- Language-specific conventions
- Linting tool configuration

### Adding Custom Agent Roles

Create new agent primers in `docs/agents/`:

```bash
cp docs/agents/AGENT_PRIMER_TEMPLATE.md docs/agents/MY_CUSTOM_AGENT.md
# Edit to define role, responsibilities, workflow
```

### Project-Specific Architecture

Edit `docs/DEVELOPMENT.md` to document:
- Your component structure
- Key modules/services
- Data flow patterns
- Deployment architecture

## Automation Scripts

AIDE provides helper scripts in `tools/`:

### Initialize New Project

```bash
# Create new project with AIDE pre-configured
./AIDE/tools/init-project.sh my-project python

# Available templates: godot-gdscript, nodejs-typescript, python, rust
```

### Update Submodule

```bash
# Pull latest AIDE updates
git submodule update --remote .aide
```

## Next Steps

1. **Read the 7-Step Workflow**: [docs/agents/IMPLEMENTATION_START.md](docs/agents/IMPLEMENTATION_START.md)
2. **Start Your First Feature**: Follow the workflow with your AI agent
3. **Review Your First PR**: Use [docs/agents/PR_REVIEW_START.md](docs/agents/PR_REVIEW_START.md)
4. **Customize Further**: Adapt templates to your team's needs

## Getting Help

- Check example implementations in `docs/examples/`
- Review case studies in main [README.md](README.md)
- Open an issue with questions or suggestions

## Tips for Success

### Do:
✅ Follow the 7-step workflow consistently
✅ Update IMPLEMENTATION_STATUS.md after every PR merge
✅ Use agent primers to guide AI behavior
✅ Customize templates to fit your team's style
✅ Keep documentation lean and reference-based

### Don't:
❌ Skip the codebase survey step
❌ Let AI agents modify tests without approval
❌ Duplicate information across multiple docs
❌ Work directly on main branch
❌ Merge PRs without review

---

**You're ready!** Start building with AI assistance using AIDE.
