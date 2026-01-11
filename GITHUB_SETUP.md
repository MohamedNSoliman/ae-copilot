# GitHub Setup & Automation Guide

This guide will help you push your AE Copilot app to GitHub and set up automated workflows.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run initial setup
./scripts/setup_github.sh
```

This will:
- Initialize git repository
- Create `.gitignore`
- Set up GitHub remote
- Make initial commit

### Option 2: Manual Setup

1. **Create GitHub repository:**
   - Go to https://github.com/new
   - Name it (e.g., `ae-copilot`)
   - Don't initialize with README (we already have files)

2. **Initialize git:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AE Copilot app"
   ```

3. **Add remote:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```

---

## 📦 Automated Push Script

After initial setup, use the automated push script:

```bash
# With custom message
./scripts/push_to_github.sh "Added new ROI calculator feature"

# With default message
./scripts/push_to_github.sh
```

The script will:
- ✅ Check for changes
- ✅ Add all files
- ✅ Commit with your message
- ✅ Push to GitHub
- ✅ Show summary

---

## 🔄 GitHub Actions Workflows

I've set up automated workflows in `.github/workflows/`:

### 1. **deploy.yml** - Testing & Deployment
- Runs on every push to `main`/`master`
- Tests your code
- Runs linting
- Creates deployment artifacts

### 2. **streamlit-cloud.yml** - Streamlit Cloud Deployment
- Reminds you to deploy to Streamlit Cloud
- Runs on push or manual trigger

---

## 🌐 Deploy to Streamlit Cloud (Free!)

1. **Push your code to GitHub** (use the script above)

2. **Go to Streamlit Cloud:**
   - Visit https://share.streamlit.io
   - Sign in with GitHub

3. **Deploy:**
   - Click "New app"
   - Select your repository
   - Set main file: `ae_copilot_app.py`
   - Click "Deploy"

4. **Add secrets (optional):**
   - Go to app settings
   - Add secrets for API keys:
     ```
     GONG_ACCESS_KEY=your_key
     GONG_ACCESS_SECRET=your_secret
     HUBSPOT_PRIVATE_APP_TOKEN=your_token
     ```

---

## 🔐 Security Best Practices

### ✅ What's Already Ignored (in `.gitignore`):
- API keys and secrets
- Database files
- Output files
- Virtual environments
- IDE files

### ⚠️ Never Commit:
- `.env` files
- API keys in code
- Database files with real data
- Personal credentials

### ✅ Safe to Commit:
- Sample data files (`data/sample_*.json`)
- Source code
- Configuration templates
- Documentation

---

## 📝 Common Git Commands

```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push

# Pull latest changes
git pull

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## 🛠️ Troubleshooting

### "Remote origin already exists"
```bash
git remote remove origin
git remote add origin YOUR_NEW_URL
```

### "Permission denied"
- Make sure you have push access to the repository
- Check your GitHub authentication (SSH keys or HTTPS token)

### "Nothing to commit"
- All changes are already committed
- Check if files are in `.gitignore`

### Scripts won't run
```bash
chmod +x scripts/*.sh
```

---

## 🎯 Workflow Example

```bash
# 1. Make changes to your code
# ... edit files ...

# 2. Test locally
streamlit run ae_copilot_app.py

# 3. Push to GitHub
./scripts/push_to_github.sh "Fixed ROI calculation bug"

# 4. Check GitHub Actions
# Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions

# 5. Deploy to Streamlit Cloud (if needed)
# Changes auto-deploy if connected
```

---

## 📚 Additional Resources

- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Docs](https://docs.github.com/)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)

---

## ✅ Checklist

Before pushing:
- [ ] Review `.gitignore` - no secrets committed
- [ ] Test app locally
- [ ] Commit message is descriptive
- [ ] GitHub repository exists
- [ ] Remote is configured

After pushing:
- [ ] Check GitHub Actions (green ✅)
- [ ] Verify files on GitHub
- [ ] Deploy to Streamlit Cloud (optional)

---

**Need help?** Check the scripts - they have helpful error messages!
