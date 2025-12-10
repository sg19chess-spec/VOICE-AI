# Call Recording Guide

All phone calls are automatically recorded and saved for MLA review.

## 📁 Storage Structure

```
recordings/
├── chennai-anna-nagar/
│   ├── call-2025-01-15-09-30-00.mp3
│   ├── call-2025-01-15-10-15-23.mp3
│   └── call-2025-01-15-14-45-12.mp3
├── madurai-central/
│   ├── call-2025-01-15-09-00-05.mp3
│   └── call-2025-01-15-11-22-18.mp3
└── coimbatore-south/
    └── call-2025-01-15-08-45-33.mp3
```

**Format:**
- **Directory:** MLA constituency name
- **Filename:** `call-{timestamp}.mp3`
- **Audio:** MP3 format (compressed, ~1MB per 10 minutes)

## 🎧 Accessing Recordings

### Local Access (On RunPod)

```bash
# SSH into RunPod instance
cd /root/VOICE-AI/recordings

# List all recordings for a constituency
ls chennai-anna-nagar/

# Play a recording (requires audio player)
mpg123 chennai-anna-nagar/call-2025-01-15-09-30-00.mp3

# Download to your computer
scp root@runpod-ip:/root/VOICE-AI/recordings/chennai-anna-nagar/*.mp3 ./
```

### Web Access (Recommended)

You'll need to build a simple web dashboard:

```python
# Flask app to serve recordings
from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/recordings/<constituency>/<filename>')
def get_recording(constituency, filename):
    path = f'/out/recordings/{constituency}/{filename}'
    return send_file(path, mimetype='audio/mpeg')

# Run: python recording_server.py
```

Then MLAs can access via browser:
- `https://voice.tnmla.in/recordings/chennai-anna-nagar/call-2025-01-15-09-30-00.mp3`

## 💾 Storage Requirements

**Estimation:**
- Average call: 5 minutes
- File size: ~500 KB per call (MP3 compressed)
- Calls per MLA per day: 20
- Days per month: 30

**Per MLA:**
- Daily: 20 calls × 500 KB = 10 MB
- Monthly: 10 MB × 30 = 300 MB

**All 234 MLAs:**
- Monthly: 300 MB × 234 = **70 GB/month**
- Yearly: 70 GB × 12 = **840 GB/year**

**Storage Costs:**
- **Local (RunPod disk):** ~₹500/month for 100GB SSD
- **S3 (AWS):** ~₹150/month for 70GB (with lifecycle policies)
- **Recommended:** S3 with 90-day retention, then delete old recordings

## ☁️ Cloud Storage (Production)

For production, use S3-compatible storage to avoid filling up RunPod disk:

### 1. Setup AWS S3

```bash
# Create S3 bucket
aws s3 mb s3://tn-mla-recordings --region ap-south-1

# Set lifecycle policy (delete after 90 days)
aws s3api put-bucket-lifecycle-configuration \
  --bucket tn-mla-recordings \
  --lifecycle-configuration file://lifecycle.json
```

### 2. Update egress.yaml

```yaml
file_output:
  s3:
    access_key: YOUR_AWS_ACCESS_KEY
    secret: YOUR_AWS_SECRET_KEY
    region: ap-south-1
    bucket: tn-mla-recordings
    endpoint: s3.amazonaws.com
```

### 3. Restart Egress

```bash
docker-compose restart egress
```

## 🔒 Security

**Important considerations:**

1. **Encryption:** Enable S3 server-side encryption (SSE-S3 or SSE-KMS)
2. **Access Control:** Only authorized MLAs can access their constituency recordings
3. **Retention Policy:** Auto-delete after 90 days (GDPR compliance)
4. **Audit Logs:** Track who accessed which recordings
5. **Data Privacy:** Don't share recordings without citizen consent

## 📊 MLA Dashboard Integration

To show recordings in MLA dashboard:

```javascript
// Fetch recordings for constituency
fetch(`/api/recordings/chennai-anna-nagar`)
  .then(r => r.json())
  .then(recordings => {
    recordings.forEach(rec => {
      // Display:
      // - Date/Time
      // - Duration
      // - Play button
      // - Download button
      // - Complaint status
    })
  })
```

## 🔍 Search & Filter

Implement search functionality:

```sql
-- Database schema for searchable recordings
CREATE TABLE recordings (
  id SERIAL PRIMARY KEY,
  constituency VARCHAR(100),
  filename VARCHAR(255),
  duration INTEGER,  -- seconds
  created_at TIMESTAMP,
  caller_phone VARCHAR(15),
  complaint_type VARCHAR(50),
  status VARCHAR(20)  -- new, reviewed, resolved
);

-- Search recordings
SELECT * FROM recordings
WHERE constituency = 'chennai-anna-nagar'
  AND created_at >= '2025-01-01'
  AND complaint_type = 'road_damage'
ORDER BY created_at DESC;
```

## 🎯 Next Steps

1. **Test recording** - Make a test call and verify recording is saved
2. **Build dashboard** - Create web interface for MLAs to access recordings
3. **Setup S3** - Move to cloud storage for production
4. **Add metadata** - Store caller info, complaint type with each recording
5. **Implement search** - Allow filtering by date, type, status
