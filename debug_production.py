#!/usr/bin/env python3
"""
Debug production deployment issues
"""

import os
import requests

def debug_production():
    """Debug production deployment"""
    
    print("🔍 Production Deployment Debug")
    print("=" * 50)
    
    url = "https://academia-carbon.onrender.com"
    
    try:
        print(f"🌐 Testing: {url}")
        
        # Make request with detailed error handling
        response = requests.get(url, timeout=30, allow_redirects=True)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 400:
            print("\n❌ 400 Bad Request - Likely ALLOWED_HOSTS issue")
            print("Response content:")
            print(response.text[:1000])  # First 1000 chars
        elif response.status_code == 500:
            print("\n❌ 500 Server Error - Application error")
            print("Response content:")
            print(response.text[:1000])
        elif response.status_code == 200:
            print("\n✅ 200 OK - Site is working!")
        else:
            print(f"\n⚠️  Unexpected status: {response.status_code}")
            print("Response content:")
            print(response.text[:500])
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_production()