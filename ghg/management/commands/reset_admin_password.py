"""
Management command to reset admin password
Usage: python manage.py reset_admin_password <email> <new_password>
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Reset admin user password'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email address of the admin user'
        )
        parser.add_argument(
            'new_password',
            type=str,
            help='New password for the admin user'
        )

    def handle(self, *args, **options):
        email = options['email']
        new_password = options['new_password']

        try:
            # Find user by email
            user = User.objects.get(email=email)
            
            # Check if user is admin/staff
            if not user.is_staff and not user.is_superuser:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  User {email} is not an admin/staff user'
                    )
                )
                confirm = input('Continue anyway? (yes/no): ')
                if confirm.lower() != 'yes':
                    self.stdout.write(self.style.ERROR('❌ Operation cancelled'))
                    return

            # Set new password
            user.set_password(new_password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Password successfully reset for {email}'
                )
            )
            
            # Show user info
            self.stdout.write(f'\nUser Details:')
            self.stdout.write(f'  Email: {user.email}')
            self.stdout.write(f'  Username: {user.username}')
            self.stdout.write(f'  Is Staff: {user.is_staff}')
            self.stdout.write(f'  Is Superuser: {user.is_superuser}')
            self.stdout.write(f'  Is Active: {user.is_active}')

        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ User with email {email} does not exist'
                )
            )
            
            # Show available admin users
            admins = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
            if admins.exists():
                self.stdout.write('\nAvailable admin users:')
                for admin in admins:
                    self.stdout.write(f'  - {admin.email} ({admin.username})')
            else:
                self.stdout.write('\n⚠️  No admin users found in database!')
                self.stdout.write('Create one with: python manage.py createsuperuser')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
