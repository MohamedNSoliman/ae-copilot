#!/bin/bash

# Automated GitHub push script for AE Copilot
# Usage: ./scripts/push_to_github.sh [commit message]

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AE Copilot - GitHub Push Automation${NC}\n"

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${YELLOW}⚠️  Git not initialized. Initializing...${NC}"
    git init
    echo -e "${GREEN}✅ Git initialized${NC}\n"
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo -e "${YELLOW}⚠️  No remote 'origin' found.${NC}"
    echo "Please add your GitHub repository:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo ""
    read -p "Enter your GitHub repository URL (or press Enter to skip): " repo_url
    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo -e "${GREEN}✅ Remote added${NC}\n"
    else
        echo -e "${YELLOW}⚠️  Skipping remote setup. Add it manually later.${NC}\n"
    fi
fi

# Get commit message
if [ -z "$1" ]; then
    read -p "Enter commit message (or press Enter for default): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Update AE Copilot app"
    fi
else
    commit_msg="$1"
fi

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    exit 0
fi

# Show status
echo -e "${BLUE}📊 Current status:${NC}"
git status --short
echo ""

# Add all changes
echo -e "${BLUE}➕ Adding changes...${NC}"
git add .

# Commit
echo -e "${BLUE}💾 Committing changes...${NC}"
git commit -m "$commit_msg"
echo -e "${GREEN}✅ Committed: $commit_msg${NC}\n"

# Get current branch
current_branch=$(git branch --show-current 2>/dev/null || echo "main")

# Push
echo -e "${BLUE}📤 Pushing to GitHub...${NC}"
if git push -u origin "$current_branch" 2>/dev/null; then
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}\n"
else
    echo -e "${YELLOW}⚠️  Push failed. Trying to set upstream...${NC}"
    git push --set-upstream origin "$current_branch" || {
        echo -e "${YELLOW}⚠️  Could not push. Make sure:${NC}"
        echo "  1. You have a GitHub repository set up"
        echo "  2. You have push permissions"
        echo "  3. Your remote URL is correct"
        exit 1
    }
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}\n"
fi

# Summary
echo -e "${GREEN}✨ All done!${NC}"
echo -e "${BLUE}📝 Repository:${NC} $(git remote get-url origin 2>/dev/null || echo 'Not set')"
echo -e "${BLUE}🌿 Branch:${NC} $current_branch"
echo -e "${BLUE}📦 Latest commit:${NC} $(git log -1 --oneline)"
echo ""
