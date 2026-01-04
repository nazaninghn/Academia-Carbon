#!/usr/bin/env python
"""
Script to populate initial industry types in the database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from ghg.models import IndustryType

# Initial industry types to populate
INITIAL_INDUSTRIES = [
    {
        'name': 'Commercial/Institutional',
        'code': 'COMM',
        'description': 'Commercial buildings, offices, retail stores, hotels, restaurants, and institutional facilities like schools and hospitals'
    },
    {
        'name': 'Residential and Agriculture/Forestry/Fishing',
        'code': 'RESAG',
        'description': 'Residential buildings, agricultural operations, forestry activities, and fishing/aquaculture facilities'
    },
    {
        'name': 'Manufacturing and Construction',
        'code': 'MANUF',
        'description': 'Manufacturing facilities, construction companies, and industrial production operations'
    },
    {
        'name': 'Energy Industries',
        'code': 'ENERGY',
        'description': 'Power generation, oil and gas extraction, refineries, and other energy sector operations'
    },
    {
        'name': 'Transportation and Logistics',
        'code': 'TRANS',
        'description': 'Transportation companies, logistics providers, shipping, aviation, and freight services'
    },
    {
        'name': 'Information Technology',
        'code': 'IT',
        'description': 'Software companies, data centers, telecommunications, and technology services'
    },
    {
        'name': 'Healthcare and Pharmaceuticals',
        'code': 'HEALTH',
        'description': 'Hospitals, clinics, pharmaceutical companies, and medical device manufacturers'
    },
    {
        'name': 'Financial Services',
        'code': 'FINANCE',
        'description': 'Banks, insurance companies, investment firms, and other financial institutions'
    },
    {
        'name': 'Education',
        'code': 'EDU',
        'description': 'Universities, schools, training centers, and educational institutions'
    },
    {
        'name': 'Retail and Consumer Goods',
        'code': 'RETAIL',
        'description': 'Retail stores, consumer product manufacturers, and distribution companies'
    },
    {
        'name': 'Food and Beverage',
        'code': 'FOOD',
        'description': 'Food processing, restaurants, beverage production, and agricultural food companies'
    },
    {
        'name': 'Textile and Apparel',
        'code': 'TEXTILE',
        'description': 'Textile manufacturing, clothing production, and fashion industry companies'
    },
    {
        'name': 'Mining and Metals',
        'code': 'MINING',
        'description': 'Mining operations, metal processing, and mineral extraction companies'
    },
    {
        'name': 'Chemical and Petrochemical',
        'code': 'CHEM',
        'description': 'Chemical manufacturing, petrochemical production, and specialty chemical companies'
    },
    {
        'name': 'Automotive',
        'code': 'AUTO',
        'description': 'Automotive manufacturing, parts suppliers, and vehicle assembly operations'
    }
]

def populate_industries():
    """Populate initial industry types"""
    created_count = 0
    updated_count = 0
    
    for industry_data in INITIAL_INDUSTRIES:
        industry, created = IndustryType.objects.get_or_create(
            name=industry_data['name'],
            defaults={
                'code': industry_data['code'],
                'description': industry_data['description'],
                'is_active': True
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created: {industry.name}")
        else:
            # Update existing industry if needed
            if industry.code != industry_data['code'] or industry.description != industry_data['description']:
                industry.code = industry_data['code']
                industry.description = industry_data['description']
                industry.save()
                updated_count += 1
                print(f"↻ Updated: {industry.name}")
            else:
                print(f"- Exists: {industry.name}")
    
    print(f"\nSummary:")
    print(f"Created: {created_count} industries")
    print(f"Updated: {updated_count} industries")
    print(f"Total: {IndustryType.objects.count()} industries in database")

if __name__ == '__main__':
    print("Populating initial industry types...")
    populate_industries()
    print("Done!")