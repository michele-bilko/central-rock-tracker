# 🖥️ Terminal Commands Cheat Sheet

Quick reference for all the commands you'll need for this project.

---

## 📂 Navigation Commands

```bash
# Print current directory
pwd

# List files in current directory
ls              # macOS/Linux
dir             # Windows

# List files with details
ls -la          # macOS/Linux
dir /A          # Windows

# Change directory
cd project-name

# Go up one level
cd ..

# Go to home directory
cd ~            # macOS/Linux
cd %USERPROFILE%  # Windows

# Go to Desktop
cd ~/Desktop    # macOS/Linux
cd %USERPROFILE%\Desktop  # Windows
```

---

## 🐍 Python & Virtual Environment

```bash
# Check Python version
python3 --version   # macOS/Linux
python --version    # Windows

# Check pip version
pip --version

# Create virtual environment
python3 -m venv venv    # macOS/Linux
python -m venv venv     # Windows

# Activate virtual environment
source venv/bin/activate          # macOS/Linux Bash
source venv/bin/activate.fish     # macOS/Linux Fish shell
venv\Scripts\activate             # Windows Command Prompt
venv\Scripts\Activate.ps1         # Windows PowerShell

# Deactivate virtual environment
deactivate

# Install packages from requirements.txt
pip install -r requirements.txt

# Install a single package
pip install package-name

# List installed packages
pip list

# Freeze current packages to requirements.txt
pip freeze > requirements.txt

# Upgrade pip
pip install --upgrade pip
```

---

## 🎯 Django Commands

### Database & Migrations

```bash
# Create migration files
python manage.py makemigrations

# Create migrations for specific app
python manage.py makemigrations project

# Apply migrations
python manage.py migrate

# Show all migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name migration_name

# Check for problems
python manage.py check
```

### User Management

```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username
```

### Server & Development

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on specific host and port
python manage.py runserver 0.0.0.0:8000

# Stop server
# Press Ctrl+C in the terminal
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic

# Collect without prompting
python manage.py collectstatic --noinput

# Clear collected static files
python manage.py collectstatic --clear
```

### Shell & Testing

```bash
# Open Django shell
python manage.py shell

# Run tests
python manage.py test

# Run tests for specific app
python manage.py test project

# Run tests with verbosity
python manage.py test --verbosity=2
```

### Data Management

```bash
# Load data from fixture
python manage.py loaddata fixture_name.json

# Dump data to fixture
python manage.py dumpdata > fixture_name.json

# Dump specific app data
python manage.py dumpdata project > project_data.json

# Dump data with indentation
python manage.py dumpdata --indent 2 > data.json
```

### Other Useful Commands

```bash
# Show all available commands
python manage.py help

# Get help for specific command
python manage.py help migrate

# Clear sessions
python manage.py clearsessions

# Create new app
python manage.py startapp app_name
```

---

## 📚 Git Commands

### Initial Setup

```bash
# Initialize new repository
git init

# Clone existing repository
git clone https://github.com/username/repo.git

# Check Git version
git --version
```

### Basic Workflow

```bash
# Check status
git status

# Add files to staging
git add filename.py
git add .              # Add all changes
git add -A             # Add all changes (alternative)

# Commit changes
git commit -m "Commit message"

# Push to remote
git push

# Push to specific branch
git push origin main

# Pull from remote
git pull
git pull origin main
```

### Branches

```bash
# List branches
git branch

# Create new branch
git branch branch-name

# Switch to branch
git checkout branch-name

# Create and switch to new branch
git checkout -b branch-name

# Delete branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Merge branch into current
git merge branch-name
```

### Remote Management

```bash
# List remotes
git remote -v

# Add remote
git remote add origin https://github.com/username/repo.git

# Change remote URL
git remote set-url origin https://github.com/username/new-repo.git

# Remove remote
git remote remove origin
```

### History & Inspection

```bash
# View commit history
git log

# View compact history
git log --oneline

# View changes
git diff

# View staged changes
git diff --staged

# View specific file history
git log filename
```

### Undoing Changes

```bash
# Discard changes in working directory
git checkout -- filename

# Unstage file
git reset filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert commit-hash
```

### Stashing

```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove stash
git stash pop

# Clear all stashes
git stash clear
```

---

## 🔍 File Operations

```bash
# Create file
touch filename.txt      # macOS/Linux
type nul > filename.txt # Windows

# Create directory
mkdir directory-name

# Remove file
rm filename            # macOS/Linux
del filename           # Windows

# Remove directory
rm -r directory        # macOS/Linux
rmdir /s directory     # Windows

# Copy file
cp source dest         # macOS/Linux
copy source dest       # Windows

# Move/rename file
mv old new             # macOS/Linux
move old new           # Windows

# View file contents
cat filename           # macOS/Linux
type filename          # Windows

# View file with pagination
less filename          # macOS/Linux
more filename          # Windows
```

---

## 🛠️ System & Process Commands

```bash
# Clear terminal screen
clear                  # macOS/Linux
cls                    # Windows

# Find process using port
lsof -ti:8000         # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process by PID
kill -9 PID           # macOS/Linux
taskkill /PID PID /F  # Windows

# Check disk usage
df -h                 # macOS/Linux
wmic logicaldisk get size,freespace,caption  # Windows

# Current user
whoami

# List environment variables
env                   # macOS/Linux
set                   # Windows

# Exit terminal
exit
```

---

## 💡 Project-Specific Quick Commands

### Daily Development Workflow

```bash
# 1. Navigate to project
cd ~/Desktop/central-rock-tracker

# 2. Activate venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Start server
python manage.py runserver

# When done: Ctrl+C then
deactivate
```

### After Modifying Models

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Saving Work to GitHub

```bash
git status
git add .
git commit -m "Description of changes"
git push
```

### Reset Database (if needed)

```bash
# macOS/Linux
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser

# Windows
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🆘 Troubleshooting Commands

```bash
# Check what's running on port 8000
lsof -i :8000                    # macOS/Linux
netstat -ano | findstr :8000     # Windows

# Verify Python packages
pip list | grep Django           # macOS/Linux
pip list | findstr Django        # Windows

# Check virtual environment is activated
which python                     # macOS/Linux (should show venv path)
where python                     # Windows (should show venv path)

# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check Django version
python -m django --version

# Validate Django project
python manage.py check
```

---

## 📝 Notes

- Always activate your virtual environment before running Django commands
- Look for `(venv)` in your terminal prompt
- Use Ctrl+C to stop the development server
- Use `exit` to close the terminal
- Tab key autocompletes file/directory names
- Up arrow recalls previous commands

---

## 🎯 Most Common Commands

You'll use these 90% of the time:

```bash
cd central-rock-tracker
source venv/bin/activate
python manage.py runserver
git status
git add .
git commit -m "message"
git push
```

Save this file for quick reference! 📌
