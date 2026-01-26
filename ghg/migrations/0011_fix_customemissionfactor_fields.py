# Generated migration to fix CustomEmissionFactor fields

from django.db import migrations, models
import ghg.models


class Migration(migrations.Migration):

    dependencies = [
        ('ghg', '0010_auto_20260126_0135'),
    ]

    operations = [
        # Rename material_name to name
        migrations.RenameField(
            model_name='customemissionfactor',
            old_name='material_name',
            new_name='name',
        ),
        # Rename emission_factor to factor_value
        migrations.RenameField(
            model_name='customemissionfactor',
            old_name='emission_factor',
            new_name='factor_value',
        ),
        # Rename source_reference to reference_source
        migrations.RenameField(
            model_name='customemissionfactor',
            old_name='source_reference',
            new_name='reference_source',
        ),
        # Update certificate_file upload_to
        migrations.AlterField(
            model_name='customemissionfactor',
            name='certificate_file',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=ghg.models.secure_upload_path,
                help_text='Certificate or supporting document (PDF, DOC, DOCX - Max 10MB)'
            ),
        ),
        # Remove fields that don't exist in current model
        migrations.RemoveField(
            model_name='customemissionfactor',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='customemissionfactor',
            name='verified_by',
        ),
        migrations.RemoveField(
            model_name='customemissionfactor',
            name='verified_at',
        ),
        # Add indexes
        migrations.AddIndex(
            model_name='customemissionfactor',
            index=models.Index(fields=['user', 'category'], name='ghg_customem_user_id_cat_idx'),
        ),
        # Add unique_together
        migrations.AlterUniqueTogether(
            name='customemissionfactor',
            unique_together={('user', 'name')},
        ),
    ]
