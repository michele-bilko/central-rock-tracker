# GitHub Setup Guide for Central Rock Tracker

## Step-by-Step Instructions

### 1. Navigate to Your Project Directory

First, open your terminal and navigate to where you want to work on this project:

```bash
cd ~/Desktop  # or wherever you want to keep the project
```

### 2. Copy the Project Files

If you've created the project structure using Claude, copy it to your desired location:

```bash
# If the project is in /home/claude/central-rock-tracker
cp -r /home/claude/central-rock-tracker ~/Desktop/central-rock-tracker
cd ~/Desktop/central-rock-tracker
```

### 3. Initialize Git Repository

```bash
# Initialize a new Git repository
git init

# Add all files to staging
git add .

# Create your first commit
git commit -m "Initial commit: Central Rock Gym Route Tracking System"
```

### 4. Create a GitHub Repository

1. Go to https://github.com
2. Log in to your account
3. Click the "+" icon in the top right corner
4. Select "New repository"
5. Fill in the details:
   - **Repository name**: `central-rock-tracker`
   - **Description**: "Django web app for tracking climbing routes at Central Rock Gym"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 5. Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see instructions. Use these commands:

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/central-rock-tracker.git

# Verify the remote was added
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 6. Verify Upload

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/central-rock-tracker`
2. You should see all your files listed
3. The README.md should be displayed on the main page

## Future Git Workflow

### Making Changes

After making changes to your code:

```bash
# Check what files have changed
git status

# Add specific files
git add filename.py

# Or add all changed files
git add .

# Commit with a descriptive message
git commit -m "Add feature: route photo upload"

# Push to GitHub
git push
```

### Creating Feature Branches

For larger features, use branches:

```bash
# Create and switch to a new branch
git checkout -b feature/route-photos

# Make your changes...
# Then commit
git add .
git commit -m "Implement route photo upload"

# Push the branch to GitHub
git push -u origin feature/route-photos

# On GitHub, create a Pull Request to merge into main
```

### Pulling Latest Changes

If you work on multiple computers or collaborate:

```bash
# Pull the latest changes
git pull origin main
```

## Common Git Commands Reference

```bash
# Check repository status
git status

# View commit history
git log

# View differences
git diff

# Create a new branch
git branch branch-name

# Switch branches
git checkout branch-name

# Merge a branch into current branch
git merge branch-name

# Delete a branch
git branch -d branch-name

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD
```

## Tips

1. **Commit Often**: Make small, focused commits with clear messages
2. **Use Branches**: Create branches for new features or experiments
3. **Write Good Commit Messages**: 
   - Start with a verb (Add, Fix, Update, Remove)
   - Keep it under 50 characters
   - Be specific: "Fix login validation bug" not "Fix bug"
4. **Don't Commit Sensitive Data**: Never commit passwords, API keys, or secrets
5. **Use .gitignore**: Make sure db.sqlite3, venv/, and other local files are ignored

## GitHub Repository Settings

### Recommended Settings

1. **Add a License**: Go to your repo → Add file → Create new file → name it "LICENSE"
2. **Enable Issues**: Settings → Features → Issues (for bug tracking)
3. **Add Topics**: Add relevant topics like `django`, `python`, `climbing`, `web-app`
4. **Add a Description**: Click the gear icon next to "About" on the right side

### Repository Description Example

```
🧗 Django web application for tracking climbing routes and member progress at Central Rock Gym
```

**Topics**: `django` `python` `climbing` `web-app` `sqlite` `route-tracking`

## Troubleshooting

### "Permission denied (publickey)"

You need to set up SSH keys. Instead, use HTTPS:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/central-rock-tracker.git
```

### "Failed to push some refs"

Pull first, then push:
```bash
git pull origin main --rebase
git push origin main
```

### Accidentally Committed Sensitive Data

```bash
# Remove file from Git but keep it locally
git rm --cached filename

# Add to .gitignore
echo "filename" >> .gitignore

# Commit the change
git commit -m "Remove sensitive file from tracking"
git push
```

For more serious cases, use `git filter-branch` or BFG Repo-Cleaner.
