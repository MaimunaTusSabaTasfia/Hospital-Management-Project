from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with role-based system"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
        ('staff', 'Staff'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class Patient(models.Model):
    """Patient information model"""
    BLOOD_TYPE_CHOICES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=50, unique=True)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.patient_id}"


class Doctor(models.Model):
    """Doctor information model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    doctor_id = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500)
    availability_status = models.BooleanField(default=True)
    available_days = models.CharField(max_length=100, blank=True, null=True)
    available_hours = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"


class Appointment(models.Model):
    """Appointment booking model"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date']
    
    def __str__(self):
        return f"Appointment: {self.patient.user.get_full_name()} - Dr. {self.doctor.user.get_full_name()}"


class Prescription(models.Model):
    """Prescription model"""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prescriptions'
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
    
    def __str__(self):
        return f"{self.medication_name} - {self.dosage}"


class MedicalRecord(models.Model):
    """Medical records for patients"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField(blank=True, null=True)
    test_results = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'medical_records'
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'
        ordering = ['-record_date']
    
    def __str__(self):
        return f"Record: {self.patient.user.get_full_name()}"


class Staff(models.Model):
    """Staff model for nurses, admin, other staff"""
    STAFF_TYPE_CHOICES = [
        ('nurse', 'Nurse'),
        ('admin', 'Administrator'),
        ('receptionist', 'Receptionist'),
        ('technician', 'Technician'),
        ('maintenance', 'Maintenance'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    staff_id = models.CharField(max_length=50, unique=True)
    staff_type = models.CharField(max_length=50, choices=STAFF_TYPE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)
    shift = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_staff_type_display()}"


def _generate_unique_role_id(prefix, model, field_name):
    index = 1
    while True:
        candidate = f"{prefix}{index:05d}"
        if not model.objects.filter(**{field_name: candidate}).exists():
            return candidate
        index += 1


def generate_unique_patient_id():
    return _generate_unique_role_id('PAT', Patient, 'patient_id')


def generate_unique_doctor_id():
    return _generate_unique_role_id('DOC', Doctor, 'doctor_id')


def generate_unique_doctor_license():
    return _generate_unique_role_id('LIC', Doctor, 'license_number')


def generate_unique_staff_id():
    return _generate_unique_role_id('STF', Staff, 'staff_id')


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """Create or backfill role-specific profile objects for users."""
    if instance.role == 'patient':
        Patient.objects.get_or_create(
            user=instance,
            defaults={
                'patient_id': generate_unique_patient_id(),
            }
        )
    elif instance.role == 'doctor':
        Doctor.objects.get_or_create(
            user=instance,
            defaults={
                'doctor_id': generate_unique_doctor_id(),
                'specialization': 'General',
                'license_number': generate_unique_doctor_license(),
            }
        )
    elif instance.role in ['staff', 'nurse']:
        Staff.objects.get_or_create(
            user=instance,
            defaults={
                'staff_id': generate_unique_staff_id(),
                'staff_type': instance.role,
            }
        )
