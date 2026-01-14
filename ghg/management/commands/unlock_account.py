"""
Management command to manually unlock locked accounts
"""
from django.core.management.base import BaseCommand
from ghg.security import AccountLockout


class Command(BaseCommand):
    help = 'Manually unlock a locked account or IP address'

    def add_arguments(self, parser):
        parser.add_argument(
            'identifier',
            type=str,
            help='Email address or IP address to unlock',
        )

    def handle(self, *args, **options):
        identifier = options['identifier']
        
        if AccountLockout.is_locked(identifier):
            AccountLockout.unlock_account(identifier)
            self.stdout.write(self.style.SUCCESS(
                f'✓ Successfully unlocked: {identifier}'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'Account/IP is not locked: {identifier}'
            ))
