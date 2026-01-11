#!/bin/bash

# Initial GitHub setup script
# Usage: ./scripts/setup_github.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔧 GitHub Setup for AE Copilot${NC}\n"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠️  Git is not installed. Please install it first.${NC}"
    exit 1
fi

# Initialize git if needed
if [ ! -d .git ]; then
    echo -e "${BLUE}📦 Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✅ Git initialized${NC}\n"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo -e "${BLUE}📝 Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
outputs/
data/*.db
data/*.json
!data/sample_*.json

# Secrets
.env
*.key
*.pem
secrets/

# Logs
*.log
logs/
EOF
    echo -e "${GREEN}✅ .gitignore created${NC}\n"
fi

# Add remote
echo -e "${BLUE}🔗 Setting up GitHub remote...${NC}"
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " repo_url

if [ ! -z "$repo_url" ]; then
    # Remove existing origin if present
    git remote remove origin 2>/dev/null || true
    git remote add origin "$repo_url"
    echo -e "${GREEN}✅ Remote added: $repo_url${NC}\n"
else
    echo -e "${YELLOW}⚠️  Skipping remote setup${NC}\n"
fi

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

# Initial commit
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
else
    echo -e "${BLUE}💾 Making initial commit...${NC}"
    git add .
    git commit -m "Initial commit: AE Copilot app"
    echo -e "${GREEN}✅ Initial commit created${NC}\n"
fi

echo -e "${GREEN}✨ Setup complete!${NC}\n"
echo -e "${BLUE}📝 Next steps:${NC}"
echo "  1. Review .gitignore to ensure sensitive files are excluded"
echo "  2. Run: ./scripts/push_to_github.sh"
echo "  3. Or manually: git push -u origin main"
