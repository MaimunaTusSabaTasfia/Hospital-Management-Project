from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import User, Patient, Doctor, Appointment, MedicalRecord, Staff, Prescription
from .forms import (
    CustomAuthenticationForm, PatientRegistrationForm, DoctorRegistrationForm,
    AppointmentForm, PrescriptionForm, UserProfileForm
)


def ensure_patient_profile(user):
    """Ensure a patient profile exists for the given user."""
    patient, _ = Patient.objects.get_or_create(
        user=user,
        defaults={
            'patient_id': f"PAT{user.id:05d}",
        }
    )
    return patient


def ensure_doctor_profile(user):
    """Ensure a doctor profile exists for the given user."""
    doctor, _ = Doctor.objects.get_or_create(
        user=user,
        defaults={
            'doctor_id': f"DOC{user.id:05d}",
            'specialization': 'General',
            'license_number': f"LIC{user.id:05d}",
        }
    )
    return doctor



# ==================== PUBLIC VIEWS ====================

def home(request):
    """Home page view"""
    context = {
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.filter(status='scheduled').count(),
    }
    return render(request, 'hospital/index.html', context)


@csrf_exempt
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.role == 'admin':
                return redirect('http://127.0.0.1:5500/admin-dashboard.html')
            if user.role == 'doctor':
                return redirect('/dashboard/doctor/')
            if user.role == 'patient':
                return redirect('/dashboard/patient/')
            if user.role in ['nurse', 'staff']:
                return redirect('/dashboard/staff/')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or email, or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'hospital/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


def patient_register(request):
    """Patient registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Doldam Hospital.')
            return redirect('patient_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'hospital/patient_register.html', {'form': form})


def doctor_register(request):
    """Doctor registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login with your credentials.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'hospital/doctor_register.html', {'form': form})


# ==================== DASHBOARD VIEWS ====================

@login_required(login_url='login')
def dashboard(request):
    """Role-based dashboard redirect"""
    user = request.user
    
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    elif user.role in ['nurse', 'staff']:
        return redirect('staff_dashboard')
    else:
        return render(request, 'hospital/dashboard.html')


@login_required(login_url='login')
def patient_dashboard(request):
    """Patient dashboard"""
    if request.user.role != 'patient':
        messages.error(request, 'Access denied. Patient access only.')
        return redirect('dashboard')
    
    patient = ensure_patient_profile(request.user)
    
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-record_date')[:5]
    upcoming_appointments = appointments.filter(status='scheduled')
    
    context = {
        'patient': patient,
        'appointments': appointments[:5],
        'upcoming_appointments': upcoming_appointments[:3],
        'medical_records': medical_records,
        'total_appointments': appointments.count(),
    }
    return render(request, 'hospital/patient_dashboard.html', context)


@login_required(login_url='login')
def doctor_dashboard(request):
    """Doctor dashboard"""
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied. Doctor access only.')
        return redirect('dashboard')
    
    doctor = ensure_doctor_profile(request.user)
    
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    scheduled_appointments = appointments.filter(status='scheduled')
    patients = Patient.objects.filter(appointments__doctor=doctor).distinct()
    
    context = {
        'doctor': doctor,
        'appointments': appointments[:10],
        'scheduled_appointments': scheduled_appointments[:5],
        'total_patients': patients.count(),
        'total_appointments': appointments.count(),
        'pending_appointments': scheduled_appointments.count(),
    }
    return render(request, 'hospital/doctor_dashboard.html', context)


@login_required(login_url='login')
def admin_dashboard(request):
    """Admin dashboard"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('dashboard')
    
    context = {
        'total_users': User.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_staff': Staff.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'scheduled_appointments': Appointment.objects.filter(status='scheduled').count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
        'recent_appointments': Appointment.objects.all().order_by('-created_at')[:10],
    }
    return render(request, 'hospital/admin_dashboard.html', context)


@login_required(login_url='login')
def staff_dashboard(request):
    """Staff/Nurse dashboard"""
    if request.user.role not in ['nurse', 'staff']:
        messages.error(request, 'Access denied. Staff access only.')
        return redirect('dashboard')
    
    appointments = Appointment.objects.all().order_by('-appointment_date')
    patients = Patient.objects.all()
    
    context = {
        'appointments': appointments[:10],
        'total_appointments': appointments.count(),
        'scheduled_appointments': appointments.filter(status='scheduled').count(),
        'total_patients': patients.count(),
    }
    return render(request, 'hospital/staff_dashboard.html', context)


# ==================== APPOINTMENT VIEWS ====================

@login_required(login_url='login')
def book_appointment(request):
    """Book appointment view"""
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('dashboard')
    
    patient = ensure_patient_profile(request.user)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
        'available_doctors': Doctor.objects.filter(availability_status=True),
    }
    return render(request, 'hospital/book_appointment.html', context)


@login_required(login_url='login')
def view_appointments(request):
    """View appointments"""
    if request.user.role == 'patient':
        patient = get_object_or_404(Patient, user=request.user)
        appointments = Appointment.objects.filter(patient=patient)
    elif request.user.role == 'doctor':
        doctor = get_object_or_404(Doctor, user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor)
    else:
        appointments = Appointment.objects.all()
    
    context = {
        'appointments': appointments.order_by('-appointment_date'),
    }
    return render(request, 'hospital/view_appointments.html', context)


@login_required(login_url='login')
def appointment_detail(request, pk):
    """Appointment detail view"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    is_patient = request.user.role == 'patient' and appointment.patient.user == request.user
    is_doctor = request.user.role == 'doctor' and appointment.doctor.user == request.user
    is_admin = request.user.role == 'admin'
    
    if not (is_patient or is_doctor or is_admin):
        messages.error(request, 'You do not have permission to view this appointment.')
        return redirect('dashboard')
    
    context = {
        'appointment': appointment,
        'is_doctor': is_doctor,
    }
    return render(request, 'hospital/appointment_detail.html', context)


# ==================== MEDICAL RECORDS VIEWS ====================

@login_required(login_url='login')
def view_medical_records(request):
    """View medical records"""
    if request.user.role == 'patient':
        patient = get_object_or_404(Patient, user=request.user)
        records = MedicalRecord.objects.filter(patient=patient)
    elif request.user.role == 'doctor':
        doctor = get_object_or_404(Doctor, user=request.user)
        records = MedicalRecord.objects.filter(doctor=doctor)
    else:
        records = MedicalRecord.objects.all()
    
    context = {
        'records': records.order_by('-record_date'),
    }
    return render(request, 'hospital/medical_records.html', context)


# ==================== PROFILE VIEWS ====================

@login_required(login_url='login')
def view_profile(request):
    """View user profile"""
    context = {
        'user': request.user,
    }
    
    # Add role-specific profile
    if request.user.role == 'patient':
        context['patient'] = ensure_patient_profile(request.user)
    elif request.user.role == 'doctor':
        context['doctor'] = ensure_doctor_profile(request.user)
    
    return render(request, 'hospital/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'hospital/edit_profile.html', context)


# ==================== DOCTOR LIST VIEWS ====================

def doctor_list(request):
    """List all available doctors"""
    doctors = Doctor.objects.filter(availability_status=True)
    
    # Filter by specialization if provided
    specialization = request.GET.get('specialization')
    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)
    
    context = {
        'doctors': doctors,
        'specializations': Doctor.objects.values_list('specialization', flat=True).distinct(),
    }
    return render(request, 'hospital/doctor_list.html', context)


def doctor_detail(request, pk):
    """Doctor detail view"""
    doctor = get_object_or_404(Doctor, pk=pk)
    context = {
        'doctor': doctor,
    }
    return render(request, 'hospital/doctor_detail.html', context)


# ==================== ADMIN VIEWS ====================

@login_required(login_url='login')
def admin_manage_users(request):
    """Admin: Manage all users"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by role if provided
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Search by name/email
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(username__icontains=search)
        )
    
    context = {
        'users': users,
        'total_users': User.objects.count(),
        'total_admins': User.objects.filter(role='admin').count(),
        'total_doctors': User.objects.filter(role='doctor').count(),
        'total_patients': User.objects.filter(role='patient').count(),
        'total_staff': User.objects.filter(role__in=['staff', 'nurse']).count(),
        'roles': [('admin', 'Admin'), ('doctor', 'Doctor'), ('patient', 'Patient'), ('staff', 'Staff'), ('nurse', 'Nurse')],
    }
    return render(request, 'hospital/admin_manage_users.html', context)
