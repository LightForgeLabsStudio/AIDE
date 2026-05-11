#!/usr/bin/env bash
# Install AIDE skills for Claude (repo-local .claude/skills)

set -e

echo -e "\033[0;36mInstalling AIDE skills for Claude...\033[0m"

# This script lives in: <consumer-repo>/.aide/skills/
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AIDE_SKILLS_DIR="$SCRIPT_DIR"
AIDE_REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -d "$AIDE_SKILLS_DIR" ]; then
    echo -e "\033[0;31mError: AIDE skills directory not found: $AIDE_SKILLS_DIR\033[0m"
    exit 1
fi

# Default to the repo that contains the .aide submodule
REPO_ROOT="$(dirname "$AIDE_REPO_DIR")"
SKILLS_PATH="$REPO_ROOT/.claude/skills"

# Parse arguments
SYMLINK=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --symlink|-s)
            SYMLINK=true
            shift
            ;;
        --repo-root)
            REPO_ROOT="$2"
            SKILLS_PATH="$REPO_ROOT/.claude/skills"
            shift 2
            ;;
        --skills-path)
            SKILLS_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: install-claude.sh [--symlink] [--repo-root PATH] [--skills-path PATH]"
            exit 1
            ;;
    esac
done

echo -e "\033[0;37mRepo root: $REPO_ROOT\033[0m"
echo -e "\033[0;37mTarget Claude skills dir: $SKILLS_PATH\033[0m"

# Create target directory if it doesn't exist
if [ ! -d "$SKILLS_PATH" ]; then
    echo -e "\033[0;33mCreating skills directory: $SKILLS_PATH\033[0m"
    mkdir -p "$SKILLS_PATH"
fi

# Count and install skills
SKILL_COUNT=0

for skill_dir in "$AIDE_SKILLS_DIR"/*/; do
    # Skip dist directory
    if [ "$(basename "$skill_dir")" = "dist" ]; then
        continue
    fi

    # Check if SKILL.md exists
    if [ ! -f "$skill_dir/SKILL.md" ]; then
        continue
    fi

    SKILL_NAME=$(basename "$skill_dir")
    TARGET_PATH="$SKILLS_PATH/$SKILL_NAME"

    if [ "$SYMLINK" = true ]; then
        # Create symlink
        if [ -d "$TARGET_PATH" ]; then
            echo -e "\033[0;33m  Removing existing: $SKILL_NAME\033[0m"
            rm -rf "$TARGET_PATH"
        fi

        echo -e "\033[0;36m  Symlinking: $SKILL_NAME\033[0m"
        ln -s "$skill_dir" "$TARGET_PATH"
    else
        # Copy files
        if [ -d "$TARGET_PATH" ]; then
            echo -e "\033[0;33m  Updating: $SKILL_NAME\033[0m"
            rm -rf "$TARGET_PATH"
        else
            echo -e "\033[0;32m  Installing: $SKILL_NAME\033[0m"
        fi

        cp -r "$skill_dir" "$TARGET_PATH"
    fi

    SKILL_COUNT=$((SKILL_COUNT + 1))
done

if [ $SKILL_COUNT -eq 0 ]; then
    echo -e "\033[0;33mWarning: No skills found in $AIDE_SKILLS_DIR\033[0m"
    exit 0
fi

echo -e "\033[0;32m\nInstallation complete!\033[0m"
echo ""
echo -e "\033[0;36mInstalled skills (repo-local .claude/skills):\033[0m"
for skill_dir in "$AIDE_SKILLS_DIR"/*/; do
    if [ "$(basename "$skill_dir")" = "dist" ]; then
        continue
    fi
    if [ -f "$skill_dir/SKILL.md" ]; then
        echo -e "\033[0;37m  /$(basename "$skill_dir")\033[0m"
    fi
done
echo ""
echo -e "\033[0;33mNext steps:\033[0m"
echo "  1. Reload your tool (VS Code: Ctrl+Shift+P -> 'Reload Window')"
echo "  2. Type '/' in Claude chat to see available commands"
echo ""

if [ "$SYMLINK" = false ]; then
    echo -e "\033[0;37mNote: Skills were copied. To auto-sync with AIDE updates, re-run with --symlink\033[0m"
fi
