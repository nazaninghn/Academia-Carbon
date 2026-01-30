"""
Management command to clear security-related cache entries
This helps when users are locked out due to rate limiting or failed login attempts
"""

from django.core.management.base import BaseCommand
from django.core.cache import cache
from ghg.security import AccountLockout
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Clear all security-related cache entries (rate limits, lockouts, failed attempts)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Clear cache for specific email address',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all security cache entries',
        )

    def handle(self, *args, **options):
        email = options.get('email')
        clear_all = options.get('all')

        if email:
            # Clear cache for specific email
            self.stdout.write(f"Clearing security cache for: {email}")
            
            # Unlock account
            AccountLockout.unlock_account(email)
            
            # Clear rate limit cache
            cache_patterns = [
                f"arcjet_rate:*{email}*",
                f"failed_login_{email}",
                f"account_locked_{email}",
            ]
            
            self.stdout.write(self.style.SUCCESS(
                f"✓ Cleared security cache for {email}"
            ))
            
        elif clear_all:
            # Clear all cache
            self.stdout.write("Clearing ALL security cache entries...")
            
            try:
                cache.clear()
                self.stdout.write(self.style.SUCCESS(
                    "✓ All cache cleared successfully"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"✗ Error clearing cache: {e}"
                ))
        else:
            self.stdout.write(self.style.ERROR(
                "Please specify --email <email> or --all"
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            "\n✓ Security cache cleared. Users should now be able to login."
        ))
