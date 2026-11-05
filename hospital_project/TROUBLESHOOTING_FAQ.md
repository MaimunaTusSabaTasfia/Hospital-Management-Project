# 🆘 Troubleshooting & FAQ Guide

## ⚠️ Common Errors & Solutions

### Error 1: Port 8000 Already in Use

**Error:**
```
OSError: [Errno 10048] Only one usage of each socket address
```

**Solution:**
```bash
# Run on different port
python manage.py runserver 8080

# Or find and kill process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Error 2: ModuleNotFoundError: No module named 'django'

**Error:**
```
ModuleNotFoundError: No module named 'django'
```

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or specific version
pip install Django==4.2.0

# Check installation
python -m django --version
```

---

### Error 3: No Such Table Error

**Error:**
```
django.db.utils.OperationalError: no such table: hospital_app_user
```

**Solution:**
```bash
# Apply migrations
python manage.py migrate

# If that doesn't work, reset database
python manage.py flush  # This deletes all data!
python manage.py migrate
```

---

### Error 4: Template Not Found

**Error:**
```
TemplateDoesNotExist at /
```

**Solution:**
1. Check file path in `templates/hospital/`
2. Verify `TEMPLATES` setting in `settings.py`
3. Restart server after creating new templates

```python
# In settings.py - make sure this is correct:
TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'hospital_app', 'templates')],
        # ...
    }
]
```

---

### Error 5: Static Files Not Loading

**Error:**
CSS/JS files not loading (404 errors)

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Add to settings.py for development:
DEBUG = True  # Must be True in development

# In base.html template:
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

---

### Error 6: Authentication Failed

**Error:**
```
Invalid username or password
```

**Solution:**
1. Create new superuser:
```bash
python manage.py createsuperuser
```

2. Reset user password:
```bash
python manage.py changepassword username
```

3. Check user role:
- Go to admin panel
- Edit user
- Set correct role

---

### Error 7: Database Locked

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Reset database
python manage.py flush

# Or restart Django
# Stop server and restart
```

---

### Error 8: CSRF Token Missing

**Error:**
```
CSRF verification failed. Request aborted.
```

**Solution:**
Add to all forms:
```django
<form method="post">
    {% csrf_token %}  <!-- Add this line -->
    <!-- form fields -->
</form>
```

---

### Error 9: Permission Denied

**Error:**
```
django.core.exceptions.PermissionDenied
```

**Solution:**
- Check user role
- Verify @login_required decorator
- Check role-based access control

---

### Error 10: Import Error

**Error:**
```
ImportError: cannot import name 'models' from 'django.db'
```

**Solution:**
```bash
# Reinstall Django
pip install Django==4.2.0 --force-reinstall

# Or check import statement
from django.db import models  # Correct
```

---

## ❓ Frequently Asked Questions

### Q1: How do I change the app title?

Edit `settings.py`:
```python
# Add after INSTALLED_APPS
ADMIN_SITE_HEADER = "Doldam Hospital Administration"
ADMIN_SITE_SITE_TITLE = "Doldam Hospital"
```

---

### Q2: How do I reset everything?

```bash
# Delete database
rm db.sqlite3

# Run migrations again
python manage.py migrate

# Create new admin
python manage.py createsuperuser
```

---

### Q3: How do I add a new field to User?

1. Add field to model:
```python
class User(AbstractUser):
    specialty = models.CharField(max_length=100, blank=True)
```

2. Create and apply migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Q4: How do I display custom user field in admin?

Edit `admin.py`:
```python
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'specialty')  # Add field
```

---

### Q5: How do I filter data in views?

```python
# Single condition
patients = Patient.objects.filter(blood_type='O+')

# Multiple conditions
patients = Patient.objects.filter(blood_type='O+', city='Seoul')

# Exclude
patients = Patient.objects.exclude(blood_type='O-')

# Complex queries
from django.db.models import Q
patients = Patient.objects.filter(
    Q(blood_type='O+') | Q(blood_type='O-')
)
```

---

### Q6: How do I send emails?

```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development

# In views.py
from django.core.mail import send_mail

send_mail(
    'Appointment Confirmation',
    'Your appointment is confirmed',
    'from@example.com',
    ['patient@example.com'],
    fail_silently=False,
)
```

---

### Q7: How do I paginate results?

```python
from django.core.paginator import Paginator

def appointment_list(request):
    all_appointments = Appointment.objects.all()
    paginator = Paginator(all_appointments, 10)  # 10 per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'template.html', {'page_obj': page_obj})
```

In template:
```django
{% for appointment in page_obj %}
    <!-- Display item -->
{% endfor %}

<div class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page=1">First</a>
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}
    
    <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Next</a>
        <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
    {% endif %}
</div>
```

---

### Q8: How do I create a custom manager?

```python
class AvailableDoctorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(availability_status=True)

class Doctor(models.Model):
    # ... fields ...
    objects = models.Manager()  # Default manager
    available = AvailableDoctorManager()  # Custom manager

# Usage:
all_doctors = Doctor.objects.all()
available_doctors = Doctor.available.all()
```

---

### Q9: How do I add search functionality?

```python
# views.py
def doctor_list(request):
    doctors = Doctor.objects.all()
    
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query)
        )
    
    return render(request, 'doctors.html', {'doctors': doctors, 'query': query})
```

In template:
```django
<form method="get">
    <input type="text" name="q" value="{{ query }}" placeholder="Search doctors">
    <button type="submit">Search</button>
</form>

{% for doctor in doctors %}
    <p>{{ doctor.user.get_full_name }}</p>
{% endfor %}
```

---

### Q10: How do I handle file uploads?

```python
# models.py
class Document(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# views.py
def upload_document(request):
    if request.method == 'POST' and request.FILES['file']:
        doc = Document.objects.create(
            patient=request.user.patient_profile,
            file=request.FILES['file']
        )
        return redirect('patient_dashboard')

# template
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="file">
    <button type="submit">Upload</button>
</form>
```

---

## 🐛 Debugging Techniques

### Method 1: Print Debugging
```python
def my_view(request):
    print(f"User: {request.user}")
    print(f"User role: {request.user.role}")
    
    appointments = Appointment.objects.all()
    print(f"Total appointments: {appointments.count()}")
    print(f"First appointment: {appointments.first()}")
    
    return render(request, 'template.html')
```

### Method 2: Django Shell
```bash
python manage.py shell

# Now you can test:
>>> from hospital_app.models import Patient
>>> Patient.objects.all()
>>> Patient.objects.filter(blood_type='O+')
>>> Patient.objects.create(...)
>>> exit()
```

### Method 3: Error Page
- Django shows detailed error page in development
- Shows which line caused error
- Shows local variables at time of error
- Shows full traceback

### Method 4: Logging
```python
import logging

logger = logging.getLogger(__name__)

def my_view(request):
    logger.info(f"User {request.user} accessed dashboard")
    logger.error("Something went wrong")
    logger.warning("This is a warning")
```

### Method 5: Browser DevTools
- F12 to open DevTools
- Network tab: See requests/responses
- Console: JavaScript errors
- Inspector: Check HTML/CSS

---

## 🔍 Testing Your App

### Create Test File
```python
# tests.py
from django.test import TestCase
from .models import Patient, Doctor, User

class PatientTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='patient'
        )
        self.patient = Patient.objects.create(
            user=user,
            patient_id='TEST001'
        )
    
    def test_patient_creation(self):
        self.assertEqual(self.patient.patient_id, 'TEST001')
        self.assertEqual(self.patient.user.role, 'patient')

# Run tests:
# python manage.py test
```

---

## 📊 Performance Tips

1. **Use select_related** for ForeignKey:
```python
appointments = Appointment.objects.select_related('patient', 'doctor')
```

2. **Use prefetch_related** for reverse relations:
```python
doctors = Doctor.objects.prefetch_related('appointments')
```

3. **Only fetch needed fields**:
```python
patients = Patient.objects.values_list('id', 'patient_id')
```

4. **Use exists()** instead of count():
```python
if Patient.objects.filter(patient_id='PAT001').exists():
    # Much faster than count() > 0
```

5. **Cache expensive queries**:
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def expensive_view(request):
    # This view is cached
```

---

## 🎯 Best Practices

1. **Keep views small** - Move logic to models
2. **Use model methods** - For repeated queries
3. **Write tests** - Before deployment
4. **Use fixtures** - For test data
5. **Version control** - Commit regularly
6. **Use environment variables** - For secrets
7. **Document code** - Add comments
8. **Follow PEP 8** - Python style guide
9. **Use logging** - Instead of print
10. **Error handling** - Try/except blocks

---

## 📱 Mobile-Friendly Tips

Add to base.html:
```django
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

In CSS:
```css
@media (max-width: 768px) {
    .nav-menu {
        flex-direction: column;
    }
    
    .container {
        padding: 0 10px;
    }
}
```

---

## 🚀 Deployment Checklist

Before going live:

- [ ] Change SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Switch to PostgreSQL
- [ ] Configure email service
- [ ] Set up static files
- [ ] Enable HTTPS
- [ ] Add error logging
- [ ] Test all features
- [ ] Backup database plan

---

## 🆘 Get Help

1. **Read error message carefully** - Django errors are helpful
2. **Google the error** - Likely someone had same issue
3. **Check Django docs** - Official documentation
4. **Ask in forums** - Stack Overflow, Django forum
5. **Debug step by step** - Use print/logging
6. **Read your own code** - Often find mistakes
7. **Take a break** - Fresh eyes help

---

**Remember: Debugging is part of programming. You've got this!** 💪
