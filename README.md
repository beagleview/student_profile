# Student Management System

A Django-based student management system that allows teachers to manage student data including photos, personal information, and academic details.

## Features

- **Student Data Management**: Store student photos, first name, last name, sex, date of birth, level, and room
- **Photo Upload**: Support for JPG, JPEG, and PNG image uploads
- **Admin Interface**: Complete Django admin interface for teachers
- **Advanced Filtering**: Filter students by level, room, sex, and dates
- **Search Functionality**: Search students by name
- **Bulk Operations**: Move multiple students between levels
- **Responsive Design**: Admin interface works on desktop and mobile

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone or create the project directory**
   ```bash
   mkdir student_management
   cd student_management
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv student_env
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   student_env\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source student_env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations to create the database**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser account (teacher account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/admin/`
   - Log in with your superuser credentials

## Usage

### For Teachers (Admin Users)

1. **Adding Students**
   - Go to Students > Students > Add student
   - Fill in all required information
   - Upload a student photo (optional)
   - Save the student record

2. **Viewing Students**
   - Go to Students > Students
   - See all students in a table format with photos
   - View creation and update timestamps

3. **Filtering Students**
   - Use the right sidebar filters to filter by:
     - Academic Level (1-6)
     - Room (1-6)
     - Gender (Male, Female, Other)
     - Creation date
     - Update date
     - Date of birth

4. **Searching Students**
   - Use the search box to find students by first or last name

5. **Bulk Operations**
   - Select multiple students using checkboxes
   - Use the "Actions" dropdown to:
     - Move selected students to Level 1
     - Move selected students to Level 2
     - (More actions can be added as needed)

### Student Data Fields

- **Photo**: Student photograph (JPG, JPEG, PNG)
- **First Name**: Student's first name (required)
- **Last Name**: Student's last name (required)
- **Sex**: Gender selection (Male, Female, Other)
- **Date of Birth**: Student's birth date (required)
- **Level**: Academic level (1-6)
- **Room**: Assigned room (1-6)
- **Created At**: Automatically set when record is created
- **Updated At**: Automatically updated when record is modified

## Database

The system uses SQLite by default, which creates a `db.sqlite3` file in the project root. This is perfect for development and small deployments.

For production use, you can configure PostgreSQL, MySQL, or other databases by modifying the `DATABASES` setting in `settings.py`.

## File Structure

```
student_management/
├── student_env/                # Virtual environment
├── media/                      # Uploaded student photos
├── student_management/         # Main project directory
│   ├── settings.py            # Django settings
│   ├── urls.py               # Main URL configuration
│   └── ...
├── students/                  # Student app
│   ├── models.py             # Student model definition
│   ├── admin.py              # Admin interface configuration
│   ├── migrations/           # Database migrations
│   └── ...
├── db.sqlite3                # SQLite database file
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Customization

### Adding More Levels or Rooms
Edit the `LEVEL_CHOICES` and `ROOM_CHOICES` in `students/models.py`:

```python
LEVEL_CHOICES = [
    ('1', 'Level 1'),
    ('2', 'Level 2'),
    # Add more levels as needed
]

ROOM_CHOICES = [
    ('1', 'Room 1'),
    ('2', 'Room 2'),
    # Add more rooms as needed
]
```

### Adding Custom Admin Actions
Add new methods to the `StudentAdmin` class in `students/admin.py`:

```python
def custom_action(self, request, queryset):
    # Your custom logic here
    pass
custom_action.short_description = "Description of your action"

actions = ['make_level_1', 'make_level_2', 'custom_action']
```

## Troubleshooting

1. **Virtual environment not activating**
   - Make sure you're in the correct directory
   - Try using the full path to the activation script

2. **Migration errors**
   - Delete `db.sqlite3` and run migrations again
   - Make sure all required fields are properly defined

3. **Photo uploads not working**
   - Check that the `media` folder exists and is writable
   - Verify `MEDIA_ROOT` and `MEDIA_URL` settings

4. **Admin interface not accessible**
   - Make sure you've created a superuser account
   - Check that DEBUG is set to True in development

## Security Notes

- Change the `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Configure proper database settings for production
- Set up proper media file serving for production (not using Django)

## License

This project is for educational purposes. Modify and use as needed for your school or institution.
