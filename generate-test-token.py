#!/usr/bin/env python3
"""
Generate a test token for LiveKit Playground
Run this script to get a token you can use to test your voice agent
"""
import sys
from livekit import api

# Your Railway LiveKit server URL
LIVEKIT_URL = "wss://livekit-server-production-a48d.up.railway.app"

def generate_token(api_key: str, api_secret: str, room_name: str = "test-room", user_name: str = "test-user"):
    """Generate a LiveKit access token"""
    token = api.AccessToken(api_key, api_secret)
    token.with_identity(user_name)
    token.with_name(user_name)
    token.with_grants(api.VideoGrants(
        room_join=True,
        room=room_name,
        can_publish=True,
        can_subscribe=True,
    ))
    return token.to_jwt()

if __name__ == "__main__":
    print("🎫 LiveKit Token Generator for Railway")
    print("=" * 60)

    # Get credentials
    if len(sys.argv) >= 3:
        api_key = sys.argv[1]
        api_secret = sys.argv[2]
        room_name = sys.argv[3] if len(sys.argv) > 3 else "test-room"
    else:
        print("\nℹ️  Get these from your Railway livekit-server service Variables tab")
        print("   Look for: LIVEKIT_KEYS (format: API_KEY:API_SECRET)\n")
        api_key = input("Enter LIVEKIT_API_KEY: ").strip()
        api_secret = input("Enter LIVEKIT_API_SECRET: ").strip()
        room_name = input("Enter room name (or press Enter for 'test-room'): ").strip() or "test-room"

    # Generate token
    try:
        token = generate_token(api_key, api_secret, room_name)

        print("\n" + "=" * 60)
        print("✅ TOKEN GENERATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n🌐 Server URL:")
        print(f"   {LIVEKIT_URL}")
        print(f"\n🎫 Room Token:")
        print(f"   {token}")
        print(f"\n🏠 Room Name:")
        print(f"   {room_name}")
        print("\n" + "=" * 60)
        print("\n📝 HOW TO USE IN LIVEKIT PLAYGROUND:")
        print("1. Go to: https://meet.livekit.io/custom")
        print("2. Paste Server URL (above)")
        print("3. Paste Token (above)")
        print("4. Click 'Connect'")
        print("5. Allow microphone access")
        print("6. Speak in Tamil or English")
        print("7. Your agent should respond!")
        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure your API key and secret are correct")
        sys.exit(1)
