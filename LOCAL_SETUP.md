# Local Development Setup Guide

## Complete Step-by-Step Instructions for Running the Project

### Prerequisites Check

Before starting, make sure you have:
- Python 3.8 or higher installed
- pip (comes with Python)
- A terminal/command prompt
- A text editor (VS Code, PyCharm, Sublime, etc.)

**Check your Python version:**
```bash
python3 --version
# or on Windows:
python --version
```

You should see something like: `Python 3.10.x` or higher

---

## Setup Instructions

### 1. Navigate to Project Directory

```bash
cd ~/Desktop/central-rock-tracker
# Or wherever you cloned/copied the project
```

### 2. Create Virtual Environment

A virtual environment keeps your project dependencies isolated.

**On macOS/Linux:**
```bash
python3 -m venv venv
```

**On Windows:**
```bash
python -m venv venv
```

This creates a `venv` folder in your project directory.

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Note**: If you get a PowerShell execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should see `(venv)` at the beginning of your terminal prompt when activated.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Django and other required packages.

**Verify installation:**
```bash
pip list
```

You should see Django 4.2.x in the list.

### 5. Set Up Database

Django uses migrations to create the database schema.

```bash
# Create migration files for the project app
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, project, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

This creates a file called `db.sqlite3` in your project root.

### 6. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- **Username**: Choose any username (e.g., "admin" or your name)
- **Email**: Your email address (optional, can skip)
- **Password**: Choose a strong password (you won't see it as you type)
- **Password (again)**: Confirm your password

**Example:**
```
Username: mbilko
Email address: mbilko@bu.edu
Password: ******** (hidden)
Password (again): ******** (hidden)
Superuser created successfully.
```

### 7. Run Development Server

```bash
python manage.py runserver
```

You should see:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 25, 2024 - 15:30:00
Django version 4.2.x, using settings 'central_rock_tracker.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 8. Access the Application

Open your web browser and go to:

- **Main Site**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/

**First time setup:**
1. Go to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Add some initial data:
   - Add Areas (e.g., "Main Wall", "Cave", "Overhang")
   - Add Routes with grades and colors
   - Optionally add more members

### 9. Register as a Regular User (Optional)

1. Go to http://127.0.0.1:8000/register/
2. Fill out the registration form
3. You'll be redirected to log in
4. Now you can browse and log route completions!

---

## Day-to-Day Development Workflow

### Starting Work

Every time you want to work on the project:

```bash
# 1. Navigate to project
cd ~/Desktop/central-rock-tracker

# 2. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 3. Start server
python manage.py runserver
```

### Stopping the Server

Press `CTRL+C` in the terminal running the server.

### Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

---

## Making Code Changes

### After Modifying Models

If you change anything in `project/models.py`:

```bash
# Create new migration
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

### After Modifying Static Files (CSS/JS)

If you're in production mode:
```bash
python manage.py collectstatic
```

For development (DEBUG=True), static files are served automatically.

### After Modifying Templates

Just refresh your browser - no commands needed!

### After Modifying Views/URLs

Just refresh your browser - the development server auto-reloads!

---

## Useful Django Management Commands

```bash
# Run the development server
python manage.py runserver

# Run on a different port
python manage.py runserver 8080

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell (interactive Python)
python manage.py shell

# Check for problems
python manage.py check

# Run tests
python manage.py test

# Show all migrations
python manage.py showmigrations

# Collect static files
python manage.py collectstatic
```

---

## Viewing Your Data

### Django Admin Interface

The easiest way to view and manage data:

1. Go to http://127.0.0.1:8000/admin/
2. Log in with superuser credentials
3. You can view/edit:
   - Members
   - Areas
   - Routes
   - Completions

### Django Shell

For programmatic access:

```bash
python manage.py shell
```

Then you can run Python code:
```python
from project.models import Member, Route, Area, Completion

# Get all routes
routes = Route.objects.all()
for route in routes:
    print(f"{route.name} - {route.grade}")

# Get a specific member
member = Member.objects.get(member_number=1001)
print(f"Member: {member.first_name} {member.last_name}")

# Get completions for a member
completions = member.completions.all()
print(f"Total completions: {completions.count()}")
```

---

## Troubleshooting

### "No module named 'django'"

Your virtual environment isn't activated or Django isn't installed.

**Solution:**
```bash
source venv/bin/activate  # Activate venv
pip install -r requirements.txt
```

### "Table doesn't exist" errors

You haven't run migrations.

**Solution:**
```bash
python manage.py migrate
```

### Port 8000 already in use

Another process is using port 8000.

**Solution:**
```bash
# Use a different port
python manage.py runserver 8080

# Or find and kill the process using port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
# Then use Task Manager to end that process
```

### Database is locked

SQLite doesn't handle concurrent access well.

**Solution:**
```bash
# Stop all running Django servers
# Delete db.sqlite3
rm db.sqlite3
# Recreate database
python manage.py migrate
python manage.py createsuperuser
```

### Changes not showing up

**Solution:**
- Make sure you saved the file
- Hard refresh browser: CTRL+F5 (or CMD+SHIFT+R on Mac)
- Check terminal for errors
- Restart the development server

### Static files not loading

**Solution:**
Make sure `DEBUG = True` in `central_rock_tracker/settings.py`

---

## Testing Your Application

### Manual Testing Checklist

1. **Registration**: Can new users sign up?
2. **Login**: Can users log in?
3. **View Routes**: Can users see all routes?
4. **Log Completion**: Can users log route completions?
5. **View Profile**: Can users see their profile and stats?
6. **Admin Functions**: Can admins add routes?

### Automated Tests

Create tests in `project/tests.py`:

```python
from django.test import TestCase
from .models import Area, Route

class RouteModelTest(TestCase):
    def setUp(self):
        self.area = Area.objects.create(name="Test Area")
        self.route = Route.objects.create(
            name="Test Route",
            grade="V3",
            color="blue",
            area=self.area,
            setter_name="Test Setter",
            date_set="2024-01-01"
        )
    
    def test_route_str(self):
        self.assertEqual(str(self.route), "Test Route (V3)")
```

Run tests:
```bash
python manage.py test
```

---

## Next Steps

1. **Add Sample Data**: Use the admin interface to add routes and areas
2. **Customize**: Modify templates and CSS to match your preferences
3. **Add Features**: Implement the TODO items throughout the code
4. **Deploy**: Eventually deploy to a production server (Heroku, PythonAnywhere, etc.)

---

## Quick Reference Card

```bash
# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations
python manage.py migrate

# Access Points
http://127.0.0.1:8000/          # Main site
http://127.0.0.1:8000/admin/    # Admin interface

# Stop server: CTRL+C
# Deactivate venv: deactivate
```

---

## Getting Help

- **Django Documentation**: https://docs.djangoproject.com/
- **Django Tutorial**: https://docs.djangoproject.com/en/4.2/intro/tutorial01/
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/django

Good luck with your project! 🧗‍♀️
