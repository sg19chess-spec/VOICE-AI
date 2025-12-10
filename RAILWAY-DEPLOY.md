# Railway Deployment Guide

Deploy Tamil Nadu MLA Voice Complaint System to Railway.

## ⚠️ Important: Railway Multi-Service Setup

Railway **no longer supports docker-compose** directly. Instead, you deploy each service separately within a single Railway project.

## 🚀 Quick Start (Recommended Path)

### Option 1: Deploy Just the Voice Agent (Simplest)

This deploys only your custom voice agent. LiveKit server runs elsewhere (LiveKit Cloud free tier or separate VPS).

**Step 1: Deploy Voice Agent to Railway**

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `VOICE-AI` repo
4. Railway detects `voice-agent/Dockerfile`
5. Set environment variables:
   ```
   LIVEKIT_URL=wss://your-livekit-server.com
   LIVEKIT_API_KEY=<your-key>
   LIVEKIT_API_SECRET=<your-secret>
   SARVAM_API_KEY=sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
   GOOGLE_API_KEY=AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI
   ```
6. Deploy!

**Where to run LiveKit Server:**
- LiveKit Cloud free tier: https://cloud.livekit.io (FREE for testing)
- Small VPS: DigitalOcean $6/month droplet
- Railway (add as separate service - see Option 2)

**Cost: $5-10/month** (just the agent)

---

### Option 2: Deploy Full Stack on Railway (Advanced)

Deploy all services (LiveKit, SIP, Recording, Agent) as separate Railway services.

**Step 1: Create Railway Project**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init
# Name it: "tn-mla-voice-system"
```

**Step 2: Add Redis Service**

```bash
# In Railway dashboard or CLI
railway add
# Select: Redis
```

**Step 3: Add LiveKit Service**

In Railway dashboard:
1. Click "New Service" → "Docker Image"
2. Image: `livekit/livekit-server:latest`
3. Add environment variable:
   ```
   LIVEKIT_KEYS=<api-key>:<api-secret>
   ```
4. Add ports:
   - 7880 (HTTP)
   - 7881 (WebRTC TCP)
5. Deploy

**Step 4: Add SIP Service**

1. Click "New Service" → "Docker Image"
2. Image: `livekit/sip:latest`
3. Add environment variables:
   ```
   LIVEKIT_URL=http://livekit:7880
   LIVEKIT_API_KEY=<your-key>
   LIVEKIT_API_SECRET=<your-secret>
   ```
4. Add ports:
   - 5060 (UDP/TCP)
5. Deploy

**Step 5: Add Egress (Recording) Service**

1. Click "New Service" → "Docker Image"
2. Image: `livekit/egress:latest`
3. Add volume for recordings
4. Deploy

**Step 6: Add Voice Agent Service**

1. Click "New Service" → "GitHub Repo"
2. Select `VOICE-AI` repo
3. Root directory: `voice-agent`
4. Add environment variables:
   ```
   LIVEKIT_URL=http://livekit:7880
   LIVEKIT_API_KEY=<your-key>
   LIVEKIT_API_SECRET=<your-secret>
   SARVAM_API_KEY=sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
   GOOGLE_API_KEY=AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI
   ```
5. Deploy

**Cost: $30-60/month** (all services)

---

## 💡 Simpler Alternative: Use LiveKit Cloud Free Tier

Instead of self-hosting LiveKit on Railway, use LiveKit Cloud's free tier:

**Step 1: Sign up for LiveKit Cloud**
https://cloud.livekit.io

**Step 2: Get credentials**
- LiveKit URL: `wss://your-project.livekit.cloud`
- API Key: (from dashboard)
- API Secret: (from dashboard)

**Step 3: Deploy just your agent to Railway**
```bash
cd voice-agent
railway init
railway up
```

**Step 4: Set environment variables**
```bash
railway variables set LIVEKIT_URL=wss://your-project.livekit.cloud
railway variables set LIVEKIT_API_KEY=<from-livekit-cloud>
railway variables set LIVEKIT_API_SECRET=<from-livekit-cloud>
railway variables set SARVAM_API_KEY=sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
railway variables set GOOGLE_API_KEY=AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI
```

**Cost:**
- LiveKit Cloud: FREE (up to 500 minutes/month)
- Railway Agent: $5-10/month
- **Total: $5-10/month** for testing!

---

## 🎯 Recommended Approach

For Tamil Nadu MLA system:

### Phase 1: Testing (5-10 MLAs)
**Use LiveKit Cloud Free Tier + Railway Agent**
- Cost: $5-10/month (₹400-800/month)
- Setup: 10 minutes
- Perfect for validation

### Phase 2: Scaling (10-50 MLAs)
**LiveKit Cloud Paid + Railway Agent**
- Cost: $50-100/month (₹4,200-8,400/month)
- No infrastructure management

### Phase 3: Full Scale (234 MLAs)
**Self-hosted on VPS or RunPod**
- Cost: ₹6,000/month
- Full control
- Unlimited usage

---

## 📋 Railway CLI Commands

```bash
# Deploy
railway up

# View logs
railway logs
railway logs -f  # Follow

# Environment variables
railway variables set KEY=value

# Restart
railway restart

# Open dashboard
railway open

# Link to project
railway link
```

---

## 🐛 Troubleshooting

### Error: "dockerfile parse error"
**Cause:** Railway trying to parse docker-compose as Dockerfile

**Fix:** Deploy services separately (see Option 2 above)

### Error: "Service won't start"
**Check:**
1. Environment variables are set
2. LIVEKIT_URL is accessible
3. Ports are configured correctly

### Error: "Can't connect to LiveKit"
**Fix:**
- If using Railway LiveKit: Use internal URL `http://livekit:7880`
- If using LiveKit Cloud: Use external URL `wss://your-project.livekit.cloud`

---

## ✅ Success Checklist

After deployment:
- [ ] Agent service is running
- [ ] Can see logs in Railway dashboard
- [ ] Environment variables are set
- [ ] Test call works
- [ ] Recordings are saved (if using Egress)

---

## 💰 Final Cost Summary

| Setup | Monthly Cost | Best For |
|-------|-------------|----------|
| **LiveKit Cloud Free + Railway Agent** | ₹400-800 | Testing 5-10 MLAs |
| **LiveKit Cloud Paid + Railway Agent** | ₹4,200-8,400 | 10-50 MLAs |
| **Full Railway Stack** | ₹5,000-10,000 | 50-100 MLAs |
| **RunPod Self-Hosted** | ₹6,000 | 234 MLAs |

**Recommendation:** Start with option 1, scale to option 4.

### Step 1: Install Railway CLI

```bash
# macOS
brew install railway

# Windows
scoop install railway

# Linux/WSL
npm install -g @railway/cli
```

### Step 2: Login

```bash
railway login
```

### Step 3: Initialize Project

```bash
cd VOICE-AI
railway init
# Choose: "Create new project"
# Name it: "tn-mla-voice-system"
```

### Step 4: Link to Docker Compose

Railway automatically detects `docker-compose.railway.yml`.

If not, create `railway.json`:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "docker-compose.railway.yml"
  }
}
```

### Step 5: Set Environment Variables

```bash
# Generate LiveKit keys
export LIVEKIT_API_KEY=$(openssl rand -base64 32)
export LIVEKIT_API_SECRET=$(openssl rand -base64 48)

# Set in Railway
railway variables set LIVEKIT_API_KEY=$LIVEKIT_API_KEY
railway variables set LIVEKIT_API_SECRET=$LIVEKIT_API_SECRET
railway variables set SARVAM_API_KEY=sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
railway variables set GOOGLE_API_KEY=AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI
```

### Step 6: Deploy

```bash
railway up
```

**Railway automatically:**
- ✅ Builds all Docker images
- ✅ Creates services (redis, livekit, sip, egress, agent)
- ✅ Assigns domains
- ✅ Provisions volumes
- ✅ Manages networking
- ✅ Sets up SSL

### Step 7: Get Your URLs

```bash
railway status

# Output:
# livekit: https://tn-mla-voice-system-production.up.railway.app
# Redis: Internal (redis:6379)
# SIP: Your-IP:5060
# Egress: Internal
# Agent: Internal
```

### Step 8: Test

```bash
# Check LiveKit is running
curl https://your-railway-domain.up.railway.app

# View logs
railway logs
```

**Total time: 10 minutes**

---

## 🏗️ What Railway Deploys

```
Railway Project: tn-mla-voice-system
├── Service: redis (redis:7-alpine)
│   └── Volume: redis_data (1GB)
├── Service: livekit (livekit/livekit-server)
│   └── Public domain: your-app.up.railway.app
│   └── Ports: 7880, 7881, 443, 3478
├── Service: sip (livekit/sip)
│   └── Ports: 5060, 10000-20000
├── Service: egress (livekit/egress)
│   └── Volume: recordings (10GB)
└── Service: agent (custom build)
    └── Built from voice-agent/Dockerfile
```

---

## 💰 Railway Pricing

### Free Tier (Trial Credit)
- $5 credit/month (enough for testing)
- **Lasts: 1-2 weeks of testing**

### Hobby Plan ($5/month)
- $5 base + usage
- **Estimated for your stack: $15-25/month**

### Pro Plan ($20/month + usage)
- Better for production
- **Estimated: $30-50/month**

**Cost Breakdown for 234 MLAs:**
```
Base:               $20/month
LiveKit:            $5-10/month (CPU hours)
Redis:              $2/month
SIP:                $2/month
Egress:             $3-5/month (storage)
Agent:              $5-10/month
API calls:          $20-50/month (Sarvam/Gemini)
────────────────────────────────
Total:              ~$60-100/month (₹5,000-8,400/month)
```

---

## 🔧 Railway Dashboard

After deployment, access Railway dashboard:

1. **Deployments**: View build logs, deployment history
2. **Metrics**: CPU, RAM, network usage
3. **Logs**: Real-time logs from all services
4. **Variables**: Manage environment variables
5. **Settings**: Custom domains, scaling, etc.

---

## 📊 Monitoring

### View Logs
```bash
# All services
railway logs

# Specific service
railway logs --service livekit

# Follow logs
railway logs -f
```

### Check Status
```bash
railway status
```

### Restart Services
```bash
railway restart
```

---

## 🔒 Security

### SSL/TLS
Railway provides free SSL for all services automatically.

### Private Networking
All services communicate privately within Railway's network.

### Secrets Management
Environment variables are encrypted at rest and in transit.

---

## 📈 Scaling

### Vertical Scaling (More Resources)
Railway dashboard → Settings → Increase CPU/RAM

### Horizontal Scaling (Not Needed)
Single instance handles 234 MLAs with API-based models.

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Check build logs
railway logs --deployment <deployment-id>

# Common fix: Increase build timeout
# Railway dashboard → Settings → Build timeout: 20 minutes
```

### Service Won't Start
```bash
# Check environment variables
railway variables

# Ensure all required vars are set:
# - LIVEKIT_API_KEY
# - LIVEKIT_API_SECRET
# - SARVAM_API_KEY
# - GOOGLE_API_KEY
```

### Can't Connect to LiveKit
```bash
# Check if service is running
railway status

# Check logs for errors
railway logs --service livekit -f

# Verify domain is accessible
curl https://your-railway-domain.up.railway.app
```

### Recording Not Working
```bash
# Check egress logs
railway logs --service egress

# Verify volume is mounted
# Railway dashboard → egress service → Volumes
```

---

## 🎯 Production Checklist

Before going live with 234 MLAs:

- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] All environment variables set
- [ ] Monitoring/alerts configured
- [ ] Backups enabled (recordings volume)
- [ ] Load tested with 50+ concurrent calls
- [ ] Phone number (SIP) configured
- [ ] Test call completed successfully
- [ ] MLA dashboard deployed
- [ ] Complaint database setup

---

## 🚀 Deployment Commands Reference

```bash
# Initialize
railway init

# Deploy
railway up

# View logs
railway logs
railway logs -f  # Follow
railway logs --service livekit

# Status
railway status

# Variables
railway variables
railway variables set KEY=value
railway variables delete KEY

# Restart
railway restart
railway restart --service livekit

# Open dashboard
railway open

# Open service URL
railway open --service livekit

# Link to different project
railway link

# Unlink
railway unlink
```

---

## 💡 Tips

1. **Use Railway's PostgreSQL addon** for complaint database
   ```bash
   railway add postgresql
   ```

2. **Connect custom domain** in Railway dashboard
   - Settings → Networking → Custom Domain

3. **Enable auto-deploys** from GitHub
   - Settings → GitHub → Enable auto-deploy

4. **Monitor costs** in Railway dashboard
   - Usage → Current billing period

5. **Backup recordings** periodically
   ```bash
   railway volume backup recordings
   ```

---

## 🎉 Success!

After deployment, you'll have:

✅ LiveKit server running on Railway
✅ SIP server for phone calls
✅ Automatic call recording
✅ Tamil voice agent (API-based)
✅ Free SSL certificate
✅ Monitoring and logs
✅ Auto-scaling (within plan limits)

**Your system is live at:**
`https://your-app.up.railway.app`

**Connection details:**
- LiveKit URL: `wss://your-app.up.railway.app`
- API Key: (from Railway variables)
- API Secret: (from Railway variables)

**Start testing with 5-10 MLAs!** 🚀

---

## 📞 Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- LiveKit Docs: https://docs.livekit.io
- This project's issues: https://github.com/your-repo/issues
