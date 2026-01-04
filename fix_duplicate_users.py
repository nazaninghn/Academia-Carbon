#!/usr/bin/env python3
"""
Script to fix duplicate users issue
Run this with: python manage.py shell < fix_duplicate_users.py
"""

from django.contrib.auth.models import User

def fix_duplicate_users():
    """Fix duplicate users with same email"""
    
    print("🔍 Checking for duplicate users...")
    
    # Find users with email nazaninghafouriann@gmail.com
    duplicate_email = "nazaninghafouriann@gmail.com"
    users = User.objects.filter(email=duplicate_email)
    
    print(f"Found {users.count()} users with email: {duplicate_email}")
    
    for user in users:
        print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}")
        print(f"    Staff: {user.is_staff}, Superuser: {user.is_superuser}")
        print(f"    Last login: {user.last_login}")
        print(f"    Date joined: {user.date_joined}")
        print()
    
    if users.count() > 1:
        print("🔧 Fixing duplicate users...")
        
        # Keep the user with the most recent activity or the one that's a superuser
        primary_user = None
        users_to_delete = []
        
        for user in users:
            if user.is_superuser or user.is_staff:
                if primary_user is None:
                    primary_user = user
                else:
                    # If we already have a primary user, add this to delete list
                    users_to_delete.append(user)
            else:
                users_to_delete.append(user)
        
        # If no superuser found, keep the most recent one
        if primary_user is None:
            primary_user = users.order_by('-date_joined').first()
            users_to_delete = [u for u in users if u.id != primary_user.id]
        
        print(f"✅ Keeping user: {primary_user.username} (ID: {primary_user.id})")
        
        for user in users_to_delete:
            print(f"🗑️  Deleting user: {user.username} (ID: {user.id})")
            user.delete()
        
        print("✅ Duplicate users fixed!")
    else:
        print("✅ No duplicate users found!")

def create_superuser_if_needed():
    """Create a superuser if none exists"""
    
    superusers = User.objects.filter(is_superuser=True)
    
    if superusers.count() == 0:
        print("🔧 No superuser found, creating one...")
        
        admin_user = User.objects.create_user(
            username='admin@academiacarbon.com',
            email='admin@academiacarbon.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True
        )
        
        print(f"✅ Created superuser: {admin_user.email}")
        print("   Password: AdminPass123!")
    else:
        print(f"✅ Found {superusers.count()} superuser(s):")
        for su in superusers:
            print(f"   - {su.email} (Username: {su.username})")

if __name__ == "__main__":
    print("🚀 Starting user cleanup...")
    fix_duplicate_users()
    print()
    create_superuser_if_needed()
    print()
    print("🎉 User cleanup completed!")
    print()
    print("🌐 Admin panel: https://academia-carbon.onrender.com/admin/")
    print("📧 Admin email: admin@academiacarbon.com")
    print("🔑 Admin password: AdminPass123!")

# Run the fix
fix_duplicate_users()
create_superuser_if_needed()