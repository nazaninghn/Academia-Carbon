#!/usr/bin/env python3
"""
Monitor production deployment status
Checks if the latest template fix is deployed
"""

import requests
import time
from datetime import datetime

def check_deployment_fix():
    """Check if the template syntax fix is deployed"""
    
    print("🔍 Monitoring Production Deployment")
    print("=" * 50)
    
    production_url = "https://academia-carbon.onrender.com/en/data-entry/"
    
    print(f"🌐 Checking: {production_url}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        response = requests.get(production_url, timeout=30)
        
        if response.status_code == 200:
            print("   ✅ Site is accessible")
            
            # Check for the specific template syntax error
            if "Could not parse the remainder" in response.text:
                print("   ❌ Template syntax error still present!")
                print("   💡 Deployment may still be in progress...")
                return False
            elif "TemplateSyntaxError" in response.text:
                print("   ❌ Template syntax error detected!")
                return False
            else:
                print("   ✅ No template syntax errors detected!")
                print("   🎉 Deployment successful!")
                return True
                
        else:
            print(f"   ❌ Site returned status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ⏰ Request timed out (deployment may be in progress)")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def monitor_with_retry(max_attempts=10, delay=30):
    """Monitor deployment with retry logic"""
    
    print(f"🚀 Starting deployment monitoring...")
    print(f"📊 Will check {max_attempts} times with {delay}s intervals")
    print()
    
    for attempt in range(1, max_attempts + 1):
        print(f"🔄 Attempt {attempt}/{max_attempts}")
        
        if check_deployment_fix():
            print(f"\n🎉 SUCCESS! Deployment is live after {attempt} attempts")
            print(f"⏱️  Total time: ~{(attempt-1) * delay} seconds")
            return True
        
        if attempt < max_attempts:
            print(f"   ⏳ Waiting {delay} seconds before next check...")
            time.sleep(delay)
        
        print()
    
    print(f"❌ Deployment not detected after {max_attempts} attempts")
    print(f"💡 Check Render.com dashboard for deployment status")
    return False

if __name__ == "__main__":
    monitor_with_retry()