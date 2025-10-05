#!/bin/bash
echo "🌐 Starting Kafebasabasi - LOCAL + NGROK MODE"
echo "=============================================="
echo "📱 Bisa diakses dari internet dengan ngrok"
echo "🏠 Juga tetap bisa diakses secara lokal"
echo "=============================================="

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok not found. Installing..."
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar xzf ngrok-v3-stable-linux-amd64.tgz
    sudo mv ngrok /usr/local/bin/
    rm ngrok-v3-stable-linux-amd64.tgz
    echo "✅ Ngrok installed"
fi

# Check authtoken
if ! ngrok config check &> /dev/null; then
    echo "⚠️  Ngrok authtoken not set!"
    echo "📝 Please:"
    echo "   1. Sign up at https://ngrok.com/signup" 
    echo "   2. Get authtoken from dashboard"
    echo "   3. Run: ngrok config add-authtoken YOUR_TOKEN"
    exit 1
fi

export USE_NGROK=true
cd "$(dirname "$0")/.." && /usr/bin/python3 app.py