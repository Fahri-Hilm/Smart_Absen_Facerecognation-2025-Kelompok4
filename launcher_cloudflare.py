#!/usr/bin/env python3
"""
KAFEBASABASI - Auto Launcher with Cloudflare Tunnel
====================================================
Script ini otomatis menjalankan Flask + Cloudflare Tunnel
Cukup jalankan: python3 launcher_cloudflare.py
"""

import subprocess
import sys
import os
import time
import signal
import re
from threading import Thread

# Fix PYTHONPATH untuk matplotlib/mpl_toolkits
user_packages = "/home/fj/.local/lib/python3.12/site-packages"
if user_packages not in sys.path:
    sys.path.insert(0, user_packages)
os.environ['PYTHONPATH'] = f"{user_packages}:{os.environ.get('PYTHONPATH', '')}"

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Global processes
flask_process = None
cloudflared_process = None

def cleanup(signum=None, frame=None):
    """Cleanup all processes on exit"""
    print("\n\n🛑 Shutting down Kafebasabasi...")
    
    if cloudflared_process:
        try:
            cloudflared_process.terminate()
            cloudflared_process.wait(timeout=5)
        except:
            cloudflared_process.kill()
    
    if flask_process:
        try:
            flask_process.terminate()
            flask_process.wait(timeout=5)
        except:
            flask_process.kill()
    
    # Also kill any remaining processes
    subprocess.run(['pkill', '-f', 'cloudflared tunnel'], capture_output=True)
    subprocess.run(['pkill', '-f', 'python3 app.py'], capture_output=True)
    
    print("✅ Cleanup complete. Goodbye!")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def check_cloudflared():
    """Check if cloudflared is installed"""
    try:
        result = subprocess.run(['which', 'cloudflared'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def print_banner():
    """Print startup banner"""
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  ☕ KAFEBASABASI ATTENDANCE SYSTEM                       ║")
    print("║  Auto-Start with Cloudflare Tunnel                       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

def monitor_cloudflared(process):
    """Monitor cloudflared output for tunnel URL"""
    tunnel_url = None
    
    for line in iter(process.stderr.readline, b''):
        line_str = line.decode('utf-8', errors='ignore').strip()
        
        # Look for tunnel URL
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line_str)
        if match and not tunnel_url:
            tunnel_url = match.group(0)
            print()
            print("╔══════════════════════════════════════════════════════════╗")
            print("║  ✅ CLOUDFLARE TUNNEL ACTIVE!                            ║")
            print("╠══════════════════════════════════════════════════════════╣")
            print("║                                                          ║")
            print(f"║  🌐 PUBLIC URL:                                          ║")
            print(f"║  {tunnel_url}")
            print("║                                                          ║")
            print(f"║  📱 QR Auth:  {tunnel_url}/auth")
            print(f"║  👨‍💼 Admin:    {tunnel_url}/admin/login")
            print("║                                                          ║")
            print("╠══════════════════════════════════════════════════════════╣")
            print("║  💡 Buka URL di atas dari HP untuk scan QR               ║")
            print("║  Press CTRL+C to stop                                    ║")
            print("╚══════════════════════════════════════════════════════════╝")
            print()

def main():
    global flask_process, cloudflared_process
    
    print_banner()
    
    # Check cloudflared
    if not check_cloudflared():
        print("❌ ERROR: cloudflared tidak ditemukan!")
        print()
        print("Install dengan:")
        print("  sudo apt install cloudflared")
        print("  atau")
        print("  sudo snap install cloudflared")
        print()
        sys.exit(1)
    
    # Kill existing processes
    print("🔄 Cleaning up old processes...")
    subprocess.run(['pkill', '-f', 'cloudflared tunnel'], capture_output=True)
    subprocess.run(['pkill', '-f', 'python3 app.py'], capture_output=True)
    time.sleep(1)
    
    # Start Flask
    print("🚀 Starting Flask server...")
    flask_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ
    )
    
    # Wait for Flask to start
    time.sleep(3)
    
    if flask_process.poll() is not None:
        print("❌ Flask server failed to start!")
        sys.exit(1)
    
    print(f"✅ Flask server running (PID: {flask_process.pid})")
    print("   Local: http://localhost:5001")
    print()
    
    # Start Cloudflare Tunnel
    print("☁️  Starting Cloudflare Tunnel...")
    print("   Please wait for tunnel URL...")
    print()
    
    cloudflared_process = subprocess.Popen(
        ['cloudflared', 'tunnel', '--url', 'http://localhost:5001'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Monitor cloudflared in background thread
    monitor_thread = Thread(target=monitor_cloudflared, args=(cloudflared_process,), daemon=True)
    monitor_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            # Check if processes are still running
            if flask_process.poll() is not None:
                print("❌ Flask server stopped unexpectedly!")
                cleanup()
            if cloudflared_process.poll() is not None:
                print("❌ Cloudflare tunnel stopped unexpectedly!")
                cleanup()
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == '__main__':
    main()
