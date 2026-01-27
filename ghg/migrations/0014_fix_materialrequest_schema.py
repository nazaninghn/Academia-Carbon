# Generated migration to fix MaterialRequest schema mismatch
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('ghg', '0013_rename_ghg_customem_user_id_cat_idx_ghg_custome_user_id_00a9ef_idx_and_more'),
    ]

    operations = [
        # Add missing columns that the current model expects
        migrations.RunSQL(
            "ALTER TABLE ghg_materialrequest ADD COLUMN IF NOT EXISTS request_type VARCHAR(20) DEFAULT 'material';",
            reverse_sql="ALTER TABLE ghg_materialrequest DROP COLUMN IF EXISTS request_type;"
        ),
        migrations.RunSQL(
            "ALTER TABLE ghg_materialrequest ADD COLUMN IF NOT EXISTS name VARCHAR(200) DEFAULT 'Unknown';",
            reverse_sql="ALTER TABLE ghg_materialrequest DROP COLUMN IF EXISTS name;"
        ),
        migrations.RunSQL(
            "ALTER TABLE ghg_materialrequest ADD COLUMN IF NOT EXISTS additional_info TEXT;",
            reverse_sql="ALTER TABLE ghg_materialrequest DROP COLUMN IF EXISTS additional_info;"
        ),
        
        # Copy data from old columns to new columns
        migrations.RunSQL(
            "UPDATE ghg_materialrequest SET name = material_name WHERE material_name IS NOT NULL AND name = 'Unknown';",
            reverse_sql=""
        ),
        migrations.RunSQL(
            "UPDATE ghg_materialrequest SET description = COALESCE(description, 'Material: ' || material_name || ' (Category: ' || category || ')') WHERE description = '';",
            reverse_sql=""
        ),
        
        # Set request_type based on existing data
        migrations.RunSQL(
            "UPDATE ghg_materialrequest SET request_type = 'material' WHERE request_type = 'material';",
            reverse_sql=""
        ),
    ]