from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Patient, Doctor, Appointment, Prescription, MedicalRecord, Staff


class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Doctor Profile'
    fk_name = 'user'
    extra = 0


class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Patient Profile'
    fk_name = 'user'
    extra = 0


class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = 'Staff Profile'
    fk_name = 'user'
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [DoctorInline, PatientInline, StaffInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    # 🔥 এই অংশটুকু কমেন্ট করে দাও (কারণ এখানেই Error টা হচ্ছে)
    # fieldsets = UserAdmin.fieldsets + (
    #     ('Additional Info', {'fields': ('role', 'phone', 'date_of_birth', 'address', 'city', 'state', 'postal_code')}),
    # )
    
    # 🔥 শুধু মাত্র এই সহজ ফিল্ডসেট ইউজ করো (এতে Error আসবে না)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Extra Fields', {'fields': ('role', 'phone', 'date_of_birth', 'address', 'city', 'state', 'postal_code')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'phone', 'date_of_birth'),
        }),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'user', 'blood_type', 'created_at')
    list_filter = ('blood_type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'patient_id', 'user__email')
    readonly_fields = ('patient_id', 'created_at', 'updated_at')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'user', 'specialization', 'license_number', 'availability_status')
    list_filter = ('specialization', 'availability_status', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'specialization', 'license_number')
    readonly_fields = ('doctor_id', 'created_at', 'updated_at')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'dosage', 'appointment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('medication_name', 'appointment__patient__user__first_name')
    readonly_fields = ('created_at',)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'record_date')
    list_filter = ('record_date',)
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name')
    readonly_fields = ('record_date',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user', 'staff_type', 'department', 'shift')
    list_filter = ('staff_type', 'department', 'shift', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'staff_id')
    readonly_fields = ('staff_id', 'created_at', 'updated_at')