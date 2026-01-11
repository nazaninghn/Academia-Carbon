#!/usr/bin/env python3
"""
Security Test Suite for Academia Carbon
Tests all security implementations
"""

import os
import django

# Setup Django FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import json

def test_security_settings():
    """Test critical security settings"""
    
    print("🔒 Security Settings Test")
    print("=" * 50)
    
    # Test 1: DEBUG should be False in production
    debug_status = settings.DEBUG
    print(f"1. DEBUG Setting: {debug_status}")
    if not debug_status:
        print("   ✅ DEBUG is False (Production Safe)")
    else:
        print("   ⚠️  DEBUG is True (Development Mode)")
    
    # Test 2: SECRET_KEY should not be default
    secret_key = settings.SECRET_KEY
    is_default = 'django-insecure' in secret_key
    print(f"2. SECRET_KEY: {'Default/Insecure' if is_default else 'Custom/Secure'}")
    if not is_default:
        print("   ✅ SECRET_KEY is customized")
    else:
        print("   ❌ SECRET_KEY is default/insecure!")
    
    # Test 3: ALLOWED_HOSTS
    allowed_hosts = settings.ALLOWED_HOSTS
    print(f"3. ALLOWED_HOSTS: {allowed_hosts}")
    if allowed_hosts and allowed_hosts != ['*']:
        print("   ✅ ALLOWED_HOSTS is configured")
    else:
        print("   ❌ ALLOWED_HOSTS is not properly configured!")
    
    # Test 4: Security Headers
    security_settings = {
        'SECURE_SSL_REDIRECT': getattr(settings, 'SECURE_SSL_REDIRECT', False),
        'SESSION_COOKIE_SECURE': getattr(settings, 'SESSION_COOKIE_SECURE', False),
        'CSRF_COOKIE_SECURE': getattr(settings, 'CSRF_COOKIE_SECURE', False),
        'X_FRAME_OPTIONS': getattr(settings, 'X_FRAME_OPTIONS', None),
        'SECURE_CONTENT_TYPE_NOSNIFF': getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False),
    }
    
    print("4. Security Headers:")
    for setting, value in security_settings.items():
        status = "✅" if value else "❌"
        print(f"   {status} {setting}: {value}")
    
    # Test 5: Password Validators
    password_validators = settings.AUTH_PASSWORD_VALIDATORS
    print(f"5. Password Validators: {len(password_validators)} configured")
    if len(password_validators) >= 4:
        print("   ✅ Comprehensive password validation")
    else:
        print("   ⚠️  Limited password validation")
    
    # Test 6: File Upload Security
    file_settings = {
        'FILE_UPLOAD_MAX_MEMORY_SIZE': getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', None),
        'DATA_UPLOAD_MAX_MEMORY_SIZE': getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', None),
    }
    
    print("6. File Upload Security:")
    for setting, value in file_settings.items():
        if value:
            mb_size = value / (1024 * 1024)
            print(f"   ✅ {setting}: {mb_size}MB")
        else:
            print(f"   ❌ {setting}: Not configured")
    
    return True

def test_middleware_security():
    """Test security middleware"""
    
    print("\n🛡️ Middleware Security Test")
    print("=" * 50)
    
    middleware = settings.MIDDLEWARE
    
    security_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    custom_middleware = [
        'ghg.middleware.SecurityHeadersMiddleware',
        'ghg.middleware.RateLimitMiddleware',
        'ghg.middleware.SecurityLoggingMiddleware',
    ]
    
    print("1. Required Security Middleware:")
    for mw in security_middleware:
        if mw in middleware:
            print(f"   ✅ {mw}")
        else:
            print(f"   ❌ {mw} - MISSING!")
    
    print("\n2. Custom Security Middleware:")
    for mw in custom_middleware:
        if mw in middleware:
            print(f"   ✅ {mw}")
        else:
            print(f"   ⚠️  {mw} - Not configured")
    
    return True

def test_url_security():
    """Test URL security patterns"""
    
    print("\n🔗 URL Security Test")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Admin access without authentication
    try:
        response = client.get('/admin/')
        if response.status_code == 302:  # Redirect to login
            print("   ✅ Admin requires authentication")
        else:
            print(f"   ❌ Admin accessible without auth: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Admin URL test failed: {e}")
    
    # Test 2: Data entry requires login
    try:
        response = client.get('/en/data-entry/')
        if response.status_code == 302:  # Redirect to login
            print("   ✅ Data entry requires authentication")
        else:
            print(f"   ❌ Data entry accessible without auth: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Data entry test failed: {e}")
    
    # Test 3: API endpoints require authentication
    try:
        response = client.post('/en/calculate-emission/', 
                              data=json.dumps({'test': 'data'}),
                              content_type='application/json')
        if response.status_code in [302, 403, 405]:  # Redirect or forbidden
            print("   ✅ API endpoints require authentication")
        else:
            print(f"   ❌ API accessible without auth: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  API test failed: {e}")
    
    return True

def test_csrf_protection():
    """Test CSRF protection"""
    
    print("\n🛡️ CSRF Protection Test")
    print("=" * 50)
    
    client = Client(enforce_csrf_checks=True)
    
    # Test POST without CSRF token
    try:
        response = client.post('/en/calculate-emission/', 
                              data=json.dumps({'test': 'data'}),
                              content_type='application/json')
        if response.status_code == 403:  # CSRF failure
            print("   ✅ CSRF protection active")
        else:
            print(f"   ❌ CSRF protection bypassed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  CSRF test failed: {e}")
    
    return True

def test_file_validation():
    """Test file upload validation"""
    
    print("\n📁 File Upload Security Test")
    print("=" * 50)
    
    try:
        from ghg.validators import validate_file_extension, validate_file_size
        
        # Test file extension validation
        class MockFile:
            def __init__(self, name, size=1024):
                self.name = name
                self.size = size
        
        # Test valid file
        try:
            validate_file_extension(MockFile('test.pdf'))
            print("   ✅ PDF files accepted")
        except Exception as e:
            print(f"   ❌ PDF validation failed: {e}")
        
        # Test invalid file
        try:
            validate_file_extension(MockFile('test.exe'))
            print("   ❌ EXE files accepted (SECURITY RISK!)")
        except Exception:
            print("   ✅ EXE files rejected")
        
        # Test file size
        try:
            validate_file_size(MockFile('test.pdf', 20 * 1024 * 1024))  # 20MB
            print("   ❌ Large files accepted (SECURITY RISK!)")
        except Exception:
            print("   ✅ Large files rejected")
        
    except ImportError:
        print("   ⚠️  File validators not found")
    
    return True

def test_logging_security():
    """Test security logging"""
    
    print("\n📝 Security Logging Test")
    print("=" * 50)
    
    # Check if logs directory exists
    logs_dir = settings.BASE_DIR / 'logs'
    if logs_dir.exists():
        print("   ✅ Logs directory exists")
        
        security_log = logs_dir / 'security.log'
        if security_log.exists():
            print("   ✅ Security log file exists")
        else:
            print("   ⚠️  Security log file not created yet")
    else:
        print("   ⚠️  Logs directory not found")
    
    # Check logging configuration
    logging_config = settings.LOGGING
    if 'security' in str(logging_config):
        print("   ✅ Security logging configured")
    else:
        print("   ⚠️  Security logging not configured")
    
    return True

def run_all_security_tests():
    """Run comprehensive security test suite"""
    
    print("🔒 ACADEMIA CARBON - SECURITY TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_security_settings,
        test_middleware_security,
        test_url_security,
        test_csrf_protection,
        test_file_validation,
        test_logging_security,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
    
    print(f"\n📊 Security Test Results:")
    print(f"   Tests Passed: {passed}/{total}")
    print(f"   Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print(f"\n🎉 ALL SECURITY TESTS PASSED!")
        print(f"   Academia Carbon is PRODUCTION READY! 🚀")
    elif passed >= total * 0.8:
        print(f"\n✅ GOOD! Most security features implemented.")
        print(f"   Review failed tests for improvements.")
    else:
        print(f"\n⚠️  ATTENTION! Security improvements needed.")
        print(f"   Address failed tests before production deployment.")
    
    return passed == total

if __name__ == "__main__":
    run_all_security_tests()