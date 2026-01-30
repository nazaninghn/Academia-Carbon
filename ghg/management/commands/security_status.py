"""
Management command to show security system status
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from ghg.security import AccountLockout, MAX_LOGIN_ATTEMPTS, LOCKOUT_DURATION
import sys


class Command(BaseCommand):
    help = 'Show security system status and configuration'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*60)
        self.stdout.write("🔒 SECURITY SYSTEM STATUS")
        self.stdout.write("="*60 + "\n")

        # 1. Environment
        self.stdout.write("📋 ENVIRONMENT:")
        self.stdout.write(f"   DEBUG: {settings.DEBUG}")
        self.stdout.write(f"   ARCJET_ENABLED: {getattr(settings, 'ARCJET_ENABLED', True)}")
        self.stdout.write(f"   ARCJET_MODE: {getattr(settings, 'ARCJET_MODE', 'SIMULATION')}")
        
        # 2. Security Settings
        self.stdout.write("\n🛡️  SECURITY SETTINGS:")
        self.stdout.write(f"   MAX_LOGIN_ATTEMPTS: {MAX_LOGIN_ATTEMPTS}")
        self.stdout.write(f"   LOCKOUT_DURATION: {LOCKOUT_DURATION} minutes")
        self.stdout.write(f"   SESSION_COOKIE_AGE: {settings.SESSION_COOKIE_AGE} seconds")
        self.stdout.write(f"   SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
        
        # 3. Cache Status
        self.stdout.write("\n💾 CACHE STATUS:")
        try:
            cache.set('test_key', 'test_value', 10)
            value = cache.get('test_key')
            if value == 'test_value':
                self.stdout.write(self.style.SUCCESS("   ✓ Cache is working"))
            else:
                self.stdout.write(self.style.ERROR("   ✗ Cache is not working"))
            
            cache_backend = settings.CACHES['default']['BACKEND']
            self.stdout.write(f"   Backend: {cache_backend}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ✗ Cache error: {e}"))
        
        # 4. Users Status
        self.stdout.write("\n👥 USERS:")
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        admin_users = User.objects.filter(is_superuser=True).count()
        
        self.stdout.write(f"   Total: {total_users}")
        self.stdout.write(f"   Active: {active_users}")
        self.stdout.write(f"   Admins: {admin_users}")
        
        # 5. Locked Accounts
        self.stdout.write("\n🔒 LOCKED ACCOUNTS:")
        locked_count = 0
        for user in User.objects.all():
            if AccountLockout.is_locked(user.email):
                locked_count += 1
                time_remaining = AccountLockout.get_lockout_time_remaining(user.email)
                self.stdout.write(self.style.WARNING(
                    f"   ⚠️  {user.email} - {time_remaining}s remaining"
                ))
        
        if locked_count == 0:
            self.stdout.write(self.style.SUCCESS("   ✓ No locked accounts"))
        else:
            self.stdout.write(self.style.WARNING(f"   ⚠️  {locked_count} locked accounts"))
        
        # 6. Middleware
        self.stdout.write("\n🔧 MIDDLEWARE:")
        security_middleware = [
            'ghg.arcjet_simulation.ArcjetSimulatorMiddleware',
            'ghg.middleware.SecurityHeadersMiddleware',
            'ghg.middleware.RateLimitMiddleware',
            'ghg.middleware.SecurityLoggingMiddleware',
        ]
        
        for mw in security_middleware:
            if mw in settings.MIDDLEWARE:
                self.stdout.write(self.style.SUCCESS(f"   ✓ {mw.split('.')[-1]}"))
            else:
                self.stdout.write(self.style.ERROR(f"   ✗ {mw.split('.')[-1]} (not found)"))
        
        # 7. Recommendations
        self.stdout.write("\n💡 RECOMMENDATIONS:")
        
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING(
                "   ⚠️  DEBUG is True - disable in production!"
            ))
        
        if getattr(settings, 'ARCJET_ENABLED', True):
            self.stdout.write(
                "   ℹ️  Arcjet is enabled - disable if blocking legitimate users"
            )
        
        cache_backend = settings.CACHES['default']['BACKEND']
        if 'locmem' in cache_backend.lower():
            self.stdout.write(self.style.WARNING(
                "   ⚠️  Using LocMemCache - consider Redis for production"
            ))
        
        if locked_count > 0:
            self.stdout.write(self.style.WARNING(
                "   ⚠️  Run: python manage.py clear_security_cache --all"
            ))
        
        self.stdout.write("\n" + "="*60 + "\n")
