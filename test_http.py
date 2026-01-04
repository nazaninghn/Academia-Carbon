#!/usr/bin/env python
"""
Test HTTP responses from the server
"""
import requests
import time

def test_server():
    """Test server responses"""
    base_url = "http://localhost:8000"
    
    print("🌐 Testing server responses...")
    print("=" * 50)
    
    # Test pages (these should redirect to login for unauthenticated users)
    pages = [
        ("/en/", "Dashboard"),
        ("/en/data-entry/", "Data Collection"),
        ("/en/action-planning/", "Action Planning"),
        ("/en/suppliers/", "Supplier Management"),
        ("/en/settings/", "Settings"),
        ("/en/support/", "Help & Support"),
    ]
    
    for path, name in pages:
        try:
            url = base_url + path
            response = requests.get(url, timeout=5)
            
            # 302 is expected for login redirect
            if response.status_code in [200, 302]:
                status = "✅ PASS"
                if response.status_code == 302:
                    status += " (Login redirect)"
            else:
                status = f"❌ FAIL ({response.status_code})"
            
            print(f"{status} | {name:<20} | {path}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR | {name:<20} | {path} - {str(e)}")
        except Exception as e:
            print(f"❌ ERROR | {name:<20} | {path} - {str(e)}")
    
    print("=" * 50)
    print("✨ HTTP test completed!")

if __name__ == '__main__':
    # Wait a moment for server to be ready
    time.sleep(1)
    test_server()