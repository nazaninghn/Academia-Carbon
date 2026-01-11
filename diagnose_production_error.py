#!/usr/bin/env python3
"""
Diagnose production deployment errors
"""

import os
import sys

def check_dependencies():
    """Check if all required packages are available"""
    print("🔍 Checking Dependencies")
    print("-" * 40)
    
    required_packages = [
        'django',
        'requests', 
        'gunicorn',
        'psycopg2',
        'whitenoise',
        'dj_database_url',
        'decouple',
        'openpyxl',
        'reportlab',
        'django_ratelimit'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'django_ratelimit':
                import django_ratelimit
            elif package == 'dj_database_url':
                import dj_database_url
            elif package == 'psycopg2':
                import psycopg2
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages

def check_django_setup():
    """Check Django configuration"""
    print("\n🔧 Checking Django Setup")
    print("-" * 40)
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print("✅ Django setup successful")
        
        # Check critical settings
        print(f"DEBUG: {settings.DEBUG}")
        print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def check_models():
    """Check model definitions"""
    print("\n📊 Checking Models")
    print("-" * 40)
    
    try:
        from ghg.models import EmissionRecord, Supplier, CustomEmissionFactor
        print("✅ Models imported successfully")
        
        # Check for duplicate model definitions
        from django.apps import apps
        app_models = apps.get_app_config('ghg').get_models()
        
        model_names = [model.__name__ for model in app_models]
        duplicates = [name for name in set(model_names) if model_names.count(name) > 1]
        
        if duplicates:
            print(f"❌ Duplicate models found: {duplicates}")
            return False
        else:
            print("✅ No duplicate models")
            return True
            
    except Exception as e:
        print(f"❌ Model check failed: {e}")
        return False

def check_urls():
    """Check URL configuration"""
    print("\n🌐 Checking URLs")
    print("-" * 40)
    
    try:
        from django.urls import reverse
        from carbon_tracker.urls import urlpatterns
        
        print("✅ URL configuration loaded")
        
        # Test some key URLs
        test_urls = ['ghg:landing', 'ghg:email_login']
        
        for url_name in test_urls:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name} -> {url}")
            except Exception as e:
                print(f"❌ {url_name} failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ URL check failed: {e}")
        return False

def check_templates():
    """Check template configuration"""
    print("\n📄 Checking Templates")
    print("-" * 40)
    
    try:
        from django.template.loader import get_template
        
        # Test key templates
        test_templates = ['landing.html', 'index.html', 'auth/login.html']
        
        for template_name in test_templates:
            try:
                template = get_template(template_name)
                print(f"✅ {template_name}")
            except Exception as e:
                print(f"❌ {template_name}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Template check failed: {e}")
        return False

def check_static_files():
    """Check static files configuration"""
    print("\n📁 Checking Static Files")
    print("-" * 40)
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        
        print(f"STATIC_URL: {settings.STATIC_URL}")
        print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        
        # Check if static directories exist
        for static_dir in settings.STATICFILES_DIRS:
            if os.path.exists(static_dir):
                print(f"✅ Static dir exists: {static_dir}")
            else:
                print(f"❌ Static dir missing: {static_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Static files check failed: {e}")
        return False

def main():
    """Run all diagnostic checks"""
    print("🚨 PRODUCTION ERROR DIAGNOSIS")
    print("=" * 50)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Django Setup", check_django_setup),
        ("Models", check_models),
        ("URLs", check_urls),
        ("Templates", check_templates),
        ("Static Files", check_static_files),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            if check_name == "Dependencies":
                missing = check_func()
                result = len(missing) == 0
                if missing:
                    print(f"\n❌ Missing packages: {', '.join(missing)}")
            else:
                result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ {check_name} check crashed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed != total:
        print("\n🔧 RECOMMENDED FIXES:")
        print("1. Install missing dependencies")
        print("2. Check for model conflicts")
        print("3. Verify template paths")
        print("4. Run: python manage.py collectstatic")
        print("5. Check Render logs for detailed errors")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)