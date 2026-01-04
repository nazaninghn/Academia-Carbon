#!/usr/bin/env python
"""
Simple test to check URL patterns
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.urls import reverse
from django.test import RequestFactory
from ghg import views

def test_url_patterns():
    """Test URL patterns and view functions"""
    print("🔗 Testing URL patterns...")
    print("=" * 50)
    
    url_tests = [
        ('ghg:index', 'Dashboard'),
        ('ghg:data_entry', 'Data Collection'),
        ('ghg:action_planning', 'Action Planning'),
        ('ghg:suppliers', 'Supplier Management'),
        ('ghg:settings', 'Settings'),
        ('ghg:support', 'Help & Support'),
    ]
    
    factory = RequestFactory()
    
    for url_name, page_name in url_tests:
        try:
            # Test URL reverse
            url = reverse(url_name)
            print(f"✅ URL  | {page_name:<20} | {url}")
            
            # Test view function exists
            if url_name == 'ghg:index':
                view_func = views.index
            elif url_name == 'ghg:data_entry':
                view_func = views.data_entry
            elif url_name == 'ghg:action_planning':
                view_func = views.action_planning
            elif url_name == 'ghg:suppliers':
                view_func = views.suppliers
            elif url_name == 'ghg:settings':
                view_func = views.settings
            elif url_name == 'ghg:support':
                view_func = views.support
            
            print(f"✅ VIEW | {page_name:<20} | {view_func.__name__}")
            
        except Exception as e:
            print(f"❌ ERROR | {page_name:<20} | {str(e)}")
    
    print("=" * 50)
    print("✨ URL pattern test completed!")

if __name__ == '__main__':
    test_url_patterns()