"""
HOSPITAL MANAGEMENT SYSTEM - ADMIN SETUP INSTRUCTIONS
====================================================

Run these commands in the hospital_project directory to set up the admin dashboard:

STEP 1: Create Virtual Environment
-----------------------------------
python -m venv venv
venv\Scripts\activate  # Windows

STEP 2: Install Dependencies  
----------------------------
pip install -r requirements.txt

STEP 3: Run Migrations
---------------------
python manage.py makemigrations
python manage.py migrate

STEP 4: Create Admin User (Interactive)
--------------------------------------
python create_admin.py

This will show you an interactive menu where you can:
- Create a new admin user
- View existing admins
- Change admin password
- Exit

Example Credentials to Create:
- Username: admin
- Email: admin@hospital.com
- Password: admin@123

STEP 5: Run Development Server
------------------------------
python manage.py runserver

STEP 6: Access Admin Panel
--------------------------
Frontend: http://localhost:8000
Admin Panel: http://localhost:8000/admin
Admin Dashboard: http://localhost:8000/dashboard/admin

DEFAULT ADMIN LOGIN (after running create_admin.py):
- Username: admin
- Password: (whatever you set in the script)

=============================================================

AVAILABLE ADMIN FEATURES:

1. Admin Dashboard (/dashboard/admin/)
   - View system statistics
   - See recent appointments
   - Quick access to management tools
   - System overview with charts

2. User Management (/admin/users/)
   - Manage all users
   - Filter by role (Admin, Doctor, Patient, Staff)
   - Search by name/email
   - View user details
   - Edit user information

3. Django Admin Panel (/admin/)
   - Full database management
   - Add/Edit/Delete any record
   - User role management
   - Permissions management

4. Management Controls
   - Doctor Directory
   - Appointment Management
   - Medical Records
   - User Profiles

=============================================================

USEFUL DJANGO COMMANDS:

# Reset database (deletes all data!)
python manage.py flush

# Create superuser via Django
python manage.py createsuperuser

# Change password for specific user
python manage.py changepassword admin

# Run Django shell (test code)
python manage.py shell

# Run on different port
python manage.py runserver 8080

# Collect static files (for production)
python manage.py collectstatic

=============================================================

TROUBLESHOOTING:

Q: "ModuleNotFoundError: No module named 'django'"
A: Run: pip install -r requirements.txt

Q: "OperationalError: no such table"
A: Run: python manage.py migrate

Q: "TemplateDoesNotExist"
A: Check file is in hospital_app/templates/hospital/
   Restart server if just created

Q: "Port 8000 already in use"
A: Run: python manage.py runserver 8080

Q: Forgot admin password
A: Run: python manage.py changepassword admin

=============================================================

ADMIN ROLES EXPLAINED:

Admin:
- Full system access
- Can manage all users
- View all appointments
- Access admin panel
- Manage doctors and patients
- View reports and statistics

Doctor:
- View own appointments
- Manage patient records
- Write prescriptions
- Access own dashboard

Patient:
- Book appointments
- View medical records
- Manage own profile
- View appointment history

Staff/Nurse:
- View all appointments
- Access patient information
- Update appointment status
- View medical records

=============================================================

PROJECT STRUCTURE:

hospital_project/
├── hospital_project/
│   ├── settings.py (Django configuration)
│   ├── urls.py (URL routing)
│   └── wsgi.py
├── hospital_app/
│   ├── models.py (Database models)
│   ├── views.py (Business logic)
│   ├── forms.py (Form handling)
│   ├── admin.py (Admin panel config)
│   ├── templates/
│   │   └── hospital/
│   │       ├── base.html
│   │       ├── admin_dashboard.html
│   │       ├── admin_manage_users.html
│   │       └── ... (other templates)
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── create_admin.py (Admin user setup)
└── manage.py

=============================================================

QUICK TEST SCENARIO:

1. Run server: python manage.py runserver
2. Create admin: python create_admin.py
3. Login: http://localhost:8000/login
4. View dashboard: http://localhost:8000/dashboard/admin
5. Manage users: http://localhost:8000/admin/users/
6. Django admin: http://localhost:8000/admin

=============================================================

For more help, see:
- README.md
- QUICKSTART.md
- DJANGO_LEARNING_GUIDE.md
- TROUBLESHOOTING_FAQ.md

Created: May 20, 2024
Version: 1.0
"""

# This file contains setup instructions for the Hospital Management System
# Open this file to see all available commands and setup steps
