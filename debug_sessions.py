#!/usr/bin/env python3
"""
Debug script to check available session IDs
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def debug_sessions():
    """Debug available sessions"""
    print("🔍 Debugging Available Sessions")
    print("=" * 50)
    
    # Get all chat history to see available sessions
    print("\n1. Getting all chat history...")
    try:
        response = requests.get(f"{API_BASE}/chatbot/history/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_sessions']} sessions")
            
            if data['history']:
                print("\n📝 Available Session IDs:")
                for session in data['history']:
                    session_id = session['session_id']
                    message_count = len(session['messages'])
                    print(f"   Session ID: {session_id} - Messages: {message_count}")
                    
                    # Test each session ID
                    print(f"   Testing session {session_id}...")
                    session_response = requests.get(f"{API_BASE}/chatbot/session/{session_id}/")
                    
                    if session_response.status_code == 200:
                        print(f"   ✅ Session {session_id} is accessible")
                    else:
                        print(f"   ❌ Session {session_id} error: {session_response.status_code} - {session_response.text}")
                    print()
            else:
                print("📭 No sessions found")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_sessions() 