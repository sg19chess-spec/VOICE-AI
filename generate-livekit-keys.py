#!/usr/bin/env python3
"""
Generate LiveKit API Key and Secret
"""
import secrets
import base64

def generate_api_credentials():
    """Generate LiveKit API key and secret"""
    # Generate API Key (16 random bytes, base62 encoded)
    api_key = "API" + base64.b32encode(secrets.token_bytes(12)).decode('utf-8').rstrip('=')

    # Generate API Secret (32 random bytes, base64 encoded)
    api_secret = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')

    return api_key, api_secret

if __name__ == "__main__":
    api_key, api_secret = generate_api_credentials()

    print("=" * 60)
    print("LiveKit API Credentials Generated")
    print("=" * 60)
    print(f"\nLIVEKIT_API_KEY={api_key}")
    print(f"LIVEKIT_API_SECRET={api_secret}")
    print("\n" + "=" * 60)
    print("Add these to your Railway LiveKit server environment variables")
    print("=" * 60)
