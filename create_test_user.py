#!/usr/bin/env python
"""
Script to create a test user for Academia Carbon
Run this with: python create_test_user.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    email = 'test@example.com'
    password = 'test123456'
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        print(f'❌ User with email {email} already exists!')
        user = User.objects.get(email=email)
        # Update password
        user.set_password(password)
        user.save()
        print(f'✅ Password updated for {email}')
    else:
        # Create new user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )
        print(f'✅ Test user created successfully!')
    
    print(f'\n📧 Email: {email}')
    print(f'🔑 Password: {password}')
    print(f'\n🌐 You can now login at: http://127.0.0.1:8000/en/login/')

if __name__ == '__main__':
    create_test_user()
