#!/usr/bin/env python
"""
Test script to verify new pages are working correctly
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

def test_new_pages():
    """Test that all new pages load correctly"""
    client = Client()
    
    # Create a test user
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    # Login
    client.login(username='testuser', password='testpass123')
    
    # Test pages
    pages_to_test = [
        ('/', 'Dashboard'),
        ('/data-entry/', 'Data Collection'),
        ('/action-planning/', 'Action Planning'),
        ('/suppliers/', 'Supplier Management'),
        ('/settings/', 'Settings'),
        ('/support/', 'Help & Support'),
    ]
    
    print("🧪 Testing new pages...")
    print("=" * 50)
    
    for url, page_name in pages_to_test:
        try:
            response = client.get(url)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            print(f"{status} | {page_name:<20} | {url}")
            
            if response.status_code != 200:
                print(f"   Error: {response.content.decode()[:100]}...")
                
        except Exception as e:
            print(f"❌ ERROR | {page_name:<20} | {url} - {str(e)}")
    
    print("=" * 50)
    print("✨ Test completed!")

if __name__ == '__main__':
    test_new_pages()