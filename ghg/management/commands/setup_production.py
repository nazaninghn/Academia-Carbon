"""
Management command to set up production environment
Usage: python manage.py setup_production
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Set up production environment with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-email',
            type=str,
            help='Admin email address',
            default='admin@academiacarbon.com'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            help='Admin password',
            default='AdminPass123!'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Setting up production environment...'))
        
        try:
            with transaction.atomic():
                # Create admin user if doesn't exist
                admin_email = options['admin_email']
                admin_password = options['admin_password']
                
                if not User.objects.filter(email=admin_email).exists():
                    admin_user = User.objects.create_user(
                        username=admin_email,
                        email=admin_email,
                        password=admin_password,
                        first_name='Admin',
                        last_name='User',
                        is_staff=True,
                        is_superuser=True
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Created admin user: {admin_email}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Admin user already exists: {admin_email}')
                    )
                
                # Load sample data for demonstration
                from ghg.management.commands.load_sample_data import Command as LoadSampleData
                load_command = LoadSampleData()
                load_command.handle()
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Sample data loaded successfully')
                )
                
        except Exception as e:
            logger.error(f"Error setting up production: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
            raise
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Production setup completed successfully!')
        )
        self.stdout.write('📝 Next steps:')
        self.stdout.write(f'   1. Login with: {admin_email}')
        self.stdout.write('   2. Create additional users via admin panel')
        self.stdout.write('   3. Configure email settings if needed')