# Railway Quick Deploy - Tamil Nadu MLA Voice System

## 🚀 Absolute Easiest Way (2 Minutes)

### Option 1: One-Click Deploy Button (Coming Soon)

Once you push to GitHub, anyone can deploy with one click using this button:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

---

## Option 2: CLI Auto-Deploy (5 Minutes) ⭐ CURRENT BEST

This automatically deploys just your voice agent. LiveKit runs on LiveKit Cloud (free).

### Step 1: Sign up for LiveKit Cloud (FREE)

1. Go to https://cloud.livekit.io
2. Click "Sign Up"
3. Create a new project
4. Copy these from dashboard:
   - LiveKit URL: `wss://your-project.livekit.cloud`
   - API Key: `APIxxxxxxxxx`
   - API Secret: `xxxxxxxxxxxxxxx`

### Step 2: Deploy Voice Agent to Railway

```bash
# Install Railway CLI (one-time)
npm install -g @railway/cli

# Navigate to voice-agent folder
cd voice-agent

# Login to Railway
railway login

# Initialize and deploy
railway init
railway up

# Set environment variables
railway variables set LIVEKIT_URL=wss://your-project.livekit.cloud
railway variables set LIVEKIT_API_KEY=<your-key-from-livekit>
railway variables set LIVEKIT_API_SECRET=<your-secret-from-livekit>
railway variables set SARVAM_API_KEY=sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
railway variables set GOOGLE_API_KEY=AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI

# Check deployment
railway logs -f
```

**Done! Your agent is live in 5 minutes.**

**Cost:**
- LiveKit Cloud: **FREE** (500 minutes/month)
- Railway: **$5/month**
- **Total: $5/month (₹420/month)**

---

## Option 3: GitHub Auto-Deploy (No CLI) ⭐ EASIEST FOR NON-TECHNICAL

### Step 1: Push to GitHub

```bash
cd VOICE-AI
git add .
git commit -m "Ready for Railway"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app/new
2. Click "**Deploy from GitHub repo**"
3. Select your `VOICE-AI` repository
4. Railway asks: "**Which service to deploy?**"
   - Select: `voice-agent` folder
5. Railway auto-detects Dockerfile ✅
6. Click "**Deploy**"

### Step 3: Set Environment Variables

In Railway dashboard:
1. Click on your service
2. Go to "**Variables**" tab
3. Click "**+ New Variable**"
4. Add these:

```
LIVEKIT_URL = wss://your-project.livekit.cloud
LIVEKIT_API_KEY = <from-livekit-dashboard>
LIVEKIT_API_SECRET = <from-livekit-dashboard>
SARVAM_API_KEY = sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
GOOGLE_API_KEY = AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI
```

5. Service auto-restarts with new variables

### Step 4: Test

1. Go to LiveKit playground: https://agents-playground.livekit.io
2. Enter your LiveKit Cloud credentials
3. Start a session
4. Your Tamil voice agent should join! 🎉

**Total time: 10 minutes (no terminal needed!)**

---

## 🎯 What Gets Deployed

```
Railway Service: voice-agent
├── Source: GitHub (VOICE-AI/voice-agent/)
├── Build: Dockerfile (auto-detected)
├── Dependencies: Downloads Sarvam/Gemini models
└── Connects to: LiveKit Cloud (external)
```

**No need to deploy:**
- ❌ LiveKit Server (using LiveKit Cloud)
- ❌ Redis (not needed for single agent)
- ❌ SIP (add later if needed)
- ❌ Egress (LiveKit Cloud has built-in recording)

---

## 📊 Cost Breakdown

| Item | Cost | Notes |
|------|------|-------|
| LiveKit Cloud | FREE | 500 minutes/month |
| Railway (voice agent) | $5/month | Hobby plan |
| Sarvam API | FREE | Using your API key |
| Gemini API | FREE | Free tier |
| **Total** | **$5/month** | **₹420/month** |

**For 234 MLAs:**
- If you exceed 500 minutes → LiveKit Cloud paid tier (~$0.03/min)
- Estimated: $50-100/month total (₹4,200-8,400/month)

---

## ✅ Success Checklist

After deployment, verify:

- [ ] Railway service shows "Active"
- [ ] Logs show "Connected to LiveKit"
- [ ] No errors in deployment logs
- [ ] Can see agent in LiveKit Cloud dashboard
- [ ] Test call works in playground

---

## 🐛 Common Issues

### Build Timeout

**Error:** "Build exceeded time limit"

**Fix:**
```bash
# In Railway dashboard
Settings → Build → Timeout → Increase to 20 minutes
```

### Can't Connect to LiveKit

**Check:**
1. LIVEKIT_URL starts with `wss://` (not `ws://`)
2. API Key and Secret are correct
3. LiveKit Cloud project is active

### Agent Not Responding

**Check logs:**
```bash
railway logs -f
```

Look for:
- ✅ "Connected to LiveKit"
- ❌ "Connection refused"
- ❌ "Authentication failed"

---

## 🚀 Next Steps

Once deployed:

1. **Test with 1 MLA**
   - Have them call in Tamil
   - Verify complaint collection works
   - Check recording quality

2. **Scale to 10 MLAs**
   - Monitor LiveKit Cloud usage
   - Check Railway resource usage

3. **Add Phone Integration** (Optional)
   - Sign up for Exotel
   - Add SIP service to Railway
   - Configure phone number

4. **Build MLA Dashboard**
   - Deploy separate service for web UI
   - Show complaints per constituency

---

## 💡 Pro Tips

1. **Enable Auto-Deploy**
   - Railway Settings → GitHub → Enable auto-deploy
   - Push to GitHub = auto-deploy

2. **Monitor Costs**
   - Railway Dashboard → Usage
   - LiveKit Cloud → Usage

3. **View Logs**
   ```bash
   railway logs -f  # Follow live logs
   ```

4. **Restart Service**
   ```bash
   railway restart
   ```

---

## 📞 Support

**Railway Issues:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**LiveKit Issues:**
- Docs: https://docs.livekit.io
- Discord: https://discord.gg/livekit

**This Project:**
- GitHub Issues: Your repo

---

## 🎉 You're Done!

Your Tamil MLA voice agent is now live on Railway + LiveKit Cloud!

**Start testing with citizens today.** 🚀
