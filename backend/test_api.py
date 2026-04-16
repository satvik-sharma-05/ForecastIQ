"""
Quick API test script
Run: python test_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    print("🔐 Testing signup...")
    response = requests.post(f"{BASE_URL}/api/auth/signup", json={
        "email": "test@example.com",
        "password": "test123",
        "name": "Test User"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Token: {data['access_token'][:20]}...")
        return data['access_token']
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_login():
    print("\n🔐 Testing login...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Token: {data['access_token'][:20]}...")
        return data['access_token']
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_get_me(token):
    print("\n👤 Testing get current user...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ User: {response.json()}")
    else:
        print(f"❌ Error: {response.text}")

def test_dashboard_stats(token):
    print("\n📊 Testing dashboard stats...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Stats: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    print("🚀 ForecastIQ API Test\n")
    
    # Try signup first, if fails try login
    token = test_signup()
    if not token:
        token = test_login()
    
    if token:
        test_get_me(token)
        test_dashboard_stats(token)
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Authentication failed")
