# Tamil Nadu MLA Voice Complaint System

A self-hosted voice AI system for 234 MLAs in Tamil Nadu to receive citizen complaints in Tamil language.

## 🎯 System Overview

- **Capacity**: 234 concurrent calls (one per MLA constituency)
- **Languages**: Tamil (primary) + English
- **Technology**: LiveKit (self-hosted) + Sarvam AI + Gemini AI
- **Cost**: ~₹42,000/month (~$500/month)
- **Per MLA**: ₹179/month (~$2.14/month)

## 🏗️ Architecture

```
Citizens (Phone/Web) → SIP Server → LiveKit Server → Voice Agent → AI Services
                          ↓                            ↓
                    Phone Network              Complaint Database
                                                       ↓
                                                 MLA Dashboard
```

### Components

1. **SIP Server** (Open Source) - Phone call integration via SIP trunks
2. **LiveKit Server** (Open Source) - WebRTC & Room Management
3. **Egress** (Open Source) - Automatic call recording for MLA review
4. **Voice Agent** - Handles conversations in Tamil
5. **AI Services**:
   - Sarvam Saarika - Tamil STT
   - Google Gemini - LLM
   - Sarvam Bulbul - Tamil TTS
6. **Redis** - Clustering & Queuing
7. **PostgreSQL** - Complaint storage (planned)

## 🚀 Quick Start (RunPod Deployment)

### Prerequisites

1. RunPod account with GPU instance (RTX 4090 recommended)
2. Domain name (e.g., voice.tnmla.in)
3. API Keys:
   - Sarvam AI: https://dashboard.sarvam.ai
   - Google Gemini: https://ai.google.dev

### Deployment Steps

1. **SSH into your RunPod instance**

2. **Clone the repository**
   ```bash
   git clone https://github.com/sg19chess-spec/VOICE-AI.git
   cd VOICE-AI
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env  # Add your API keys
   ```

4. **Run deployment script**
   ```bash
   chmod +x deploy-runpod.sh
   sudo ./deploy-runpod.sh
   ```

5. **Configure domain** (Choose one):

   **Option A: Cloudflare Tunnel (Recommended - FREE SSL)**
   ```bash
   cloudflared tunnel login
   cloudflared tunnel create tn-mla-voice
   cloudflared tunnel route dns tn-mla-voice voice.tnmla.in

   # Create config
   cat > ~/.cloudflared/config.yml <<EOF
   tunnel: tn-mla-voice
   credentials-file: /root/.cloudflared/[UUID].json
   ingress:
     - hostname: voice.tnmla.in
       service: http://localhost:7880
     - service: http_status:404
   EOF

   # Run tunnel
   cloudflared tunnel run tn-mla-voice
   ```

   **Option B: Direct IP (Simpler but less secure)**
   - Point your domain A record to RunPod instance IP
   - Configure SSL separately

6. **Verify deployment**
   ```bash
   docker-compose ps
   docker-compose logs -f agent
   ```

## 📱 Testing

### Console Test (Text)
```bash
cd voice-agent
uv run python src/agent.py console
```

### Web Test
1. Get your LiveKit URL and credentials from `.env`
2. Use: https://agents-playground.livekit.io/
3. Connect and test in Tamil!

### Test Phrases (Tamil)
- "வணக்கம், என் பெயர் ராஜ்" (Hello, my name is Raj)
- "சாலை பழுது குறித்து புகார் தெரிவிக்க வேண்டும்" (I want to complain about road damage)
- "மின் வசதி இல்லை" (No electricity)

## 📞 Phone Integration (SIP)

The system includes a SIP server that allows citizens to call via regular phone numbers.

### How It Works

1. **Citizen calls** → Phone number (e.g., +91-98765-43210)
2. **SIP trunk** → Routes to your LiveKit SIP server
3. **SIP server** → Creates LiveKit room and connects voice agent
4. **Voice agent** → Handles complaint in Tamil using Sarvam AI

### SIP Providers

You'll need a SIP trunk provider to connect phone numbers:

**Recommended Indian Providers:**
- **Exotel** - ₹500/month for 1000 minutes
- **Knowlarity** - ₹1,000/month for 2000 minutes
- **Twilio** - $1/month per number + $0.017/min
- **Telnyx** - $0.40/month per number + $0.004/min

### Setup Steps

1. **Sign up with SIP provider** (e.g., Exotel)
2. **Get phone numbers** - One per MLA or use IVR to route by constituency
3. **Configure SIP trunk** in `sip-config.yaml`:

```yaml
trunks:
  - name: "exotel"
    address: "sip.exotel.com:5060"
    username: "your-exotel-username"
    password: "your-exotel-password"
    inbound_numbers:
      - "+919876543210"  # Your phone number
    outbound_number: "+919876543210"
```

4. **Restart services:**
```bash
docker-compose restart sip
```

### Architecture Options

**Option 1: One Number Per MLA**
- 234 phone numbers (one per constituency)
- Direct routing to specific MLA agent
- Cost: ₹500 × 234 = ₹1,17,000/month

**Option 2: Single Number with IVR** (Recommended)
- 1 phone number for all MLAs
- IVR: "Press 1 for Chennai Anna Nagar, Press 2 for..."
- OR: "Enter your constituency code"
- Cost: ₹500/month + per-minute charges

**Option 3: Regional Numbers**
- 5-10 numbers for different regions
- IVR sub-menu for specific constituencies
- Cost: ₹2,500-5,000/month

### Testing SIP

```bash
# Check SIP server status
docker-compose logs sip

# View active calls
docker exec -it sip livekit-cli sip list

# Test with softphone (Zoiper, Linphone)
# SIP URI: sip:your-server-ip:5060
```

### Ports Required

The following ports must be open for SIP:
- **5060/UDP** - SIP signaling
- **5060/TCP** - SIP signaling (TCP)
- **10000-20000/UDP** - RTP media (voice)

These are automatically configured by `deploy-runpod.sh`.

## 🎙️ Call Recording

All calls are **automatically recorded** for MLA review using LiveKit Egress.

### How It Works

1. **Citizen calls/connects** → Recording starts automatically
2. **Conversation happens** → Full audio captured
3. **Call ends** → Recording saved as MP3 file
4. **MLA reviews** → Access via dashboard or file system

### Storage

**Recordings are saved to:**
```
recordings/
├── constituency-name/
│   ├── call-2025-01-15-09-30-00.mp3
│   ├── call-2025-01-15-10-15-23.mp3
│   └── ...
```

**File format:** MP3 (compressed audio)
**File size:** ~500 KB per 5-minute call
**Naming:** `call-{timestamp}.mp3`

### Accessing Recordings

**On RunPod instance:**
```bash
# Navigate to recordings
cd /root/VOICE-AI/recordings

# List recordings for a constituency
ls chennai-anna-nagar/

# Download to your computer
scp root@runpod-ip:/root/VOICE-AI/recordings/*.mp3 ./
```

**Via MLA Dashboard (planned):**
- Web interface to browse recordings
- Filter by date, constituency, complaint type
- Play inline or download
- Mark as reviewed/resolved

### Storage Requirements

| MLAs | Calls/Day (Each) | Monthly Storage |
|------|------------------|-----------------|
| 10   | 20              | 3 GB           |
| 50   | 20              | 15 GB          |
| 234  | 20              | **70 GB**      |

**Storage Costs:**
- Local (RunPod SSD): ~₹500/month for 100GB
- AWS S3: ~₹150/month for 70GB (recommended)

### Cloud Storage (Production)

For production, configure S3 in `egress.yaml`:

```yaml
file_output:
  s3:
    access_key: YOUR_AWS_ACCESS_KEY
    secret: YOUR_AWS_SECRET_KEY
    region: ap-south-1
    bucket: tn-mla-recordings
```

**Benefits:**
- Automatic backups
- 90-day retention policies
- Cheaper than local storage
- Access from anywhere

See **[RECORDINGS.md](./RECORDINGS.md)** for detailed guide.

## 🔧 Configuration

### Agent Configuration
- File: `voice-agent/src/agent.py`
- Modify:
  - Language (line 89): `language="ta-IN"` for Tamil
  - TTS Voice (line 101): `speaker="anushka"` (female) or `speaker="karun"` (male)
  - Instructions (lines 25-44): Customize agent behavior

### LiveKit Configuration
- File: `livekit.yaml`
- Key settings:
  - `turn.domain`: Your domain
  - `port_range_start/end`: WebRTC ports
  - `max_participants`: Per room limit

## 📊 Monitoring

### Check Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f agent
docker-compose logs -f livekit
```

### Restart Services
```bash
docker-compose restart agent
docker-compose restart livekit
```

## 💰 Cost Breakdown

| Component | Cost | Details |
|-----------|------|---------|
| RunPod GPU (RTX 4090) | $497/month | 24/7 operation |
| Domain | $10/year | .in domain |
| Cloudflare | FREE | SSL, CDN, DDoS |
| LiveKit | FREE | Open source |
| AI Models | FREE | Whisper, IndicF5 |
| Gemini API | $0-100/month | Free tier |
| Database | FREE | Supabase free tier |
| **TOTAL** | **~$500/month** | **₹42,000/month** |

**Per MLA: ~$2/month (₹179/month)**

## 🔒 Security

- Run services as non-root user
- Use firewall (UFW configured automatically)
- SSL via Cloudflare Tunnel
- API keys in `.env` (never commit!)
- Redis password protected (optional)

## 📈 Scaling

Current setup handles **234 concurrent calls**. To scale:

1. **Vertical Scaling**: Upgrade to larger GPU (RTX 6000)
2. **Horizontal Scaling**: Add more RunPod instances
3. **Load Balancing**: Use nginx in front of multiple instances

## 🤖 Auto-Scaling (Recommended)

Save **70-80%** on costs by automatically scaling RunPod instances based on demand.

### How It Works

The auto-scaler monitors LiveKit load and:
- Starts instances when calls come in
- Scales up when load increases
- Scales down when load decreases
- Stops instances after 30 minutes of idle time

### Scaling Rules

| Active Sessions | Instance Type | Cost/Hour | Total Capacity |
|----------------|---------------|-----------|----------------|
| 1-30 | RTX 3070 | $0.30 | 30 sessions |
| 31-80 | RTX 4070 | $0.45 | 80 sessions |
| 81-150 | RTX 4080 | $0.60 | 150 sessions |
| 151-240 | RTX 4090 | $0.69 | 240+ sessions |

### Cost Comparison

**Without Auto-Scaling:**
- RTX 4090 running 24/7: $497/month (₹42,000/month)

**With Auto-Scaling:**
- Average usage (business hours): ~$100/month (₹8,400/month)
- **Savings: 80%**

### Setup

Auto-scaler is installed automatically during deployment:

```bash
sudo ./deploy-runpod.sh
# Answer "y" when asked about auto-scaling
```

### Manual Setup

If you skipped it during deployment:

```bash
# Install dependencies
pip3 install -r autoscaler-requirements.txt

# Copy service file
sudo cp autoscaler.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable autoscaler.service
sudo systemctl start autoscaler.service
```

### Management

```bash
# Check status
sudo systemctl status autoscaler

# View logs
sudo journalctl -u autoscaler -f

# Restart
sudo systemctl restart autoscaler

# Stop
sudo systemctl stop autoscaler
```

### Configuration

Edit `autoscaler.py` to customize:
- Scaling thresholds (line 24-49)
- Check interval (line 258, default: 5 minutes)
- Idle timeout (line 61, default: 30 minutes)
- GPU types and costs

### Requirements

- RunPod API key in `.env`
- LiveKit server accessible
- Python 3.9+
- Internet connection for RunPod API

## 🐛 Troubleshooting

### Agent not connecting
```bash
# Check logs
docker-compose logs agent

# Verify environment
cat .env

# Restart agent
docker-compose restart agent
```

### No audio in calls
- Check firewall: UDP ports 50000-60000
- Verify TURN configuration in `livekit.yaml`
- Test with: `netstat -an | grep 50000`

### High CPU usage
- Reduce concurrent sessions per worker
- Use lighter models
- Add more instances

## 📚 Documentation

- [LiveKit Docs](https://docs.livekit.io)
- [Sarvam AI Docs](https://docs.sarvam.ai)
- [Voice Agent Guide](voice-agent/README.md)

## 🤝 Support

- Issues: https://github.com/sg19chess-spec/VOICE-AI/issues
- Email: support@tnmla.in (if configured)

## 📄 License

MIT License - See LICENSE file

---

**Built for Tamil Nadu MLAs to serve citizens better** 🇮🇳
