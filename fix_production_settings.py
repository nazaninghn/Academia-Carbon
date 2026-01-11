#!/usr/bin/env python3
"""
Production Settings Fix for Academia Carbon
Ensures proper configuration for Render.com deployment
"""

import os
import sys

def check_production_environment():
    """Check if we're in production environment"""
    
    print("🔧 Production Environment Check")
    print("=" * 50)
    
    # Check environment variables
    render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
    database_url = os.environ.get('DATABASE_URL', '')
    debug_env = os.environ.get('DEBUG', 'False')
    
    print(f"RENDER_EXTERNAL_HOSTNAME: {render_hostname}")
    print(f"DATABASE_URL: {'Set' if database_url else 'Not set'}")
    print(f"DEBUG environment: {debug_env}")
    
    # Determine if we're in production
    is_production = bool(render_hostname or database_url.startswith('postgres'))
    
    print(f"\n🎯 Environment: {'PRODUCTION' if is_production else 'DEVELOPMENT'}")
    
    if is_production:
        print("\n✅ Production Environment Detected")
        print("   - DEBUG will be forced to False")
        print("   - ALLOWED_HOSTS will include render domains")
        print("   - Security settings will be enforced")
    else:
        print("\n⚠️  Development Environment")
        print("   - DEBUG may be True")
        print("   - Local hosts allowed")
    
    return is_production

def verify_settings():
    """Verify Django settings are correct"""
    
    print("\n🔍 Django Settings Verification")
    print("=" * 50)
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Check critical settings
        print(f"DEBUG: {settings.DEBUG}")
        print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"SECRET_KEY: {'Set' if settings.SECRET_KEY else 'Not set'}")
        print(f"CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
        
        # Verify production readiness
        if not settings.DEBUG and 'academia-carbon.onrender.com' in settings.ALLOWED_HOSTS:
            print("\n✅ Settings are production ready!")
            return True
        else:
            print("\n❌ Settings need adjustment for production")
            return False
            
    except Exception as e:
        print(f"\n❌ Error checking settings: {e}")
        return False

def main():
    """Main function"""
    
    print("🚀 Academia Carbon - Production Settings Fix")
    print("=" * 60)
    
    # Check environment
    is_production = check_production_environment()
    
    # Verify settings
    settings_ok = verify_settings()
    
    print(f"\n📊 Summary:")
    print(f"   Production Environment: {'✅' if is_production else '⚠️'}")
    print(f"   Settings Configuration: {'✅' if settings_ok else '❌'}")
    
    if is_production and settings_ok:
        print(f"\n🎉 Production deployment is properly configured!")
    elif is_production and not settings_ok:
        print(f"\n⚠️  Production environment detected but settings need adjustment")
        print(f"   The updated settings.py should fix the ALLOWED_HOSTS issue")
    else:
        print(f"\n💡 Running in development mode")
    
    return settings_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)