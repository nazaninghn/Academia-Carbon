#!/usr/bin/env python3
"""
Simple i18n test to debug translation issues
"""

import os
import django
from django.conf import settings
from django.utils.translation import activate, gettext as _, get_language

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

def simple_test():
    print("🔍 Simple i18n Debug Test")
    print("=" * 50)
    
    # Test basic language switching
    print(f"Current language: {get_language()}")
    
    # Test in English
    activate('en')
    print(f"\nEnglish (en):")
    print(f"  Language: {get_language()}")
    print(f"  Dashboard: {_('Dashboard')}")
    print(f"  Emissions: {_('Emissions')}")
    print(f"  Natural Gas: {_('Natural Gas')}")
    
    # Test in Turkish
    activate('tr')
    print(f"\nTurkish (tr):")
    print(f"  Language: {get_language()}")
    print(f"  Dashboard: {_('Dashboard')}")
    print(f"  Emissions: {_('Emissions')}")
    print(f"  Natural Gas: {_('Natural Gas')}")
    
    # Check if translations are different
    activate('en')
    en_dashboard = _('Dashboard')
    en_emissions = _('Emissions')
    
    activate('tr')
    tr_dashboard = _('Dashboard')
    tr_emissions = _('Emissions')
    
    print(f"\nComparison:")
    print(f"  Dashboard: EN='{en_dashboard}' vs TR='{tr_dashboard}' -> {'✅ Different' if en_dashboard != tr_dashboard else '❌ Same'}")
    print(f"  Emissions: EN='{en_emissions}' vs TR='{tr_emissions}' -> {'✅ Different' if en_emissions != tr_emissions else '❌ Same'}")
    
    # Check locale paths
    print(f"\nSettings:")
    print(f"  LOCALE_PATHS: {settings.LOCALE_PATHS}")
    print(f"  USE_I18N: {settings.USE_I18N}")
    print(f"  LANGUAGES: {settings.LANGUAGES}")
    
    # Check if files exist
    locale_dir = settings.LOCALE_PATHS[0] / 'tr' / 'LC_MESSAGES'
    po_file = locale_dir / 'django.po'
    mo_file = locale_dir / 'django.mo'
    
    print(f"\nFiles:")
    print(f"  PO file exists: {po_file.exists()} ({po_file})")
    print(f"  MO file exists: {mo_file.exists()} ({mo_file})")
    
    if mo_file.exists():
        print(f"  MO file size: {mo_file.stat().st_size} bytes")

if __name__ == "__main__":
    simple_test()