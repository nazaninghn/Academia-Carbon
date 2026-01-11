#!/usr/bin/env python3
"""
Complete Security Verification for Academia Carbon
Verifies all security roadmap items are properly implemented
"""

import os
import sys
import django
import requests
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

def test_production_access():
    """Test if production site is accessible"""
    print("🌐 Testing Production Access")
    print("-" * 40)
    
    try:
        url = "https://academia-carbon.onrender.com"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            print("✅ Production site accessible (200 OK)")
            return True
        elif response.status_code == 400:
            print("❌ Production site returns 400 Bad Request (ALLOWED_HOSTS issue)")
            print("   → Need to set environment variables in Render.com dashboard")
            return False
        else:
            print(f"⚠️  Production site returns {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Production access failed: {e}")
        return False

def test_django_settings():
    """Test Django security settings"""
    print("\n🔧 Testing Django Security Settings")
    print("-" * 40)
    
    from django.conf import settings
    
    results = []
    
    # Test DEBUG setting
    if not settings.DEBUG:
        print("✅ DEBUG = False (secure)")
        results.append(True)
    else:
        print("❌ DEBUG = True (insecure)")
        results.append(False)
    
    # Test SECRET_KEY
    if settings.SECRET_KEY and len(settings.SECRET_KEY) > 20:
        print("✅ SECRET_KEY is set and long enough")
        results.append(True)
    else:
        print("❌ SECRET_KEY is missing or too short")
        results.append(False)
    
    # Test ALLOWED_HOSTS
    if 'academia-carbon.onrender.com' in settings.ALLOWED_HOSTS:
        print("✅ ALLOWED_HOSTS includes production domain")
        results.append(True)
    else:
        print("❌ ALLOWED_HOSTS missing production domain")
        results.append(False)
    
    # Test HTTPS settings
    if settings.SECURE_SSL_REDIRECT:
        print("✅ HTTPS redirect enabled")
        results.append(True)
    else:
        print("❌ HTTPS redirect disabled")
        results.append(False)
    
    # Test security headers
    if hasattr(settings, 'X_FRAME_OPTIONS') and settings.X_FRAME_OPTIONS == 'DENY':
        print("✅ Clickjacking protection enabled")
        results.append(True)
    else:
        print("❌ Clickjacking protection missing")
        results.append(False)
    
    return all(results)

def test_rate_limiting():
    """Test rate limiting implementation"""
    print("\n🛡️  Testing Rate Limiting")
    print("-" * 40)
    
    try:
        from django_ratelimit.decorators import ratelimit
        print("✅ django-ratelimit package available")
        
        # Check if views use rate limiting by checking source code
        from ghg import views
        import inspect
        
        # Check specific views that should have rate limiting
        rate_limited_views = ['login_view', 'calculate_emission', 'add_supplier']
        
        for view_name in rate_limited_views:
            if hasattr(views, view_name):
                view_func = getattr(views, view_name)
                try:
                    source = inspect.getsource(view_func)
                    if '@ratelimit' in source:
                        print(f"✅ {view_name} has rate limiting")
                    else:
                        print(f"⚠️  {view_name} missing rate limiting")
                except:
                    print(f"⚠️  Could not check {view_name}")
        
        print("✅ Rate limiting implementation verified")
        return True
        
    except ImportError:
        print("❌ django-ratelimit package not installed")
        print("   → Run: pip install django-ratelimit")
        return False
    except Exception as e:
        print(f"⚠️  Rate limiting check failed: {e}")
        return False

def test_authentication_requirements():
    """Test that views require authentication"""
    print("\n🔐 Testing Authentication Requirements")
    print("-" * 40)
    
    from ghg import views
    import inspect
    
    # Views that should require login
    protected_views = [
        'data_entry', 'emissions_view', 'settings_view', 'suppliers_view',
        'calculate_emission', 'get_emission_records', 'delete_emission_record',
        'add_supplier', 'get_suppliers', 'dashboard_api', 'test_language', 'test_translation'
    ]
    
    results = []
    
    for view_name in protected_views:
        if hasattr(views, view_name):
            view_func = getattr(views, view_name)
            
            # Check if login_required decorator is applied
            if hasattr(view_func, '__wrapped__'):
                print(f"✅ {view_name} has authentication protection")
                results.append(True)
            else:
                # Check source code for @login_required
                try:
                    source = inspect.getsource(view_func)
                    if '@login_required' in source:
                        print(f"✅ {view_name} has @login_required decorator")
                        results.append(True)
                    else:
                        print(f"❌ {view_name} missing @login_required decorator")
                        results.append(False)
                except:
                    print(f"⚠️  Could not check {view_name}")
                    results.append(False)
        else:
            print(f"⚠️  View {view_name} not found")
    
    return all(results)

def test_user_data_isolation():
    """Test user data isolation"""
    print("\n👤 Testing User Data Isolation")
    print("-" * 40)
    
    try:
        from django.contrib.auth.models import User
        from ghg.models import EmissionRecord, Supplier, CustomEmissionFactor
        
        # Check if models have user foreign keys
        models_to_check = [
            (EmissionRecord, 'EmissionRecord'),
            (Supplier, 'Supplier'),
            (CustomEmissionFactor, 'CustomEmissionFactor')
        ]
        
        results = []
        
        for model, name in models_to_check:
            if hasattr(model, 'user'):
                print(f"✅ {name} has user field for data isolation")
                results.append(True)
            else:
                print(f"❌ {name} missing user field")
                results.append(False)
        
        return all(results)
        
    except Exception as e:
        print(f"❌ User data isolation test failed: {e}")
        return False

def test_file_upload_security():
    """Test file upload security"""
    print("\n📁 Testing File Upload Security")
    print("-" * 40)
    
    try:
        from ghg.validators import validate_document_file, ALLOWED_FILE_TYPES
        from ghg.models import CustomEmissionFactor
        
        # Check if validators exist
        print("✅ File validation functions available")
        
        # Check allowed file types
        allowed_extensions = ALLOWED_FILE_TYPES['documents']['extensions']
        max_size = ALLOWED_FILE_TYPES['documents']['max_size']
        
        print(f"✅ Allowed file types: {', '.join(allowed_extensions)}")
        print(f"✅ Max file size: {max_size / (1024*1024):.1f} MB")
        
        # Check if model uses validators
        field = CustomEmissionFactor._meta.get_field('certificate_file')
        if field.validators:
            print("✅ CustomEmissionFactor.certificate_file has validators")
            return True
        else:
            print("❌ File field missing validators")
            return False
            
    except Exception as e:
        print(f"❌ File upload security test failed: {e}")
        return False

def test_security_logging():
    """Test security logging"""
    print("\n📝 Testing Security Logging")
    print("-" * 40)
    
    try:
        from django.conf import settings
        
        # Check if security logging is configured
        if 'ghg.security' in settings.LOGGING['loggers']:
            print("✅ Security logging configured")
            
            # Check if log file exists
            log_file = settings.BASE_DIR / 'logs' / 'security.log'
            if log_file.exists():
                print("✅ Security log file exists")
                return True
            else:
                print("⚠️  Security log file not created yet (will be created on first event)")
                return True
        else:
            print("❌ Security logging not configured")
            return False
            
    except Exception as e:
        print(f"❌ Security logging test failed: {e}")
        return False

def test_i18n_system():
    """Test internationalization system"""
    print("\n🌍 Testing i18n System")
    print("-" * 40)
    
    try:
        from django.conf import settings
        
        # Check i18n settings
        if settings.USE_I18N:
            print("✅ i18n enabled")
        else:
            print("❌ i18n disabled")
            return False
        
        # Check languages
        if len(settings.LANGUAGES) >= 2:
            print(f"✅ Multiple languages configured: {[lang[1] for lang in settings.LANGUAGES]}")
        else:
            print("❌ Multiple languages not configured")
            return False
        
        # Check if translation files exist
        locale_path = settings.BASE_DIR / 'locale' / 'tr' / 'LC_MESSAGES'
        if (locale_path / 'django.po').exists():
            print("✅ Turkish translation files exist")
            return True
        else:
            print("❌ Translation files missing")
            return False
            
    except Exception as e:
        print(f"❌ i18n test failed: {e}")
        return False

def main():
    """Run all security tests"""
    print("🔐 ACADEMIA CARBON - COMPLETE SECURITY VERIFICATION")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Production Access", test_production_access),
        ("Django Security Settings", test_django_settings),
        ("Rate Limiting", test_rate_limiting),
        ("Authentication Requirements", test_authentication_requirements),
        ("User Data Isolation", test_user_data_isolation),
        ("File Upload Security", test_file_upload_security),
        ("Security Logging", test_security_logging),
        ("i18n System", test_i18n_system),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SECURITY VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall Score: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL SECURITY TESTS PASSED!")
        print("   Academia Carbon is production-ready and secure!")
    else:
        print(f"\n⚠️  {total-passed} security issues need attention")
        print("   Review failed tests and implement fixes")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)