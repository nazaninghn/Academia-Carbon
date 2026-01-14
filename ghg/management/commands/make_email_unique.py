"""
Management command to make email field unique in User model
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection


class Command(BaseCommand):
    help = 'Make email field unique in User model'

    def handle(self, *args, **options):
        self.stdout.write('Checking for duplicate emails...')
        
        # Find duplicate emails
        from django.db.models import Count
        duplicates = User.objects.values('email').annotate(
            count=Count('email')
        ).filter(count__gt=1)
        
        if duplicates.exists():
            self.stdout.write(self.style.WARNING(
                f'Found {duplicates.count()} duplicate emails:'
            ))
            for dup in duplicates:
                self.stdout.write(f"  - {dup['email']} ({dup['count']} times)")
            
            self.stdout.write(self.style.ERROR(
                '\nPlease fix duplicate emails before making field unique!'
            ))
            self.stdout.write('You can run: python manage.py fix_duplicate_emails')
            return
        
        # Add unique constraint
        self.stdout.write('Adding unique constraint to email field...')
        
        with connection.cursor() as cursor:
            # Check database type
            db_vendor = connection.vendor
            
            if db_vendor == 'postgresql':
                cursor.execute("""
                    ALTER TABLE auth_user 
                    ADD CONSTRAINT auth_user_email_unique UNIQUE (email);
                """)
            elif db_vendor == 'sqlite':
                # SQLite doesn't support ALTER TABLE ADD CONSTRAINT
                # We need to use a migration instead
                self.stdout.write(self.style.WARNING(
                    'SQLite detected. Please use Django migration instead:'
                ))
                self.stdout.write('  python manage.py makemigrations')
                self.stdout.write('  python manage.py migrate')
                return
            elif db_vendor == 'mysql':
                cursor.execute("""
                    ALTER TABLE auth_user 
                    ADD UNIQUE INDEX auth_user_email_unique (email);
                """)
        
        self.stdout.write(self.style.SUCCESS(
            '✓ Email field is now unique at database level!'
        ))
