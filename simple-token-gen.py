#!/usr/bin/env python3
"""
Simple LiveKit token generator using PyJWT
"""
import jwt
import time
import sys

# Your Railway LiveKit credentials
API_KEY = "MPbzW/lu62PdK+YR7awF6H8IgemQt8JB7Fp7s9i/dHw="
API_SECRET = "quOTTctt4qbIUOu4aitlwug+1SBdJ7Wd48KyiaNlias="
LIVEKIT_URL = "wss://livekit-server-production-a48d.up.railway.app"

def generate_token(room_name="test-room", user_name="test-user"):
    """Generate LiveKit JWT token"""
    now = int(time.time())
    exp = now + (6 * 60 * 60)  # 6 hours validity

    payload = {
        "exp": exp,
        "iss": API_KEY,
        "nbf": now,
        "sub": user_name,
        "name": user_name,
        "video": {
            "room": room_name,
            "roomJoin": True,
            "canPublish": True,
            "canSubscribe": True,
        }
    }

    token = jwt.encode(payload, API_SECRET, algorithm="HS256")
    return token

if __name__ == "__main__":
    print("=" * 70)
    print("🎫 LIVEKIT TOKEN FOR PLAYGROUND")
    print("=" * 70)

    room = sys.argv[1] if len(sys.argv) > 1 else "test-room"
    token = generate_token(room)

    print(f"\n🌐 Server URL (copy this):")
    print(f"   {LIVEKIT_URL}")
    print(f"\n🎫 Token (copy this):")
    print(f"   {token}")
    print(f"\n🏠 Room Name:")
    print(f"   {room}")
    print("\n" + "=" * 70)
    print("\n📝 INSTRUCTIONS:")
    print("1. Go to: https://meet.livekit.io/custom")
    print("2. Paste Server URL (above)")
    print("3. Paste Token (above)")
    print("4. Click 'Connect'")
    print("5. Allow microphone")
    print("6. Speak in Tamil or English!")
    print("7. Your MLA voice agent will respond!")
    print("\n" + "=" * 70)
