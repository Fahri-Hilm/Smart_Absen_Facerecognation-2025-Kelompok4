#!/bin/bash
# ============================================
# KAFEBASABASI - AUTO START WITH CLOUDFLARE TUNNEL
# ============================================
# Script ini langsung menjalankan sistem dengan Cloudflare Tunnel
# tanpa menu - cocok untuk production/daily use

# Fix matplotlib/mpl_toolkits conflict
export PYTHONPATH="/home/fj/.local/lib/python3.12/site-packages:$PYTHONPATH"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down Kafebasabasi...${NC}"
    pkill -f "cloudflared tunnel" 2>/dev/null
    pkill -f "python3 app.py" 2>/dev/null
    echo -e "${GREEN}✅ Cleanup complete. Goodbye!${NC}"
    exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM EXIT

# Change to script directory
cd "$(dirname "$0")"

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}☕ KAFEBASABASI ATTENDANCE SYSTEM${NC}                        ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  ${YELLOW}Auto-Start with Cloudflare Tunnel${NC}                        ${CYAN}║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}❌ ERROR: cloudflared tidak ditemukan!${NC}"
    echo ""
    echo -e "${YELLOW}Install dengan salah satu cara berikut:${NC}"
    echo ""
    echo "  1. Via apt (Debian/Ubuntu):"
    echo "     sudo apt install cloudflared"
    echo ""
    echo "  2. Via snap:"
    echo "     sudo snap install cloudflared"
    echo ""
    echo "  3. Manual download:"
    echo "     curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared"
    echo "     chmod +x cloudflared"
    echo "     sudo mv cloudflared /usr/local/bin/"
    echo ""
    exit 1
fi

# Kill any existing instances
echo -e "${YELLOW}🔄 Cleaning up old processes...${NC}"
pkill -f "cloudflared tunnel" 2>/dev/null
pkill -f "python3 app.py" 2>/dev/null
sleep 1

# Start Flask app in background
echo -e "${BLUE}🚀 Starting Flask server...${NC}"
python3 app.py > /tmp/kafebasabasi_flask.log 2>&1 &
FLASK_PID=$!

# Check if Flask started successfully
sleep 3
if ! ps -p $FLASK_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Flask server failed to start!${NC}"
    echo "Check logs: /tmp/kafebasabasi_flask.log"
    cat /tmp/kafebasabasi_flask.log
    exit 1
fi

echo -e "${GREEN}✅ Flask server running (PID: $FLASK_PID)${NC}"
echo -e "${BLUE}   Local: http://localhost:5001${NC}"
echo ""

# Start Cloudflare Tunnel and capture URL
echo -e "${BLUE}☁️  Starting Cloudflare Tunnel...${NC}"
echo -e "${YELLOW}   Please wait for tunnel URL...${NC}"
echo ""

# Create a temp file to store the tunnel URL
TUNNEL_URL_FILE="/tmp/kafebasabasi_tunnel_url.txt"
rm -f "$TUNNEL_URL_FILE"

# Start cloudflared and monitor output
cloudflared tunnel --url http://localhost:5001 2>&1 | while IFS= read -r line; do
    # Check for tunnel URL
    if echo "$line" | grep -qE 'https://[a-zA-Z0-9-]+\.trycloudflare\.com'; then
        TUNNEL_URL=$(echo "$line" | grep -oE 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' | head -1)
        if [ ! -z "$TUNNEL_URL" ] && [ ! -f "$TUNNEL_URL_FILE" ]; then
            echo "$TUNNEL_URL" > "$TUNNEL_URL_FILE"
            echo ""
            echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║${NC}  ${CYAN}✅ CLOUDFLARE TUNNEL ACTIVE!${NC}                            ${GREEN}║${NC}"
            echo -e "${GREEN}╠══════════════════════════════════════════════════════════╣${NC}"
            echo -e "${GREEN}║${NC}                                                            ${GREEN}║${NC}"
            echo -e "${GREEN}║${NC}  ${YELLOW}🌐 PUBLIC URL:${NC}                                           ${GREEN}║${NC}"
            echo -e "${GREEN}║${NC}  ${CYAN}$TUNNEL_URL${NC}"
            echo -e "${GREEN}║${NC}                                                            ${GREEN}║${NC}"
            echo -e "${GREEN}║${NC}  ${YELLOW}📱 QR Auth Page:${NC}                                         ${GREEN}║${NC}"
            echo -e "${GREEN}║${NC}  ${CYAN}$TUNNEL_URL/auth${NC}"
            echo -e "${GREEN}║${NC}                                                            ${GREEN}║${NC}"
            echo -e "${GREEN}║${NC}  ${YELLOW}👨‍💼 Admin Panel:${NC}                                          ${GREEN}║${NC}"
            echo -e "${GREEN}║${NC}  ${CYAN}$TUNNEL_URL/admin/login${NC}"
            echo -e "${GREEN}║${NC}                                                            ${GREEN}║${NC}"
            echo -e "${GREEN}╠══════════════════════════════════════════════════════════╣${NC}"
            echo -e "${GREEN}║${NC}  ${YELLOW}💡 TIP: Buka URL di atas dari HP untuk scan QR${NC}           ${GREEN}║${NC}"
            echo -e "${GREEN}║${NC}  ${YELLOW}Press CTRL+C to stop the server${NC}                         ${GREEN}║${NC}"
            echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
            echo ""
        fi
    fi
    
    # Show errors if any
    if echo "$line" | grep -qi "error\|failed\|unable"; then
        echo -e "${RED}$line${NC}"
    fi
done &

CLOUDFLARED_PID=$!

# Wait for tunnel URL (max 30 seconds)
WAIT_COUNT=0
while [ ! -f "$TUNNEL_URL_FILE" ] && [ $WAIT_COUNT -lt 30 ]; do
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
done

if [ ! -f "$TUNNEL_URL_FILE" ]; then
    echo -e "${YELLOW}⏳ Tunnel is starting... URL will appear shortly${NC}"
fi

# Keep script running
wait $CLOUDFLARED_PID
