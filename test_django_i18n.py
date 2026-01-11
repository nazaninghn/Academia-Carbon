#!/usr/bin/env python3
"""
Test Django i18n system directly
"""

import os
import django
from django.conf import settings
from django.utils.translation import activate, gettext as _, get_language
from django.utils import translation

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

def test_django_i18n():
    """Test Django i18n system directly"""
    
    print("🔍 Django i18n System Test")
    print("=" * 50)
    
    # Check settings
    print(f"USE_I18N: {settings.USE_I18N}")
    print(f"LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
    print(f"LANGUAGES: {settings.LANGUAGES}")
    print(f"LOCALE_PATHS: {settings.LOCALE_PATHS}")
    
    # Check if locale directory exists
    locale_path = settings.LOCALE_PATHS[0]
    tr_path = locale_path / 'tr' / 'LC_MESSAGES'
    po_file = tr_path / 'django.po'
    mo_file = tr_path / 'django.mo'
    
    print(f"\nFile system check:")
    print(f"  Locale path exists: {locale_path.exists()}")
    print(f"  TR path exists: {tr_path.exists()}")
    print(f"  PO file exists: {po_file.exists()}")
    print(f"  MO file exists: {mo_file.exists()}")
    
    if mo_file.exists():
        print(f"  MO file size: {mo_file.stat().st_size} bytes")
    
    # Test translation loading
    print(f"\nTranslation test:")
    
    # Force reload translations
    translation._default = None
    translation._active = translation.trans_real.TranslationCatalog()
    
    activate('en')
    print(f"  English: Dashboard = {_('Dashboard')}")
    
    activate('tr')
    print(f"  Turkish: Dashboard = {_('Dashboard')}")
    
    # Test a simple string that should definitely be translated
    test_strings = ['Dashboard', 'Emissions', 'Save', 'Cancel']
    
    for test_str in test_strings:
        translated = _(test_str)
        status = "✅ Translated" if test_str != translated else "❌ Not translated"
        print(f"  '{test_str}' -> '{translated}' ({status})")

if __name__ == "__main__":
    test_django_i18n()