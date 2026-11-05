# 🔐 Admin Dashboard Setup & Login Guide

## ✅ Quick Start (2 Minutes)

### Step 1: Navigate to Project Directory
```bash
cd d:\Hospital Management Project\hospital_project
```

### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Run Migration (if not done)
```bash
python manage.py migrate
```

### Step 4: Create Admin User
```bash
python create_admin.py
```

You'll see an interactive menu:
```
Options:
1. Create new admin user
2. View existing admins
3. Change admin password
4. Exit

Enter your choice (1-4): 
```

Select **Option 1** and fill in:
- Username: `admin`
- Email: `admin@hospital.com`
- Password: `admin@123` (or your choice)
- First Name: `Admin`
- Last Name: `User`

### Step 5: Run Server
```bash
python manage.py runserver
```

### Step 6: Login to Admin Dashboard
```
URL: http://localhost:8000/login

Login with:
- Username: admin
- Password: admin@123
```

After login, you'll be redirected to `/dashboard/admin/`

---

## 🔑 Default Credentials

| Field | Value |
|-------|-------|
| **URL** | http://localhost:8000 |
| **Login Page** | http://localhost:8000/login |
| **Admin Dashboard** | http://localhost:8000/dashboard/admin |
| **Django Admin** | http://localhost:8000/admin |
| **Username** | admin |
| **Password** | admin@123 |

---

## 🚀 Admin Panel Features

### 1. **Admin Dashboard** (`/dashboard/admin/`)

Shows:
- Total Users count
- Total Patients count
- Total Doctors count
- Total Staff count
- Appointment statistics
- Recent appointments table
- System controls
- Quick action buttons

### 2. **User Management** (`/admin/users/`)

Manage all users with:
- Search by name/email
- Filter by role (Admin, Doctor, Patient, Staff, Nurse)
- View user details
- Edit user information
- Active/Inactive status
- Join date info

### 3. **System Controls**

Quick access to:
- Django Admin Panel
- Manage Users
- Manage Appointments
- Medical Records
- Doctor Directory
- Your Profile

### 4. **Django Admin Panel** (`/admin/`)

Full database management:
- Add/Edit/Delete Users
- Manage Doctors
- Manage Patients
- Manage Appointments
- Manage Medical Records
- Manage Staff
- User permissions
- Group management

---

## 📊 Dashboard Components

### Statistics Cards
```
┌─────────────┬──────────────┬──────────────┬──────────────┐
│ Total Users │ Total Doctors│ Total Patients│ Total Staff │
│     25      │      8       │      12      │      5       │
└─────────────┴──────────────┴──────────────┴──────────────┘
```

### Recent Appointments Table
Shows latest 10 appointments with:
- Patient name
- Doctor name
- Appointment date & time
- Status (scheduled, completed, cancelled)
- Action link (View details)

### System Controls
One-click access to:
- Django Admin Panel (database management)
- User Management (view/edit all users)
- Appointment Management (schedule/reschedule)
- Medical Records (patient medical history)
- Doctor Directory (view all doctors)
- User Profile (edit your profile)

---

## 🛡️ Role-Based Access

### Admin Role Permissions:
✅ View all users
✅ View all appointments
✅ View all medical records
✅ Manage all doctors
✅ Manage all patients
✅ Access Django admin panel
✅ Full system statistics
✅ Create/Edit/Delete records

### Doctor Role Permissions:
✅ View own appointments
✅ View assigned patients
✅ Write prescriptions
✅ Update medical records
✅ Access doctor dashboard

### Patient Role Permissions:
✅ Book appointments
✅ View own appointments
✅ View own medical records
✅ Manage profile
✅ Access patient dashboard

### Staff/Nurse Role Permissions:
✅ View all appointments
✅ View all patients
✅ Update appointment status
✅ View medical records
✅ Access staff dashboard

---

## 🔧 Creating Additional Admin Users

### Method 1: Using create_admin.py (Recommended)
```bash
python create_admin.py
# Then select option 1
```

### Method 2: Using Django createsuperuser
```bash
python manage.py createsuperuser
```
Then set role to 'admin' in Django admin panel

### Method 3: Django Admin Panel
1. Go to http://localhost:8000/admin
2. Click "Add User" under Users
3. Enter username and password
4. Save
5. Edit user and set role to 'admin'

---

## 🔑 Changing Admin Password

### Method 1: Using create_admin.py
```bash
python create_admin.py
# Select option 3: Change admin password
```

### Method 2: Using Django command
```bash
python manage.py changepassword admin
```

### Method 3: Django Admin Panel
1. Login to http://localhost:8000/admin
2. Click Users
3. Click the admin username
4. Scroll down to "Password"
5. Click "Change password"

---

## 🎯 Admin Dashboard Walkthrough

### First Time Login:

1. **Open Browser**
   - Go to: http://localhost:8000/login

2. **Enter Credentials**
   - Username: `admin`
   - Password: `admin@123` (or your password)

3. **You'll See Admin Dashboard**
   - Statistics cards at top
   - Recent appointments table
   - System controls section

4. **Click "Manage Users"**
   - View all registered users
   - Filter by role
   - Search by name/email
   - Edit user details

5. **Click "Django Admin Panel"**
   - Full database access
   - Add new records
   - Edit existing records
   - Delete records

---

## 📝 Common Tasks

### Task 1: Add New Doctor
```
1. Go to Admin Dashboard
2. Click "Django Admin Panel"
3. Click "Doctors" → "Add Doctor"
4. Fill details:
   - Select user (or create new user)
   - Specialization
   - License number
   - Experience
   - Consultation fee
   - Availability status
5. Save
```

### Task 2: Add New Patient
```
1. Go to Admin Dashboard
2. Click "Django Admin Panel"
3. Click "Patients" → "Add Patient"
4. Fill details:
   - Select user
   - Patient ID
   - Blood type
   - Allergies
   - Medical history
5. Save
```

### Task 3: Create Appointment
```
1. Go to Admin Dashboard
2. Click "Manage Appointments"
3. Click "Add Appointment"
4. Select:
   - Patient
   - Doctor
   - Date & Time
   - Reason
5. Save
```

### Task 4: View User Information
```
1. Go to Admin Dashboard
2. Click "Manage Users"
3. Use search/filter to find user
4. Click "Edit" to view details
5. Can edit and save changes
```

### Task 5: Change User Role
```
1. Go to Django Admin Panel
2. Click "Users"
3. Find user
4. Change "Role" dropdown
5. Save
```

---

## 🔒 Security Tips

1. **Change Default Password**
   - Don't use 'admin@123' in production
   - Use strong passwords (8+ chars, mix of letters/numbers/symbols)

2. **Create Multiple Admins**
   ```bash
   python create_admin.py
   # Create 2-3 admin accounts for backup
   ```

3. **Backup Database**
   ```bash
   # Before making major changes
   # Database file: db.sqlite3
   # Make a copy!
   ```

4. **Set DEBUG = False for Production**
   - Edit: hospital_project/settings.py
   - Change: DEBUG = False

5. **Use HTTPS in Production**
   - Add SSL certificate
   - Update ALLOWED_HOSTS
   - Update SECRET_KEY

---

## 🐛 Troubleshooting

### Problem: Can't Login
**Solution:**
```bash
# Reset password
python manage.py changepassword admin

# Or create new admin
python create_admin.py
```

### Problem: "OperationalError: no such table"
**Solution:**
```bash
python manage.py migrate
```

### Problem: "Port 8000 already in use"
**Solution:**
```bash
python manage.py runserver 8080
# Then visit: http://localhost:8080/login
```

### Problem: Can't see admin dashboard
**Cause:** You're not logged in as admin

**Solution:**
1. Check your role at Django admin
2. Change role to 'admin'
3. Refresh and try again

### Problem: Static files not loading (no CSS)
**Solution:**
```bash
python manage.py collectstatic --noinput
# Restart server
```

---

## 📚 Useful URLs

| Page | URL |
|------|-----|
| Home | http://localhost:8000 |
| Login | http://localhost:8000/login |
| Admin Dashboard | http://localhost:8000/dashboard/admin |
| User Management | http://localhost:8000/admin/users |
| Django Admin | http://localhost:8000/admin |
| Doctor List | http://localhost:8000/doctors |
| Appointments | http://localhost:8000/appointments |
| Medical Records | http://localhost:8000/medical-records |
| Profile | http://localhost:8000/profile |
| Edit Profile | http://localhost:8000/profile/edit |

---

## 🎓 Learning Resources

- **Django Tutorial**: Check `DJANGO_LEARNING_GUIDE.md`
- **Quick Setup**: Check `QUICKSTART.md`
- **Troubleshooting**: Check `TROUBLESHOOTING_FAQ.md`
- **README**: Check `README.md` for detailed info

---

## ✨ Next Steps

1. ✅ Create admin user with create_admin.py
2. ✅ Login to admin dashboard
3. ✅ Explore all features
4. ✅ Create test doctor user
5. ✅ Create test patient user
6. ✅ Book test appointment
7. ✅ View appointments in admin panel
8. ✅ Customize your branding

---

## 📞 Support

If you face any issues:

1. **Check error message carefully**
   - Read the error completely
   - Search exact error in documentation

2. **Check the docs**
   - TROUBLESHOOTING_FAQ.md
   - DJANGO_LEARNING_GUIDE.md
   - README.md

3. **Check terminal output**
   - May show helpful information
   - Copy error and search online

4. **Check Django logs**
   - File: hospital_project/settings.py
   - Configure logging if needed

---

**Happy Admin! 🎉**

Created: May 20, 2024
Version: 1.0
For: Hospital Management System
