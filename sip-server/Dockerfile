FROM livekit/sip:latest

# Copy configuration file
COPY config.yaml /sip/config.yaml

# Expose SIP port (signaling)
EXPOSE 5060/tcp
EXPOSE 5060/udp

# Expose RTP ports (media)
EXPOSE 10000-20000/udp

# Expose health check port
EXPOSE 8080/tcp

# Start SIP server with config
CMD ["sip", "--config", "/sip/config.yaml"]
