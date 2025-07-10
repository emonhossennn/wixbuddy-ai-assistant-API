#!/usr/bin/env python3
"""
Test single session per message behavior
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_single_sessions():
    """Test that each message creates a new session"""
    print("🆕 Testing Single Session Per Message")
    print("=" * 50)
    
    # Send multiple messages to create separate sessions
    messages = [
        "What is Python?",
        "How does Django work?",
        "Tell me about AI"
    ]
    
    session_ids = []
    
    for i, message in enumerate(messages, 1):
        print(f"\n{i}. Sending message: '{message}'")
        try:
            response = requests.post(f"{API_BASE}/chatbot/", json={
                "message": message
            })
            
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                session_ended = data.get('session_ended', False)
                session_ids.append(session_id)
                
                print(f"   ✅ Created Session ID: {session_id}")
                print(f"   📝 Response: {data['response'][:80]}...")
                print(f"   🔚 Session Ended: {session_ended}")
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Check if we got different session IDs
    print(f"\n📊 Session Summary:")
    print(f"   Total sessions created: {len(session_ids)}")
    print(f"   Unique session IDs: {len(set(session_ids))}")
    print(f"   Session IDs: {session_ids}")
    
    if len(set(session_ids)) == len(session_ids):
        print("   ✅ Each message created a unique session!")
    else:
        print("   ❌ Some messages reused the same session")
    
    # Get chat history to see all sessions
    print(f"\n📚 Getting chat history...")
    try:
        history_response = requests.get(f"{API_BASE}/chatbot/history/")
        if history_response.status_code == 200:
            history_data = history_response.json()
            print(f"   ✅ Found {history_data['total_sessions']} total sessions")
            
            for session in history_data['history']:
                print(f"   Session {session['session_id']}: {len(session['messages'])} messages")
        else:
            print(f"   ❌ Error getting history: {history_response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    test_single_sessions() 