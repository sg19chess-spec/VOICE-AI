#!/bin/bash

# Local Testing Script - No Cost!
# Test on your PC before deploying to cloud

echo "================================================"
echo "  Tamil Nadu MLA Voice Agent - Local Testing"
echo "  FREE - No cloud costs!"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Check if in voice-agent directory
if [ ! -f "src/agent.py" ]; then
    echo "❌ Please run this from the voice-agent directory"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env.local for testing
echo "⚙️  Setting up environment..."
if [ ! -f ".env.local" ]; then
    cat > .env.local <<EOF
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
SARVAM_API_KEY=sk_iaapa9l4_pc4l7fFmz1xru1RhSQ5wjzuL
GOOGLE_API_KEY=AIzaSyCZ66PBhYc686h8KtjC1x_K2yeq8i5LuUI
EOF
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To test the agent:"
echo "  1. Console mode (text): python src/agent.py console"
echo "  2. Dev mode (with frontend): python src/agent.py dev"
echo ""
echo "💡 This runs entirely on your PC - no cloud costs!"
echo ""
