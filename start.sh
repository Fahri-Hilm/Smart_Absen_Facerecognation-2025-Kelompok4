#!/bin/bash
# Helper script untuk menjalankan Kafebasabasi Attendance System dalam berbagai mode

echo "🚀 KAFEBASABASI ATTENDANCE SYSTEM - LAUNCHER"
echo "=============================================="
echo ""
echo "Pilih mode yang ingin dijalankan:"
echo ""
echo "1. DUAL MODE (Local + Ngrok) - Default"
echo "2. LOCAL ONLY (Tanpa Ngrok)"
echo "3. NGROK ONLY (Dengan Ngrok paksa)"
echo "4. EXIT"
echo ""

read -p "Masukkan pilihan (1-4): " choice

case $choice in
    1)
        echo "🔄 Starting DUAL MODE (Local + Ngrok)..."
        echo "Local access: http://localhost:5001"
        echo "Public access: akan ditampilkan jika ngrok berhasil"
        echo ""
        python3 app.py
        ;;
    2)
        echo "🏠 Starting LOCAL ONLY mode..."
        echo "Hanya akses local: http://localhost:5001"
        echo ""
        LOCAL_ONLY=true python3 app.py
        ;;
    3)
        echo "🌐 Starting dengan NGROK..."
        echo "Memaksa ngrok untuk public access"
        echo ""
        USE_NGROK=true python3 app.py
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