# Custom LiveKit Server with Agent API enabled for Railway
FROM livekit/livekit-server:v1.9.7

# Copy config file with agent API enabled
COPY livekit-config.yaml /etc/livekit.yaml

# Expose ports
EXPOSE 7880 7881

# Start LiveKit with config
CMD ["livekit-server", "--config", "/etc/livekit.yaml", "--bind", "0.0.0.0"]
