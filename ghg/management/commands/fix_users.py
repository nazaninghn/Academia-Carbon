"""
Management command to fix duplicate users and create superuser
Usage: python manage.py fix_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Fix duplicate users and ensure superuser exists'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting user cleanup...'))
        
        try:
            with transaction.atomic():
                self.fix_duplicate_users()
                self.create_superuser_if_needed()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
            raise
        
        self.stdout.write(self.style.SUCCESS('🎉 User cleanup completed!'))
        self.stdout.write('')
        self.stdout.write('🌐 Admin panel: https://academia-carbon.onrender.com/admin/')
        self.stdout.write('📧 Admin email: admin@academiacarbon.com')
        self.stdout.write('🔑 Admin password: AdminPass123!')

    def fix_duplicate_users(self):
        """Fix duplicate users with same email"""
        
        self.stdout.write('🔍 Checking for duplicate users...')
        
        # Find users with duplicate emails
        duplicate_email = "nazaninghafouriann@gmail.com"
        users = User.objects.filter(email=duplicate_email)
        
        self.stdout.write(f'Found {users.count()} users with email: {duplicate_email}')
        
        for user in users:
            self.stdout.write(f'  - ID: {user.id}, Username: {user.username}')
            self.stdout.write(f'    Staff: {user.is_staff}, Superuser: {user.is_superuser}')
            self.stdout.write(f'    Last login: {user.last_login}')
        
        if users.count() > 1:
            self.stdout.write('🔧 Fixing duplicate users...')
            
            # Keep the user that's a superuser/staff, or the most recent one
            primary_user = None
            users_to_delete = []
            
            # First, try to find a superuser or staff user
            for user in users:
                if user.is_superuser or user.is_staff:
                    if primary_user is None:
                        primary_user = user
                    else:
                        users_to_delete.append(user)
                else:
                    users_to_delete.append(user)
            
            # If no superuser/staff found, keep the most recent one
            if primary_user is None:
                primary_user = users.order_by('-date_joined').first()
                users_to_delete = [u for u in users if u.id != primary_user.id]
            
            self.stdout.write(f'✅ Keeping user: {primary_user.username} (ID: {primary_user.id})')
            
            for user in users_to_delete:
                self.stdout.write(f'🗑️  Deleting user: {user.username} (ID: {user.id})')
                user.delete()
            
            self.stdout.write('✅ Duplicate users fixed!')
        else:
            self.stdout.write('✅ No duplicate users found!')

    def create_superuser_if_needed(self):
        """Create a superuser if none exists"""
        
        superusers = User.objects.filter(is_superuser=True)
        
        if superusers.count() == 0:
            self.stdout.write('🔧 No superuser found, creating one...')
            
            admin_user = User.objects.create_user(
                username='admin@academiacarbon.com',
                email='admin@academiacarbon.com',
                password='AdminPass123!',
                first_name='Admin',
                last_name='User',
                is_staff=True,
                is_superuser=True
            )
            
            self.stdout.write(f'✅ Created superuser: {admin_user.email}')
        else:
            self.stdout.write(f'✅ Found {superusers.count()} superuser(s):')
            for su in superusers:
                self.stdout.write(f'   - {su.email} (Username: {su.username})')