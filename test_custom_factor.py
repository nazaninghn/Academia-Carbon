import requests
import json

# Test add custom factor
url = "http://127.0.0.1:8000/api/custom-factors/add/"

# First login to get session
login_url = "http://127.0.0.1:8000/auth/login/"
session = requests.Session()

# Get CSRF token
response = session.get(login_url)
csrf_token = session.cookies.get('csrftoken')

# Login (you'll need to create a test user first)
login_data = {
    'email': 'test@test.com',
    'password': 'test123',
    'csrfmiddlewaretoken': csrf_token
}

# Try to login
login_response = session.post(login_url, data=login_data, headers={'Referer': login_url})
print(f"Login status: {login_response.status_code}")

# Now test custom factor
csrf_token = session.cookies.get('csrftoken')
headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrf_token,
    'Referer': url
}

data = {
    "name": "Test Material",
    "category": "fuel",
    "factor_value": 2.5,
    "unit": "kg",
    "description": "Test description"
}

response = session.post(url, json=data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
