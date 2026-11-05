# Doldam Hospital - Django Management System

A comprehensive hospital management system built with Django. This application manages patients, doctors, appointments, prescriptions, and medical records.

## Features

✅ **User Management**
- Role-based authentication (Admin, Doctor, Patient, Nurse, Staff)
- User profiles with detailed information
- Secure login and registration

✅ **Patient Features**
- Book appointments with doctors
- View medical records
- Manage prescriptions
- Track appointment history

✅ **Doctor Features**
- View scheduled appointments
- Manage patient information
- Create medical records
- Write prescriptions

✅ **Admin Features**
- Hospital statistics dashboard
- User management
- Appointment management
- Django admin panel

✅ **Additional Features**
- Responsive design
- Modern UI with Font Awesome icons
- Real-time appointment scheduling
- Medical record management
- Secure password handling

---

## Project Structure

```
hospital_project/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── hospital_project/            # Project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI configuration
│   └── __init__.py
├── hospital_app/               # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── urls.py                 # App URL routing
│   ├── forms.py                # Form definitions
│   ├── admin.py                # Admin configuration
│   ├── migrations/             # Database migrations
│   ├── templates/hospital/     # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Home page
│   │   ├── login.html          # Login page
│   │   ├── patient_dashboard.html
│   │   ├── doctor_dashboard.html
│   │   ├── admin_dashboard.html
│   │   ├── book_appointment.html
│   │   └── ...                 # Other templates
│   └── static/                 # Static files
│       ├── css/style.css       # Stylesheet
│       └── js/main.js          # JavaScript
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (venv)

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd hospital_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Enter the following information:
- Username: `admin`
- Email: `admin@example.com`
- Password: (create a strong password)
- Confirm Password: (repeat password)

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## Admin Panel Access

1. Go to `http://localhost:8000/admin/`
2. Login with superuser credentials (created in Step 4)
3. Manage users, patients, doctors, appointments, etc.

---

## Database Models

### User Model
- Custom user model with role-based system
- Roles: Admin, Doctor, Patient, Nurse, Staff
- Fields: name, email, phone, address, date of birth

### Patient
- Linked to User model
- Blood type, allergies, medical history
- Insurance information
- Emergency contact

### Doctor
- Linked to User model
- Specialization, license number
- Experience years, consultation fee
- Availability status

### Appointment
- Links Patient and Doctor
- Date/time, reason, status
- Notes and follow-ups

### Prescription
- Linked to Appointment
- Medication name, dosage, frequency
- Duration and instructions

### MedicalRecord
- Patient medical history
- Diagnosis, treatment, test results
- Doctor notes

### Staff
- Staff members (nurses, admin, etc.)
- Department, shift information

---

## URL Routing

### Public URLs
- `/` - Home page
- `/login/` - User login
- `/logout/` - User logout
- `/register/patient/` - Patient registration
- `/register/doctor/` - Doctor registration
- `/doctors/` - Doctor listing

### Authenticated URLs
- `/dashboard/` - Role-based dashboard redirect
- `/dashboard/patient/` - Patient dashboard
- `/dashboard/doctor/` - Doctor dashboard
- `/dashboard/admin/` - Admin dashboard
- `/dashboard/staff/` - Staff dashboard

### Appointment URLs
- `/appointments/book/` - Book appointment
- `/appointments/` - View appointments
- `/appointments/<id>/` - Appointment details

### Profile URLs
- `/profile/` - View profile
- `/profile/edit/` - Edit profile

### Records URLs
- `/medical-records/` - View medical records

---

## Django Admin Features

1. **User Management**: Create, edit, delete users with specific roles
2. **Patient Management**: View and manage patient profiles
3. **Doctor Management**: Manage doctor details and specializations
4. **Appointment Management**: Schedule, update, cancel appointments
5. **Medical Records**: Store patient health information
6. **Prescriptions**: Record medications and dosages

### Access Admin Panel:
```
URL: http://localhost:8000/admin/
Username: admin
Password: (your superuser password)
```

---

## Authentication & Authorization

The system uses Django's built-in authentication with custom role-based access control:

- **Admin**: Full access to all features and admin panel
- **Doctor**: Can view appointments, manage patients, write prescriptions
- **Patient**: Can book appointments, view medical records
- **Nurse/Staff**: Can view appointments and patient information

---

## File Management

### Static Files
- CSS files in `hospital_app/static/css/`
- JavaScript files in `hospital_app/static/js/`
- Images in `hospital_app/static/images/` (if needed)

### Templates
- Base template: `hospital_app/templates/hospital/base.html`
- Role-specific templates in the same directory

### Media Files
- Uploaded files stored in `media/` directory

---

## Django Template Syntax

### Variables
```django
{{ user.first_name }}
{{ appointment.date|date:"M d, Y" }}
```

### Logic
```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.first_name }}!</p>
{% endif %}

{% for appointment in appointments %}
    <p>{{ appointment.patient.name }}</p>
{% endfor %}
```

### Filters
```django
{{ text|truncatewords:10 }}
{{ date|date:"M d, Y" }}
{{ list|length }}
```

---

## Common Django Commands

```bash
# Create new app
python manage.py startapp app_name

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell (interactive Python)
python manage.py shell

# Clear database and start fresh
python manage.py flush
```

---

## Debugging Tips

1. **Check error messages**: Django provides detailed error pages in development
2. **Use print() statements**: Add debugging in views
3. **Django shell**: Test database queries interactively
4. **Logs**: Check console output for error messages
5. **Browser DevTools**: Check browser console for JavaScript errors

---

## Important Notes

1. **SECRET_KEY**: Change in production (`settings.py`)
2. **DEBUG**: Set to False in production
3. **ALLOWED_HOSTS**: Configure for production domain
4. **Database**: SQLite is for development; use PostgreSQL for production
5. **Static files**: Collect with `python manage.py collectstatic` before deployment

---

## Next Steps

1. Customize models as per business requirements
2. Add more fields to User and Patient models if needed
3. Create custom management commands
4. Add email notifications
5. Implement payment processing
6. Add API endpoints (DRF)
7. Implement advanced search and filtering
8. Add appointment reminders
9. Create reports and analytics
10. Deploy to production

---

## Support & Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8080
```

### Clear Database
```bash
python manage.py flush
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

---

## License

This project is for educational purposes.

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/intro/contributing/)
- [Python Documentation](https://docs.python.org/)

---

**Last Updated**: May 2024
**Version**: 1.0.0
