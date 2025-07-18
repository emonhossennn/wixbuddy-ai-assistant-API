#!/usr/bin/env python3
"""
Test script for authentication and API endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
EMAIL = "test@example.com"
PASSWORD = "testpassword123"

def test_signup():
    """Test user signup"""
    print("Testing signup...")
    url = f"{BASE_URL}/auth/signup/"
    data = {
        "email": EMAIL,
        "name": "Test",
        "family_name": "User",
        "password": PASSWORD,
        "agreed_to_policy": True
    }
    
    response = requests.post(url, json=data)
    print(f"Signup Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201

def test_signin():
    """Test user signin and get token"""
    print("\nTesting signin...")
    url = f"{BASE_URL}/auth/signin/"
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    response = requests.post(url, json=data)
    print(f"Signin Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json().get('tokens', {}).get('access')
    return None

def test_dashboard(token):
    """Test dashboard endpoint with authentication"""
    print("\nTesting dashboard...")
    url = f"{BASE_URL}/dashboard/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Dashboard Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_account_settings(token):
    """Test account settings endpoint"""
    print("\nTesting account settings...")
    url = f"{BASE_URL}/account-settings/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test GET (get profile)
    response = requests.get(url, headers=headers)
    print(f"Get Profile Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test PUT (update profile)
    update_data = {
        "name": "Updated",
        "family_name": "Name",
        "job_title": "Developer",
        "current_company": "Test Company"
    }
    response = requests.put(url, json=update_data, headers=headers)
    print(f"Update Profile Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=== API Authentication Test ===\n")
    
    # Test signup
    if not test_signup():
        print("Signup failed. User might already exist.")
    
    # Test signin
    token = test_signin()
    if not token:
        print("Signin failed. Cannot proceed with authenticated tests.")
        return
    
    print(f"\nToken received: {token[:20]}...")
    
    # Test authenticated endpoints
    test_dashboard(token)
    test_account_settings(token)
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main() 