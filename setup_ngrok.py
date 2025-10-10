#!/usr/bin/env python3
"""
Script untuk setup ngrok dengan konfigurasi yang proper
Mengatasi masalah HSTS dan warning page
"""

import os
import sys
import subprocess
import json

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ngrok sudah terinstall: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ngrok tidak terinstall atau tidak bisa diakses")
            return False
    except FileNotFoundError:
        print("❌ Ngrok tidak ditemukan di PATH")
        return False

def setup_ngrok_config():
    """Setup ngrok configuration"""
    config_dir = os.path.expanduser("~/.config/ngrok")
    config_file = os.path.join(config_dir, "ngrok.yml")
    
    # Create config directory if not exists
    os.makedirs(config_dir, exist_ok=True)
    
    # Basic configuration
    config_content = """
version: "2"
authtoken: ""
region: us
console_ui: true
console_ui_color: transparent
log_level: info
log_format: logfmt
log: /tmp/ngrok.log

tunnels:
  kafebasabasi:
    proto: http
    addr: 5001
    bind_tls: true
    host_header: rewrite
    inspect: true
"""
    
    try:
        with open(config_file, 'w') as f:
            f.write(config_content.strip())
        print(f"✅ Ngrok config dibuat di: {config_file}")
        return True
    except Exception as e:
        print(f"❌ Error membuat config: {e}")
        return False

def get_ngrok_authtoken():
    """Get ngrok authtoken from user"""
    print("\n🔑 SETUP NGROK AUTHTOKEN")
    print("=" * 40)
    print("1. Buka https://dashboard.ngrok.com/get-started/your-authtoken")
    print("2. Copy authtoken Anda")
    print("3. Paste di sini (atau tekan Enter untuk skip)")
    print()
    
    authtoken = input("Masukkan authtoken (atau Enter untuk skip): ").strip()
    
    if authtoken:
        try:
            result = subprocess.run(['ngrok', 'config', 'add-authtoken', authtoken], 
                                    capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Authtoken berhasil diset!")
                return True
            else:
                print(f"❌ Error setting authtoken: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("⚠️ Skip authtoken - menggunakan free tier dengan limitasi")
        return True

def test_ngrok_tunnel():
    """Test ngrok tunnel"""
    print("\n🧪 TESTING NGROK TUNNEL")
    print("=" * 30)
    
    try:
        # Start a simple test tunnel
        print("Starting test tunnel...")
        result = subprocess.run([
            'ngrok', 'http', '8000', 
            '--log=stdout', 
            '--log-level=info'
        ], capture_output=True, text=True, timeout=10)
        
        if "started tunnel" in result.stdout:
            print("✅ Ngrok tunnel test berhasil!")
            return True
        else:
            print("❌ Ngrok tunnel test gagal")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("✅ Ngrok tunnel started (timeout expected)")
        return True
    except Exception as e:
        print(f"❌ Error testing tunnel: {e}")
        return False

def show_solutions():
    """Show alternative solutions"""
    print("\n🔧 SOLUSI ALTERNATIF UNTUK MASALAH NGROK HSTS")
    print("=" * 50)
    print()
    print("1. 🌐 BYPASS WARNING NGROK:")
    print("   - Tambahkan parameter: ?ngrok-skip-browser-warning=true")
    print("   - URL menjadi: https://xxx.ngrok-free.dev?ngrok-skip-browser-warning=true")
    print()
    print("2. 🔑 GUNAKAN AUTHTOKEN:")
    print("   - Daftar di: https://dashboard.ngrok.com")
    print("   - Dapatkan authtoken gratis")
    print("   - Jalankan: ngrok config add-authtoken YOUR_TOKEN")
    print()
    print("3. 🏠 GUNAKAN LOCAL SAJA:")
    print("   - Jalankan: LOCAL_ONLY=true python3 app.py")
    print("   - Akses via: http://localhost:5001")
    print()
    print("4. 🔥 GUNAKAN ALTERNATIF TUNNEL:")
    print("   - Cloudflare Tunnel")
    print("   - LocalTunnel (npx localtunnel --port 5001)")
    print("   - Serveo (ssh -R 80:localhost:5001 serveo.net)")
    print()
    print("5. 🖥️ NETWORK SHARING:")
    print("   - Gunakan IP lokal untuk akses dalam jaringan yang sama")
    print("   - Buka firewall untuk port 5001")
    print()

def main():
    print("🚀 NGROK SETUP & TROUBLESHOOT")
    print("=" * 40)
    print()
    
    # Check ngrok installation
    if not check_ngrok_installed():
        print("\n📥 INSTALL NGROK:")
        print("Ubuntu/Debian: sudo snap install ngrok")
        print("macOS: brew install ngrok")
        print("Windows: Download dari https://ngrok.com/download")
        return 1
    
    # Setup config
    setup_ngrok_config()
    
    # Setup authtoken
    get_ngrok_authtoken()
    
    # Show solutions
    show_solutions()
    
    print("\n✅ Setup selesai!")
    print("Sekarang coba jalankan aplikasi dengan: python3 launcher.py")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())