import requests
import json

url = "http://127.0.0.1:8000/en/api/materials/request/"

# Login first
session = requests.Session()
login_url = "http://127.0.0.1:8000/en/login/"

# Get CSRF token
response = session.get(login_url)
csrf_token = session.cookies.get('csrftoken')

# Login
login_data = {
    'email': 'arman.habibii1993@gmail.com',
    'password': 'your_password_here',  # Replace with actual password
    'csrfmiddlewaretoken': csrf_token
}

print("Logging in...")
login_response = session.post(login_url, data=login_data, headers={'Referer': login_url})
print(f"Login status: {login_response.status_code}")

# Get new CSRF token
csrf_token = session.cookies.get('csrftoken')

# Test material request
headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrf_token,
    'Referer': url,
    'X-Requested-With': 'XMLHttpRequest'
}

data = {
    "material_name": "Test Material",
    "category": "fuel",
    "description": "Test description for material request",
    "suggested_factor": 2.5,
    "suggested_unit": "kg",
    "suggested_source": "Test source"
}

print("\nSending material request...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

response = session.post(url, json=data, headers=headers)
print(f"\nStatus: {response.status_code}")
print(f"Response: {response.text}")
