#!/usr/bin/env python
"""
Django Admin Setup Script
========================

This script helps you create admin users for the Hospital Management System.
Run this after you've done: python manage.py migrate

Usage:
    python create_admin.py
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from hospital_app.models import User

def create_admin():
    """Create admin user interactively"""
    print("\n" + "="*60)
    print("HOSPITAL MANAGEMENT SYSTEM - Admin Setup")
    print("="*60 + "\n")
    
    # Check if admin already exists
    existing_admins = User.objects.filter(role='admin')
    if existing_admins.exists():
        print(f"✓ Found {existing_admins.count()} existing admin(s):")
        for admin in existing_admins:
            print(f"  - {admin.username} ({admin.email})")
        print()
    else:
        default_username = 'admin'
        default_email = 'admin@hospital.com'
        default_password = 'admin12345'
        if not User.objects.filter(username=default_username).exists():
            User.objects.create_superuser(
                username=default_username,
                email=default_email,
                password=default_password,
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
            )
            print('✓ No admins found. Created default admin account:')
            print(f'  Username: {default_username}')
            print(f'  Email: {default_email}')
            print(f'  Password: {default_password}')
            print()
    
    while True:
        print("\nOptions:")
        print("1. Create new admin user")
        print("2. View existing admins")
        print("3. Change admin password")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            create_new_admin()
        elif choice == '2':
            view_admins()
        elif choice == '3':
            change_admin_password()
        elif choice == '4':
            print("\n✓ Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def create_new_admin():
    """Create a new admin user"""
    print("\n" + "-"*60)
    print("CREATE NEW ADMIN USER")
    print("-"*60)
    
    username = input("Enter admin username: ").strip()
    
    # Check if username exists
    if User.objects.filter(username=username).exists():
        print("✗ Username already exists!")
        return
    
    email = input("Enter admin email: ").strip()
    
    # Check if email exists
    if User.objects.filter(email=email).exists():
        print("✗ Email already exists!")
        return
    
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    
    password = input("Enter password: ").strip()
    password_confirm = input("Confirm password: ").strip()
    
    if password != password_confirm:
        print("✗ Passwords don't match!")
        return
    
    if len(password) < 6:
        print("✗ Password must be at least 6 characters!")
        return
    
    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='admin',  # Set as admin
            is_staff=True,  # Allow access to admin panel
            is_superuser=True  # Full permissions
        )
        print(f"\n✓ Admin user '{username}' created successfully!")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Role: Admin")
        print(f"  Name: {first_name} {last_name}")
    except Exception as e:
        print(f"✗ Error creating admin: {e}")

def view_admins():
    """View all admin users"""
    print("\n" + "-"*60)
    print("EXISTING ADMIN USERS")
    print("-"*60)
    
    admins = User.objects.filter(role='admin')
    
    if not admins.exists():
        print("No admin users found.")
        return
    
    print(f"\nTotal Admins: {admins.count()}\n")
    
    for i, admin in enumerate(admins, 1):
        status = "✓ Active" if admin.is_active else "✗ Inactive"
        print(f"{i}. {admin.get_full_name() or admin.username}")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Status: {status}")
        print(f"   Joined: {admin.date_joined.strftime('%Y-%m-%d %H:%M')}")
        print()

def change_admin_password():
    """Change admin password"""
    print("\n" + "-"*60)
    print("CHANGE ADMIN PASSWORD")
    print("-"*60)
    
    username = input("Enter admin username: ").strip()
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"✗ User '{username}' not found!")
        return
    
    new_password = input("Enter new password: ").strip()
    confirm_password = input("Confirm new password: ").strip()
    
    if new_password != confirm_password:
        print("✗ Passwords don't match!")
        return
    
    if len(new_password) < 6:
        print("✗ Password must be at least 6 characters!")
        return
    
    user.set_password(new_password)
    user.save()
    print(f"✓ Password changed successfully for '{username}'!")

def main():
    """Main entry point"""
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
