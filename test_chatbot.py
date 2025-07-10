#!/usr/bin/env python3
"""
Test script for chatbot functionality with history
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_chatbot():
    """Test the chatbot functionality"""
    print("🤖 Testing Chatbot with History")
    print("=" * 50)
    
    # Test 1: Send a message (without authentication for now)
    print("\n1. Testing chatbot message...")
    try:
        response = requests.post(f"{API_BASE}/chatbot/", json={
            "message": "Hello! How are you today?"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {data['response'][:100]}...")
            print(f"   Session ID: {data.get('session_id')}")
            print(f"   Message ID: {data.get('message_id')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Send another message
    print("\n2. Testing second message...")
    try:
        response = requests.post(f"{API_BASE}/chatbot/", json={
            "message": "What's the weather like?"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {data['response'][:100]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("📝 Note: To test history endpoints, you need to:")
    print("   1. Sign up/sign in to get an access token")
    print("   2. Use the token in Authorization header")
    print("   3. Test these endpoints:")
    print("      - GET /api/chatbot/history/")
    print("      - DELETE /api/chatbot/session/<id>/delete/")
    print("      - DELETE /api/chatbot/history/delete-all/")

if __name__ == "__main__":
    test_chatbot() 