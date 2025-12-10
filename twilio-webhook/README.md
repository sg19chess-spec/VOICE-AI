# Twilio → LiveKit Webhook

Simple Flask webhook server that forwards Twilio phone calls to LiveKit voice agents.

## How It Works

1. Citizen calls Twilio phone number
2. Twilio sends webhook request to this server
3. Server returns TwiML that forwards call to LiveKit SIP
4. LiveKit voice agent handles the call in Tamil

## Deployment on Railway

### 1. Create New Service

1. Go to Railway dashboard
2. Click **"+ New"** → **"GitHub Repo"**
3. Select this repository
4. Click **"Add Service"**

### 2. Configure Build

Railway will auto-detect the configuration from `railway.toml` and `Procfile`.

**Root Directory**: Set to `twilio-webhook`

### 3. Set Environment Variables

Add this variable in Railway:

```
LIVEKIT_SIP_URI=sip:your-trunk-id@sip.livekit.cloud
```

Replace with your actual LiveKit SIP URI from the trunk you created.

### 4. Deploy

Railway will automatically deploy. Wait for deployment to complete.

### 5. Get Public URL

Railway will give you a public URL like:
```
https://twilio-webhook-production-xxxx.up.railway.app
```

## Configure Twilio

1. Go to Twilio Console → **Phone Numbers**
2. Click on your phone number
3. Under **"Voice Configuration"**:
   - **A CALL COMES IN**: Webhook
   - **URL**: `https://your-railway-url.up.railway.app/voice`
   - **Method**: POST
4. Under **"Status Callback URL"** (optional):
   - **URL**: `https://your-railway-url.up.railway.app/voice/status`
   - **Method**: POST
5. Click **Save**

## Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /voice` - Main webhook for incoming calls
- `POST /voice/status` - Call status updates

## Testing

```bash
# Check if service is running
curl https://your-railway-url.up.railway.app/health

# View service info
curl https://your-railway-url.up.railway.app/
```

## Logs

View logs in Railway dashboard to see:
- Incoming calls
- Call forwarding to LiveKit
- Call status updates

## Cost

- **Railway**: Free tier (500 hours/month) - plenty for testing
- **Twilio**: $15 free credit
- **LiveKit Cloud**: Free tier (10,000 minutes/month)

**Total: FREE for testing! 🎉**
