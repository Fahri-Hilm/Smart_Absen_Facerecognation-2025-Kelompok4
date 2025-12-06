#!/bin/bash

# Script untuk menjalankan Flask + Cloudflare Tunnel bersamaan
# dan menampilkan URL public

cd "$(dirname "$0")"

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  KAFEBASABASI ATTENDANCE SYSTEM${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Kill proses lama jika ada
echo -e "${YELLOW}[1/3] Membersihkan proses lama...${NC}"
pkill -f "python3.*app.py" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 1

# Jalankan Flask di background
echo -e "${YELLOW}[2/3] Menjalankan Flask server...${NC}"
python3 app.py > /tmp/flask_output.log 2>&1 &
FLASK_PID=$!
sleep 3

# Cek apakah Flask berhasil jalan
if ! ps -p $FLASK_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Flask gagal dijalankan!${NC}"
    cat /tmp/flask_output.log
    exit 1
fi
echo -e "${GREEN}✅ Flask berjalan di port 5001${NC}"

# Jalankan Cloudflare Tunnel dan capture URL
echo -e "${YELLOW}[3/3] Menjalankan Cloudflare Tunnel...${NC}"
cloudflared tunnel --url http://localhost:5001 > /tmp/cloudflare_output.log 2>&1 &
CLOUDFLARE_PID=$!

# Tunggu URL muncul (max 15 detik)
echo -e "${YELLOW}    Menunggu URL tunnel...${NC}"
for i in {1..15}; do
    TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cloudflare_output.log 2>/dev/null | head -1)
    if [ -n "$TUNNEL_URL" ]; then
        break
    fi
    sleep 1
done

if [ -z "$TUNNEL_URL" ]; then
    echo -e "${RED}❌ Gagal mendapatkan URL Cloudflare Tunnel!${NC}"
    cat /tmp/cloudflare_output.log
    exit 1
fi

# Tampilkan informasi
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ SISTEM BERHASIL DIJALANKAN!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${CYAN}🌐 URL PUBLIC (Cloudflare Tunnel):${NC}"
echo -e "${GREEN}   $TUNNEL_URL${NC}"
echo ""
echo -e "${CYAN}📱 Halaman-halaman:${NC}"
echo -e "   ${BLUE}QR Auth:${NC}  $TUNNEL_URL/auth"
echo -e "   ${BLUE}Admin:${NC}    $TUNNEL_URL/admin/login"
echo -e "   ${BLUE}Absensi:${NC}  $TUNNEL_URL/web_attendance"
echo ""
echo -e "${CYAN}🖥️  Local URL:${NC}"
echo -e "   http://localhost:5001"
echo -e "   http://localhost:5001/auth"
echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Tekan Ctrl+C untuk menghentikan${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Fungsi cleanup saat exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Menghentikan semua proses...${NC}"
    kill $FLASK_PID 2>/dev/null
    kill $CLOUDFLARE_PID 2>/dev/null
    pkill -f "python3.*app.py" 2>/dev/null
    pkill -f "cloudflared tunnel" 2>/dev/null
    echo -e "${GREEN}✅ Semua proses dihentikan${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Tunggu sampai user stop
wait $CLOUDFLARE_PID
