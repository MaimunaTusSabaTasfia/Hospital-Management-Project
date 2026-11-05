from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/patient/', views.patient_register, name='patient_register'),
    path('register/doctor/', views.doctor_register, name='doctor_register'),
    
    # Dashboard views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'),
    
    # Appointment views
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.view_appointments, name='view_appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    
    # Medical records
    path('medical-records/', views.view_medical_records, name='view_medical_records'),
    
    # Profile views
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Doctor views
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    
    # Admin views
    path('admin/users/', views.admin_manage_users, name='admin_manage_users'),
]
