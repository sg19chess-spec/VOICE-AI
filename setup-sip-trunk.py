#!/usr/bin/env python3
"""
Setup SIP Trunk and Dispatch Rule for Railway LiveKit
"""
import asyncio
import os
from livekit import api

# LiveKit Server Configuration
LIVEKIT_URL = "wss://livekit-server-production-498a.up.railway.app"
LIVEKIT_API_KEY = "KHhSGRWrBFS0YPUe0x3s8+hMz5PY46y9O8po+/SgeXI="
LIVEKIT_API_SECRET = "xUpwb5OD4DHbx02Cd1Gz72HmpOCOGdEigqj1RAHmrUTPg78nVmzkPs3SPe6Zr/Xk"


async def setup_sip():
    """Setup SIP trunk and dispatch rule"""

    # Initialize LiveKit API client
    lkapi = api.LiveKitAPI(
        url=LIVEKIT_URL,
        api_key=LIVEKIT_API_KEY,
        api_secret=LIVEKIT_API_SECRET
    )

    print("=" * 60)
    print("Setting up SIP Trunk and Dispatch Rule")
    print("=" * 60)

    try:
        # Step 1: Create Inbound SIP Trunk
        print("\n1. Creating inbound SIP trunk...")

        trunk = await lkapi.sip.create_sip_inbound_trunk(
            api.CreateSIPInboundTrunkRequest(
                trunk=api.SIPInboundTrunkInfo(
                    name="Twilio-Trunk",
                    # Add your Twilio phone numbers here
                    numbers=["+15105550123"],  # Replace with YOUR Twilio number
                    # Optional: Add Twilio IP addresses for security
                    # allowed_addresses=["54.172.60.0/23", "54.244.51.0/24"],
                )
            )
        )

        print(f"✓ SIP Trunk created: {trunk.name}")
        print(f"  Trunk ID: {trunk.sip_trunk_id}")
        print(f"  Numbers: {trunk.numbers}")

        # Step 2: Create Dispatch Rule
        print("\n2. Creating dispatch rule for voice agent...")

        dispatch_rule = await lkapi.sip.create_sip_dispatch_rule(
            api.CreateSIPDispatchRuleRequest(
                rule=api.SIPDispatchRuleInfo(
                    name="MLA-Voice-Agent",
                    trunk_ids=[trunk.sip_trunk_id],
                    rule=api.SIPDispatchRuleDirect(
                        room_name="mla-call-",  # Room name prefix
                        pin="",  # No PIN required
                    ),
                )
            )
        )

        print(f"✓ Dispatch rule created: {dispatch_rule.name}")
        print(f"  Rule ID: {dispatch_rule.sip_dispatch_rule_id}")
        print(f"  Room prefix: mla-call-")

        print("\n" + "=" * 60)
        print("✅ SIP Setup Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Get your Railway SIP server URL")
        print("2. Configure Twilio to forward calls to your SIP server")
        print("3. Test by calling your Twilio number!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("- LiveKit server is running")
        print("- API credentials are correct")
        print("- Railway URL is accessible")

    finally:
        await lkapi.aclose()


if __name__ == "__main__":
    asyncio.run(setup_sip())
