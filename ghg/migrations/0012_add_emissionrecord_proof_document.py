# Generated migration to add proof_document to EmissionRecord

from django.db import migrations, models
import ghg.models
import ghg.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ghg', '0011_fix_customemissionfactor_fields'),
    ]

    operations = [
        # Add proof_document field
        migrations.AddField(
            model_name='emissionrecord',
            name='proof_document',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=ghg.models.secure_upload_path,
                validators=[ghg.validators.validate_document_file],
                help_text='Supporting document (PDF, DOC, DOCX, TXT - Max 10MB)'
            ),
        ),
        # Add indexes
        migrations.AddIndex(
            model_name='emissionrecord',
            index=models.Index(fields=['user', '-created_at'], name='ghg_emissio_user_id_created_idx'),
        ),
        migrations.AddIndex(
            model_name='emissionrecord',
            index=models.Index(fields=['user', 'scope'], name='ghg_emissio_user_id_scope_idx'),
        ),
    ]
