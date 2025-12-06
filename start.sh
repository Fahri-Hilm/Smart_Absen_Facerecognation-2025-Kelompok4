#!/bin/bash
# Helper script untuk menjalankan Kafebasabasi Attendance System dalam berbagai mode

# Fix matplotlib/mpl_toolkits conflict - prioritize user packages
export PYTHONPATH="/home/fj/.local/lib/python3.12/site-packages:$PYTHONPATH"

# Fungsi untuk cleanup saat exit
cleanup() {
    echo ""
    echo "� Shutting down..."
    # Kill cloudflared jika berjalan
    pkill -f "cloudflared tunnel" 2>/dev/null
    # Kill Flask app
    pkill -f "python3 app.py" 2>/dev/null
    exit 0
}

# Trap CTRL+C
trap cleanup SIGINT SIGTERM

echo "�🚀 KAFEBASABASI ATTENDANCE SYSTEM - LAUNCHER"
echo "=============================================="
echo ""
echo "Pilih mode yang ingin dijalankan:"
echo ""
echo "1. CLOUDFLARE TUNNEL (Recommended) - Auto Public Access"
echo "2. LOCAL ONLY (Tanpa Public Access)"
echo "3. DUAL MODE (Local + Ngrok) - Legacy"
echo "4. EXIT"
echo ""

read -p "Masukkan pilihan (1-4): " choice

case $choice in
    1)
        echo ""
        echo "☁️  Starting dengan CLOUDFLARE TUNNEL..."
        echo "=============================================="
        
        # Check if cloudflared is installed
        if ! command -v cloudflared &> /dev/null; then
            echo "❌ cloudflared tidak ditemukan!"
            echo ""
            echo "Install dengan:"
            echo "  sudo apt install cloudflared"
            echo "  atau"
            echo "  curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared"
            echo "  chmod +x cloudflared && sudo mv cloudflared /usr/local/bin/"
            exit 1
        fi
        
        echo "🏠 Local access: http://localhost:5001"
        echo "☁️  Cloudflare Tunnel starting..."
        echo ""
        
        # Start Flask app in background
        python3 app.py &
        FLASK_PID=$!
        
        # Wait for Flask to start
        sleep 3
        
        # Start Cloudflare Tunnel
        echo ""
        echo "🌐 Starting Cloudflare Tunnel..."
        echo "=============================================="
        cloudflared tunnel --url http://localhost:5001 2>&1 | while read line; do
            # Extract and display the tunnel URL
            if echo "$line" | grep -q "trycloudflare.com"; then
                TUNNEL_URL=$(echo "$line" | grep -oE 'https://[a-zA-Z0-9-]+\.trycloudflare\.com')
                if [ ! -z "$TUNNEL_URL" ]; then
                    echo ""
                    echo "=============================================="
                    echo "✅ CLOUDFLARE TUNNEL ACTIVE!"
                    echo "=============================================="
                    echo "🌐 PUBLIC URL: $TUNNEL_URL"
                    echo "🔐 QR Auth:    $TUNNEL_URL/auth"
                    echo "👨‍💼 Admin:      $TUNNEL_URL/admin/login"
                    echo "=============================================="
                    echo ""
                    echo "📱 Scan QR code dari HP menggunakan URL di atas"
                    echo "Press CTRL+C to stop"
                    echo ""
                fi
            fi
            echo "$line"
        done
        
        # Wait for Flask process
        wait $FLASK_PID
        ;;
    2)
        echo ""
        echo "🏠 Starting LOCAL ONLY mode..."
        echo "Hanya akses local: http://localhost:5001"
        echo ""
        LOCAL_ONLY=true python3 app.py
        ;;
    3)
        echo ""
        echo "🔄 Starting DUAL MODE (Local + Ngrok)..."
        echo "Local access: http://localhost:5001"
        echo "Public access: akan ditampilkan jika ngrok berhasil"
        echo ""
        python3 app.py
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Pilihan tidak valid!"
        exit 1
        ;;
esac