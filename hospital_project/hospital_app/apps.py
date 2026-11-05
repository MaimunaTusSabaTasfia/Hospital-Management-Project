import os
from pathlib import Path

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError


class HospitalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_app'

    def ready(self):
        post_migrate.connect(self.create_default_accounts, sender=self)

    def create_default_accounts(self, **kwargs):
        """Create a default admin user and demo accounts after migrations."""
        User = get_user_model()
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@hospital.com',
                    password='admin12345',
                    first_name='Admin',
                    last_name='User',
                    role='admin',
                    is_staff=True,
                )

            if not User.objects.filter(username='drkim').exists():
                doctor = User.objects.create_user(
                    username='drkim',
                    email='drkim@hospital.com',
                    password='doctor123',
                    first_name='Kim',
                    last_name='Tae-ho',
                    role='doctor',
                    is_staff=False,
                )
                from .models import Doctor
                Doctor.objects.create(
                    user=doctor,
                    doctor_id='DOC00001',
                    specialization='Cardiothoracic Surgery',
                    license_number='LIC-DRKIM-01',
                    experience_years=10,
                    availability_status=True,
                )

            if not User.objects.filter(username='patient1').exists():
                patient = User.objects.create_user(
                    username='patient1',
                    email='patient1@hospital.com',
                    password='patient123',
                    first_name='John',
                    last_name='Doe',
                    role='patient',
                )
                from .models import Patient
                Patient.objects.create(
                    user=patient,
                    patient_id='PAT00001',
                )

            if not User.objects.filter(username='staff1').exists():
                staff_user = User.objects.create_user(
                    username='staff1',
                    email='staff1@hospital.com',
                    password='staff123',
                    first_name='Staff',
                    last_name='Member',
                    role='staff',
                    is_staff=True,
                )
                from .models import Staff
                Staff.objects.create(
                    user=staff_user,
                    staff_id='STF00001',
                    staff_type='receptionist',
                )
            # Backfill any missing role-specific profiles for existing users.
            def unique_id(prefix, model, field):
                index = 1
                while True:
                    candidate = f"{prefix}{index:05d}"
                    if not model.objects.filter(**{field: candidate}).exists():
                        return candidate
                    index += 1

            for user in User.objects.filter(role='patient'):
                from .models import Patient
                Patient.objects.get_or_create(
                    user=user,
                    defaults={'patient_id': unique_id('PAT', Patient, 'patient_id')}
                )

            for user in User.objects.filter(role='doctor'):
                from .models import Doctor
                Doctor.objects.get_or_create(
                    user=user,
                    defaults={
                        'doctor_id': unique_id('DOC', Doctor, 'doctor_id'),
                        'specialization': 'General',
                        'license_number': unique_id('LIC', Doctor, 'license_number'),
                    }
                )

            for user in User.objects.filter(role__in=['staff', 'nurse']):
                from .models import Staff
                Staff.objects.get_or_create(
                    user=user,
                    defaults={
                        'staff_id': unique_id('STF', Staff, 'staff_id'),
                        'staff_type': user.role,
                    }
                )
        except (OperationalError, ProgrammingError):
            # Database is not ready yet or migrations are still running.
            pass
