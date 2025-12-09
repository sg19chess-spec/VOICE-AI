#!/bin/bash

# Tamil Nadu MLA Voice Agent Deployment Script
# For RunPod GPU Instance

set -e  # Exit on error

echo "================================================"
echo "  Tamil Nadu MLA Voice Agent Deployment"
echo "  Self-hosted on RunPod"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root (use sudo)${NC}"
  exit 1
fi

# Step 1: Install Docker if not present
echo -e "${GREEN}Step 1: Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo -e "${GREEN}✓ Docker installed${NC}"
else
    echo -e "${YELLOW}✓ Docker already installed${NC}"
fi

# Step 2: Install Docker Compose
echo -e "${GREEN}Step 2: Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose installed${NC}"
else
    echo -e "${YELLOW}✓ Docker Compose already installed${NC}"
fi

# Step 3: Install NVIDIA Container Toolkit (for GPU support)
echo -e "${GREEN}Step 3: Installing NVIDIA Container Toolkit...${NC}"
if ! command -v nvidia-container-toolkit &> /dev/null; then
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | apt-key add -
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    apt-get update
    apt-get install -y nvidia-container-toolkit
    systemctl restart docker
    echo -e "${GREEN}✓ NVIDIA Container Toolkit installed${NC}"
else
    echo -e "${YELLOW}✓ NVIDIA Container Toolkit already installed${NC}"
fi

# Step 4: Generate LiveKit keys if .env doesn't exist
echo -e "${GREEN}Step 4: Setting up environment...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env

    # Generate secure API keys
    API_KEY=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
    API_SECRET=$(openssl rand -base64 48 | tr -d "=+/" | cut -c1-48)

    sed -i "s/generate_with_openssl_rand_base64_32/$API_KEY/" .env
    sed -i "s/generate_with_openssl_rand_base64_48/$API_SECRET/" .env

    echo -e "${GREEN}✓ Generated LiveKit API keys${NC}"
    echo -e "${YELLOW}API Key: $API_KEY${NC}"
    echo -e "${YELLOW}API Secret: $API_SECRET${NC}"
    echo -e "${YELLOW}Please save these keys securely!${NC}"
else
    echo -e "${YELLOW}✓ .env file already exists${NC}"
fi

# Step 5: Configure firewall
echo -e "${GREEN}Step 5: Configuring firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 443/udp
    ufw allow 7880/tcp
    ufw allow 7881/tcp
    ufw allow 3478/udp
    ufw allow 50000:60000/udp
    echo -e "${GREEN}✓ Firewall configured${NC}"
else
    echo -e "${YELLOW}! UFW not found, please configure firewall manually${NC}"
fi

# Step 6: Install Cloudflare Tunnel (optional but recommended)
echo -e "${GREEN}Step 6: Installing Cloudflare Tunnel...${NC}"
read -p "Do you want to install Cloudflare Tunnel for free SSL? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if ! command -v cloudflared &> /dev/null; then
        wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        dpkg -i cloudflared-linux-amd64.deb
        rm cloudflared-linux-amd64.deb
        echo -e "${GREEN}✓ Cloudflare Tunnel installed${NC}"
        echo -e "${YELLOW}Run 'cloudflared tunnel login' to authenticate${NC}"
    else
        echo -e "${YELLOW}✓ Cloudflare Tunnel already installed${NC}"
    fi
fi

# Step 7: Build and start services
echo -e "${GREEN}Step 7: Building Docker images...${NC}"
docker-compose build

echo -e "${GREEN}Step 8: Starting services...${NC}"
docker-compose up -d

echo ""
echo "================================================"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo "================================================"
echo ""
echo "Services running:"
echo "  - LiveKit Server: http://localhost:7880"
echo "  - Redis: localhost:6379"
echo "  - Voice Agent: Running with 4 workers"
echo ""
echo "Next steps:"
echo "  1. Set up your domain DNS to point to this server"
echo "  2. Configure Cloudflare Tunnel for SSL (if installed)"
echo "  3. Test the agent with: docker-compose logs -f agent"
echo ""
echo "To check status: docker-compose ps"
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""
echo "Your LiveKit credentials:"
echo "  URL: ws://your-domain.com:7880"
echo "  (Check .env file for API_KEY and API_SECRET)"
echo ""
echo "================================================"
