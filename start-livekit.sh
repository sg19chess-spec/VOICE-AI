#!/bin/bash
# Startup script for LiveKit with agent API enabled

# Create config file
cat > /tmp/livekit.yaml << 'EOF'
port: 8081
log_level: info

# Enable Agent API - CRITICAL
agent:
  enabled: true

# Redis
redis:
  address: redis.railway.internal:6379

# WebRTC
rtc:
  use_external_ip: true

# Rooms
room:
  auto_create: true
EOF

# Start LiveKit with config
exec livekit-server --config /tmp/livekit.yaml --bind 0.0.0.0
