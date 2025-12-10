# Railway Deployment Guide

Deploy Tamil Nadu MLA Voice Complaint System to Railway in 10 minutes.

## 🚀 Quick Start

### Prerequisites
- GitHub account
- Railway account (free: https://railway.app)
- Your API keys ready

### Method 1: One-Click Deploy (Easiest)

1. **Fork this repo** to your GitHub

2. **Go to Railway**: https://railway.app

3. **Click "New Project"** → **"Deploy from GitHub repo"**

4. **Select your forked repo**

5. **Railway auto-detects** docker-compose and deploys!

6. **Set environment variables** in Railway dashboard:
   ```
   LIVEKIT_API_KEY=<generate with: openssl rand -base64 32>
   LIVEKIT_API_SECRET=<generate with: openssl rand -base64 48>
   SARVAM_API_KEY=sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
   GOOGLE_API_KEY=AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI
   ```

7. **Done!** Railway builds and deploys everything.

**Total time: 5 minutes**

---

## Method 2: Railway CLI (Manual Control)

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
