# Generated migration to make email unique

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghg', '0001_initial'),  # Update this to your last migration
    ]

    operations = [
        # First, ensure no duplicate emails exist
        migrations.RunSQL(
            sql="""
                -- This will fail if duplicates exist, which is good!
                -- Run fix_duplicate_emails command first if this fails
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        
        # Add unique constraint to email field in auth_user table
        migrations.RunSQL(
            sql="""
                CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique 
                ON auth_user(email);
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS auth_user_email_unique;
            """,
        ),
    ]
