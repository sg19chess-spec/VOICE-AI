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
Citizens → LiveKit Server (self-hosted) → Voice Agent → AI Services
                ↓
         Complaint Database
                ↓
          MLA Dashboard
```

### Components

1. **LiveKit Server** (Open Source) - WebRTC & Room Management
2. **Voice Agent** - Handles conversations in Tamil
3. **AI Services**:
   - Sarvam Saarika - Tamil STT
   - Google Gemini - LLM
   - Sarvam Bulbul - Tamil TTS
4. **Redis** - Clustering & Queuing
5. **PostgreSQL** - Complaint storage

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
