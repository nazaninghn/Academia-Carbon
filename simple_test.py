#!/usr/bin/env python
"""
Simple test for industry models
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from ghg.models import IndustryType, IndustryRequest
from django.contrib.auth.models import User

def simple_test():
    print("🔍 Simple Industry Test...")
    
    # Check industries
    industries = IndustryType.objects.all()
    print(f"✓ Found {industries.count()} industries:")
    for industry in industries[:5]:  # Show first 5
        print(f"   - {industry.name} ({industry.code})")
    
    if industries.count() > 5:
        print(f"   ... and {industries.count() - 5} more")
    
    # Check requests
    requests = IndustryRequest.objects.all()
    print(f"✓ Found {requests.count()} industry requests")
    
    # Test auto-approval logic
    test_names = [
        'Manufacturing Solutions',
        'Retail Store',
        'Healthcare Services', 
        'Custom Weird Industry Name'
    ]
    
    auto_approve_patterns = [
        'manufacturing', 'retail', 'healthcare', 'education', 'finance', 
        'technology', 'construction', 'transportation', 'energy', 'agriculture'
    ]
    
    print("\n🤖 Auto-approval test:")
    for name in test_names:
        should_auto_approve = any(pattern in name.lower() for pattern in auto_approve_patterns)
        status = "✅ AUTO-APPROVE" if should_auto_approve else "📋 MANUAL REVIEW"
        print(f"   {name}: {status}")
    
    print("\n✅ Simple test completed!")

if __name__ == '__main__':
    simple_test()