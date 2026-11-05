# 📚 Django Learning Guide - Hospital Management System

This guide helps you understand the Django concepts used in your hospital management project.

---

## 🎯 Django Overview

**Django** is a "batteries-included" web framework that follows the **MVT (Model-View-Template)** pattern:

```
User Request
    ↓
URL Routing (urls.py)
    ↓
View (views.py) - Business Logic
    ↓
Model (models.py) - Database
    ↓
Template (html files) - Display
    ↓
Response to User
```

---

## 🗄️ Models - Database Structure

### What Are Models?
Models define your database structure. Each model = One database table.

### Example from Your Project:

```python
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=50, unique=True)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES)
    allergies = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.patient_id}"
```

### Field Types Used:
- `CharField()` - Short text
- `TextField()` - Long text
- `DateTimeField()` - Date and time
- `ForeignKey()` - Link to another table
- `OneToOneField()` - One-to-one relationship
- `IntegerField()` - Numbers
- `DecimalField()` - Prices/decimals
- `BooleanField()` - True/False

### Relationships:

1. **One-to-Many** (ForeignKey)
```python
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
```
One doctor can have many appointments.

2. **One-to-One** (OneToOneField)
```python
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
```
Each user has exactly one patient profile.

3. **Many-to-Many** (ManyToManyField)
```python
class Doctor(models.Model):
    specializations = models.ManyToManyField(Specialization)
```
Each doctor can have multiple specializations.

---

## 👁️ Views - Business Logic

### What Are Views?
Views contain the logic that processes requests and returns responses.

### Function-Based View Example:

```python
@login_required(login_url='login')
def patient_dashboard(request):
    """Patient dashboard view"""
    if request.user.role != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    
    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'hospital/patient_dashboard.html', context)
```

### Key Concepts:

1. **@login_required**: Decorator that requires user to be logged in
2. **Role-based access**: Check user role before showing data
3. **QuerySet**: Fetch data from database
4. **Context**: Data to pass to template
5. **render()**: Render template with context

### Common View Patterns:

```python
# Get single object
doctor = Doctor.objects.get(id=1)

# Get multiple objects
appointments = Appointment.objects.filter(status='scheduled')

# Get all objects
doctors = Doctor.objects.all()

# Create object
patient = Patient.objects.create(user=user, patient_id='PAT001')

# Update object
appointment.status = 'completed'
appointment.save()

# Delete object
appointment.delete()
```

---

## 📄 Templates - Display Layer

### What Are Templates?
Templates are HTML files with Django template syntax.

### Django Template Syntax:

**1. Variables** - Display data
```django
{{ user.first_name }}
{{ appointment.appointment_date|date:"M d, Y" }}
{{ total_patients|add:"1" }}
```

**2. Tags** - Control flow
```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.first_name }}!</p>
{% else %}
    <p>Please login</p>
{% endif %}
```

**3. Loops**
```django
{% for appointment in appointments %}
    <h3>{{ appointment.patient.user.first_name }}</h3>
    <p>{{ appointment.appointment_date }}</p>
{% endfor %}
```

**4. Template Inheritance**
```django
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <header>Navigation</header>
    {% block content %}{% endblock %}
    <footer>Footer</footer>
</body>
</html>

<!-- child.html -->
{% extends "hospital/base.html" %}

{% block title %}Patient Dashboard{% endblock %}

{% block content %}
    <h1>Welcome Patient</h1>
{% endblock %}
```

**5. Filters** - Modify data
```django
{{ text|truncatewords:10 }}          <!-- Truncate text -->
{{ date|date:"M d, Y" }}              <!-- Format date -->
{{ list|length }}                     <!-- Get length -->
{{ number|add:"5" }}                  <!-- Add number -->
{{ string|upper }}                    <!-- Convert to uppercase -->
```

**6. URL Generation**
```django
<a href="{% url 'appointment_detail' appointment.pk %}">
    View Appointment
</a>
```

**7. Static Files**
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
```

**8. CSRF Token** (in forms)
```django
<form method="post">
    {% csrf_token %}
    <input type="text" name="name">
    <button type="submit">Submit</button>
</form>
```

---

## 🔑 Forms - User Input

### What Are Forms?
Forms handle user input, validation, and error handling.

### Form Types:

1. **Regular Forms**
```python
class AppointmentForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())
    date = forms.DateTimeField()
    reason = forms.CharField(widget=forms.Textarea)
```

2. **ModelForms** (Recommended)
```python
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 4})
        }
```

### Using Forms in Views:
```python
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    
    return render(request, 'hospital/book_appointment.html', {'form': form})
```

### In Template:
```django
<form method="post">
    {% csrf_token %}
    {{ form.doctor }}
    {{ form.appointment_date }}
    {{ form.reason }}
    <button type="submit">Book Appointment</button>
</form>
```

---

## 🔐 Authentication & Authorization

### What Is It?
Authentication = Who are you?
Authorization = What can you do?

### Built-in Authentication:
```python
# Login check
{% if user.is_authenticated %}
    Logged in as {{ user.username }}
{% endif %}

# In views
if request.user.is_authenticated:
    # User is logged in
```

### Role-Based Access:
```python
# Check user role
if request.user.role == 'doctor':
    # Show doctor content

# Using decorators
@login_required
def some_view(request):
    # Only logged-in users
```

### Your Custom User Model:
```python
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
```

---

## 🌐 URL Routing

### What Is It?
URL routing maps URLs to views.

### In urls.py:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/<int:pk>/', views.dashboard_detail, name='dashboard'),
]
```

### URL Parts:
- `''` - The path
- `<int:pk>` - Parameter (integer named pk)
- `views.home` - Which view to call
- `name='home'` - URL name (for reverse lookups)

### In Templates:
```django
<a href="{% url 'home' %}">Home</a>
<a href="{% url 'dashboard' pk=1 %}">Dashboard</a>
```

### Available URL Parameters:
- `<int:pk>` - Integer
- `<str:slug>` - String
- `<uuid:uuid>` - UUID
- `<path:page>` - Full path with slashes

---

## 🛡️ Decorators & Middleware

### Login Required Decorator:
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def protected_view(request):
    # Only logged-in users can access
```

### Custom Decorators:
```python
def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@role_required('doctor')
def doctor_view(request):
    # Only doctors can access
```

---

## 📊 Database Queries (ORM)

### Fetch Data:
```python
# Get all
all_patients = Patient.objects.all()

# Get with filter
doctors = Doctor.objects.filter(specialization='Cardiology')

# Get one specific
patient = Patient.objects.get(id=1)

# Get or create
patient, created = Patient.objects.get_or_create(patient_id='PAT001')

# Count
total_patients = Patient.objects.count()

# Get first
first_patient = Patient.objects.first()
```

### Filter Options:
```python
# Exact match
Doctor.objects.filter(specialization='Cardiology')

# Contains
Doctor.objects.filter(specialization__icontains='cardio')

# Greater than
Appointment.objects.filter(appointment_date__gt=datetime.now())

# Less than
Appointment.objects.filter(appointment_date__lt=datetime.now())

# Range
Appointment.objects.filter(appointment_date__range=[start, end])

# In list
Doctor.objects.filter(specialization__in=['Cardiology', 'Neurology'])

# Is null
Patient.objects.filter(allergies__isnull=True)
```

### Update & Delete:
```python
# Update single
appointment = Appointment.objects.get(id=1)
appointment.status = 'completed'
appointment.save()

# Update multiple
Appointment.objects.filter(status='pending').update(status='confirmed')

# Delete single
appointment.delete()

# Delete multiple
Appointment.objects.filter(status='cancelled').delete()
```

### Aggregation:
```python
from django.db.models import Count, Sum

# Count
Doctor.objects.filter(specialization='Cardiology').count()

# Get with related count
doctors = Doctor.objects.annotate(appointment_count=Count('appointments'))

# Aggregate multiple
from django.db.models import Count, Q
stats = {
    'total_patients': Patient.objects.count(),
    'total_appointments': Appointment.objects.count(),
    'completed': Appointment.objects.filter(status='completed').count(),
}
```

---

## 🏗️ Project Structure Best Practices

### Good Organization:
```
app/
├── models.py          # Database models
├── views.py           # Business logic
├── urls.py            # URL routing
├── forms.py           # User forms
├── admin.py           # Admin configuration
├── templates/         # HTML templates
│   └── app/
│       ├── base.html
│       ├── list.html
│       └── detail.html
└── static/            # CSS, JS, images
    ├── css/
    ├── js/
    └── images/
```

### Code Organization Tips:
1. Keep views small (move logic to model methods if complex)
2. Use model methods for repeated logic
3. Create separate forms for different purposes
4. Organize templates in app-specific folders
5. Keep static files organized by type

---

## ⚙️ Common Commands

### Setup & Database:
```bash
# Create new app
python manage.py startapp app_name

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Reset database
python manage.py flush
```

### Running & Testing:
```bash
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Run tests
python manage.py test

# Interactive shell
python manage.py shell
```

### Production:
```bash
# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check

# Create production backup
python manage.py dumpdata > backup.json
```

---

## 🎓 Key Learning Points

1. **MVT Pattern**: Models store data, Views process logic, Templates display
2. **ORM**: Write database queries in Python instead of SQL
3. **Models Relationships**: ForeignKey, OneToOne, ManyToMany
4. **Template Inheritance**: Reuse code with extends and blocks
5. **Forms**: Handle user input safely and validate it
6. **Authentication**: Django provides built-in user management
7. **Decorators**: Control access to views
8. **Admin Interface**: Manage data without custom interfaces
9. **Static Files**: Serve CSS, JS, images efficiently
10. **URL Routing**: Map URLs to views cleanly

---

## 📖 Next Steps

### Learn:
1. Read your project's code (`models.py`, `views.py`)
2. Explore Django admin panel
3. Understand template inheritance
4. Practice writing queries
5. Build small features

### Build:
1. Add email notifications
2. Create reports
3. Add search functionality
4. Implement file uploads
5. Create API endpoints

### Deploy:
1. Set up production database
2. Configure static files
3. Use Gunicorn server
4. Set up domain
5. Enable HTTPS

---

## 🔗 Resources

- **Official Docs**: https://docs.djangoproject.com/
- **Django Girls Tutorial**: https://tutorial.djangogirls.org/
- **Real Python Tutorials**: https://realpython.com/search?q=django
- **Your Project**: `hospital_app/` folder contains working examples

---

## 💡 Tips & Tricks

1. **Debug in shell**: `python manage.py shell` to test queries
2. **Print objects**: Add `__str__` method to models
3. **Use fixtures**: Load test data with migrations
4. **Cache queries**: Use `select_related()` and `prefetch_related()`
5. **Use managers**: Custom managers for common queries
6. **Signals**: Auto-run code on model changes
7. **Middleware**: Process all requests
8. **Context processors**: Data for all templates

---

## ✅ Checklist for Learning

- [ ] Understand MVT pattern
- [ ] Know model relationships
- [ ] Can write basic views
- [ ] Can create templates with inheritance
- [ ] Understand form handling
- [ ] Know authentication basics
- [ ] Understand URL routing
- [ ] Can use Django admin
- [ ] Know common ORM queries
- [ ] Can debug issues

---

**Now go explore your Django project and build awesome features!** 🚀
