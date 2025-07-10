#!/usr/bin/env python3
"""
Test script for chat history functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_chat_history():
    """Test the chat history functionality"""
    print("📚 Testing Chat History")
    print("=" * 50)
    
    # Test 1: Get chat history
    print("\n1. Getting chat history...")
    try:
        response = requests.get(f"{API_BASE}/chatbot/history/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {data['total_sessions']} sessions")
            
            if data['history']:
                print("\n📝 Chat History:")
                for i, session in enumerate(data['history'], 1):
                    print(f"\nSession {i} (ID: {session['session_id']}):")
                    print(f"  Start: {session['start_time']}")
                    for msg in session['messages']:
                        sender = "👤 User" if msg['sender'] == 'user' else "🤖 Bot"
                        print(f"  {sender}: {msg['content'][:100]}...")
            else:
                print("📭 No chat history found")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Send a new message
    print("\n2. Sending a new message...")
    try:
        response = requests.post(f"{API_BASE}/chatbot/", json={
            "message": "Tell me a joke!"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {data['response'][:100]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Get updated history
    print("\n3. Getting updated chat history...")
    try:
        response = requests.get(f"{API_BASE}/chatbot/history/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Now found {data['total_sessions']} sessions")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_chat_history() 