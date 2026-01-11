#!/usr/bin/env python3
"""
Debug specific translation issues
"""

import os
import django
from django.conf import settings
from django.utils.translation import activate, gettext as _, get_language
from django.utils import translation

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

def debug_specific_translations():
    """Debug specific failing translations"""
    
    print("🔍 Debug Specific Translations")
    print("=" * 50)
    
    # Test specific failing translations
    failing_translations = [
        "Emissions",
        "Stationary Combustion", 
        "Mobile Combustion",
        "Natural Gas",
        "Kilograms",
        "Liters"
    ]
    
    activate('tr')
    print(f"Current language: {get_language()}")
    print(f"Translation catalog loaded: {translation.get_language()}")
    
    for text in failing_translations:
        translated = _(text)
        print(f"'{text}' -> '{translated}' ({'✅ Translated' if text != translated else '❌ Not translated'})")
    
    # Check translation backend
    from django.utils.translation import trans_real
    print(f"\nTranslation backend: {type(trans_real._active)}")
    
    # Try to get the current translation catalog
    try:
        current_translation = trans_real._active.value
        if hasattr(current_translation, '_catalog'):
            print(f"Current catalog has {len(current_translation._catalog)} entries")
            # Check a few specific entries
            for text in failing_translations[:3]:
                if text in current_translation._catalog:
                    print(f"  '{text}' found: '{current_translation._catalog[text]}'")
                else:
                    print(f"  '{text}' NOT found in catalog")
        else:
            print("No _catalog attribute found")
    except Exception as e:
        print(f"Error accessing catalog: {e}")
    
    # Check locale paths
    print(f"\nLocale paths: {settings.LOCALE_PATHS}")
    
    # Check if mo file exists and size
    mo_file = settings.LOCALE_PATHS[0] / 'tr' / 'LC_MESSAGES' / 'django.mo'
    if mo_file.exists():
        print(f"MO file exists: {mo_file} ({mo_file.stat().st_size} bytes)")
    else:
        print(f"MO file missing: {mo_file}")

if __name__ == "__main__":
    debug_specific_translations()