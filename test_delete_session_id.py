#!/usr/bin/env python3
"""
Test deleting sessions by session_id
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_delete_by_session_id():
    """Test deleting sessions by session_id"""
    print("🗑️ Testing Delete by Session ID")
    print("=" * 50)
    
    # First, create a new session
    print("\n1. Creating a new session...")
    try:
        response = requests.post(f"{API_BASE}/chatbot/", json={
            "message": "This is a test message for deletion"
        })
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Created session with session_id: {session_id}")
            
            # Get the session to verify it exists
            print(f"\n2. Verifying session {session_id} exists...")
            get_response = requests.get(f"{API_BASE}/chatbot/session/{session_id}/")
            
            if get_response.status_code == 200:
                session_data = get_response.json()
                print(f"✅ Session {session_id} found with {session_data['total_messages']} messages")
                
                # Delete the session by session_id
                print(f"\n3. Deleting session {session_id}...")
                delete_response = requests.delete(f"{API_BASE}/chatbot/session/{session_id}/delete/")
                
                if delete_response.status_code == 200:
                    delete_data = delete_response.json()
                    print(f"✅ {delete_data['message']}")
                    
                    # Verify the session was deleted
                    print(f"\n4. Verifying session {session_id} was deleted...")
                    verify_response = requests.get(f"{API_BASE}/chatbot/session/{session_id}/")
                    
                    if verify_response.status_code == 404:
                        print(f"✅ Session {session_id} was successfully deleted")
                    else:
                        print(f"❌ Session {session_id} still exists")
                else:
                    print(f"❌ Error deleting session: {delete_response.status_code} - {delete_response.text}")
            else:
                print(f"❌ Error getting session: {get_response.status_code} - {get_response.text}")
        else:
            print(f"❌ Error creating session: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_delete_by_session_id() 