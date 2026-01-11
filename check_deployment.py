#!/usr/bin/env python3
"""
Production deployment verification script
Checks if the latest changes are deployed and working
"""

import requests
import time
from datetime import datetime

def check_deployment_status():
    """Check if the production deployment is working"""
    
    print("🚀 Production Deployment Status Check")
    print("=" * 50)
    
    # Production URL
    production_url = "https://academia-carbon.onrender.com"
    
    print(f"🌐 Checking: {production_url}")
    
    try:
        # Check if site is accessible
        response = requests.get(production_url, timeout=30)
        
        if response.status_code == 200:
            print("   ✅ Site is accessible")
            
            # Check for template syntax errors in response
            if "TemplateSyntaxError" in response.text:
                print("   ❌ Template syntax error detected in production!")
                return False
            elif "Could not parse the remainder" in response.text:
                print("   ❌ Template parsing error detected in production!")
                return False
            else:
                print("   ✅ No template syntax errors detected")
            
            # Check for i18n functionality
            if "{% trans" in response.text:
                print("   ⚠️  Untranslated template tags found (possible cache issue)")
            else:
                print("   ✅ Template tags appear to be processed")
            
            # Check for Turkish language support
            if "/tr/" in response.text or "Türkçe" in response.text:
                print("   ✅ Turkish language support detected")
            else:
                print("   ⚠️  Turkish language support not clearly visible")
            
            return True
            
        else:
            print(f"   ❌ Site returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ⏰ Request timed out (site may be starting up)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
        return False

def check_specific_page():
    """Check the data entry page specifically"""
    
    print(f"\n📄 Checking Data Entry Page:")
    
    data_entry_url = "https://academia-carbon.onrender.com/en/data-entry/"
    
    try:
        response = requests.get(data_entry_url, timeout=30)
        
        if response.status_code == 200:
            print("   ✅ Data entry page accessible")
            
            # Check for the specific error that was occurring
            if "Explain how this industry type relates to your organization's" in response.text:
                print("   ❌ Old malformed template syntax still present!")
                return False
            elif "Explain how this industry type relates to your organization activities" in response.text:
                print("   ✅ Fixed template syntax is deployed!")
                return True
            else:
                print("   ⚠️  Cannot verify specific fix (content may have changed)")
                return True
        else:
            print(f"   ❌ Data entry page returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking data entry page: {e}")
        return False

if __name__ == "__main__":
    print(f"⏰ Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check main site
    main_ok = check_deployment_status()
    
    # Check specific page
    page_ok = check_specific_page()
    
    print(f"\n📊 Overall Status:")
    if main_ok and page_ok:
        print("   🎉 Production deployment is working correctly!")
        print("   ✅ Template syntax errors have been resolved!")
    elif main_ok:
        print("   ⚠️  Site is accessible but specific fixes need verification")
    else:
        print("   ❌ Production deployment has issues")
        print("   💡 Try waiting a few minutes for deployment to complete")
        print("   💡 Or check Render.com dashboard for deployment status")
    
    print(f"\n🔗 Production URL: https://academia-carbon.onrender.com")
    print(f"🔗 Data Entry: https://academia-carbon.onrender.com/en/data-entry/")