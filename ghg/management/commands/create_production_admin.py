from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Create production admin user for Render deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Admin username (default: admin)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@academiacarbon.com',
            help='Admin email (default: admin@academiacarbon.com)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='AcademiaCarbon2026!',
            help='Admin password (default: AcademiaCarbon2026!)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        self.stdout.write(
            self.style.SUCCESS('🔧 Creating Production Admin User...')
        )

        try:
            with transaction.atomic():
                # Check if admin already exists
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.WARNING(f"✅ Admin user '{username}' already exists")
                    )
                    admin_user = User.objects.get(username=username)
                    # Update password in case it changed
                    admin_user.set_password(password)
                    admin_user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"🔄 Updated password for '{username}'")
                    )
                else:
                    # Create new admin user
                    admin_user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Created new admin user: {username}")
                    )

                # Display admin credentials
                self.stdout.write("\n" + "="*50)
                self.stdout.write(
                    self.style.SUCCESS("🚀 PRODUCTION ADMIN CREDENTIALS")
                )
                self.stdout.write("="*50)
                self.stdout.write(f"URL: https://academia-carbon.onrender.com/admin/")
                self.stdout.write(f"Username: {username}")
                self.stdout.write(f"Password: {password}")
                self.stdout.write(f"Email: {email}")
                self.stdout.write("="*50)

                # Security reminder
                self.stdout.write("\n⚠️  SECURITY REMINDER:")
                self.stdout.write("- Change the password after first login")
                self.stdout.write("- Enable 2FA if available")
                self.stdout.write("- Only share credentials with authorized personnel")
                self.stdout.write("- Monitor admin access logs regularly")

                self.stdout.write(
                    self.style.SUCCESS("\n🎉 Production admin setup complete!")
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating admin user: {e}")
            )
            raise