"""
Management command to test login functionality
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ghg.security import AccountLockout
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Test login functionality and security settings'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email address to test',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password to test (optional)',
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options.get('password')

        self.stdout.write(f"\n🔍 Testing login for: {email}\n")
        
        # 1. Check if user exists
        self.stdout.write("1️⃣ Checking if user exists...")
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ User found: {user.username}"
            ))
            self.stdout.write(f"   - Active: {user.is_active}")
            self.stdout.write(f"   - Staff: {user.is_staff}")
            self.stdout.write(f"   - Superuser: {user.is_superuser}")
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "   ✗ User not found!"
            ))
            return

        # 2. Check account lockout status
        self.stdout.write("\n2️⃣ Checking account lockout status...")
        is_locked = AccountLockout.is_locked(email)
        failed_attempts = AccountLockout.get_failed_attempts(email)
        attempts_remaining = AccountLockout.get_attempts_remaining(email)
        
        if is_locked:
            self.stdout.write(self.style.ERROR(
                f"   ✗ Account is LOCKED!"
            ))
            time_remaining = AccountLockout.get_lockout_time_remaining(email)
            self.stdout.write(f"   - Time remaining: {time_remaining} seconds")
        else:
            self.stdout.write(self.style.SUCCESS(
                "   ✓ Account is not locked"
            ))
        
        self.stdout.write(f"   - Failed attempts: {failed_attempts}")
        self.stdout.write(f"   - Attempts remaining: {attempts_remaining}")

        # 3. Check cache
        self.stdout.write("\n3️⃣ Checking cache...")
        try:
            cache.set('test_key', 'test_value', 10)
            value = cache.get('test_key')
            if value == 'test_value':
                self.stdout.write(self.style.SUCCESS(
                    "   ✓ Cache is working"
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    "   ✗ Cache is not working properly"
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"   ✗ Cache error: {e}"
            ))

        # 4. Test authentication (if password provided)
        if password:
            self.stdout.write("\n4️⃣ Testing authentication...")
            auth_user = authenticate(username=email, password=password)
            if auth_user:
                self.stdout.write(self.style.SUCCESS(
                    "   ✓ Authentication successful!"
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    "   ✗ Authentication failed - wrong password"
                ))

        # 5. Recommendations
        self.stdout.write("\n📋 Recommendations:")
        if is_locked:
            self.stdout.write("   - Run: python manage.py unlock_account " + email)
        if failed_attempts > 0:
            self.stdout.write("   - Run: python manage.py clear_security_cache --email " + email)
        if not user.is_active:
            self.stdout.write("   - User is inactive - activate in admin panel")

        self.stdout.write("\n✅ Test complete\n")
