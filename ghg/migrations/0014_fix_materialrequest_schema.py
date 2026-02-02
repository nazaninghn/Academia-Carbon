# Generated migration to fix MaterialRequest schema mismatch
from django.db import migrations

def add_columns_if_not_exist(apps, schema_editor):
    """Add columns only if they don't exist (SQLite compatible)"""
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Get existing columns
        cursor.execute("PRAGMA table_info(ghg_materialrequest);")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        # Add request_type if not exists
        if 'request_type' not in existing_columns:
            cursor.execute("ALTER TABLE ghg_materialrequest ADD COLUMN request_type VARCHAR(20) DEFAULT 'material';")
        
        # Add name if not exists
        if 'name' not in existing_columns:
            cursor.execute("ALTER TABLE ghg_materialrequest ADD COLUMN name VARCHAR(200) DEFAULT 'Unknown';")
        
        # Add additional_info if not exists
        if 'additional_info' not in existing_columns:
            cursor.execute("ALTER TABLE ghg_materialrequest ADD COLUMN additional_info TEXT;")

def copy_data(apps, schema_editor):
    """Copy data from old columns to new columns"""
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Get existing columns
        cursor.execute("PRAGMA table_info(ghg_materialrequest);")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        # Copy material_name to name if material_name exists
        if 'material_name' in existing_columns and 'name' in existing_columns:
            cursor.execute("UPDATE ghg_materialrequest SET name = material_name WHERE material_name IS NOT NULL AND name = 'Unknown';")

class Migration(migrations.Migration):

    dependencies = [
        ('ghg', '0013_rename_ghg_customem_user_id_cat_idx_ghg_custome_user_id_00a9ef_idx_and_more'),
    ]

    operations = [
        migrations.RunPython(add_columns_if_not_exist, migrations.RunPython.noop),
        migrations.RunPython(copy_data, migrations.RunPython.noop),
    ]