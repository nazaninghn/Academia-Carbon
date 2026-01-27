#!/usr/bin/env python
"""
Script to create production admin user for Render deployment
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from django.core.management.utils import get_random_secret_key

def create_production_admin():
    """Create production admin user"""
    print("🔧 Creating Production Admin User...")
    
    # Admin credentials for production
    admin_username = 'admin'
    admin_email = 'admin@academiacarbon.com'
    admin_password = 'AcademiaCarbon2026!'  # Strong password for production
    
    try:
        # Check if admin already exists
        if User.objects.filter(username=admin_username).exists():
            print(f"✅ Admin user '{admin_username}' already exists")
            admin_user = User.objects.get(username=admin_username)
        else:
            # Create new admin user
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            print(f"✅ Created new admin user: {admin_username}")
        
        # Display admin credentials
        print("\n" + "="*50)
        print("🚀 PRODUCTION ADMIN CREDENTIALS")
        print("="*50)
        print(f"URL: https://academia-carbon.onrender.com/admin/")
        print(f"Username: {admin_username}")
        print(f"Password: {admin_password}")
        print(f"Email: {admin_email}")
        print("="*50)
        
        # Security reminder
        print("\n⚠️  SECURITY REMINDER:")
        print("- Change the password after first login")
        print("- Enable 2FA if available")
        print("- Only share credentials with authorized personnel")
        print("- Monitor admin access logs regularly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    success = create_production_admin()
    if success:
        print("\n🎉 Production admin setup complete!")
    else:
        print("\n💥 Failed to setup production admin")