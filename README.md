# Central Rock Gym Route Tracking System

A Django-based web application for tracking climbing routes and member progress at Central Rock Gym Fenway.

**Author:** Michele Bilko  
**Contact:** mbilko@bu.edu

## Features

- **Route Management**: Add, view, and manage climbing routes with grades, colors, and areas
- **Member Profiles**: Track individual climbing progress and statistics
- **Completion Tracking**: Log route completions with ratings and notes
- **Area Organization**: Organize routes by gym areas
- **Admin Dashboard**: Comprehensive admin tools for gym staff
- **Statistics**: View grade distributions, area statistics, and progress tracking

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (development), PostgreSQL-ready
- **Frontend**: HTML/CSS/JavaScript
- **Python**: 3.8+

## Project Structure

```
central-rock-tracker/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── central_rock_tracker/        # Main project configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
└── project/                     # Main application
    ├── __init__.py
    ├── admin.py                # Admin interface configuration
    ├── apps.py                 # App configuration
    ├── forms.py                # Form definitions
    ├── models.py               # Database models
    ├── urls.py                 # App URL patterns
    ├── views.py                # View functions
    ├── tests.py                # Test cases
    ├── static/                 # Static files (CSS, JS, images)
    │   └── project/
    │       └── css/
    │           └── styles.css
    └── templates/              # HTML templates
        └── project/
            ├── base.html
            ├── home.html
            ├── login.html
            ├── register.html
            └── ...
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/central-rock-tracker.git
cd central-rock-tracker
```

### Step 2: Create a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Step 6: Load Initial Data (Optional)

If you have fixture data:
```bash
python manage.py loaddata initial_data.json
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Usage

### Accessing the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/

### User Roles

1. **Regular Members**:
   - View routes and areas
   - Log route completions
   - View personal statistics
   - Edit profile

2. **Admin Users** (staff):
   - All member features
   - Add/manage routes
   - Archive routes
   - View all completions
   - Manage member accounts

### Creating Sample Data

To test the application with sample data, you can use the Django admin interface:

1. Go to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Add Areas (e.g., "Main Wall", "Cave", "Overhang")
4. Add Routes with grades, colors, and areas
5. Add Members (or register through the site)

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

For production deployment:
```bash
python manage.py collectstatic
```

### Adding Custom CSS

Edit or create: `project/static/project/css/styles.css`

Then run:
```bash
python manage.py collectstatic
```

## Common Issues & Troubleshooting

### Issue: "No module named 'django'"
**Solution**: Make sure your virtual environment is activated and Django is installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete `db.sqlite3` and run migrations again:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Static files not loading
**Solution**: Make sure DEBUG=True in settings.py for development, or run collectstatic:
```bash
python manage.py collectstatic
```

## Future Enhancements

- [ ] Add route photos/images
- [ ] Implement route difficulty consensus system
- [ ] Add social features (following, comments)
- [ ] Mobile app integration via REST API
- [ ] Route beta/tips section
- [ ] Progress tracking charts and visualizations
- [ ] Email notifications for new routes
- [ ] Export data (CSV, PDF)
- [ ] Advanced filtering and search
- [ ] Route recommendation system

## Contributing

This is a personal project, but suggestions and feedback are welcome! Feel free to open an issue or reach out.

## License

This project was created as a CS412 final project and is being developed further as a personal project.

## Contact

**Michele Bilko**  
Email: mbilko@bu.edu  
GitHub: [Your GitHub Profile]

## Acknowledgments

- Originally created as a CS412 final project at Boston University
- Central Rock Gym Fenway for inspiration
- Django community for excellent documentation
