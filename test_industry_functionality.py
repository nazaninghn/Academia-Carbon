#!/usr/bin/env python
"""
Test script for industry functionality
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from ghg.models import IndustryType, IndustryRequest
from django.test import Client
from django.urls import reverse

def test_industry_functionality():
    """Test all industry-related functionality"""
    print("🧪 Testing Industry Functionality...")
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='testuser@example.com',
        email='testuser@example.com',
        defaults={'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("✓ Created test user")
    else:
        print("✓ Using existing test user")
    
    # Test 1: Check if industries are loaded
    industry_count = IndustryType.objects.count()
    print(f"✓ Found {industry_count} industry types in database")
    
    # Test 2: Test API endpoints
    client = Client()
    client.login(username='testuser@example.com', password='testpass123')
    
    # Test get industries API
    response = client.get('/api/industries/')
    if response.status_code == 200:
        data = response.json()
        print(f"✓ GET /api/industries/ returned {len(data.get('industries', []))} industries")
    else:
        print(f"❌ GET /api/industries/ failed with status {response.status_code}")
    
    # Test 3: Test industry request API
    test_industry_data = {
        'industry_name': 'Test Robotics Manufacturing',
        'industry_code': 'ROBOT',
        'description': 'Manufacturing of robotic systems and automation equipment for industrial applications',
        'business_context': 'Our company specializes in industrial automation solutions'
    }
    
    response = client.post(
        '/api/industries/request/',
        data=json.dumps(test_industry_data),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✓ Industry request API working - {data.get('message', 'Success')}")
            if data.get('auto_approved'):
                print("  🎉 Industry was auto-approved!")
            else:
                print("  📋 Industry request sent for manual review")
        else:
            print(f"❌ Industry request failed: {data.get('error', 'Unknown error')}")
    else:
        print(f"❌ Industry request API failed with status {response.status_code}")
    
    # Test 4: Check validation
    invalid_data = {
        'industry_name': 'AB',  # Too short
        'description': 'Short'  # Too short
    }
    
    response = client.post(
        '/api/industries/request/',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )
    
    if response.status_code == 400:
        print("✓ Validation working - rejected invalid data")
    else:
        print("❌ Validation not working properly")
    
    # Test 5: Check duplicate prevention
    duplicate_data = {
        'industry_name': 'Manufacturing and Construction',  # Already exists
        'description': 'This should be rejected as duplicate'
    }
    
    response = client.post(
        '/api/industries/request/',
        data=json.dumps(duplicate_data),
        content_type='application/json'
    )
    
    if response.status_code == 400:
        data = response.json()
        if 'already exists' in data.get('error', '').lower():
            print("✓ Duplicate prevention working")
        else:
            print(f"⚠️ Got 400 but different error: {data.get('error')}")
    else:
        print("❌ Duplicate prevention not working")
    
    # Test 6: Check auto-approval patterns
    auto_approve_data = {
        'industry_name': 'Advanced Manufacturing Solutions',
        'description': 'Advanced manufacturing processes and solutions for modern industry'
    }
    
    response = client.post(
        '/api/industries/request/',
        data=json.dumps(auto_approve_data),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('auto_approved'):
            print("✓ Auto-approval working for manufacturing industry")
        else:
            print("📋 Manufacturing industry sent for manual review (expected behavior)")
    
    print("\n📊 Final Statistics:")
    print(f"   Total Industries: {IndustryType.objects.count()}")
    print(f"   Pending Requests: {IndustryRequest.objects.filter(status='pending').count()}")
    print(f"   Approved Requests: {IndustryRequest.objects.filter(status='approved').count()}")
    print(f"   Total Requests: {IndustryRequest.objects.count()}")
    
    print("\n✅ Industry functionality test completed!")

if __name__ == '__main__':
    test_industry_functionality()