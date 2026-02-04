#!/bin/bash
# AIDE Project Initialization Script
#
# Usage: ./init-project.sh <project-name> <tech-stack>
# Example: ./init-project.sh my-app nodejs-typescript

set -e

PROJECT_NAME=$1
TECH_STACK=$2
AIDE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -z "$PROJECT_NAME" ] || [ -z "$TECH_STACK" ]; then
    echo "Usage: ./init-project.sh <project-name> <tech-stack>"
    echo ""
    echo "Available tech stacks:"
    echo "  - godot-gdscript"
    echo "  - nodejs-typescript"
    echo "  - python"
    echo "  - rust"
    exit 1
fi

EXAMPLE_DIR="$AIDE_DIR/docs/examples/$TECH_STACK"

if [ ! -d "$EXAMPLE_DIR" ]; then
    echo "Error: Tech stack '$TECH_STACK' not found."
    echo "Available: godot-gdscript, nodejs-typescript, python, rust"
    exit 1
fi

echo "📦 Initializing AIDE project: $PROJECT_NAME ($TECH_STACK)"
echo ""

# Create project directory
mkdir -p "$PROJECT_NAME/docs/agents"
cd "$PROJECT_NAME"

echo "✓ Created project directory"

# Initialize git
git init
echo "✓ Initialized git repository"

# Add AIDE as submodule
git submodule add "$AIDE_DIR" .aide
echo "✓ Added AIDE as git submodule"

# Symlink core docs
ln -s ../.aide/docs/core/DOCUMENTATION_POLICY.md docs/DOCUMENTATION_POLICY.md
ln -s ../.aide/docs/core/CONTRIBUTING.md docs/CONTRIBUTING.md
echo "✓ Symlinked core documentation"

# Copy tech-specific docs
cp ".aide/docs/examples/$TECH_STACK/TESTING_POLICY.md" docs/
cp ".aide/docs/examples/$TECH_STACK/CODING_GUIDELINES.md" docs/
echo "✓ Copied $TECH_STACK documentation templates"

# Symlink agent primers
ln -s ../../.aide/docs/agents/IMPLEMENTATION_START.md docs/agents/
ln -s ../../.aide/docs/agents/PR_REVIEW_START.md docs/agents/
ln -s ../../.aide/docs/agents/DOC_REVIEW_START.md docs/agents/
ln -s ../../.aide/docs/agents/CODEBASE_REVIEW_START.md docs/agents/
ln -s ../../.aide/docs/agents/DESIGN_WORKSHOP_START.md docs/agents/
ln -s ../../.aide/docs/agents/design/DESIGN_SPEC_REFERENCE.md docs/agents/
ln -s ../../.aide/docs/agents/AGENT_PRIMER_TEMPLATE.md docs/agents/
echo "✓ Symlinked agent primers"

# Copy templates
cp .aide/docs/core/IMPLEMENTATION_STATUS.template.md docs/IMPLEMENTATION_STATUS.md
cp .aide/docs/core/PROJECT_SUMMARY.template.md docs/PROJECT_SUMMARY.md
cp .aide/docs/core/README.template.md README.md
echo "✓ Copied project templates"

# Create design directory
mkdir -p docs/design
echo "✓ Created design directory"

# Initial commit
git add .
git commit -m "Initial commit: Add AIDE framework

- Add AIDE as submodule
- Copy $TECH_STACK templates
- Initialize documentation structure

Generated with AIDE init-project.sh"
echo "✓ Created initial commit"

echo ""
echo "🎉 Project initialized successfully!"
echo ""
echo "Next steps:"
echo "  1. cd $PROJECT_NAME"
echo "  2. Edit docs/IMPLEMENTATION_STATUS.md (replace {{PLACEHOLDERS}})"
echo "  3. Edit docs/PROJECT_SUMMARY.md (replace {{PLACEHOLDERS}})"
echo "  4. Edit README.md (replace {{PLACEHOLDERS}})"
echo "  5. Start building with: docs/agents/IMPLEMENTATION_START.md"
echo ""
