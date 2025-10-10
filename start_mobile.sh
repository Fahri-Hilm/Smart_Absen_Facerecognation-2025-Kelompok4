#!/bin/bash

# Script untuk menjalankan ngrok dengan HTTPS untuk mobile attendance
echo "🚀 Starting Kafebasabasi with Ngrok HTTPS..."

# Kill existing ngrok processes
pkill -f ngrok

# Start ngrok with HTTPS tunnel in background
echo "📱 Starting HTTPS tunnel for mobile camera access..."
ngrok http 5001 --log=stdout > ngrok.log 2>&1 &

# Wait for ngrok to start
sleep 5

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for tunnel in data['tunnels']:
        if tunnel['proto'] == 'https':
            print(tunnel['public_url'])
            break
except:
    pass
")

if [ ! -z "$NGROK_URL" ]; then
    echo "✅ Ngrok HTTPS tunnel active!"
    echo "📱 Mobile URL: $NGROK_URL"
    echo "📱 Mobile Attendance: $NGROK_URL/mobile"
    echo "🔐 QR Auth: $NGROK_URL/auth"
    echo ""
    echo "⚠️  PENTING untuk mobile:"
    echo "   1. Gunakan URL HTTPS yang ditampilkan di atas"
    echo "   2. Izinkan akses kamera di browser mobile"
    echo "   3. Pastikan pencahayaan cukup untuk deteksi wajah"
    echo ""
else
    echo "❌ Failed to get ngrok URL"
    echo "💡 Make sure ngrok is installed and authenticated"
    exit 1
fi

# Set environment variable for app
export NGROK_URL="$NGROK_URL"

# Start the Flask app
echo "🏁 Starting Flask application..."
cd /home/fj/Desktop/PROJECT/Absenn
python3 app.py