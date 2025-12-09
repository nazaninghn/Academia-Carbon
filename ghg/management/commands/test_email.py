"""
Management command to test email configuration
Usage: python manage.py test_email
"""

from django.core.management.base import BaseCommand
from ghg.notifications import send_test_notification
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email notification system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Testing email configuration...'))
        self.stdout.write(f'Email Backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'Email Host: {settings.EMAIL_HOST}')
        self.stdout.write(f'From Email: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'Admin Emails: {", ".join(settings.ADMIN_NOTIFICATION_EMAILS)}')
        self.stdout.write('')
        
        try:
            success = send_test_notification()
            
            if success:
                self.stdout.write(self.style.SUCCESS('✓ Test email sent successfully!'))
                self.stdout.write('Check your inbox for the test email.')
            else:
                self.stdout.write(self.style.ERROR('✗ Failed to send test email'))
                self.stdout.write('Check your email configuration in settings.py or .env file')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
            self.stdout.write('')
            self.stdout.write('Common issues:')
            self.stdout.write('1. Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env')
            self.stdout.write('2. For Gmail, enable "App Passwords" in your Google Account')
            self.stdout.write('3. Check EMAIL_HOST and EMAIL_PORT settings')
