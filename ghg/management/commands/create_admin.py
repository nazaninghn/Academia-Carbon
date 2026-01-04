"""
Management command to create a new admin user
Usage: python manage.py create_admin --email admin@example.com --password mypassword
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
import getpass

class Command(BaseCommand):
    help = 'Create a new admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Admin email address',
            required=True
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Admin password (if not provided, will prompt)',
            default=None
        )
        parser.add_argument(
            '--first-name',
            type=str,
            help='First name',
            default='Admin'
        )
        parser.add_argument(
            '--last-name',
            type=str,
            help='Last name',
            default='User'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']
        
        # If password not provided, prompt for it
        if not password:
            password = getpass.getpass('Enter password: ')
            password_confirm = getpass.getpass('Confirm password: ')
            
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('❌ Passwords do not match!')
                )
                return
        
        try:
            with transaction.atomic():
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    self.stdout.write(
                        self.style.ERROR(f'❌ User with email {email} already exists!')
                    )
                    return
                
                # Create admin user
                admin_user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=True,
                    is_superuser=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Admin user created successfully!')
                )
                self.stdout.write(f'   📧 Email: {email}')
                self.stdout.write(f'   👤 Name: {first_name} {last_name}')
                self.stdout.write(f'   🔑 Admin privileges: Yes')
                self.stdout.write('')
                self.stdout.write('🌐 You can now login at:')
                self.stdout.write('   https://academia-carbon.onrender.com/admin/')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating admin user: {str(e)}')
            )