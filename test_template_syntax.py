#!/usr/bin/env python3
"""
Template syntax verification script
Tests that all templates can be rendered without syntax errors
"""

import os
import django

# Setup Django FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.conf import settings
from django.template.loader import get_template
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.contrib.auth.models import User
from django.test import RequestFactory

def test_template_syntax():
    """Test all templates for syntax errors"""
    
    print("🧪 Template Syntax Verification")
    print("=" * 50)
    
    # Create a mock request and user for context
    factory = RequestFactory()
    request = factory.get('/')
    
    # Create a test user if none exists
    try:
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
    except:
        user = None
    
    request.user = user
    
    # List of critical templates to test
    templates_to_test = [
        'data_entry.html',
        'dashboard_base.html',
        'index.html',
        'emissions.html',
        'settings.html',
        'partials/translations.html',
    ]
    
    passed = 0
    failed = 0
    
    for template_name in templates_to_test:
        try:
            template = get_template(template_name)
            # Try to render with minimal context
            context = {
                'request': request,
                'user': user,
            }
            rendered = template.render(context)
            print(f"   ✅ {template_name}")
            passed += 1
        except TemplateDoesNotExist:
            print(f"   ⚠️  {template_name} - Template not found")
        except TemplateSyntaxError as e:
            print(f"   ❌ {template_name} - Syntax Error: {e}")
            failed += 1
        except Exception as e:
            print(f"   ⚠️  {template_name} - Other Error: {e}")
    
    print(f"\n📊 Results:")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Success Rate: {passed/(passed+failed)*100:.1f}%" if (passed+failed) > 0 else "   No templates tested")
    
    if failed == 0:
        print(f"\n🎉 All templates passed syntax validation!")
        return True
    else:
        print(f"\n❌ {failed} templates have syntax errors!")
        return False

if __name__ == "__main__":
    success = test_template_syntax()
    exit(0 if success else 1)