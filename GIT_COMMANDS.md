# Git Commands for GitHub Update 🚀

## Step-by-Step Guide

### 1. Check Current Status

```bash
git status
```

This shows all modified and new files.

---

### 2. Add All Changes

```bash
git add .
```

Or add specific files:
```bash
git add README.md
git add requirements.txt
git add carbon_tracker/settings.py
git add build.sh
git add render.yaml
```

---

### 3. Commit Changes

```bash
git commit -m "feat: Prepare for production deployment

- Add Render.com deployment configuration
- Update settings for production (PostgreSQL, WhiteNoise)
- Remove test credentials from README for security
- Add comprehensive deployment guides
- Add security documentation
- Update dependencies for production
- Configure environment variables
- Add build script for Render
"
```

Or shorter version:
```bash
git commit -m "feat: Production ready - Render deployment + security updates"
```

---

### 4. Push to GitHub

```bash
git push origin main
```

Or if your branch is named differently:
```bash
git push origin master
```

---

## Complete Command Sequence

Copy and paste these commands one by one:

```bash
# 1. Check status
git status

# 2. Add all changes
git add .

# 3. Commit with message
git commit -m "feat: Production ready - Render deployment + security updates"

# 4. Push to GitHub
git push origin main
```

---

## If You Haven't Initialized Git Yet

```bash
# 1. Initialize Git
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: Academia Carbon v2.0"

# 4. Add remote (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/academia-carbon.git

# 5. Set branch name
git branch -M main

# 6. Push
git push -u origin main
```

---

## If You Get Errors

### Error: "fatal: not a git repository"

**Solution:**
```bash
git init
git remote add origin https://github.com/yourusername/academia-carbon.git
```

### Error: "rejected - non-fast-forward"

**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

### Error: "Permission denied (publickey)"

**Solution:**
1. Check your SSH key: `ssh -T git@github.com`
2. Or use HTTPS instead: `git remote set-url origin https://github.com/yourusername/academia-carbon.git`

### Error: "Updates were rejected"

**Solution:**
```bash
git pull origin main
git push origin main
```

---

## Verify Upload

After pushing, check:

1. Go to your GitHub repository
2. Refresh the page
3. Check that all files are updated
4. Look at the commit history

---

## Create a Release (Optional)

### 1. Tag the Version

```bash
git tag -a v2.0.0 -m "Academia Carbon v2.0.0 - Production Ready"
git push origin v2.0.0
```

### 2. Create Release on GitHub

1. Go to your repository on GitHub
2. Click "Releases"
3. Click "Create a new release"
4. Select tag: `v2.0.0`
5. Title: `Academia Carbon v2.0.0`
6. Description: Copy from CHANGELOG.md
7. Click "Publish release"

---

## Files Being Updated

### New Files
- ✅ build.sh
- ✅ render.yaml
- ✅ .env.example
- ✅ LICENSE
- ✅ CONTRIBUTING.md
- ✅ CHANGELOG.md
- ✅ SECURITY.md
- ✅ SECURITY_NOTES.md
- ✅ INSTALLATION.md
- ✅ RENDER_DEPLOY.md
- ✅ DEPLOYMENT_CHECKLIST.md
- ✅ GITHUB_READY.md

### Modified Files
- ✅ README.md (removed test credentials)
- ✅ requirements.txt (added production dependencies)
- ✅ carbon_tracker/settings.py (production configuration)
- ✅ .gitignore (added .env and render files)
- ✅ templates/auth/login.html (Google login button)

---

## After Pushing to GitHub

### 1. Check Repository

Visit: `https://github.com/yourusername/academia-carbon`

### 2. Update Repository Settings

- Add description
- Add topics/tags
- Enable issues
- Enable discussions
- Enable wiki

### 3. Add Topics

```
django
python
carbon-tracking
ghg-emissions
sustainability
climate-change
academic
environmental
emission-factors
carbon-footprint
render
postgresql
```

### 4. Update About Section

```
Django web application for tracking and calculating greenhouse gas (GHG) emissions. 
Designed for academic institutions and research organizations. 
Features country-specific emission factors and comprehensive Scope 1, 2, 3 tracking.
```

---

## Next Steps After GitHub Update

### 1. Deploy to Render

Follow: `RENDER_DEPLOY.md`

### 2. Share Your Project

- Tweet about it
- Post on LinkedIn
- Share on Reddit (r/django, r/Python)
- Submit to Product Hunt

### 3. Monitor

- Watch for issues
- Respond to pull requests
- Update documentation

---

## Quick Reference

### Most Common Commands

```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest
git pull origin main

# View history
git log --oneline

# Create branch
git checkout -b feature-name

# Switch branch
git checkout main
```

---

## Commit Message Guidelines

### Format

```
type: subject

body (optional)

footer (optional)
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples

```bash
git commit -m "feat: Add Google OAuth login"
git commit -m "fix: Resolve database connection issue"
git commit -m "docs: Update installation guide"
git commit -m "chore: Update dependencies"
```

---

## Summary

**Ready to push?** Run these commands:

```bash
git add .
git commit -m "feat: Production ready - Render deployment + security updates"
git push origin main
```

**That's it!** Your code is now on GitHub! 🎉

---

**Date**: November 24, 2025  
**Version**: 2.0.0  
**Status**: Ready to Push ✅
