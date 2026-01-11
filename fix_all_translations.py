#!/usr/bin/env python3
"""
Complete i18n fix script for Academia Carbon
This script fixes all untranslated strings in templates
"""

import os
import re
import glob

def fix_template_translations():
    """Fix all untranslated strings in HTML templates"""
    
    print("🔧 Fixing all template translations...")
    
    # Common translations mapping
    translations = {
        # Basic UI
        "Unit": "{% trans 'Unit' %}",
        "Source": "{% trans 'Source' %}",
        "Value": "{% trans 'Value' %}",
        "Percentage": "{% trans 'Percentage' %}",
        "Distribution": "{% trans 'Distribution' %}",
        "Scope": "{% trans 'Scope' %}",
        "Description": "{% trans 'Description' %}",
        "Optional": "{% trans 'Optional' %}",
        
        # Emission sources
        "Stationary Combustion": "{% trans 'Stationary Combustion' %}",
        "Mobile Combustion": "{% trans 'Mobile Combustion' %}",
        "Process Emissions": "{% trans 'Process Emissions' %}",
        "Fugitive Emissions": "{% trans 'Fugitive Emissions' %}",
        "Natural Gas": "{% trans 'Natural Gas' %}",
        "Propane": "{% trans 'Propane' %}",
        "Motor Gasoline": "{% trans 'Motor Gasoline' %}",
        "Diesel": "{% trans 'Diesel' %}",
        "Electricity": "{% trans 'Electricity' %}",
        
        # Units
        "Kilometers": "{% trans 'Kilometers' %}",
        "Kilograms": "{% trans 'Kilograms' %}",
        "Gigajoules": "{% trans 'Gigajoules' %}",
        "MMBtu": "{% trans 'MMBtu' %}",
        "Tons": "{% trans 'Tons' %}",
        "Liters": "{% trans 'Liters' %}",
        
        # Materials
        "Chemical": "{% trans 'Chemical' %}",
        "Chemical Oil": "{% trans 'Chemical Oil' %}",
        "Plastic": "{% trans 'Plastic' %}",
        "Carton": "{% trans 'Carton' %}",
        "Wood": "{% trans 'Wood' %}",
        "Glass": "{% trans 'Glass' %}",
        "Metal": "{% trans 'Metal' %}",
        "Mineral Oil": "{% trans 'Mineral Oil' %}",
        "Foam Tape": "{% trans 'Foam Tape' %}",
        
        # Energy sources
        "District Heating": "{% trans 'District Heating' %}",
        "District Cooling": "{% trans 'District Cooling' %}",
        "Steam": "{% trans 'Steam' %}",
        "Chilled Water": "{% trans 'Chilled Water' %}",
        
        # Common phrases
        "Scope Summary": "{% trans 'Scope Summary' %}",
        "Academia Carbon": "{% trans 'Academia Carbon' %}",
        "Select an option": "{% trans 'Select an option' %}",
        "Select Unit": "{% trans 'Select Unit' %}",
        "Select Emission Source": "{% trans 'Select Emission Source' %}",
        "Add description": "{% trans 'Add description' %}",
        "You can": "{% trans 'You can' %}",
        "add your proof document": "{% trans 'add your proof document' %}",
        "here": "{% trans 'here' %}",
        "gas bills": "{% trans 'gas bills' %}",
        
        # Descriptions
        "Emissions from purchased electricity consumption": "{% trans 'Emissions from purchased electricity consumption' %}",
        "Emissions from production of purchased goods and services": "{% trans 'Emissions from production of purchased goods and services' %}",
    }
    
    # Find all HTML template files
    template_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        if any(skip in root for skip in ['venv', 'node_modules', '.git', '__pycache__']):
            continue
        for file in files:
            if file.endswith('.html'):
                template_files.append(os.path.join(root, file))
    
    print(f"Found {len(template_files)} template files")
    
    fixed_count = 0
    
    for template_file in template_files:
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Add {% load i18n %} if missing
            if '{% load i18n %}' not in content and '{% extends' in content:
                # Add after extends and load static
                if '{% load static %}' in content:
                    content = content.replace('{% load static %}', '{% load static %}\n{% load i18n %}')
                else:
                    # Add after extends
                    content = re.sub(r'({% extends [^%]+%})', r'\1\n{% load i18n %}', content)
            
            # Apply translations
            for english, translated in translations.items():
                # Replace in various contexts
                patterns = [
                    f'>{english}<',  # Between tags
                    f'"{english}"',  # In attributes
                    f"'{english}'",  # In single quotes
                    f'>{english}:',  # With colon
                    f'>{english} <',  # With space
                ]
                
                for pattern in patterns:
                    if pattern in content and translated not in content:
                        if '>' in pattern and '<' in pattern:
                            new_pattern = pattern.replace(english, translated)
                        elif '"' in pattern:
                            new_pattern = f'"{translated}"'
                        elif "'" in pattern:
                            new_pattern = f"'{translated}'"
                        elif ':' in pattern:
                            new_pattern = f'>{translated}:'
                        elif ' <' in pattern:
                            new_pattern = f'>{translated} <'
                        else:
                            new_pattern = pattern.replace(english, translated)
                        
                        content = content.replace(pattern, new_pattern)
            
            # Save if changed
            if content != original_content:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed: {template_file}")
                fixed_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {template_file}: {e}")
    
    print(f"\n🎉 Fixed {fixed_count} template files")
    return fixed_count > 0

def add_missing_translations_to_po():
    """Add missing translations to django.po file"""
    
    print("\n📝 Adding missing translations to django.po...")
    
    po_file = 'locale/tr/LC_MESSAGES/django.po'
    
    if not os.path.exists(po_file):
        print("❌ django.po file not found")
        return False
    
    # New translations to add
    new_translations = {
        "Stationary Combustion": "Sabit Yanma",
        "Mobile Combustion": "Mobil Yanma", 
        "Process Emissions": "Proses Emisyonları",
        "Fugitive Emissions": "Kaçak Emisyonlar",
        "Natural Gas": "Doğal Gaz",
        "Propane": "Propan",
        "Motor Gasoline": "Motor Benzini",
        "Diesel": "Dizel",
        "Electricity": "Elektrik",
        "Kilometers": "Kilometre",
        "Kilograms": "Kilogram",
        "Gigajoules": "Gigajul",
        "MMBtu": "MMBtu",
        "Tons": "Ton",
        "Liters": "Litre",
        "Chemical": "Kimyasal",
        "Chemical Oil": "Kimyasal Yağ",
        "Plastic": "Plastik",
        "Carton": "Karton",
        "Wood": "Ahşap",
        "Glass": "Cam",
        "Metal": "Metal",
        "Mineral Oil": "Mineral Yağ",
        "Foam Tape": "Köpük Bant",
        "District Heating": "Bölgesel Isıtma",
        "District Cooling": "Bölgesel Soğutma",
        "Steam": "Buhar",
        "Chilled Water": "Soğutulmuş Su",
        "Scope Summary": "Kapsam Özeti",
        "Select an option": "Bir seçenek seçin",
        "Select Unit": "Birim Seçin",
        "Select Emission Source": "Emisyon Kaynağı Seçin",
        "Add description": "Açıklama ekleyin",
        "You can": "Yapabilirsiniz",
        "add your proof document": "kanıt belgenizi ekleyin",
        "here": "buraya",
        "gas bills": "gaz faturaları",
        "Emissions from purchased electricity consumption": "Satın alınan elektrik tüketiminden emisyonlar",
        "Emissions from production of purchased goods and services": "Satın alınan mal ve hizmetlerin üretiminden emisyonlar",
        "Unit": "Birim",
        "Source": "Kaynak",
        "Value": "Değer",
        "Percentage": "Yüzde",
        "Distribution": "Dağılım",
        "Scope": "Kapsam",
        "Description": "Açıklama",
        "Optional": "İsteğe bağlı",
    }
    
    try:
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add new translations
        new_entries = []
        for english, turkish in new_translations.items():
            if f'msgid "{english}"' not in content:
                new_entries.append(f'\nmsgid "{english}"\nmsgstr "{turkish}"\n')
        
        if new_entries:
            with open(po_file, 'a', encoding='utf-8') as f:
                f.write('\n'.join(new_entries))
            print(f"✅ Added {len(new_entries)} new translations")
        else:
            print("✅ All translations already exist")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating django.po: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting complete i18n fix...")
    
    # Fix template translations
    fix_template_translations()
    
    # Add missing translations
    add_missing_translations_to_po()
    
    print("\n✅ Complete i18n fix completed!")
    print("\nNext steps:")
    print("1. Run: python manage.py compilemessages")
    print("2. Test the application in Turkish")
    print("3. Check for any remaining untranslated strings")

if __name__ == "__main__":
    main()