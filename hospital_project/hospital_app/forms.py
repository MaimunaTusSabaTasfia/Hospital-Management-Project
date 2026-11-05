from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Patient, Doctor, Appointment, Prescription, Staff


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class PatientRegistrationForm(UserCreationForm):
    """Patient registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            # Create patient profile
            Patient.objects.create(
                user=user,
                patient_id=f"PAT{user.id:05d}"
            )
        return user


class DoctorRegistrationForm(UserCreationForm):
    """Doctor registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=15, required=False)
    specialization = forms.CharField(max_length=100, required=True)
    license_number = forms.CharField(max_length=50, required=True)
    experience_years = forms.IntegerField(required=False, initial=0)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'doctor'
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            # Create doctor profile
            Doctor.objects.create(
                user=user,
                doctor_id=f"DOC{user.id:05d}",
                specialization=self.cleaned_data['specialization'],
                license_number=self.cleaned_data['license_number'],
                experience_years=self.cleaned_data.get('experience_years', 0) or 0
            )
        return user


class AppointmentForm(forms.ModelForm):
    """Appointment booking form"""
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your symptoms or reason for visit'
            })
        }


class PrescriptionForm(forms.ModelForm):
    """Prescription form"""
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class UserProfileForm(forms.ModelForm):
    """User profile update form"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'postal_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
