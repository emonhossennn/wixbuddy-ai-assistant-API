#!/usr/bin/env python3
"""
Test script for delete session functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_delete_session():
    """Test the delete session functionality"""
    print("🗑️ Testing Delete Session")
    print("=" * 50)
    
    # Test 1: Get current chat history to see available sessions
    print("\n1. Getting current chat history...")
    try:
        response = requests.get(f"{API_BASE}/chatbot/history/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_sessions']} sessions")
            
            if data['history']:
                print("\n📝 Available Sessions:")
                for session in data['history']:
                    print(f"  Session ID: {session['session_id']} - Messages: {len(session['messages'])}")
                
                # Test 2: Delete the first session
                first_session_id = data['history'][0]['session_id']
                print(f"\n2. Deleting session {first_session_id}...")
                
                delete_response = requests.delete(f"{API_BASE}/chatbot/session/{first_session_id}/delete/")
                
                if delete_response.status_code == 200:
                    print(f"✅ Successfully deleted session {first_session_id}")
                else:
                    print(f"❌ Error deleting session: {delete_response.status_code} - {delete_response.text}")
                
                # Test 3: Check if session was deleted
                print(f"\n3. Checking if session {first_session_id} was deleted...")
                check_response = requests.get(f"{API_BASE}/chatbot/history/")
                
                if check_response.status_code == 200:
                    check_data = check_response.json()
                    print(f"✅ Now found {check_data['total_sessions']} sessions")
                    
                    # Check if the session still exists
                    session_exists = any(s['session_id'] == first_session_id for s in check_data['history'])
                    if not session_exists:
                        print(f"✅ Session {first_session_id} was successfully deleted")
                    else:
                        print(f"❌ Session {first_session_id} still exists")
                else:
                    print(f"❌ Error checking history: {check_response.status_code}")
            else:
                print("📭 No sessions to delete")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_delete_session() 