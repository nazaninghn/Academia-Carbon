"""
Security validators for Academia Carbon
"""

import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Allowed file types for uploads
ALLOWED_FILE_TYPES = {
    'documents': {
        'extensions': ['.pdf', '.doc', '.docx', '.txt'],
        'max_size': 10 * 1024 * 1024,  # 10MB
    },
    'images': {
        'extensions': ['.jpg', '.jpeg', '.png', '.gif'],
        'max_size': 5 * 1024 * 1024,  # 5MB
    }
}

def validate_file_extension(file, allowed_types='documents'):
    """Validate file extension"""
    if not file:
        return
    
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = ALLOWED_FILE_TYPES[allowed_types]['extensions']
    
    if ext not in allowed_extensions:
        raise ValidationError(
            _('File type not allowed. Allowed types: %(extensions)s'),
            params={'extensions': ', '.join(allowed_extensions)},
        )

def validate_file_size(file, allowed_types='documents'):
    """Validate file size"""
    if not file:
        return
    
    max_size = ALLOWED_FILE_TYPES[allowed_types]['max_size']
    
    if file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(
            _('File too large. Maximum size: %(max_size)s MB'),
            params={'max_size': max_size_mb},
        )

def validate_document_file(file):
    """Validate document file specifically"""
    if not file:
        return
    
    validate_file_extension(file, 'documents')
    validate_file_size(file, 'documents')

def sanitize_filename(filename):
    """Sanitize filename for security"""
    import re
    
    # Remove path components
    filename = os.path.basename(filename)
    
    # Remove dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    
    return filename

def validate_user_permission(user, obj):
    """Validate that user has permission to access object"""
    if not user.is_authenticated:
        raise ValidationError(_('Authentication required'))
    
    if hasattr(obj, 'user') and obj.user != user:
        raise ValidationError(_('Permission denied'))
    
    return True