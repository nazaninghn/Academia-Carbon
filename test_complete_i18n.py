#!/usr/bin/env python3
"""
Complete i18n test for Academia Carbon
Tests all aspects of the i18n system
"""

import os
import django
from django.conf import settings
from django.utils.translation import activate, gettext as _

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

def test_complete_i18n():
    """Test complete i18n system"""
    
    print("🧪 Complete i18n System Test")
    print("=" * 60)
    
    # Test 1: Language switching
    print("\n1️⃣ Testing Language Switching:")
    
    activate('en')
    english_dashboard = _("Dashboard")
    print(f"   English: {english_dashboard}")
    
    activate('tr')
    turkish_dashboard = _("Dashboard")
    print(f"   Turkish: {turkish_dashboard}")
    
    if english_dashboard != turkish_dashboard:
        print("   ✅ Language switching works!")
    else:
        print("   ❌ Language switching failed!")
    
    # Test 2: Core UI translations
    print("\n2️⃣ Testing Core UI Translations:")
    activate('tr')
    
    core_tests = [
        ("Dashboard", "Kontrol Paneli"),
        ("Data Collection", "Veri Toplama"),
        ("Analysis", "Analiz"),
        ("Settings", "Ayarlar"),
        ("Emissions", "Emisyonlar"),
        ("Login", "Giriş"),
        ("Save", "Kaydet"),
        ("Cancel", "İptal"),
        ("Delete", "Sil"),
        ("Add", "Ekle"),
        ("Search", "Ara"),
        ("Export", "Dışa Aktar"),
        ("Import", "İçe Aktar"),
        ("Home", "Ana Sayfa"),
        ("Help", "Yardım"),
        ("Support", "Destek"),
    ]
    
    passed = 0
    for english, expected in core_tests:
        translated = _(english)
        if translated == expected:
            print(f"   ✅ {english} → {translated}")
            passed += 1
        else:
            print(f"   ❌ {english} → {translated} (expected: {expected})")
    
    print(f"\n   Core UI: {passed}/{len(core_tests)} passed ({passed/len(core_tests)*100:.1f}%)")
    
    # Test 3: Emission-specific translations
    print("\n3️⃣ Testing Emission-Specific Translations:")
    
    emission_tests = [
        ("Stationary Combustion", "Sabit Yanma"),
        ("Mobile Combustion", "Mobil Yanma"),
        ("Process Emissions", "Proses Emisyonları"),
        ("Fugitive Emissions", "Kaçak Emisyonlar"),
        ("Natural Gas", "Doğal Gaz"),
        ("Propane", "Propan"),
        ("Motor Gasoline", "Motor Benzini"),
        ("Carbon Footprint", "Karbon Ayak İzi"),
        ("Scope Summary", "Kapsam Özeti"),
    ]
    
    emission_passed = 0
    for english, expected in emission_tests:
        translated = _(english)
        if translated == expected:
            print(f"   ✅ {english} → {translated}")
            emission_passed += 1
        else:
            print(f"   ❌ {english} → {translated} (expected: {expected})")
    
    print(f"\n   Emissions: {emission_passed}/{len(emission_tests)} passed ({emission_passed/len(emission_tests)*100:.1f}%)")
    
    # Test 4: Units and materials
    print("\n4️⃣ Testing Units and Materials:")
    
    unit_tests = [
        ("Kilometers", "Kilometre"),
        ("Kilograms", "Kilogram"),
        ("Tons", "Ton"),
        ("Liters", "Litre"),
        ("Chemical", "Kimyasal"),
        ("Plastic", "Plastik"),
        ("Wood", "Ahşap"),
        ("Glass", "Cam"),
        ("Metal", "Metal"),
    ]
    
    unit_passed = 0
    for english, expected in unit_tests:
        translated = _(english)
        if translated == expected:
            print(f"   ✅ {english} → {translated}")
            unit_passed += 1
        else:
            print(f"   ❌ {english} → {translated} (expected: {expected})")
    
    print(f"\n   Units/Materials: {unit_passed}/{len(unit_tests)} passed ({unit_passed/len(unit_tests)*100:.1f}%)")
    
    # Test 5: File system check
    print("\n5️⃣ Testing File System:")
    
    mo_file = os.path.join(settings.BASE_DIR, 'locale', 'tr', 'LC_MESSAGES', 'django.mo')
    po_file = os.path.join(settings.BASE_DIR, 'locale', 'tr', 'LC_MESSAGES', 'django.po')
    
    if os.path.exists(mo_file):
        mo_size = os.path.getsize(mo_file)
        print(f"   ✅ django.mo exists: {mo_size} bytes")
    else:
        print("   ❌ django.mo missing!")
    
    if os.path.exists(po_file):
        po_size = os.path.getsize(po_file)
        print(f"   ✅ django.po exists: {po_size} bytes")
    else:
        print("   ❌ django.po missing!")
    
    # Test 6: Settings verification
    print("\n6️⃣ Testing Django Settings:")
    
    print(f"   USE_I18N: {settings.USE_I18N}")
    print(f"   LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
    print(f"   LANGUAGES: {settings.LANGUAGES}")
    print(f"   LOCALE_PATHS: {settings.LOCALE_PATHS}")
    
    # Calculate overall score
    total_tests = len(core_tests) + len(emission_tests) + len(unit_tests)
    total_passed = passed + emission_passed + unit_passed
    overall_score = (total_passed / total_tests) * 100
    
    print(f"\n📊 Overall Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {total_passed}")
    print(f"   Success Rate: {overall_score:.1f}%")
    
    if overall_score >= 90:
        print(f"\n🎉 EXCELLENT! i18n system is working perfectly!")
    elif overall_score >= 75:
        print(f"\n✅ GOOD! i18n system is working well with minor issues.")
    elif overall_score >= 50:
        print(f"\n⚠️  FAIR! i18n system needs improvement.")
    else:
        print(f"\n❌ POOR! i18n system needs major fixes.")
    
    return overall_score >= 75

if __name__ == "__main__":
    test_complete_i18n()