"""
Management command to fix duplicate emails before making field unique
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count


class Command(BaseCommand):
    help = 'Fix duplicate emails by keeping the oldest account'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write('Searching for duplicate emails...')
        
        # Find duplicate emails
        duplicates = User.objects.values('email').annotate(
            count=Count('email')
        ).filter(count__gt=1)
        
        if not duplicates.exists():
            self.stdout.write(self.style.SUCCESS('✓ No duplicate emails found!'))
            return
        
        self.stdout.write(self.style.WARNING(
            f'Found {duplicates.count()} duplicate emails'
        ))
        
        total_removed = 0
        
        for dup in duplicates:
            email = dup['email']
            users = User.objects.filter(email=email).order_by('date_joined')
            
            # Keep the first (oldest) user
            keep_user = users.first()
            duplicate_users = users.exclude(id=keep_user.id)
            
            self.stdout.write(f'\nEmail: {email}')
            self.stdout.write(f'  Keeping: User #{keep_user.id} (joined {keep_user.date_joined})')
            
            for user in duplicate_users:
                if dry_run:
                    self.stdout.write(self.style.WARNING(
                        f'  Would remove: User #{user.id} (joined {user.date_joined})'
                    ))
                else:
                    self.stdout.write(self.style.ERROR(
                        f'  Removing: User #{user.id} (joined {user.date_joined})'
                    ))
                    user.delete()
                    total_removed += 1
        
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'\nDry run complete. Would remove {total_removed} duplicate accounts.'
            ))
            self.stdout.write('Run without --dry-run to actually remove duplicates.')
        else:
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Removed {total_removed} duplicate accounts!'
            ))
            self.stdout.write('Now you can run: python manage.py make_email_unique')
