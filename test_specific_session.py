#!/usr/bin/env python3
"""
Test script for specific chat session functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_specific_session():
    """Test getting a specific chat session"""
    print("🔍 Testing Specific Chat Session")
    print("=" * 50)
    
    # First, send a message to create a session
    print("\n1. Creating a new chat session...")
    try:
        response = requests.post(f"{API_BASE}/chatbot/", json={
            "message": "Hello! This is a test message for session ID testing."
        })
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Created session with ID: {session_id}")
            
            # Now get the specific session
            print(f"\n2. Getting specific session {session_id}...")
            session_response = requests.get(f"{API_BASE}/chatbot/session/{session_id}/")
            
            if session_response.status_code == 200:
                session_data = session_response.json()
                print(f"✅ Successfully retrieved session {session_id}")
                print(f"📊 Session Details:")
                print(f"   - Start Time: {session_data['start_time']}")
                print(f"   - Total Messages: {session_data['total_messages']}")
                print(f"   - Messages:")
                
                for i, msg in enumerate(session_data['messages'], 1):
                    sender = "👤 User" if msg['sender'] == 'user' else "🤖 Bot"
                    print(f"     {i}. {sender}: {msg['content'][:80]}...")
            else:
                print(f"❌ Error getting session: {session_response.status_code} - {session_response.text}")
        else:
            print(f"❌ Error creating session: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_specific_session() 