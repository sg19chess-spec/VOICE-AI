# Gradual Scaling Guide
## Tamil Nadu MLA Voice Complaint System

Scale from 1 MLA to 234 MLAs gradually, paying only for what you use.

---

## 🎯 Scaling Phases

### Phase 1: Pilot (1-10 MLAs)
**Timeline:** Weeks 1-4
**Goal:** Test system, get feedback, refine workflow

#### Option A: Local Testing (FREE)
```bash
cd voice-agent
./test-local.sh
python src/agent.py console
```
**Cost:** ₹0/month

#### Option B: LiveKit Cloud Free Tier
```bash
lk agent create
```
**Cost:** ₹0/month (within 1,000 min)
**Limit:** ~16 hours of calls/month

#### Option C: RunPod CPU Instance
```bash
./deploy-runpod.sh --instance-type cpu
```
**Cost:** ₹2,500/month (24/7)
**Or:** ₹750/month (office hours only)

**Recommended:** Start with Option B (LiveKit Cloud Free)

---

### Phase 2: Regional Rollout (10-50 MLAs)
**Timeline:** Month 2-3
**Goal:** Expand to 2-3 districts

#### Option A: LiveKit Cloud (Ship Plan)
- Handles 20 concurrent sessions
- $50/month base + $0.01/min
**Cost:** ₹8,000-12,000/month

#### Option B: RunPod Small GPU
- RTX 3070: $0.30/hour
- Handles 50 concurrent sessions
**Cost:**
- 24/7: ₹7,500/month
- Office hours (12h): ₹3,750/month
- Business days (264h): ₹2,640/month

**Recommended:** Option B with office hours

---

### Phase 3: State-wide (50-150 MLAs)
**Timeline:** Month 4-6

#### RunPod Medium GPU
- RTX 4070: $0.45/hour
- Handles 120 concurrent sessions

**Cost:**
- 24/7: ₹11,250/month
- Office hours: ₹5,625/month
- Business days: ₹3,960/month

**Recommended:** Business days mode

---

### Phase 4: Full Deployment (150-234 MLAs)
**Timeline:** Month 7+

#### RunPod High-End GPU
- RTX 4090: $0.69/hour
- Handles 240+ concurrent sessions

**Cost:**
- 24/7: ₹17,250/month
- Office hours: ₹8,625/month
- Business days: ₹6,072/month

**Recommended:** Office hours mode

---

## 💰 Cost Comparison by Phase

| Phase | MLAs | Best Option | 24/7 Cost | Office Hours | Business Days |
|-------|------|-------------|-----------|--------------|---------------|
| Pilot | 1-10 | LiveKit Free | ₹0 | ₹0 | ₹0 |
| Regional | 10-50 | RunPod 3070 | ₹7,500 | ₹3,750 | ₹2,640 |
| State-wide | 50-150 | RunPod 4070 | ₹11,250 | ₹5,625 | ₹3,960 |
| Full | 150-234 | RunPod 4090 | ₹17,250 | ₹8,625 | ₹6,072 |

---

## 🤖 Auto Start/Stop (Advanced)

Save 70-80% by auto-starting instance only when needed:

### Setup
```bash
# Install RunPod CLI
pip install runpod

# Create auto-start script
cat > auto-manage.py <<EOF
import runpod
import time

# Start instance when needed
def start_if_calls_waiting():
    # Check if calls in queue
    if has_pending_calls():
        runpod.start_pod(POD_ID)
        wait_for_ready()

def stop_if_idle():
    # Stop after 30 min idle
    if idle_time() > 1800:
        runpod.stop_pod(POD_ID)

# Run every 5 minutes
while True:
    start_if_calls_waiting()
    stop_if_idle()
    time.sleep(300)
EOF
```

**Estimated Savings:** 70-80%
**Example:** ₹17,250 → ₹3,450/month

---

## 📊 Recommended Path

### Month 1: FREE
- Test locally: 1-2 MLAs
- Use LiveKit Cloud free tier
- Refine Tamil conversations
- **Cost: ₹0**

### Month 2: ₹2,640
- Deploy 5-10 MLAs
- RunPod RTX 3070 (business days)
- Collect feedback
- **Cost: ₹2,640/month**

### Month 3-4: ₹3,960
- Expand to 30-50 MLAs
- Upgrade to RTX 4070
- **Cost: ₹3,960/month**

### Month 5-6: ₹6,072
- Expand to 100-150 MLAs
- Upgrade to RTX 4090
- **Cost: ₹6,072/month**

### Month 7+: ₹8,625
- Full 234 MLAs
- Office hours mode
- **Cost: ₹8,625/month**

**Total Spent (7 months):** ~₹32,000
**vs buying full infrastructure upfront:** ₹2.9 lakh

**Savings: ₹2.58 lakh!**

---

## 🎯 Action Plan

### This Week
```bash
# Test on your PC
cd C:\Users\sg13c\Documents\VOICE-AI\voice-agent
git pull
./test-local.sh
python src/agent.py console
```

### Next Week
```bash
# Deploy to LiveKit Cloud (free tier)
lk agent create --secrets-file secrets.txt
# Test with 2-3 MLAs
```

### Month 2
```bash
# Get RunPod account
# Deploy small instance
# Onboard 5-10 MLAs
```

### Month 3+
```bash
# Scale gradually as you add MLAs
# Upgrade instance when needed
```

---

## 📞 Support

Questions? Contact:
- GitHub Issues
- Email: support@tnmla.in

---

**Start small, scale smart!** 🚀
