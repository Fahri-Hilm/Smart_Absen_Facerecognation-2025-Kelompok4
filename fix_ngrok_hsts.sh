#!/bin/bash
# Script untuk mengatasi masalah HSTS ngrok

echo "🔧 MENGATASI MASALAH NGROK HSTS"
echo "================================"
echo

# Cek apakah ngrok terinstall
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok tidak terinstall!"
    echo "Install dengan: sudo snap install ngrok"
    exit 1
fi

echo "✅ Ngrok terinstall: $(ngrok version)"
echo

# Solusi 1: Install ngrok dengan authtoken
echo "🔑 SOLUSI 1: SETUP AUTHTOKEN (RECOMMENDED)"
echo "1. Daftar gratis di: https://dashboard.ngrok.com"
echo "2. Copy authtoken dari dashboard"
echo "3. Jalankan: ngrok config add-authtoken YOUR_TOKEN"
echo

# Solusi 2: Bypass warning
echo "🌐 SOLUSI 2: BYPASS WARNING URL"
echo "Tambahkan parameter ke URL ngrok:"
echo "https://xxx.ngrok-free.dev?ngrok-skip-browser-warning=true"
echo

# Solusi 3: Alternatif tunnel
echo "🔥 SOLUSI 3: ALTERNATIF TUNNEL"
echo "LocalTunnel: npx localtunnel --port 5001"
echo "Serveo: ssh -R 80:localhost:5001 serveo.net"
echo

# Test koneksi
echo "🧪 TESTING NGROK CONNECTIVITY"
echo "Mencoba koneksi ke ngrok..."

# Cek koneksi internet
if ping -c 1 ngrok.com &> /dev/null; then
    echo "✅ Koneksi ke ngrok.com berhasil"
else
    echo "❌ Tidak bisa terhubung ke ngrok.com"
    echo "Cek koneksi internet Anda"
fi

echo
echo "📱 UNTUK AKSES MOBILE:"
echo "1. Gunakan authtoken untuk menghindari warning page"
echo "2. Atau gunakan IP lokal jika dalam jaringan yang sama"
echo "3. Atau gunakan bypass URL dengan parameter"

# Tampilkan IP lokal
echo
echo "🏠 IP LOKAL ANDA:"
hostname -I | awk '{print "http://"$1":5001"}'

echo
echo "✅ Selesai! Pilih solusi yang paling cocok untuk Anda."