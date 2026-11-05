# 🚀 Hospital Management System - Command Quick Reference

## Complete Setup Commands

Copy and paste these commands in order (in hospital_project directory):

### 1️⃣ Initial Setup (First Time Only)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install all packages
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate
```

### 2️⃣ Create Admin User

```bash
# Interactive admin setup (recommended)
python create_admin.py
```

**Then select option 1 and enter:**
- Username: `admin`
- Email: `admin@hospital.com`
- First Name: `Admin`
- Last Name: `User`
- Password: `admin@123`

---

## 🏃 Running the Application

### Start Development Server
```bash
python manage.py runserver
```

Access at: `http://localhost:8000`

### Start on Different Port
```bash
python manage.py runserver 8080
```

Access at: `http://localhost:8080`

---

## 🔐 Login Process

1. Navigate to: `http://localhost:8000/login`
2. Enter credentials:
   - **Username**: `admin`
   - **Password**: `admin@123`
3. Click Login
4. You'll be redirected to Admin Dashboard

---

## 📍 Important URLs

### User Accessible
```
Home              → http://localhost:8000/
Login             → http://localhost:8000/login/
Register Patient  → http://localhost:8000/register/patient/
Register Doctor   → http://localhost:8000/register/doctor/
Doctor List       → http://localhost:8000/doctors/
```

### Admin Only (After Login as Admin)
```
Admin Dashboard    → http://localhost:8000/dashboard/admin/
Manage Users       → http://localhost:8000/admin/users/
Django Admin       → http://localhost:8000/admin/
Appointments       → http://localhost:8000/appointments/
Medical Records    → http://localhost:8000/medical-records/
```

---

## 👤 Admin User Management

### View Existing Admins
```bash
python create_admin.py
# Select option 2
```

### Create Another Admin
```bash
python create_admin.py
# Select option 1
# Fill in details
```

### Change Admin Password
```bash
python create_admin.py
# Select option 3
# Enter username and new password
```

### Django Command Method
```bash
python manage.py changepassword admin
```

---

## 💾 Database Commands

### Create Fresh Database
```bash
python manage.py migrate
```

### Make Migrations (After model changes)
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Reset All Data (⚠️ Deletes Everything!)
```bash
python manage.py flush
```

---

## 🐚 Django Shell (Testing Code)

```bash
# Start shell
python manage.py shell

# Inside shell, you can:
from hospital_app.models import User, Patient, Doctor

# View all users
User.objects.all()

# Create user
User.objects.create_user(username='test', password='test123')

# Filter users
User.objects.filter(role='patient')

# Exit shell
exit()
```

---

## 🔧 Useful Admin Commands

### Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### Test Project Configuration
```bash
python manage.py check
```

### Show Installed Apps
```bash
python manage.py shell
>>> from django.apps import apps
>>> for app in apps.get_app_configs():
...     print(app.name)
```

### Show All Models
```bash
python manage.py inspectdb
```

---

## 📋 Troubleshooting Commands

### Port Already in Use
```bash
# Windows - Find process on port 8000
netstat -ano | findstr :8000

# Kill process (replace <PID> with actual ID)
taskkill /PID <PID> /F

# Or just use different port
python manage.py runserver 8080
```

### Import Error - Reinstall Django
```bash
pip install Django==4.2.0 --force-reinstall
```

### Missing Migrations
```bash
python manage.py makemigrations hospital_app
python manage.py migrate
```

### Debug Slow Query
```bash
# In settings.py temporarily add:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

---

## 🧪 Test Scenarios

### Scenario 1: Quick Admin Login Test
```bash
# Start server
python manage.py runserver

# In another terminal/window, open:
# http://localhost:8000/login
# Login with: admin / admin@123
# Check if redirected to dashboard
```

### Scenario 2: Create Test Doctor
```bash
# Server running...
# Go to: http://localhost:8000/register/doctor/
# Fill form and register
# Login as that doctor
# Check doctor dashboard
```

### Scenario 3: Create Test Patient
```bash
# Go to: http://localhost:8000/register/patient/
# Fill form and register
# Login as that patient
# Check patient dashboard
```

### Scenario 4: Book Appointment
```bash
# Login as patient
# Go to: http://localhost:8000/appointments/book/
# Select doctor and date
# Book appointment
# Admin can see it in dashboard
```

---

## 📊 Admin Dashboard Features

After logging in as admin:

1. **Statistics**
   - Total users, patients, doctors, staff
   - Appointment statistics

2. **Recent Appointments**
   - Last 10 appointments
   - Status, patient, doctor info

3. **System Controls**
   - Django Admin Panel
   - Manage Users
   - Manage Appointments
   - Medical Records
   - Doctor Directory
   - Profile Settings

4. **User Management**
   - Search users
   - Filter by role
   - Edit user details
   - View user status

---

## 🔄 Complete Daily Workflow

```bash
# Morning - Start work
cd d:\Hospital Management Project\hospital_project
venv\Scripts\activate
python manage.py runserver

# Visit http://localhost:8000/login
# Login with admin credentials
# Check dashboard
# Manage users/appointments as needed

# Evening - Stop work
Ctrl+C  # Stop server
deactivate  # Deactivate virtual environment
```

---

## 📁 Important Files

```
hospital_project/
├── manage.py              ← Run commands here
├── db.sqlite3             ← Database file
├── create_admin.py        ← Admin setup tool
├── ADMIN_SETUP_GUIDE.md   ← This guide
├── hospital_app/
│   ├── models.py          ← Database models
│   ├── views.py           ← Business logic
│   ├── admin.py           ← Admin config
│   └── templates/hospital/ ← HTML templates
└── hospital_project/
    └── settings.py        ← Django config
```

---

## 🆘 Quick Help Commands

```bash
# Show all commands
python manage.py help

# Show help for specific command
python manage.py help migrate

# Show Django version
python -m django --version

# List all installed packages
pip list

# Upgrade pip
python -m pip install --upgrade pip
```

---

## ✅ Installation Verification

After setup, verify everything works:

```bash
# Check Django
python -m django --version
# Should show: 4.2.0

# Check database
python manage.py migrate
# Should show: No changes detected

# Check settings
python manage.py check
# Should show: System check identified no issues

# View in browser
http://localhost:8000
# Should show: Hospital Management System home page
```

---

## 🎯 Success Checklist

✅ Virtual environment created and activated
✅ Dependencies installed (`pip install -r requirements.txt`)
✅ Migrations applied (`python manage.py migrate`)
✅ Admin user created (`python create_admin.py`)
✅ Server running (`python manage.py runserver`)
✅ Can login to admin dashboard
✅ Can view statistics and appointments
✅ Can access Django admin panel

---

## 💡 Pro Tips

1. **Keep terminal open**
   - Shows errors and logs
   - Very helpful for debugging

2. **Use Ctrl+C to stop server**
   - Clean shutdown
   - Can restart anytime

3. **Create backup of database**
   - Copy `db.sqlite3` file
   - Before making changes

4. **Read error messages**
   - Django errors are very helpful
   - Often tell you exactly what's wrong

5. **Use Django shell to test**
   - `python manage.py shell`
   - Test queries before implementing

---

## 📖 Need More Help?

See these files in project directory:

- **QUICKSTART.md** - 5-minute setup
- **README.md** - Complete documentation
- **DJANGO_LEARNING_GUIDE.md** - Learn Django
- **TROUBLESHOOTING_FAQ.md** - Common errors
- **SETUP_SUMMARY.md** - Project overview

---

**Last Updated**: May 20, 2024
**Version**: 1.0
**Status**: ✅ Ready to Use
