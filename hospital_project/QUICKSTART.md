# Hospital Management System - Quick Start Guide

## 🚀 Getting Started (5 minutes)

### 1️⃣ Setup Virtual Environment

```bash
cd hospital_project
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Create Admin Account

```bash
python manage.py createsuperuser
# Follow the prompts to create your admin account
```

### 5️⃣ Run Server

```bash
python manage.py runserver
```

### 6️⃣ Access Application

- **Frontend**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin`

---

## 📋 Test Accounts

### Admin
- Email: `admin@example.com`
- Password: (what you set during createsuperuser)

### Create Test Users in Admin Panel

1. Go to `http://localhost:8000/admin`
2. Login with admin credentials
3. Click "Users" → "Add User"
4. Create accounts with different roles

---

## 🎯 Key Features to Try

1. **Register as Patient**
   - Go to `http://localhost:8000/register/patient/`
   - Fill in details and create account

2. **View Doctors**
   - Go to `http://localhost:8000/doctors/`
   - See all available doctors

3. **Book Appointment**
   - Login as patient
   - Click "Book Appointment"
   - Select doctor and time

4. **Admin Dashboard**
   - Login as admin
   - View statistics and manage system

5. **Doctor Portal**
   - Login as doctor
   - View scheduled appointments
   - Manage patients

---

## 📁 Project Layout

- **Models**: Data structure (User, Patient, Doctor, etc.)
- **Views**: Business logic and page rendering
- **Templates**: HTML files for UI
- **Static**: CSS and JavaScript files
- **URLs**: Routing configuration

---

## 🔧 Useful Commands

```bash
# View all available commands
python manage.py help

# Reset entire database
python manage.py flush

# Run on different port
python manage.py runserver 8080

# Interactive Python shell
python manage.py shell

# Create new app
python manage.py startapp app_name
```

---

## 📝 Django Template Tags You'll Use

```django
{{ variable }}                          # Display variable
{% if condition %} ... {% endif %}      # Conditional
{% for item in list %} ... {% endfor %} # Loop
{% url 'view_name' %}                   # Generate URL
{% load static %}                       # Load static files
{{ value|filter }}                      # Apply filter
{% csrf_token %}                        # CSRF protection in forms
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Run `python manage.py runserver 8080` |
| Database locked | Run `python manage.py flush` |
| Template not found | Check `TEMPLATES` in settings.py |
| Static files missing | Run `python manage.py collectstatic` |
| Import errors | Install dependencies: `pip install -r requirements.txt` |

---

## 📚 Database Structure

```
User (Custom)
├── Patient
├── Doctor
├── Staff
└── Appointment
    ├── Prescription
    └── MedicalRecord
```

---

## 🔐 Security Notes

- ⚠️ Change `SECRET_KEY` before production
- ⚠️ Set `DEBUG = False` for production
- ⚠️ Update `ALLOWED_HOSTS` for your domain
- ⚠️ Use PostgreSQL instead of SQLite for production
- ⚠️ Never commit `.env` file to git

---

## 📚 Learn More

- Read [README.md](README.md) for detailed documentation
- Check [Django Official Docs](https://docs.djangoproject.com/)
- Explore `hospital_app/models.py` to understand data structure
- Review `hospital_app/views.py` to see how logic works

---

**Happy Coding! 🎉**
