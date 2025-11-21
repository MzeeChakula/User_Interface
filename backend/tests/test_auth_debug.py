import requests
import sys

BASE_URL = "http://localhost:8000"
EMAIL = "test_debug_user@example.com"
PASSWORD = "TestPassword123!"
NAME = "Debug User"

def test_auth():
    print(f"Testing auth against {BASE_URL}...")
    
    # 1. Register
    print("\n1. Testing Registration...")
    reg_data = {
        "email": EMAIL,
        "password": PASSWORD,
        "full_name": NAME
    }
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
        if resp.status_code == 200:
            print("Registration successful")
        elif resp.status_code == 400 and "already registered" in resp.text:
            print("ℹUser already exists, proceeding to login")
        else:
            print(f"Registration failed: {resp.status_code} - {resp.text}")
            return
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 2. Login
    print("\n2. Testing Login...")
    login_data = {
        "username": EMAIL,
        "password": PASSWORD
    }
    try:
        resp = requests.post(f"{BASE_URL}/auth/token", data=login_data)
        if resp.status_code == 200:
            print("Login successful")
            token = resp.json().get("access_token")
            print(f"Token received: {token[:10]}...")
        else:
            print(f"Login failed: {resp.status_code} - {resp.text}")
            return
    except Exception as e:
        print(f"Connection failed: {e}")
        return

if __name__ == "__main__":
    test_auth()
