#!/usr/bin/env python3
"""
Test script to verify LiveKit voice agent is working on Railway
"""
import os
from livekit import api

# Get these from your Railway livekit-server service Variables tab
LIVEKIT_URL = "https://livekit-server-production-a48d.up.railway.app"
LIVEKIT_API_KEY = input("Enter your LIVEKIT_API_KEY: ").strip()
LIVEKIT_API_SECRET = input("Enter your LIVEKIT_API_SECRET: ").strip()

def create_test_token():
    """Create a test token to join the room"""
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity("test-user")
    token.with_name("Test User")
    token.with_grants(api.VideoGrants(
        room_join=True,
        room="test-tamil-agent"
    ))
    return token.to_jwt()

if __name__ == "__main__":
    print("🧪 Testing LiveKit Voice Agent on Railway")
    print("=" * 50)

    # Generate test token
    jwt = create_test_token()

    print("\n✅ Test token generated!")
    print(f"\n🔗 Test URL:")
    print(f"{LIVEKIT_URL}/test?url={LIVEKIT_URL}&token={jwt}")
    print("\n📝 Instructions:")
    print("1. Copy the URL above")
    print("2. Open it in your browser")
    print("3. Allow microphone access")
    print("4. Click 'Connect'")
    print("5. Speak in Tamil or English")
    print("6. The agent should respond as a Tamil Nadu MLA assistant")
    print("\n" + "=" * 50)
