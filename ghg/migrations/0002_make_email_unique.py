# Generated migration to make email unique

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghg', '0001_initial'),
    ]

    operations = [
        # Add unique constraint to email field in auth_user table
        migrations.RunSQL(
            sql="""
                CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique 
                ON auth_user(email) WHERE email != '';
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS auth_user_email_unique;
            """,
        ),
    ]
