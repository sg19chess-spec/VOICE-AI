# LiveKit SIP Server for Railway

This SIP server receives phone calls from Twilio and forwards them to your Railway LiveKit server, where your Tamil voice agent handles the conversation.

## Deployment on Railway

### 1. Create New Service

1. Go to Railway dashboard
2. Click **"+ New"** → **"GitHub Repo"**
3. Select this repository
4. Click **"Add Service"**

### 2. Configure Root Directory

Railway will auto-detect the Dockerfile. Set:
- **Root Directory**: `sip-server`

### 3. Set Environment Variables

Add these variables in Railway:

```bash
LIVEKIT_URL=wss://livekit-server-production-498a.up.railway.app
LIVEKIT_API_KEY=KHhSGRWrBFS0YPUe0x3s8+hMz5PY46y9O8po+/SgeXI=
LIVEKIT_API_SECRET=xUpwb5OD4DHbx02Cd1Gz72HmpOCOGdEigqj1RAHmrUTPg78nVmzkPs3SPe6Zr/Xk
```

### 4. Configure Networking

1. Go to **Settings** → **Networking**
2. **Generate Service Domain**
3. Note your public URL: `sip-server-production-xxxx.up.railway.app`

### 5. Deploy

Railway will automatically build and deploy. Check logs for:
```
✓ SIP server listening on :5060
✓ Connected to LiveKit
```

## Architecture

```
Phone Call → Twilio → Railway SIP Server → Railway LiveKit → Voice Agent
```

## Next Steps

After deployment:
1. Run `setup-sip-trunk.py` to create SIP trunk in LiveKit
2. Configure Twilio Elastic SIP Trunking
3. Test by calling your Twilio number!

## Troubleshooting

**If SIP server can't connect to LiveKit:**
- Check LIVEKIT_URL is correct (wss://)
- Verify API credentials match LiveKit server
- Check LiveKit server logs for connection errors

**If calls don't connect:**
- Railway's networking might not support SIP/UDP properly
- Consider using the webhook approach instead (see `/twilio-webhook/`)
