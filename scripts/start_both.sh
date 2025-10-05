#!/bin/bash
echo "🚀 KAFEBASABASI DUAL ACCESS LAUNCHER"
echo "===================================="
echo "🎯 Pilih mode akses:"
echo "1️⃣  Local Only (localhost saja)"
echo "2️⃣  Local + Ngrok (bisa diakses dari internet)"
echo "3️⃣  Auto (ngrok jika tersedia, local jika tidak)"
echo "===================================="

read -p "Pilih mode (1/2/3): " choice

case $choice in
    1)
        echo "🏠 Starting LOCAL ONLY mode..."
        export USE_NGROK=false
        ;;
    2)
        echo "🌐 Starting LOCAL + NGROK mode..."
        
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
            echo "📝 Setup instructions:"
            echo "   1. Sign up at https://ngrok.com/signup" 
            echo "   2. Get authtoken from dashboard"
            echo "   3. Run: ngrok config add-authtoken YOUR_TOKEN"
            echo "   4. Restart this script"
            exit 1
        fi
        
        export USE_NGROK=true
        ;;
    3)
        echo "🎯 AUTO mode - checking ngrok availability..."
        export USE_NGROK=true
        ;;
    *)
        echo "❌ Invalid choice. Using AUTO mode..."
        export USE_NGROK=true
        ;;
esac

echo ""
echo "🚀 Starting Kafebasabasi Attendance System..."
echo "⏳ Please wait..."
echo ""

/usr/bin/python3 app.py